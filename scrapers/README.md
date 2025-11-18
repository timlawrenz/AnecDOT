# Graphviz Gallery Scraper

Scrapes the official Graphviz Gallery (graphviz.org/gallery/) to extract DOT examples for training data generation.

## Overview

This is the **documentation stream** scraper (Phase I.1) - the first of three data collection pipelines for the AnecDOT project.

**What it does:**
- Fetches the Graphviz Gallery index page
- Extracts links to individual example pages
- Parses each page for title, description, and DOT code
- Validates all DOT code using the Graphviz compiler
- Outputs JSONL training pairs in canonical schema format

## Usage

### Textual TUI (Recommended)

For the best experience, use the interactive Textual TUI:

```bash
python3 -m scrapers.graphviz_gallery_tui
```

**Features:**
- 📊 Live statistics dashboard
- 📈 Real-time progress bar with ETA
- 📝 Activity log viewer
- ⏸️ Pause/resume controls
- ⏹️ Graceful stop
- ⌨️ Keyboard shortcuts (q=quit, p=pause, s=stop)

**Custom options:**
```bash
python3 -m scrapers.graphviz_gallery_tui \
  --output data/gallery.jsonl \
  --delay 2.0 \
  --retries 5
```

### Command-Line Interface

For automation or headless environments, use the CLI:

```bash
python3 -m scrapers.graphviz_gallery
```

This will:
- Scrape graphviz.org/gallery/
- Validate all DOT code
- Write to `./data/documentation-stream.jsonl`
- Display progress and summary statistics

### CLI Options

**Custom Output Path:**
```bash
python3 -m scrapers.graphviz_gallery --output /path/to/output.jsonl
```

**Dry Run (No Output):**
```bash
python3 -m scrapers.graphviz_gallery --dry-run
```
Useful for testing scraper logic without writing files.

**Configurable Delay:**
```bash
python3 -m scrapers.graphviz_gallery --delay 2.0
```
Sets delay between requests to 2.0 seconds (default: 1.0).

**Custom Retry Count:**
```bash
python3 -m scrapers.graphviz_gallery --retries 5
```
Sets retry attempts for failed requests (default: 3).

## Output Format

Each line in the output JSONL file is a JSON object with:

```json
{
  "id": "graphviz-gallery-a3f5b8c1d2e4f6a8",
  "source": "graphviz_gallery",
  "source_url": "https://graphviz.org/gallery/example/",
  "license": "EPL-2.0",
  "task_type": "NL_TO_DOT",
  "input_text": "Example Title. Optional description text.",
  "context_snippet": null,
  "output_dot": "digraph { ... }",
  "verification_status": "passed_compiler",
  "scraped_at": "2025-11-18T17:00:00Z"
}
```

## Resume Capability

The scraper supports resuming interrupted runs:

1. Run scraper, gets interrupted
2. Re-run with same `--output` path
3. Scraper loads existing IDs and skips duplicates
4. Continues from where it left off

```bash
# First run (interrupted)
python -m scrapers.graphviz_gallery --output data.jsonl
# ... interrupted after 50 examples

# Resume
python -m scrapers.graphviz_gallery --output data.jsonl
# Loads 50 existing IDs, scrapes remaining examples
```

## Quality Metrics

The scraper tracks and reports:
- **Total examples found**: Example pages discovered
- **Validation pass rate**: % of DOT code that compiles successfully
- **Duplicates skipped**: Examples with duplicate content
- **Examples written**: Final count in output file

**Quality Threshold:** >98% validation pass rate

If pass rate < 98%, the scraper exits with error code 1 and logs a warning.

## Architecture

The scraper uses shared infrastructure for maximum reusability:

- `validation.dot_validator` - DOT validation (reused in Phase I.2, I.3, II.3)
- `validation.schema` - JSONL schema (consistent across all streams)
- `validation.writer` - Atomic writer with deduplication
- `common.id_generator` - Content-hash IDs (global dedup)
- `common.metrics` - Statistics tracking
- `common.logging_config` - Structured logging

**Stream-specific code:** ~450 lines (HTML parsing + orchestration)  
**Shared infrastructure:** ~650 lines (reused by future scrapers)

## Respectful Scraping

The scraper follows web scraping best practices:

- **User-Agent header**: Identifies as "AnecDOT-Scraper/1.0"
- **Rate limiting**: 1 second delay between requests (configurable)
- **Exponential backoff**: 2^n second delay on retries
- **Timeout**: 30 second timeout per request
- **Error handling**: Graceful handling of 4xx/5xx errors

## Future Scrapers

Phase I.2 (FSM Parser) and Phase I.3 (Synthetic Generator) will:
- Import all shared modules from `validation/` and `common/`
- Implement only source-specific extraction logic (~100 lines)
- Produce identical JSONL output format
- Use same validation, deduplication, and metrics

## Requirements

- Python 3.10+
- **Graphviz installed** (`dot` command must be in PATH)
- Dependencies: `beautifulsoup4`, `lxml`, `requests`

Install dependencies:
```bash
pip install -r requirements.txt
```

Install Graphviz:
```bash
# Linux
sudo apt-get install graphviz

# macOS
brew install graphviz

# Windows
choco install graphviz
```

## Testing

Run tests with:
```bash
pytest tests/test_graphviz_gallery.py -v
```

## License

This scraper is licensed under MIT/Apache-2.0 (tooling repository).  
The generated dataset is licensed under EPL-2.0 (separate artifact repository).
