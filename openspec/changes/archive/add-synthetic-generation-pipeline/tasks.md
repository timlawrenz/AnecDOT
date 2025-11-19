## 1. Research & Setup
- [ ] 1.1 Evaluate teacher LLM capabilities
  - [ ] 1.1.1 Test GPT-4 DOT generation quality (10 manual prompts)
  - [ ] 1.1.2 Test Gemini 1.5 Pro DOT generation quality (10 manual prompts)
  - [ ] 1.1.3 Compare outputs for consistency and quality
  - [ ] 1.1.4 Document strengths/weaknesses of each provider
- [ ] 1.2 Set up API access
  - [ ] 1.2.1 Obtain OpenAI API key
  - [ ] 1.2.2 Obtain Google AI API key
  - [ ] 1.2.3 Test basic API connectivity
  - [ ] 1.2.4 Create .env.example template
- [ ] 1.3 Analyze current dataset gaps
  - [ ] 1.3.1 Identify underrepresented domains
  - [ ] 1.3.2 Identify missing DOT features
  - [ ] 1.3.3 Determine target distribution for synthetic data

## 2. Core Infrastructure
- [ ] 2.1 Create generator module structure
  - [ ] 2.1.1 Create `generators/__init__.py`
  - [ ] 2.1.2 Create `generators/synthetic_generator/` directory
  - [ ] 2.1.3 Create `generators/synthetic_generator/__init__.py`
- [ ] 2.2 Implement LLM provider abstraction
  - [ ] 2.2.1 Create base `LLMProvider` interface
  - [ ] 2.2.2 Implement `OpenAIProvider` class
  - [ ] 2.2.3 Implement `GeminiProvider` class
  - [ ] 2.2.4 Add provider factory and selection logic
- [ ] 2.3 Implement prompt templating system
  - [ ] 2.3.1 Design template YAML/JSON schema
  - [ ] 2.3.2 Create template loader and parser
  - [ ] 2.3.3 Implement parameter randomization
  - [ ] 2.3.4 Add few-shot example injection

## 3. Prompt Engineering
- [ ] 3.1 Create base prompt templates
  - [ ] 3.1.1 Design system prompt for DOT generation
  - [ ] 3.1.2 Create few-shot examples library (5-10 diverse examples)
  - [ ] 3.1.3 Design output format specification
- [ ] 3.2 Create domain-specific templates
  - [ ] 3.2.1 Game AI templates (combat, dialogue, inventory)
  - [ ] 3.2.2 Network protocol templates (TCP, HTTP, WebSocket)
  - [ ] 3.2.3 Workflow templates (CI/CD, approvals)
  - [ ] 3.2.4 UI navigation templates
  - [ ] 3.2.5 Robotics templates
  - [ ] 3.2.6 Database transaction templates
  - [ ] 3.2.7 E-commerce templates
  - [ ] 3.2.8 Document lifecycle templates
- [ ] 3.3 Test and refine templates
  - [ ] 3.3.1 Generate 5 examples per template
  - [ ] 3.3.2 Measure success rates
  - [ ] 3.3.3 Refine low-performing templates

## 4. Quality Validation
- [ ] 4.1 Implement syntactic validation
  - [ ] 4.1.1 Create `validate_dot_syntax()` function (reuse from existing)
  - [ ] 4.1.2 Add error message parsing
  - [ ] 4.1.3 Track validation statistics
- [ ] 4.2 Implement semantic validation (optional)
  - [ ] 4.2.1 Create validation LLM wrapper (GPT-3.5/Gemini Flash)
  - [ ] 4.2.2 Design validation prompt template
  - [ ] 4.2.3 Parse yes/no responses
  - [ ] 4.2.4 Add cost tracking for validation calls
- [ ] 4.3 Implement deduplication
  - [ ] 4.3.1 Create DOT normalization function
  - [ ] 4.3.2 Implement structural similarity scoring
  - [ ] 4.3.3 Create hash-based duplicate detection
  - [ ] 4.3.4 Add similarity threshold checks
- [ ] 4.4 Implement diversity scoring
  - [ ] 4.4.1 Track domain distribution
  - [ ] 4.4.2 Track complexity distribution
  - [ ] 4.4.3 Track DOT feature usage
  - [ ] 4.4.4 Generate diversity report

