## ADDED Requirements

### Requirement: DOT Compilation Validation
The validator SHALL verify DOT code syntax by invoking the Graphviz compiler and returning validation results with detailed diagnostics.

#### Scenario: Valid DOT code compilation
- **WHEN** `validate_dot(dot_code)` is called with syntactically correct DOT code
- **THEN** the function returns a ValidationResult with:
  - `is_valid`: True
  - `error_message`: None
  - `validation_method`: "graphviz_compiler"
- **AND** the compilation completes within the timeout period

#### Scenario: Invalid DOT syntax
- **WHEN** `validate_dot(dot_code)` is called with invalid syntax (e.g., mixing `--` and `->`)
- **THEN** the function returns a ValidationResult with:
  - `is_valid`: False
  - `error_message`: compiler's stderr output
  - `validation_method`: "graphviz_compiler"
- **AND** the error message includes line number and syntax issue description

#### Scenario: Compilation timeout
- **WHEN** DOT code causes the compiler to hang or run beyond timeout (default 10 seconds)
- **THEN** the subprocess is terminated gracefully
- **AND** returns ValidationResult with:
  - `is_valid`: False
  - `error_message`: "Compilation timeout after {timeout} seconds"
  - `validation_method`: "graphviz_compiler"

#### Scenario: Graphviz not installed
- **WHEN** the `dot` command is not found in system PATH
- **THEN** a GraphvizNotFoundError exception is raised
- **AND** the exception message includes installation instructions for common platforms
- **AND** the validator does not attempt to proceed with validation

### Requirement: Validation Configuration
The validator SHALL support configurable parameters for timeout, output format, and error handling behavior.

#### Scenario: Custom timeout configuration
- **WHEN** `validate_dot(dot_code, timeout=30)` is called
- **THEN** the compiler subprocess is allowed up to 30 seconds before termination
- **AND** the default remains 10 seconds if not specified

#### Scenario: Strict vs permissive mode
- **WHEN** `validate_dot(dot_code, strict=True)` is called
- **THEN** warnings from the compiler are treated as validation failures
- **AND** when `strict=False` (default), only errors cause validation failure

#### Scenario: Output format validation
- **WHEN** `validate_dot(dot_code, output_format='svg')` is called
- **THEN** the validator uses `dot -Tsvg` instead of default `-Tpng`
- **AND** format-specific compilation errors are captured

### Requirement: Batch Validation
The validator SHALL support efficient batch validation of multiple DOT code samples with progress tracking.

#### Scenario: Batch validation of multiple examples
- **WHEN** `validate_batch(dot_codes: List[str])` is called with 100 DOT examples
- **THEN** each example is validated sequentially
- **AND** returns a list of ValidationResult objects in the same order
- **AND** progress callback is invoked after each validation (if provided)

#### Scenario: Batch validation with failure threshold
- **WHEN** `validate_batch(dot_codes, fail_fast=True)` is called
- **AND** 10% of examples fail validation
- **THEN** validation stops early and returns results for processed examples
- **AND** when `fail_fast=False` (default), all examples are validated

#### Scenario: Parallel batch validation
- **WHEN** `validate_batch(dot_codes, parallel=True, max_workers=4)` is called
- **THEN** validation uses ThreadPoolExecutor with 4 workers
- **AND** results maintain input order despite parallel processing
- **AND** timeout applies per individual validation, not total batch time

### Requirement: Validation Result Schema
The validator SHALL return structured validation results with consistent schema for programmatic processing.

#### Scenario: Validation result structure
- **WHEN** any validation is performed
- **THEN** the result is a ValidationResult object with fields:
  - `is_valid`: bool
  - `error_message`: Optional[str]
  - `validation_method`: str (e.g., "graphviz_compiler")
  - `compiler_version`: Optional[str] (from `dot -V`)
  - `validation_duration`: float (seconds)
- **AND** the result can be serialized to JSON

#### Scenario: Detailed error diagnostics
- **WHEN** validation fails due to syntax error
- **THEN** the error_message includes:
  - Line number where error occurred (if available)
  - Description of the syntax issue
  - Full stderr from compiler
