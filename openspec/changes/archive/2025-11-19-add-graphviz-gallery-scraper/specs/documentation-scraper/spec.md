## ADDED Requirements

### Requirement: Gallery Index Crawling
The scraper SHALL fetch the Graphviz Gallery index page (graphviz.org/gallery/) and extract all links to individual example pages.

#### Scenario: Successful gallery index retrieval
- **WHEN** the scraper requests the gallery index page
- **THEN** all example page URLs are extracted and returned as a list
- **AND** the HTTP request includes a respectful User-Agent header
- **AND** the request completes within 30 seconds or times out gracefully

#### Scenario: Gallery index page unavailable
- **WHEN** the gallery index page returns HTTP 5xx error or network timeout
- **THEN** the scraper logs the error with timestamp
- **AND** retries up to 3 times with exponential backoff (2s, 4s, 8s)
- **AND** fails gracefully if all retries exhausted

#### Scenario: No example links found
- **WHEN** the gallery index page HTML structure has changed and no links are extracted
- **THEN** the scraper logs a warning indicating zero examples found
- **AND** exits with non-zero status code
- **AND** provides diagnostic information about the page structure

### Requirement: Example Page Parsing
The scraper SHALL fetch each example page and extract the title, description, natural language context, and literal DOT source code.

#### Scenario: Complete example page
- **WHEN** an example page contains title, description, and DOT code block
- **THEN** all fields are extracted and stored
- **AND** the DOT code preserves exact formatting (whitespace, indentation, comments)
- **AND** the source URL is recorded in metadata

#### Scenario: Example page with minimal metadata
- **WHEN** an example page contains only title and DOT code (no description)
- **THEN** the scraper uses the title as the instruction text
- **AND** marks the description field as null
- **AND** logs the example ID for potential manual review
- **AND** continues processing (does not skip the example)

#### Scenario: Malformed HTML in example page
- **WHEN** an example page has malformed HTML or unexpected structure
- **THEN** Beautiful Soup attempts to parse with lxml backend
- **AND** the scraper logs parsing warnings
- **AND** extracts fields using fallback CSS selectors
- **AND** skips the example only if DOT code block cannot be located

#### Scenario: Example page with multiple DOT blocks
- **WHEN** an example page contains multiple DOT code blocks
- **THEN** each DOT block is extracted as a separate training example
- **AND** each shares the same title and description
- **AND** each receives a unique ID with sequential index suffix (e.g., -1, -2)

### Requirement: DOT Syntax Validation
The scraper SHALL validate all extracted DOT code using the reusable DOT validator component (see `specs/dot-validator/`) before including examples in the dataset.

#### Scenario: Valid DOT code
- **WHEN** the scraper calls `validate_dot(dot_code)` from the validator module
- **AND** the validation returns is_valid=True
- **THEN** the example is marked with verification_status "passed_compiler"
- **AND** the example is included in the output JSONL file

#### Scenario: Invalid DOT syntax
- **WHEN** validation returns is_valid=False
- **THEN** the example is marked with verification_status "failed_compiler"
- **AND** the validator's error_message is logged
- **AND** the example is excluded from the output JSONL file
- **AND** the failure is counted in summary statistics

#### Scenario: Validation exception
- **WHEN** the validator raises a GraphvizNotFoundError
- **THEN** the scraper exits immediately with the error message
- **AND** instructs user to install Graphviz
- **AND** does not attempt to scrape or write partial data

**Note:** See `specs/dot-validator/spec.md` for complete validation behavior including timeout handling, caching, and cross-platform compatibility.

### Requirement: JSONL Output Generation
The scraper SHALL generate structured JSONL output conforming to the project's data schema with proper metadata and licensing information.

#### Scenario: Valid example output
- **WHEN** a DOT example passes validation
- **THEN** a JSON record is appended to the output file with fields:
  - `id`: "graphviz-gallery-{sha256(output_dot)[:16]}"
  - `source`: "graphviz_gallery"
  - `source_url`: full URL to example page
  - `license`: "EPL-2.0"
  - `task_type`: "NL_TO_DOT"
  - `input_text`: "{title}. {description}" or "{title}" if no description
  - `context_snippet`: null (reserved for future use)
  - `output_dot`: exact DOT code with preserved formatting
  - `verification_status`: "passed_compiler"
  - `scraped_at`: ISO 8601 timestamp
- **AND** the record is written with atomic append operation

#### Scenario: Duplicate DOT code detected
- **WHEN** two examples produce the same SHA256 hash of output_dot
- **THEN** only the first occurrence is written to output
- **AND** the duplicate is logged with both source URLs
- **AND** the duplicate count is included in summary statistics

#### Scenario: Output file already exists
- **WHEN** the scraper is run and the output file path exists
- **THEN** the scraper loads existing IDs to enable resume capability
- **AND** skips examples already present in the file
- **AND** appends only new examples
- **AND** logs "Resuming from existing file with {count} examples"

