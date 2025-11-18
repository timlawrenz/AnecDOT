# Common Utilities

Shared utilities for AnecDOT data collection pipelines.

## Modules

### `id_generator.py`
Content-hash based ID generation for global deduplication across all data streams.

**Usage:**
```python
from common.id_generator import generate_id

# Generate ID with source prefix
id1 = generate_id("digraph { A -> B; }", "gallery")
# Result: "gallery-a3f5b8c1d2e4f6a8"

# Generate ID without prefix
id2 = generate_id("digraph { A -> B; }")
# Result: "a3f5b8c1d2e4f6a8"
```

**Deduplication:**
If the same DOT code appears in multiple sources, it will have the same hash,
enabling cross-stream deduplication.

### `metrics.py`
Summary statistics tracking for scraper runs.

**Usage:**
```python
from common.metrics import ScraperMetrics

metrics = ScraperMetrics()

# Increment counters
metrics.increment('validation_passed')
metrics.increment('validation_failed')

# Finish and get summary
metrics.finish()
print(metrics.summary())
print(f"Pass rate: {metrics.pass_rate():.1f}%")
```

**Tracked Metrics:**
- `total_found`: Total examples discovered
- `total_scraped`: Examples successfully extracted
- `validation_passed`: Passed DOT validation
- `validation_failed`: Failed DOT validation
- `duplicates_skipped`: Skipped due to duplicate IDs
- `examples_written`: Final count written to output

### `logging_config.py`
Structured logging configuration for consistent log format across all scrapers.

**Usage:**
```python
from common.logging_config import setup_logger

logger = setup_logger(__name__)

logger.info("Starting scraper")
logger.warning("Potential issue detected")
logger.error("Failed to process example")
```

**Log Format:**
```
2025-11-18T17:00:00 - module_name - INFO - Starting scraper
```

## Design Philosophy

These utilities are designed to be:
- **Simple**: Single responsibility, minimal dependencies
- **Reusable**: Used by all three data streams without modification
- **Consistent**: Same behavior and output format across all scrapers
- **Stateless**: No global state, easy to test