- **AND** multi-line errors are preserved with formatting

### Requirement: Caching for Performance
The validator SHALL implement optional caching to avoid redundant validation of identical DOT code.

#### Scenario: Cache hit for duplicate DOT code
- **WHEN** the same DOT code (by SHA256 hash) is validated twice
- **AND** caching is enabled
- **THEN** the second validation returns cached result immediately
- **AND** no subprocess is spawned for the cached validation
- **AND** cache size is limited to prevent memory exhaustion (default: 1000 entries)

#### Scenario: Cache disabled
- **WHEN** `validate_dot(dot_code, use_cache=False)` is called
- **OR** caching is globally disabled
- **THEN** validation always invokes the compiler
- **AND** no cache lookup or storage occurs

#### Scenario: Cache eviction policy
- **WHEN** cache exceeds maximum size (default 1000 entries)
- **THEN** least recently used (LRU) entries are evicted
- **AND** cache statistics are available via `get_cache_stats()`

### Requirement: Error Handling and Robustness
The validator SHALL handle edge cases and system errors gracefully without crashing.

#### Scenario: Empty DOT code
- **WHEN** `validate_dot("")` is called with empty string
- **THEN** returns ValidationResult with:
  - `is_valid`: False
  - `error_message`: "Empty DOT code provided"

#### Scenario: Extremely large DOT code
- **WHEN** DOT code exceeds size threshold (default 10MB)
- **THEN** returns ValidationResult with:
  - `is_valid`: False
  - `error_message`: "DOT code exceeds maximum size limit"
- **AND** does not attempt compilation to prevent resource exhaustion

#### Scenario: Invalid UTF-8 encoding
- **WHEN** DOT code contains invalid UTF-8 byte sequences
- **THEN** the validator attempts to decode with error='replace'
- **AND** proceeds with validation using replacement characters
- **AND** logs a warning about encoding issues

#### Scenario: System resource limits
- **WHEN** subprocess creation fails due to system limits (e.g., max processes)
- **THEN** raises a SystemResourceError with descriptive message
- **AND** includes retry suggestions in the error message

### Requirement: Integration with Data Schema
The validator SHALL integrate seamlessly with the project's JSONL data schema for consistent validation status recording.

#### Scenario: Validation status enum compatibility
- **WHEN** validation result is_valid is True
- **THEN** it maps to schema enum value "passed_compiler"
- **AND** when is_valid is False, maps to "failed_compiler"

#### Scenario: Metadata enrichment
- **WHEN** validation is performed for dataset generation
- **THEN** validation result can be converted to schema-compatible dict with:
  - `verification_status`: "passed_compiler" | "failed_compiler"
  - `compiler_version`: str (for reproducibility)
  - `validated_at`: ISO 8601 timestamp

### Requirement: Logging and Observability
The validator SHALL provide structured logging for monitoring validation performance and debugging issues.

#### Scenario: Validation logging
- **WHEN** validation is performed with logging enabled
- **THEN** log entries include:
  - Validation start and completion timestamps
  - DOT code size (bytes)
  - Validation duration
  - Result (pass/fail)
  - Error message if failed
- **AND** logs use structured format (JSON) for easy parsing

#### Scenario: Performance metrics
- **WHEN** `get_validation_metrics()` is called
- **THEN** returns statistics including:
  - Total validations performed
  - Success/failure counts
  - Average validation duration
  - Cache hit rate (if caching enabled)
  - Compiler version

### Requirement: Cross-Platform Compatibility
The validator SHALL work consistently across Linux, macOS, and Windows platforms where Graphviz is installed.

#### Scenario: Platform-specific binary resolution
- **WHEN** validator is initialized on any platform
- **THEN** the `dot` binary is located using shutil.which()
- **AND** falls back to common installation paths if not in PATH
- **AND** raises GraphvizNotFoundError with platform-specific installation instructions

#### Scenario: Path handling on Windows
- **WHEN** validation runs on Windows
- **THEN** subprocess uses shell=False for security
- **AND** handles Windows-style path separators correctly
- **AND** uses `NUL` instead of `/dev/null` for output redirection
