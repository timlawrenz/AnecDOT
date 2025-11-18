"""Graphviz Gallery scraper for documentation stream data collection.

Scrapes graphviz.org/gallery/ to extract DOT examples with titles, descriptions,
and source code for training data generation.
"""

import argparse
import time
from datetime import datetime
from typing import List, Optional, Dict
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
GALLERY_URL = "https://graphviz.org/gallery/"
USER_AGENT = "AnecDOT-Scraper/1.0 (+https://github.com/anecdot-project)"
DEFAULT_OUTPUT = "./data/documentation-stream.jsonl"
DEFAULT_DELAY = 1.0
DEFAULT_RETRIES = 3


logger = setup_logger(__name__)


class GalleryExample:
    """Represents a single example from the Graphviz Gallery."""
    
    def __init__(
        self,
        url: str,
        title: str,
        description: Optional[str],
        dot_code: str,
        index: int = 0
    ):
        self.url = url
        self.title = title
        self.description = description
        self.dot_code = dot_code
        self.index = index
    
    def to_instruction(self) -> str:
        """Generate instruction text for training."""
        if self.description:
            return f"{self.title}. {self.description}"
        return self.title


class GraphvizGalleryScraper:
    """Scraper for Graphviz Gallery documentation stream."""
    
    def __init__(
        self,
        output_path: str = DEFAULT_OUTPUT,
        delay: float = DEFAULT_DELAY,
        retries: int = DEFAULT_RETRIES,
        dry_run: bool = False
    ):
        """Initialize scraper.
        
        Args:
            output_path: Path to output JSONL file
            delay: Delay between requests in seconds
            retries: Number of retries for failed requests
            dry_run: If True, don't write output file
        """
        self.output_path = output_path
        self.delay = delay
        self.retries = retries
        self.dry_run = dry_run
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
        self.writer = None if dry_run else JSONLWriter(output_path)
        self.metrics = ScraperMetrics()
    
    def _fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL with retry logic and error handling.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if all retries failed
        """
        for attempt in range(self.retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retries}): {url} - {e}")
                if attempt < self.retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
                else:
                    logger.error(f"All retries exhausted for {url}")
                    return None
    
    def extract_example_links(self, html: str) -> List[str]:
        """Extract links to individual example pages from gallery index.
        
        Args:
            html: HTML content of gallery index page
            
        Returns:
            List of absolute URLs to example pages
        """
        soup = BeautifulSoup(html, 'lxml')
        links = []
        
        # Find all links that point to Gallery examples
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Gallery examples are in /Gallery/ directory with .html extension
            if '/Gallery/' in href and href.endswith('.html'):
                abs_url = urljoin(GALLERY_URL, href)
                links.append(abs_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    def extract_example_content(self, url: str, html: str) -> List[GalleryExample]:
        """Extract title, description, and DOT code from example page.
        
        Args:
            url: URL of the example page
            html: HTML content of example page
            
        Returns:
            List of GalleryExample objects (may contain multiple DOT blocks)
        """
        soup = BeautifulSoup(html, 'lxml')
        examples = []
        
        # Extract title - look for h1 in main content, not nav
        title = "Untitled Example"
        main_content = soup.find('main') or soup.find('article') or soup
        title_elem = main_content.find('h1')
        if title_elem:
            title = title_elem.get_text().strip()
        
        # Extract description - look for paragraphs in main content, skip nav/header
        description = None
        if main_content:
            for p in main_content.find_all('p', recursive=True):
                # Skip if inside nav, header, footer
                if p.find_parent(['nav', 'header', 'footer']):
                    continue
                text = p.get_text().strip()
                if text and len(text) > 20 and not text.startswith('digraph'):
                    description = text
                    break
        
        # Extract DOT code blocks - look for code/pre elements
        code_blocks = []
        
        # Look for code blocks with DOT content
        for pre in soup.find_all('pre'):
            code = pre.get_text().strip()
            # Check if it looks like DOT code
            if code and (code.startswith('digraph') or code.startswith('graph') or 
                        'digraph' in code[:50] or 'graph {' in code[:50]):
                code_blocks.append(code)
        
        # Also check for code elements not already in pre
        for code_elem in soup.find_all('code'):
            # Skip if already inside a pre we captured
            if code_elem.find_parent('pre'):
                continue
            code = code_elem.get_text().strip()
            if code and (code.startswith('digraph') or code.startswith('graph')):
                code_blocks.append(code)
        
        # Clean up code blocks - filter out shell commands and extract pure DOT
        clean_codes = []
        for code in code_blocks:
            # Skip shell commands completely
            if any(x in code for x in ['echo ', '| dot', '> ', '< ']):
                # Try to extract DOT from shell command
                if 'digraph' in code:
                    # Extract the DOT part from echo command
                    if '"digraph' in code:
                        start = code.index('"digraph')
                        end = code.find('"', start + 1)
                        if end > start:
                            dot_code = code[start+1:end]
                            clean_codes.append(dot_code)
                continue
            # Keep pure DOT code
            if code.startswith('digraph') or code.startswith('graph') or code.startswith('strict'):
                clean_codes.append(code)
        
        # Remove duplicates while preserving order
        unique_codes = []
        seen_codes = set()
        for code in clean_codes:
            if code not in seen_codes and len(code) > 10:  # Minimum viable size
                seen_codes.add(code)
                unique_codes.append(code)
        
        # Create GalleryExample for each DOT block
        if not unique_codes:
            logger.warning(f"No DOT code found in {url}")
        else:
            for idx, code in enumerate(unique_codes):
                examples.append(GalleryExample(
                    url=url,
                    title=title,
                    description=description,
                    dot_code=code,
                    index=idx
                ))
        
        return examples
    
    def scrape(self) -> ScraperMetrics:
        """Run the scraper.
        
        Returns:
            ScraperMetrics with run statistics
        """
        logger.info("Starting Graphviz Gallery scraper")
        
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
        
        # Fetch gallery index
        logger.info(f"Fetching gallery index: {GALLERY_URL}")
        index_html = self._fetch_url(GALLERY_URL)
        if not index_html:
            logger.error("Failed to fetch gallery index")
            self.metrics.finish()
            return self.metrics
        
        # Extract example links
        example_urls = self.extract_example_links(index_html)
        self.metrics.total_found = len(example_urls)
        logger.info(f"Found {len(example_urls)} example pages")
        
        if len(example_urls) == 0:
            logger.warning("No example links found - gallery structure may have changed")
            self.metrics.finish()
            return self.metrics
        
        # Process each example
        for idx, url in enumerate(example_urls, 1):
            logger.info(f"Processing {idx}/{len(example_urls)}: {url}")
            
            # Fetch example page
            html = self._fetch_url(url)
            if not html:
                continue
            
            # Extract content
            examples = self.extract_example_content(url, html)
            self.metrics.total_scraped += len(examples)
            
            # Process each DOT block
            for example in examples:
                self._process_example(example)
            
            # Progress update
            pass_rate = self.metrics.pass_rate()
            logger.info(
                f"Progress: {idx}/{len(example_urls)} pages, "
                f"{self.metrics.validation_passed} passed, "
                f"{self.metrics.validation_failed} failed "
                f"({pass_rate:.1f}% pass rate)"
            )
            
            # Rate limiting
            if idx < len(example_urls):  # Don't delay after last request
                time.sleep(self.delay)
        
        # Finish metrics
        self.metrics.finish()
        
        # Final summary
        logger.info("\n" + self.metrics.summary())
        
        # Check pass rate threshold
        if self.metrics.pass_rate() < 98.0 and self.metrics.validation_passed > 0:
            logger.warning(
                f"Pass rate ({self.metrics.pass_rate():.1f}%) is below 98% threshold. "
                f"Please investigate failures."
            )
        
        return self.metrics
    
    def _process_example(self, example: GalleryExample):
        """Process a single example: validate and write to output.
        
        Args:
            example: GalleryExample to process
        """
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
        record_id = generate_id(example.dot_code, "graphviz-gallery")
        if example.index > 0:
            record_id = f"{record_id}-{example.index}"
        
        # Create DataRecord
        record = DataRecord(
            id=record_id,
            source="graphviz_gallery",
            source_url=example.url,
            license="EPL-2.0",
            task_type="NL_TO_DOT",
            input_text=example.to_instruction(),
            output_dot=example.dot_code,
            verification_status=result.to_schema_status(),
            scraped_at=datetime.utcnow().isoformat() + 'Z'
        )
        
        # Write to output (or just log in dry run)
        if self.dry_run:
            logger.info(f"[DRY RUN] Would write: {record.id}")
            self.metrics.increment('examples_written')
        else:
            written = self.writer.append(record)
            if written:
                self.metrics.increment('examples_written')
            else:
                self.metrics.increment('duplicates_skipped')
                logger.debug(f"Skipped duplicate: {record.id}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape Graphviz Gallery for DOT training examples"
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
        '--dry-run',
        action='store_true',
        help='Run without writing output file'
    )
    
    args = parser.parse_args()
    
    # Run scraper
    scraper = GraphvizGalleryScraper(
        output_path=args.output,
        delay=args.delay,
        retries=args.retries,
        dry_run=args.dry_run
    )
    
    metrics = scraper.scrape()
    
    # Exit with error code if pass rate too low
    if metrics.pass_rate() < 98.0 and metrics.validation_passed > 0:
        exit(1)
    
    exit(0)


if __name__ == '__main__':
    main()
