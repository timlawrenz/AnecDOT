# Validation Modules

This directory contains reusable validation and data handling modules used by all AnecDOT data streams.

## Modules

### `dot_validator.py`
DOT code validation using the Graphviz compiler. Used by all data streams (documentation, logic, synthetic) and Phase II training validation.

**Key Features:**
- Subprocess-based validation using official Graphviz compiler
- LRU caching for performance (1000 entry cache)
- Batch validation with optional parallelization
- Cross-platform support (Linux, macOS, Windows)
- Configurable timeout and strict mode

**Usage:**
```python
from validation.dot_validator import validate_dot

result = validate_dot("digraph { A -> B; }")
if result.is_valid:
    print("Valid DOT code!")
else:
    print(f"Invalid: {result.error_message}")
```

### `schema.py`
JSONL data schema for training datasets. All streams produce records conforming to this schema.

**Schema Fields:**
- `id`: Unique identifier (format: "{source}-{hash}")
- `source`: Data stream identifier
- `source_url`: Attribution URL
- `license`: Source license (e.g., "EPL-2.0")
- `task_type`: "NL_TO_DOT" or "CODE_TO_DOT"
- `input_text`: Natural language or source code
- `output_dot`: DOT code (exact formatting preserved)
- `verification_status`: "passed_compiler" or "failed_compiler"
- `scraped_at`: ISO 8601 timestamp

**Usage:**
```python
from validation.schema import DataRecord
from datetime import datetime

record = DataRecord(
    id="example-123",
    source="my_scraper",
    source_url="https://example.com",
    license="EPL-2.0",
    task_type="NL_TO_DOT",
    input_text="Create a simple graph",
    output_dot="digraph { A -> B; }",
    verification_status="passed_compiler",
    scraped_at=datetime.utcnow().isoformat() + 'Z'
)
```

### `writer.py`
Atomic JSONL writer with deduplication support. Enables safe, resumable writing.

**Key Features:**
- Atomic append operations (safe for interruptions)
- Automatic deduplication by record ID
- Resume capability (loads existing IDs on init)
- Schema validation before writing

**Usage:**
```python
from validation.writer import JSONLWriter
from validation.schema import DataRecord

writer = JSONLWriter("output.jsonl")

if not writer.is_duplicate(record.id):
    written = writer.append(record)
```

## Adding a New Data Stream

To add a new scraper/generator that uses this infrastructure:

```python
from validation.dot_validator import validate_dot
from validation.schema import DataRecord
from validation.writer import JSONLWriter
from common.id_generator import generate_id
from common.metrics import ScraperMetrics

# 1. Extract data (source-specific logic)
examples = extract_from_your_source()

# 2. Use shared infrastructure
writer = JSONLWriter("output.jsonl")
metrics = ScraperMetrics()

for example in examples:
    # Validate
    result = validate_dot(example.dot_code)
    
    if result.is_valid:
        # Create record
        record = DataRecord(
            id=generate_id(example.dot_code, "your-source"),
            source="your_source",
            output_dot=example.dot_code,
            # ... other fields
        )
        
        # Write (handles deduplication)
        if writer.append(record):
            metrics.increment("examples_written")
```

## Requirements

- Python 3.10+
- Graphviz installed (`dot` command in PATH)

## Testing

Run tests with:
```bash
pytest tests/ -v
```
