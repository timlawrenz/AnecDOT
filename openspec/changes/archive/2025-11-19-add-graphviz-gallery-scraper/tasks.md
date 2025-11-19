## 1. Design & Architecture

- [x] 1.1 Review Graphviz Gallery structure and HTML patterns
- [x] 1.2 Design scraper architecture (single-pass vs incremental)
- [x] 1.3 Define JSONL schema for all data streams (shared format)
- [x] 1.4 Design shared infrastructure interfaces (validator, writer, metrics)
- [x] 1.5 Design reusable DOT validator API for cross-project use

## 2. Shared Infrastructure - Schema & Writing

- [x] 2.1 Create `validation/schema.py` with DataRecord class
- [x] 2.2 Implement JSONL schema validation (all required fields)
- [x] 2.3 Create `validation/writer.py` for atomic JSONL writes
- [x] 2.4 Implement deduplication logic in writer (check existing IDs)
- [x] 2.5 Create `common/id_generator.py` with content-hash generation
- [x] 2.6 Create `common/metrics.py` for summary statistics tracking
- [x] 2.7 Create `common/logging_config.py` for structured logging

## 3. Reusable DOT Validator Implementation

- [x] 3.1 Create `validation/dot_validator.py` module
- [x] 3.2 Implement `validate_dot()` function with subprocess wrapper
- [x] 3.3 Add ValidationResult dataclass for structured results
- [x] 3.4 Implement timeout handling and Graphviz binary detection
- [x] 3.5 Add batch validation support (`validate_batch()`)
- [x] 3.6 Implement LRU caching for duplicate validation optimization
- [x] 3.7 Add cross-platform compatibility (Linux, macOS, Windows)
- [x] 3.8 Add structured logging and performance metrics

## 4. Core Scraper Implementation

- [x] 4.1 Implement gallery index page crawler
- [x] 4.2 Extract links to individual example pages
- [x] 4.3 Implement example page parser (title, description, DOT code)
- [x] 4.4 Handle edge cases (missing fields, malformed HTML)
- [x] 4.5 Add rate limiting and respectful crawling (User-Agent, delays)

## 5. Scraper Integration with Shared Infrastructure

- [x] 5.1 Import and use DataRecord schema from validation.schema
- [x] 5.2 Integrate reusable DOT validator into scraper pipeline
- [x] 5.3 Use shared JSONLWriter for output with deduplication
- [x] 5.4 Use shared ID generator for consistent ID format
- [x] 5.5 Implement error logging using shared logging config

## 6. Data Output

- [x] 6.1 Add metadata fields (source URL, license, timestamp) to records
- [x] 6.2 Ensure EPL-2.0 compliance in all records
- [x] 6.3 Generate summary statistics using shared metrics module
- [x] 6.4 Verify output JSONL format matches schema

## 7. Testing

- [x] 7.1 Create unit tests for shared schema validation
- [x] 7.2 Create unit tests for shared writer and ID generator
- [x] 7.3 Create unit tests for DOT validator (all scenarios)
- [x] 7.4 Create unit tests for HTML parsing logic
- [x] 7.5 Create integration tests for validator caching and batch operations
- [x] 7.6 Add integration test with mock HTML responses for scraper
- [x] 7.7 Test cross-stream deduplication (shared ID space)
- [x] 7.8 Manual verification with actual gallery data

## 8. Documentation

- [x] 8.1 Add comprehensive docstrings to shared schema module
- [x] 8.2 Add comprehensive docstrings to DOT validator module
- [x] 8.3 Create README for `validation/` directory (validator + schema usage)
- [x] 8.4 Create README for `common/` directory (shared utilities)
- [x] 8.5 Add usage documentation to scraper module docstrings
- [x] 8.6 Create README in scrapers/ directory
- [x] 8.7 Document how future scrapers should use shared infrastructure
- [x] 8.8 Add example commands and expected output

## 9. Interface & Configuration

- [x] 9.1 Create command-line interface for scraper (argparse)
- [x] 9.2 Add configurable options (output path, retry attempts, delay)
- [x] 9.3 Create TUI interface using Textual for better UX
- [x] 9.4 Add live progress display (current/total, pass rate, speed)
- [x] 9.5 Add interactive controls (pause/resume, stop gracefully)
- [x] 9.6 Display real-time statistics dashboard
- [x] 9.7 Add log viewer panel for errors and warnings
- [x] 9.8 Implement resume capability for interrupted scrapes