### Requirement: Rate Limiting and Respectful Crawling
The scraper SHALL implement rate limiting and follow web scraping best practices to avoid overloading the Graphviz website.

#### Scenario: Request rate limiting
- **WHEN** the scraper fetches multiple pages sequentially
- **THEN** a minimum delay of 1 second is enforced between HTTP requests
- **AND** the delay is configurable via command-line option (default: 1.0 seconds)

#### Scenario: User-Agent header
- **WHEN** any HTTP request is made
- **THEN** the User-Agent header identifies the scraper
- **AND** includes contact information or project URL
- **AND** follows format: "AnecDOT-Scraper/1.0 (+https://github.com/...)"

#### Scenario: HTTP error handling
- **WHEN** an HTTP request returns 4xx or 5xx status
- **THEN** the error is logged with URL and status code
- **AND** exponential backoff is applied for 5xx errors (up to 3 retries)
- **AND** 4xx errors skip the example after logging (no retries)

### Requirement: Progress Reporting and Logging
The scraper SHALL provide clear progress indicators and detailed logging for troubleshooting and monitoring.

#### Scenario: Progress during scraping
- **WHEN** the scraper processes multiple examples
- **THEN** progress is printed to stdout in format: "Processing {current}/{total}: {title}"
- **AND** the percentage complete is displayed
- **AND** the current pass/fail validation rate is shown

#### Scenario: Summary statistics
- **WHEN** the scraper completes (successfully or with errors)
- **THEN** summary statistics are printed:
  - Total examples found
  - Examples scraped
  - Validation pass count
  - Validation fail count
  - Duplicates skipped
  - Examples written to JSONL
  - Total execution time
- **AND** statistics are logged to a separate JSON file

#### Scenario: Error logging
- **WHEN** any error occurs (network, parsing, validation)
- **THEN** the error is logged to stderr with:
  - Timestamp (ISO 8601)
  - Example ID or URL
  - Error type and message
  - Stack trace for unexpected errors

### Requirement: Command-Line Interface
The scraper SHALL provide a command-line interface with configurable options for flexibility and automation.

#### Scenario: Basic scraper execution
- **WHEN** user runs `python -m scrapers.graphviz_gallery`
- **THEN** the scraper executes with default options:
  - Output: `./data/documentation-stream.jsonl`
  - Delay: 1.0 seconds
  - Retries: 3
- **AND** displays progress to stdout
- **AND** exits with status 0 on success or non-zero on failure

#### Scenario: Custom output path
- **WHEN** user runs with `--output /custom/path.jsonl`
- **THEN** the JSONL file is written to the specified path
- **AND** parent directories are created if they don't exist

#### Scenario: Configurable delay and retries
- **WHEN** user runs with `--delay 2.5 --retries 5`
- **THEN** the scraper uses 2.5 second delay between requests
- **AND** attempts up to 5 retries for failed requests

#### Scenario: Dry run mode
- **WHEN** user runs with `--dry-run` flag
- **THEN** the scraper fetches and parses examples
- **AND** validates DOT code
- **AND** prints what would be written to JSONL
- **AND** does not write any output file

#### Scenario: Resume capability
- **WHEN** a previous scrape was interrupted and output file exists
- **THEN** user can resume by running with same output path
- **AND** the scraper automatically detects existing examples by ID
- **AND** skips already-scraped examples
- **AND** continues from where it left off

### Requirement: Error Handling and Robustness
The scraper SHALL handle errors gracefully and provide clear diagnostics without crashing unexpectedly.

#### Scenario: Network interruption during scrape
- **WHEN** network connection is lost mid-scrape
- **THEN** the current request fails with timeout or connection error
- **AND** the scraper logs the error and continues with next example
- **AND** already-scraped examples remain in output file (atomic writes)

#### Scenario: Invalid UTF-8 in example page
- **WHEN** an example page contains invalid UTF-8 sequences
- **THEN** Beautiful Soup decodes with error='replace' strategy
- **AND** the scraper logs a warning about encoding issues
- **AND** continues processing with placeholder characters

#### Scenario: Disk full during write
- **WHEN** the output file write fails due to insufficient disk space
- **THEN** the scraper catches the IOError exception
- **AND** prints clear error message: "Disk full, cannot write to {path}"
- **AND** exits with status code 1
- **AND** does not corrupt the existing JSONL file

### Requirement: Deduplication
The scraper SHALL detect and skip duplicate DOT examples to prevent training data redundancy.

#### Scenario: Exact DOT code duplicate
- **WHEN** two gallery examples have identical output_dot content
- **THEN** only the first example is included in output
- **AND** the duplicate is detected via SHA256 hash comparison
- **AND** both source URLs are logged for reference

#### Scenario: Whitespace-only differences
- **WHEN** two examples differ only in trailing whitespace or blank lines
- **THEN** they are treated as separate examples (exact formatting preserved)
- **AND** both are included in output
- **AND** no normalization is applied to DOT code

**Rationale**: Preserving exact formatting maintains authorship style as training signal. True duplicates (identical hashes) are rare in curated gallery.
