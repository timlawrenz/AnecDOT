# Change: Implement Graphviz Gallery Scraper for Documentation Stream

## Why

Phase I.1 requires building the documentation stream scraper to extract DOT examples from the official Graphviz Gallery (graphviz.org/gallery/). This is the first of three data streams needed to create high-quality training pairs for teaching LLMs to generate syntactically valid and semantically accurate DOT graphs.

Currently, there is no mechanism to automatically collect and structure DOT examples from the Graphviz documentation. Manual collection would be time-consuming, error-prone, and not reproducible. An automated scraper ensures consistent quality, proper metadata tracking (source, license), and enables incremental updates as the gallery is updated.

## What Changes

- Create new capability `dot-validator` as a **reusable component** for validating DOT syntax across all data pipelines and training validation
- Create shared infrastructure (`validation/`, `common/`) for **all three data streams** to avoid code duplication
- Create new capability `documentation-scraper` for extracting training data from Graphviz documentation
- Implement scraper to crawl graphviz.org/gallery/ and extract all example pages
- Parse each example page to extract: title, description, natural language context, and literal DOT source code
- Generate structured JSONL training pairs following the project's data schema
- Use the reusable DOT validator to verify all extracted code before dataset inclusion
- Add metadata tracking for source URLs and EPL-2.0 license compliance
- Include error handling, retry logic, and rate limiting to respect the source website

## Impact

- **New capabilities**: 
  - `specs/dot-validator/` - Reusable DOT validation component (used by all data streams + Phase II)
  - `specs/documentation-scraper/` - Gallery scraper using the validator
- **New shared infrastructure** (used by all three streams):
  - `validation/dot_validator.py` - **Reusable** DOT syntax validation module
  - `validation/schema.py` - JSONL schema definition and validation
  - `validation/writer.py` - Atomic JSONL writer with deduplication
  - `common/id_generator.py` - Content-hash ID generation
  - `common/metrics.py` - Summary statistics tracking
  - `common/logging_config.py` - Structured logging setup
- **Stream-specific code**:
  - `scrapers/graphviz_gallery.py` - Gallery scraper implementation
- **Dependencies**: Beautiful Soup 4, lxml, requests (already in project.md)
- **Outputs**: `data/documentation-stream.jsonl` (will live in separate Repo B under EPL-2.0)
- **Roadmap**: Completes Phase I.1 checkbox, unblocks Phase I.2 (FSM parser) with zero code duplication
- **Future use**: All shared modules will be imported by Phase I.2 (FSM parser) and Phase I.3 (synthetic generator)
