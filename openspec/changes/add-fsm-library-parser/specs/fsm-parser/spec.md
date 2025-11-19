## ADDED Requirements

### Requirement: FSM Repository Discovery
The parser SHALL accept a list of GitHub repositories or local filesystem paths containing FSM library usage examples.

#### Scenario: Repository URL provided
- **WHEN** user provides a GitHub repository URL containing FSM code
- **THEN** the parser clones the repository to a temporary location and scans for FSM patterns

#### Scenario: Local path provided
- **WHEN** user provides a local directory path
- **THEN** the parser scans the directory recursively for files matching FSM library import patterns

#### Scenario: Invalid repository
- **WHEN** repository URL is invalid or inaccessible
- **THEN** the parser logs an error and continues with remaining repositories

### Requirement: Static FSM Detection
The parser SHALL use static code analysis to identify FSM class definitions and their configuration.

#### Scenario: Python python-statemachine detected
- **WHEN** scanning a Python file with `from statemachine import StateMachine`
- **THEN** extract all StateMachine subclasses and their state/transition definitions

#### Scenario: Python transitions library detected
- **WHEN** scanning a Python file with `from transitions import Machine`
- **THEN** extract Machine instantiations and their state/transition configurations

#### Scenario: No FSM pattern found
- **WHEN** file contains no recognized FSM library imports
- **THEN** skip the file without error

#### Scenario: Malformed Python code
- **WHEN** file contains syntax errors preventing AST parsing
- **THEN** log a warning with file path and continue processing

### Requirement: Dynamic DOT Extraction
The parser SHALL execute FSM library methods to generate DOT representations in an isolated environment.

#### Scenario: Successful DOT generation
- **WHEN** FSM instance has a `.to_dot()` or equivalent method
- **THEN** execute the method and capture the resulting DOT string

#### Scenario: Method execution timeout
- **WHEN** DOT generation takes longer than 30 seconds
- **THEN** terminate execution and log a timeout error

#### Scenario: Method requires parameters
- **WHEN** DOT export method requires configuration parameters
- **THEN** attempt common defaults (empty title, default layout) before skipping

#### Scenario: Execution sandbox violation
- **WHEN** code attempts network access or filesystem writes during execution
- **THEN** block the operation and terminate with security warning

### Requirement: Code Context Extraction
The parser SHALL capture the original FSM source code as context for training pairs.

#### Scenario: Extract class definition
- **WHEN** FSM is defined as a class
- **THEN** capture the complete class definition including docstrings

#### Scenario: Extract inline configuration
- **WHEN** FSM is configured via dictionary or builder pattern
- **THEN** capture the configuration block and instantiation code

#### Scenario: Context size limit
- **WHEN** extracted context exceeds 2000 characters
- **THEN** truncate with ellipsis while preserving key structural elements

### Requirement: DOT Syntax Validation
The parser SHALL validate all extracted DOT strings using the Graphviz compiler before inclusion in the dataset.

#### Scenario: Valid DOT output
- **WHEN** extracted DOT compiles successfully with `dot -Tpng`
- **THEN** mark as `verification_status: "passed_compiler"` and include in output

#### Scenario: Invalid DOT syntax
- **WHEN** DOT compilation fails with syntax errors
- **THEN** mark as `verification_status: "failed_compiler"` and log the error details

#### Scenario: Compiler not available
- **WHEN** Graphviz `dot` binary is not found in PATH
- **THEN** raise a configuration error and halt processing

### Requirement: License Compliance Tracking
The parser SHALL record source license metadata for each extracted example to ensure dataset licensing compliance.

#### Scenario: Repository with LICENSE file
- **WHEN** processing code from a repository with a LICENSE file
- **THEN** parse the license type and include in `license` field

#### Scenario: OSI-approved license detected
- **WHEN** license is MIT, Apache-2.0, BSD, or other OSI-approved
- **THEN** include example in output with proper attribution

#### Scenario: Proprietary or non-OSI license
- **WHEN** license is proprietary, AGPL, or uncertain
- **THEN** skip the repository and log a license compliance warning

#### Scenario: No license found
- **WHEN** repository has no LICENSE file
- **THEN** assume all rights reserved and skip with warning

### Requirement: JSONL Output Format
The parser SHALL generate output in strict JSONL format matching the project schema with `task_type: CODE_TO_DOT`.

#### Scenario: Complete training pair
- **WHEN** FSM code and DOT are successfully extracted
- **THEN** output includes `id`, `source`, `license`, `task_type`, `context_snippet` (FSM code), `output_dot`, and `verification_status`

#### Scenario: Incremental output
- **WHEN** processing multiple repositories
- **THEN** append each valid pair to the JSONL file immediately (streaming output)

#### Scenario: Deduplication
- **WHEN** identical DOT output is encountered from different sources
- **THEN** generate unique `id` but flag for manual deduplication review

### Requirement: Command-Line Interface
The parser SHALL provide a CLI for batch processing with options for output path, repository sources, and dry-run mode.

#### Scenario: Basic usage
- **WHEN** user runs `python -m parsers.fsm_extractor --repos repos.txt`
- **THEN** process all repositories and output to `./data/logic-stream.jsonl`

#### Scenario: Custom output path
- **WHEN** user specifies `--output custom.jsonl`
- **THEN** write results to the specified file path

#### Scenario: Dry run mode
- **WHEN** user passes `--dry-run` flag
- **THEN** log extraction results without creating output file

#### Scenario: Verbose logging
- **WHEN** user passes `--verbose` flag
- **THEN** output detailed progress for each file processed

### Requirement: Interactive TUI (Optional Enhancement)
The parser SHALL provide a Textual-based TUI for interactive repository selection and real-time extraction monitoring.

#### Scenario: Repository selection interface
- **WHEN** user runs `python -m parsers.fsm_extractor_tui`
- **THEN** display a list of discovered FSM repositories with selection checkboxes

#### Scenario: Real-time extraction progress
- **WHEN** extraction is running
- **THEN** display progress bar, current file, and success/failure counts

#### Scenario: Results preview
- **WHEN** extraction completes
- **THEN** show sample extracted pairs with syntax-highlighted DOT output

### Requirement: Error Recovery and Reporting
The parser SHALL continue processing after individual failures and provide a comprehensive error report.

#### Scenario: Partial failure recovery
- **WHEN** one repository fails to process
- **THEN** log the error and continue with remaining repositories

#### Scenario: Error summary report
- **WHEN** processing completes
- **THEN** output summary with total processed, succeeded, failed, and skipped counts

#### Scenario: Detailed error log
- **WHEN** failures occur
- **THEN** write detailed error information to `logic-stream-errors.log`

### Requirement: Performance Optimization
The parser SHALL process repositories efficiently to handle large codebases.

#### Scenario: Parallel file processing
- **WHEN** scanning a large repository
- **THEN** use multiprocessing to analyze files in parallel (default: 4 workers)

#### Scenario: Smart filtering
- **WHEN** repository contains >10,000 files
- **THEN** pre-filter by file extension and import patterns before full AST parsing

#### Scenario: Execution caching
- **WHEN** the same repository is processed multiple times
- **THEN** cache successful DOT extractions keyed by file hash
