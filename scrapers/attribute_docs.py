"""Graphviz Attribute Documentation scraper for documentation stream data collection.

Scrapes graphviz.org/doc/info/attrs.html and individual attribute pages to extract
DOT examples with template-based instruction generation.
"""

import argparse
import time
import re
from datetime import datetime
from typing import List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from validation.dot_validator import validate_dot, GraphvizNotFoundError
from validation.schema import DataRecord
from validation.writer import JSONLWriter
from common.id_generator import generate_id
from common.metrics import ScraperMetrics
from common.logging_config import setup_logger


# Constants
ATTRS_INDEX_URL = "https://www.graphviz.org/doc/info/attrs.html"
BASE_URL = "https://www.graphviz.org"
USER_AGENT = "AnecDOT-Scraper/1.0 (+https://github.com/anecdot-project)"
DEFAULT_OUTPUT = "./data/attribute-docs-stream.jsonl"
DEFAULT_DELAY = 0.5
DEFAULT_RETRIES = 3

# Confidence thresholds
MIN_CONFIDENCE = 0.6
HIGH_CONFIDENCE = 0.8
MEDIUM_CONFIDENCE = 0.65

logger = setup_logger(__name__)


class AttributeExample:
    """Represents a single DOT example from an attribute page."""
    
    def __init__(
        self,
        url: str,
        attribute_name: str,
        description: Optional[str],
        dot_code: str,
        confidence: float,
        index: int = 0
    ):
        self.url = url
        self.attribute_name = attribute_name
        self.description = description
        self.dot_code = dot_code
        self.confidence = confidence
        self.index = index
    
    def to_instruction(self) -> str:
        """Generate instruction text using templates and confidence scoring."""
        attr = self.attribute_name
        
        # Clean up description if available
        if self.description:
            desc = self.description.strip()
            # Remove type information (e.g., "type: color | colorList, default: black")
            if desc.startswith('type:'):
                # Extract meaningful part after default
                parts = desc.split(',')
                meaningful_parts = [p for p in parts if not p.strip().startswith('type:') 
                                   and not p.strip().startswith('default:')]
                if meaningful_parts:
                    desc = ' '.join(meaningful_parts).strip()
                else:
                    desc = None
            
            # Use first sentence if description is long
            if desc and len(desc) > 150:
                sentences = re.split(r'[.!?]', desc)
                if sentences:
                    desc = sentences[0] + '.'
        else:
            desc = None
        
        # Generate instruction based on available information
        if desc and len(desc) > 30 and len(desc) < 150:
            return f"Demonstrate the '{attr}' attribute. {desc}"
        elif desc:
            return f"Demonstrate the '{attr}' attribute usage in Graphviz. {desc[:80]}..."
        else:
            return f"Show how to use the '{attr}' attribute in a Graphviz graph"


