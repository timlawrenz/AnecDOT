## 1. Research & Discovery
- [ ] 1.1 Survey target FSM libraries and document their DOT export APIs
  - [ ] 1.1.1 Test `python-statemachine` `.to_dot()` method signatures
  - [ ] 1.1.2 Test `transitions` library DOT export capabilities
  - [ ] 1.1.3 Document any Ruby `aasm` export methods (optional)
- [ ] 1.2 Identify candidate repositories using FSM libraries
  - [ ] 1.2.1 GitHub search for `python-statemachine` usage
  - [ ] 1.2.2 GitHub search for `transitions` library usage
  - [ ] 1.2.3 Create curated list of 10-20 high-quality repositories
- [ ] 1.3 Analyze license distribution of candidate repositories
  - [ ] 1.3.1 Filter for OSI-approved licenses only
  - [ ] 1.3.2 Document attribution requirements

## 2. Core Infrastructure
- [ ] 2.1 Create `parsers/` module structure
  - [ ] 2.1.1 Create `parsers/__init__.py`
  - [ ] 2.1.2 Create `parsers/common/` for shared utilities
  - [ ] 2.1.3 Create `parsers/fsm_extractor/` for main logic
- [ ] 2.2 Set up static analysis tooling
  - [ ] 2.2.1 Add `astroid` or `tree-sitter-python` to requirements.txt
  - [ ] 2.2.2 Implement AST-based FSM pattern detector
  - [ ] 2.2.3 Create library-specific extractors (python-statemachine, transitions)
- [ ] 2.3 Implement execution sandbox
  - [ ] 2.3.1 Design isolated execution environment (subprocess or Docker)
  - [ ] 2.3.2 Implement timeout mechanism (30-second limit)
  - [ ] 2.3.3 Add resource monitoring and network/filesystem restrictions

## 3. Repository Processing
- [ ] 3.1 Implement repository discovery
  - [ ] 3.1.1 Support GitHub URL cloning (temporary directory)
  - [ ] 3.1.2 Support local filesystem path scanning
  - [ ] 3.1.3 Add repository cleanup after processing
- [ ] 3.2 Build license compliance checker
  - [ ] 3.2.1 Parse LICENSE files using `licensee` or similar
  - [ ] 3.2.2 Implement OSI-approved license allowlist
  - [ ] 3.2.3 Log and skip non-compliant repositories
- [ ] 3.3 Create file filtering logic
  - [ ] 3.3.1 Pre-filter by extension (.py for Python)
  - [ ] 3.3.2 Quick scan for FSM library imports
  - [ ] 3.3.3 Skip test files and documentation directories

## 4. FSM Extraction Logic
- [ ] 4.1 Implement StateMachine class detector
  - [ ] 4.1.1 Parse AST to find class definitions inheriting from StateMachine
  - [ ] 4.1.2 Extract state and transition decorators
  - [ ] 4.1.3 Capture complete class source code as context
- [ ] 4.2 Implement transitions library detector
  - [ ] 4.2.1 Find Machine() instantiations
  - [ ] 4.2.2 Extract configuration dictionaries
  - [ ] 4.2.3 Capture configuration block as context
- [ ] 4.3 Build dynamic DOT generator
  - [ ] 4.3.1 Instantiate FSM classes safely in sandbox
  - [ ] 4.3.2 Call `.to_dot()` or equivalent methods
  - [ ] 4.3.3 Handle common parameter variations
  - [ ] 4.3.4 Capture DOT string output

## 5. Validation Pipeline
- [ ] 5.1 Integrate Graphviz compiler validation
  - [ ] 5.1.1 Reuse existing `common/validation.py` utilities
  - [ ] 5.1.2 Validate each extracted DOT with `dot -Tpng`
  - [ ] 5.1.3 Log compiler error messages for failures
- [ ] 5.2 Implement schema validation
  - [ ] 5.2.1 Ensure JSONL output matches project schema
  - [ ] 5.2.2 Validate required fields: id, source, license, task_type, context_snippet, output_dot
  - [ ] 5.2.3 Set `task_type: CODE_TO_DOT` for all entries
- [ ] 5.3 Add deduplication detection
  - [ ] 5.3.1 Hash DOT output for duplicate detection
  - [ ] 5.3.2 Flag duplicates in output for manual review
  - [ ] 5.3.3 Track duplicate sources for attribution