## 5. Generation Logic
- [ ] 5.1 Implement single generation flow
  - [ ] 5.1.1 Load template
  - [ ] 5.1.2 Randomize parameters
  - [ ] 5.1.3 Build prompt
  - [ ] 5.1.4 Call LLM API
  - [ ] 5.1.5 Parse response
  - [ ] 5.1.6 Validate DOT
  - [ ] 5.1.7 Create training pair object
- [ ] 5.2 Implement retry logic
  - [ ] 5.2.1 Add retry decorator with exponential backoff
  - [ ] 5.2.2 Handle API timeouts
  - [ ] 5.2.3 Handle rate limiting
  - [ ] 5.2.4 Max retry limits (3 attempts)
- [ ] 5.3 Implement batch generation
  - [ ] 5.3.1 Create batch generation orchestrator
  - [ ] 5.3.2 Add concurrent API calls (5-10 parallel)
  - [ ] 5.3.3 Implement progress tracking
  - [ ] 5.3.4 Add early termination on budget limit
- [ ] 5.4 Implement stratified sampling
  - [ ] 5.4.1 Define complexity quotas (30/50/20)
  - [ ] 5.4.2 Track progress toward quotas
  - [ ] 5.4.3 Stop when all quotas met

## 6. Cost Management
- [ ] 6.1 Implement cost tracking
  - [ ] 6.1.1 Add token counting for prompts
  - [ ] 6.1.2 Track API response token usage
  - [ ] 6.1.3 Calculate costs per provider pricing
  - [ ] 6.1.4 Accumulate total costs during generation
- [ ] 6.2 Implement budget controls
  - [ ] 6.2.1 Add cost estimation before generation
  - [ ] 6.2.2 Add max budget parameter
  - [ ] 6.2.3 Check budget before each API call
  - [ ] 6.2.4 Graceful shutdown on budget limit
- [ ] 6.3 Implement cost reporting
  - [ ] 6.3.1 Generate cost summary report
  - [ ] 6.3.2 Break down by provider and model
  - [ ] 6.3.3 Calculate cost per successful generation

## 7. JSONL Output
- [ ] 7.1 Implement schema compliance
  - [ ] 7.1.1 Create `SyntheticPair` dataclass
  - [ ] 7.1.2 Ensure all required fields present
  - [ ] 7.1.3 Set proper task_type (NL_TO_DOT)
  - [ ] 7.1.4 Set provenance source (synthetic-{provider})
- [ ] 7.2 Implement streaming output
  - [ ] 7.2.1 Write pairs to JSONL immediately after generation
  - [ ] 7.2.2 Add file locking for concurrent writes
  - [ ] 7.2.3 Implement append-only mode
- [ ] 7.3 Implement output validation
  - [ ] 7.3.1 Validate JSONL syntax
  - [ ] 7.3.2 Verify schema compliance
  - [ ] 7.3.3 Check for required fields

## 8. Command-Line Interface
- [ ] 8.1 Design CLI arguments
  - [ ] 8.1.1 `--count`: Number of examples to generate
  - [ ] 8.1.2 `--provider`: Provider selection (openai/gemini/auto)
  - [ ] 8.1.3 `--domains`: Domain filter (comma-separated)
  - [ ] 8.1.4 `--complexity`: Complexity filter (simple/medium/complex)
  - [ ] 8.1.5 `--output`: Output JSONL file path
  - [ ] 8.1.6 `--max-cost`: Budget limit in USD
  - [ ] 8.1.7 `--validate-semantics`: Enable semantic validation
  - [ ] 8.1.8 `--dry-run`: Estimate costs without generating
  - [ ] 8.1.9 `--resume`: Resume from previous run
  - [ ] 8.1.10 `--verbose`: Detailed logging
- [ ] 8.2 Implement CLI logic
  - [ ] 8.2.1 Create argparse configuration
  - [ ] 8.2.2 Validate arguments
  - [ ] 8.2.3 Load configuration from env vars
  - [ ] 8.2.4 Call generation logic
  - [ ] 8.2.5 Display progress and results
- [ ] 8.3 Add `__main__.py` entry point
  - [ ] 8.3.1 Make module executable
  - [ ] 8.3.2 Add usage examples in docstring