class AttributeDocsScraper:
    """Scraper for Graphviz attribute documentation stream."""
    
    def __init__(
        self,
        output_path: str = DEFAULT_OUTPUT,
        delay: float = DEFAULT_DELAY,
        retries: int = DEFAULT_RETRIES,
        dry_run: bool = False,
        limit: Optional[int] = None
    ):
        """Initialize scraper.
        
        Args:
            output_path: Path to output JSONL file
            delay: Delay between requests in seconds
            retries: Number of retries for failed requests
            dry_run: If True, don't write output file
            limit: If set, only scrape first N attribute pages (for testing)
        """
        self.output_path = output_path
        self.delay = delay
        self.retries = retries
        self.dry_run = dry_run
        self.limit = limit
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
        self.writer = None if dry_run else JSONLWriter(output_path)
        self.metrics = ScraperMetrics()
    
    def _fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL with retry logic and error handling."""
        for attempt in range(self.retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retries}): {url} - {e}")
                if attempt < self.retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    logger.error(f"All retries exhausted for {url}")
                    return None
    
    def extract_attribute_links(self, html: str) -> List[str]:
        """Extract links to individual attribute pages from index."""
        soup = BeautifulSoup(html, 'lxml')
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/docs/attrs/' in href and href.endswith('/'):
                abs_url = urljoin(BASE_URL, href)
                links.append(abs_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    def calculate_confidence(self, attr_name: str, description: Optional[str], 
                           dot_code: str) -> float:
        """Calculate confidence score for instruction quality."""
        score = MEDIUM_CONFIDENCE
        
        # Boost for clear, meaningful description
        if description:
            # Remove type/default info noise
            clean_desc = description
            if 'type:' in description or 'default:' in description:
                clean_desc = re.sub(r'type:.*?,', '', description)
                clean_desc = re.sub(r'default:.*?,', '', clean_desc)
            
            # Good length and content
            if 30 < len(clean_desc.strip()) < 200:
                score = HIGH_CONFIDENCE
            # Has some content but might be technical
            elif len(clean_desc.strip()) > 10:
                score = MEDIUM_CONFIDENCE + 0.05
        
        # Penalty for very long or very complex DOT
        if len(dot_code) > 2000:
            score -= 0.05
        
        # Penalty for common attributes with trivial examples
        trivial_attrs = ['label', 'color', 'style']
        if attr_name.lower() in trivial_attrs and len(dot_code) < 100:
            score -= 0.1
        
        return max(MIN_CONFIDENCE, min(1.0, score))
    
    def extract_attribute_content(self, url: str, html: str) -> List[AttributeExample]:
        """Extract attribute name, description, and DOT examples from page."""
        soup = BeautifulSoup(html, 'lxml')
        examples = []
        
        # Extract attribute name from URL (more reliable than H1)
        attr_name = url.rstrip('/').split('/')[-1]
        
        # Extract description - look for first substantial paragraph
        description = None
        main_content = soup.find('main') or soup.find('article') or soup
        for p in main_content.find_all('p', recursive=True):
            if p.find_parent(['nav', 'header', 'footer']):
                continue
            text = p.get_text().strip()
            if text and len(text) > 20:
                description = text
                break
        
        # Extract DOT code blocks
        code_blocks = []
        for pre in soup.find_all('pre'):
            code = pre.get_text().strip()
            if code and (code.startswith('digraph') or code.startswith('graph') or 
                        'digraph' in code[:50] or 'graph {' in code[:50]):
                code_blocks.append(code)
        
        # Also check standalone code elements
        for code_elem in soup.find_all('code'):
            if code_elem.find_parent('pre'):
                continue
            code = code_elem.get_text().strip()
            if code and (code.startswith('digraph') or code.startswith('graph')):
                code_blocks.append(code)
        
        # Clean and deduplicate
        clean_codes = []
        seen = set()
        for code in code_blocks:
            # Skip shell commands
            if any(x in code for x in ['echo ', '| dot', '> ', '< ']):
                continue
            # Skip if too small
            if len(code) < 20:
                continue
            # Deduplicate
            if code not in seen:
                seen.add(code)
                clean_codes.append(code)
        
        # Create AttributeExample for each DOT block
        for idx, code in enumerate(clean_codes):
            confidence = self.calculate_confidence(attr_name, description, code)
            
            # Only include if meets minimum confidence
            if confidence >= MIN_CONFIDENCE:
                examples.append(AttributeExample(
                    url=url,
                    attribute_name=attr_name,
                    description=description,
                    dot_code=code,
                    confidence=confidence,
                    index=idx
                ))
        
        if not examples:
            logger.debug(f"No qualifying DOT code found in {url}")
        
        return examples
    
    def scrape(self) -> ScraperMetrics:
        """Run the scraper."""
        logger.info("Starting Graphviz Attribute Documentation scraper")
        
        # Check if Graphviz is installed
        try:
            validate_dot("digraph { A }")
        except GraphvizNotFoundError as e:
            logger.error(str(e))
            self.metrics.finish()
            return self.metrics
        
        # Load existing records if resuming
        if not self.dry_run and self.writer:
            existing_count = self.writer.count_existing()
            if existing_count > 0:
                logger.info(f"Resuming from existing file with {existing_count} examples")
        
        # Fetch attribute index
        logger.info(f"Fetching attribute index: {ATTRS_INDEX_URL}")
        index_html = self._fetch_url(ATTRS_INDEX_URL)
        if not index_html:
            logger.error("Failed to fetch attribute index")
            self.metrics.finish()
            return self.metrics
        
        # Extract attribute links
        attr_urls = self.extract_attribute_links(index_html)
        
        # Apply limit if set (for testing)
        if self.limit:
            attr_urls = attr_urls[:self.limit]
            logger.info(f"Limited to first {self.limit} attribute pages (testing mode)")
        
        self.metrics.total_found = len(attr_urls)
        logger.info(f"Found {len(attr_urls)} attribute pages")
        
        # Process each attribute page
        for idx, url in enumerate(attr_urls, 1):
            logger.info(f"Processing {idx}/{len(attr_urls)}: {url}")
            
            # Fetch attribute page
            html = self._fetch_url(url)
            if not html:
                continue
            
            # Extract content
            examples = self.extract_attribute_content(url, html)
            self.metrics.total_scraped += len(examples)
            
            # Process each DOT block
            for example in examples:
                self._process_example(example)
            
            # Progress update
            pass_rate = self.metrics.pass_rate()
            logger.info(
                f"Progress: {idx}/{len(attr_urls)} pages, "
                f"{self.metrics.validation_passed} passed, "
                f"{self.metrics.validation_failed} failed "
                f"({pass_rate:.1f}% pass rate)"
            )
            
            # Rate limiting
            if idx < len(attr_urls):
                time.sleep(self.delay)
        
        # Finish metrics
        self.metrics.finish()
        
        # Final summary
        logger.info("\n" + self.metrics.summary())
        
        # Quality assessment
        if self.metrics.examples_written > 0:
            logger.info(f"\nAttribute-focused examples collected: {self.metrics.examples_written}")
            logger.info(f"These examples demonstrate fine-grained attribute control")
        
        return self.metrics
    
    def _process_example(self, example: AttributeExample):
        """Process a single example: validate and write to output."""
        # Validate DOT code
        result = validate_dot(example.dot_code)
        
        if not result.is_valid:
            self.metrics.increment('validation_failed')
            logger.debug(
                f"Validation failed for {example.url} "
                f"(block {example.index}): {result.error_message}"
            )
            return
        
        self.metrics.increment('validation_passed')
        
        # Generate ID
        record_id = generate_id(example.dot_code, "attr-docs")
        if example.index > 0:
            record_id = f"{record_id}-{example.index}"
        
        # Create DataRecord with confidence score
        record = DataRecord(
            id=record_id,
            source="attribute_docs",
            source_url=example.url,
            license="EPL-2.0",
            task_type="NL_TO_DOT",
            input_text=example.to_instruction(),
            output_dot=example.dot_code,
            verification_status=result.to_schema_status(),
            scraped_at=datetime.utcnow().isoformat() + 'Z',
            instruction_confidence=example.confidence
        )
        
        # Write to output (or just log in dry run)
        if self.dry_run:
            logger.info(f"[DRY RUN] Would write: {record.id} (confidence: {example.confidence:.2f})")
            self.metrics.increment('examples_written')
        else:
            written = self.writer.append(record)
            if written:
                self.metrics.increment('examples_written')
                logger.debug(f"Written: {record.id} (confidence: {example.confidence:.2f})")
            else:
                self.metrics.increment('duplicates_skipped')
                logger.debug(f"Skipped duplicate: {record.id}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape Graphviz Attribute Documentation for DOT training examples"
    )
    parser.add_argument(
        '--output',
        default=DEFAULT_OUTPUT,
        help=f'Output JSONL file path (default: {DEFAULT_OUTPUT})'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=DEFAULT_DELAY,
        help=f'Delay between requests in seconds (default: {DEFAULT_DELAY})'
    )
    parser.add_argument(
        '--retries',
        type=int,
        default=DEFAULT_RETRIES,
        help=f'Number of retries for failed requests (default: {DEFAULT_RETRIES})'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit to first N attribute pages (for testing)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without writing output file'
    )
    
    args = parser.parse_args()
    
    # Run scraper
    scraper = AttributeDocsScraper(
        output_path=args.output,
        delay=args.delay,
        retries=args.retries,
        dry_run=args.dry_run,
        limit=args.limit
    )
    
    metrics = scraper.scrape()
    
    # Exit with error code if pass rate too low
    if metrics.pass_rate() < 95.0 and metrics.validation_passed > 0:
        logger.warning("Pass rate below 95% - please investigate")
        exit(1)
    
    exit(0)


if __name__ == '__main__':
    main()