## 6. CLI Implementation
- [ ] 6.1 Create command-line interface
  - [ ] 6.1.1 Implement `parsers/fsm_extractor/__main__.py`
  - [ ] 6.1.2 Add `--repos` flag for repository list file
  - [ ] 6.1.3 Add `--output` flag for custom JSONL path (default: ./data/logic-stream.jsonl)
  - [ ] 6.1.4 Add `--dry-run` flag for testing without output
  - [ ] 6.1.5 Add `--verbose` flag for detailed logging
- [ ] 6.2 Implement streaming JSONL output
  - [ ] 6.2.1 Append results immediately (don't buffer in memory)
  - [ ] 6.2.2 Ensure atomic writes to prevent corruption
- [ ] 6.3 Add progress reporting
  - [ ] 6.3.1 Display current file/repository being processed
  - [ ] 6.3.2 Show running success/failure counts
  - [ ] 6.3.3 Generate final summary statistics

## 7. Optional TUI
- [ ] 7.1 Create Textual-based interactive interface
  - [ ] 7.1.1 Implement `parsers/fsm_extractor_tui.py`
  - [ ] 7.1.2 Add repository selection screen with checkboxes
  - [ ] 7.1.3 Display real-time extraction progress
  - [ ] 7.1.4 Show preview of extracted DOT graphs
- [ ] 7.2 Integrate with existing TUI patterns
  - [ ] 7.2.1 Follow design from `scrapers/graphviz_gallery_tui.py`
  - [ ] 7.2.2 Reuse common UI components if available

## 8. Error Handling & Logging
- [ ] 8.1 Implement comprehensive error handling
  - [ ] 8.1.1 Catch AST parsing failures gracefully
  - [ ] 8.1.2 Handle execution sandbox timeouts
  - [ ] 8.1.3 Manage repository cloning errors
  - [ ] 8.1.4 Continue processing after individual failures
- [ ] 8.2 Create detailed error logging
  - [ ] 8.2.1 Write errors to `logic-stream-errors.log`
  - [ ] 8.2.2 Include file path, error type, and traceback
  - [ ] 8.2.3 Generate error summary report
- [ ] 8.3 Add performance monitoring
  - [ ] 8.3.1 Track processing time per repository
  - [ ] 8.3.2 Log resource usage warnings
  - [ ] 8.3.3 Identify slow files for optimization

## 9. Testing
- [ ] 9.1 Create unit tests
  - [ ] 9.1.1 Test FSM pattern detection with sample code
  - [ ] 9.1.2 Test DOT extraction with known FSM examples
  - [ ] 9.1.3 Test license compliance checker
  - [ ] 9.1.4 Test JSONL schema validation
- [ ] 9.2 Create integration tests
  - [ ] 9.2.1 Test end-to-end processing with mock repository
  - [ ] 9.2.2 Test error handling with malformed code
  - [ ] 9.2.3 Test deduplication logic
- [ ] 9.3 Add test fixtures
  - [ ] 9.3.1 Create sample FSM code snippets (python-statemachine)
  - [ ] 9.3.2 Create sample FSM code snippets (transitions)
  - [ ] 9.3.3 Create expected DOT outputs for validation

## 10. Documentation
- [ ] 10.1 Write usage documentation
  - [ ] 10.1.1 Update README.md with FSM parser quick start
  - [ ] 10.1.2 Document CLI flags and options
  - [ ] 10.1.3 Provide example repository list format
- [ ] 10.2 Create developer documentation
  - [ ] 10.2.1 Document FSM library detection patterns
  - [ ] 10.2.2 Document sandbox security model
  - [ ] 10.2.3 Document how to add support for new FSM libraries
- [ ] 10.3 Update project roadmap
  - [ ] 10.3.1 Mark Phase I.2 as complete in README
  - [ ] 10.3.2 Update data stream statistics

## 11. Validation & Deployment
- [ ] 11.1 Run against curated repository list
  - [ ] 11.1.1 Process 10-20 target repositories
  - [ ] 11.1.2 Validate extracted DOT compilation rate >90%
  - [ ] 11.1.3 Review sample outputs for quality
- [ ] 11.2 Performance validation
  - [ ] 11.2.1 Ensure processing completes in reasonable time
  - [ ] 11.2.2 Verify memory usage stays within bounds
  - [ ] 11.2.3 Test parallel processing efficiency
- [ ] 11.3 Integration with existing pipeline
  - [ ] 11.3.1 Verify compatibility with documentation stream data
  - [ ] 11.3.2 Test combined dataset deduplication
  - [ ] 11.3.3 Validate merged JSONL schema consistency