## 9. Error Handling & Logging
- [ ] 9.1 Implement error handling
  - [ ] 9.1.1 Catch API errors gracefully
  - [ ] 9.1.2 Handle network failures
  - [ ] 9.1.3 Handle invalid API keys
  - [ ] 9.1.4 Handle malformed LLM responses
- [ ] 9.2 Implement logging
  - [ ] 9.2.1 Configure structured logging
  - [ ] 9.2.2 Log all API calls with timestamps
  - [ ] 9.2.3 Log validation results
  - [ ] 9.2.4 Log costs incurred
- [ ] 9.3 Implement error reporting
  - [ ] 9.3.1 Aggregate errors by type
  - [ ] 9.3.2 Generate error summary report
  - [ ] 9.3.3 Output failed prompts for debugging

## 10. Testing & Validation
- [ ] 10.1 Unit tests
  - [ ] 10.1.1 Test template loading and parsing
  - [ ] 10.1.2 Test parameter randomization
  - [ ] 10.1.3 Test DOT normalization
  - [ ] 10.1.4 Test similarity scoring
  - [ ] 10.1.5 Test cost calculation
- [ ] 10.2 Integration tests
  - [ ] 10.2.1 Test full generation flow (mocked APIs)
  - [ ] 10.2.2 Test batch generation
  - [ ] 10.2.3 Test error handling
  - [ ] 10.2.4 Test budget limits
- [ ] 10.3 End-to-end validation
  - [ ] 10.3.1 Generate 10-20 examples with real APIs
  - [ ] 10.3.2 Manually review quality
  - [ ] 10.3.3 Verify compilation success
  - [ ] 10.3.4 Check diversity metrics

## 11. Production Run
- [ ] 11.1 Small batch generation (20 examples)
  - [ ] 11.1.1 Run with Gemini (cheaper)
  - [ ] 11.1.2 Review quality
  - [ ] 11.1.3 Adjust templates if needed
- [ ] 11.2 Medium batch generation (50 examples)
  - [ ] 11.2.1 Mix providers (30 Gemini, 20 GPT-4)
  - [ ] 11.2.2 Monitor costs and quality
  - [ ] 11.2.3 Verify diversity distribution
- [ ] 11.3 Full dataset generation (100-200 examples)
  - [ ] 11.3.1 Run stratified generation
  - [ ] 11.3.2 Monitor all quotas and budgets
  - [ ] 11.3.3 Generate final synthetic-stream.jsonl
- [ ] 11.4 Post-generation analysis
  - [ ] 11.4.1 Validate all DOT with Graphviz
  - [ ] 11.4.2 Generate diversity report
  - [ ] 11.4.3 Generate cost report
  - [ ] 11.4.4 Manual quality spot-check (10-20 examples)

## 12. Documentation
- [ ] 12.1 Write user documentation
  - [ ] 12.1.1 Document CLI usage with examples
  - [ ] 12.1.2 Document configuration (API keys, env vars)
  - [ ] 12.1.3 Document template format
  - [ ] 12.1.4 Add troubleshooting guide
- [ ] 12.2 Write technical documentation
  - [ ] 12.2.1 Document architecture and design decisions
  - [ ] 12.2.2 Document provider integration
  - [ ] 12.2.3 Document cost calculations
  - [ ] 12.2.4 Document quality validation pipeline
- [ ] 12.3 Update project README
  - [ ] 12.3.1 Add Phase I.3 completion status
  - [ ] 12.3.2 Add synthetic generator usage section
  - [ ] 12.3.3 Update dataset statistics

## Summary

**Total Tasks**: 12 phases, 140+ subtasks

**Estimated Effort**:
- Research & Setup: 4-6 hours
- Core Infrastructure: 6-8 hours
- Prompt Engineering: 8-12 hours (most time-consuming)
- Quality Validation: 4-6 hours
- Generation Logic: 6-8 hours
- Cost Management: 2-4 hours
- CLI & Error Handling: 4-6 hours
- Testing: 6-8 hours
- Production Run: 4-6 hours (+ API wait time)
- Documentation: 3-4 hours

**Total**: ~50-70 hours

**Critical Path**:
1. Provider integration → 2. Prompt templates → 3. Quality validation → 4. Production run

**Cost Estimate**:
- Development/testing: $5-10
- Production generation: $20-40
- Total: $25-50
