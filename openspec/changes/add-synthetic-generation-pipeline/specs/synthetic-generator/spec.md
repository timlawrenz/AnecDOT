## ADDED Requirements

### Requirement: Teacher LLM Integration
The generator SHALL support multiple teacher LLM providers for DOT generation.

#### Scenario: GPT-4 generation
- **WHEN** user configures OpenAI API key
- **THEN** generator uses GPT-4 to generate DOT graphs from prompts

#### Scenario: Gemini generation
- **WHEN** user configures Google AI API key
- **THEN** generator uses Gemini 1.5 Pro to generate DOT graphs

#### Scenario: Fallback handling
- **WHEN** primary provider fails or rate limits
- **THEN** generator falls back to secondary provider

#### Scenario: API key missing
- **WHEN** no API keys are configured
- **THEN** generator raises configuration error with instructions

### Requirement: Prompt Engineering
The generator SHALL use structured prompts to elicit diverse, valid DOT graphs.

#### Scenario: Domain-specific prompts
- **WHEN** generating for a specific domain (e.g., "game AI")
- **THEN** prompt includes domain context and expected graph structure

#### Scenario: Complexity progression
- **WHEN** generating examples
- **THEN** start with simple graphs (2-3 nodes) and progress to complex (10+ nodes)

#### Scenario: Feature targeting
- **WHEN** specific DOT features are needed (subgraphs, clusters, styling)
- **THEN** prompts explicitly request those features

#### Scenario: Few-shot learning
- **WHEN** generating DOT
- **THEN** prompt includes 1-2 example DOT graphs for reference

### Requirement: Quality Validation
The generator SHALL validate all generated DOT graphs for syntactic and semantic correctness.

#### Scenario: Syntactic validation
- **WHEN** DOT is generated
- **THEN** compile with `dot -Tpng` to verify syntax

#### Scenario: Semantic validation
- **WHEN** DOT passes syntax check
- **THEN** verify graph matches the prompt intent (using validation LLM or heuristics)

#### Scenario: Node/edge count validation
- **WHEN** prompt requests specific graph size
- **THEN** verify generated graph meets size requirements (±20% tolerance)

#### Scenario: Failed validation
- **WHEN** DOT fails validation
- **THEN** log the failure and regenerate (max 3 retries per prompt)

### Requirement: Deduplication
The generator SHALL detect and prevent duplicate or near-duplicate DOT graphs.

#### Scenario: Exact duplicate detection
- **WHEN** generated DOT exactly matches existing example
- **THEN** discard and regenerate

#### Scenario: Structural similarity detection
- **WHEN** generated DOT has similar structure (>90% node/edge overlap)
- **THEN** flag for manual review or regenerate

#### Scenario: Hash-based tracking
- **WHEN** generating DOT
- **THEN** compute normalized hash and check against existing dataset

### Requirement: Prompt Template Library
The generator SHALL maintain a curated library of prompt templates for diverse domains.

#### Scenario: Load template by domain
- **WHEN** user requests "game AI" domain
- **THEN** load game AI prompt template with appropriate context

#### Scenario: Random template selection
- **WHEN** generating diverse dataset
- **THEN** randomly sample from available templates

#### Scenario: Template customization
- **WHEN** template is loaded
- **THEN** inject random parameters (names, states, transitions) for variety

#### Scenario: Template validation
- **WHEN** adding new template
- **THEN** test-generate 5 examples to verify quality

### Requirement: Batch Generation
The generator SHALL efficiently generate multiple DOT graphs in parallel.

#### Scenario: Batch API calls
- **WHEN** generating 100 examples
- **THEN** batch API calls (5-10 concurrent) to optimize throughput

#### Scenario: Progress tracking
- **WHEN** batch generation is running
- **THEN** display progress bar with success/failure counts

#### Scenario: Partial failure handling
- **WHEN** some generations fail in batch
- **THEN** continue processing remaining items and report failures at end

#### Scenario: Cost estimation
- **WHEN** starting batch generation
- **THEN** estimate API costs based on prompt count and provider pricing

### Requirement: JSONL Output Format
The generator SHALL output synthetic pairs in the same JSONL schema as other streams.

#### Scenario: Synthetic pair schema
- **WHEN** generating a pair
- **THEN** include all required fields: id, source, license, task_type, input_text, output_dot, verification_status

#### Scenario: Provenance tracking
- **WHEN** writing pair to JSONL
- **THEN** set source to "synthetic-{provider}-{model}" (e.g., "synthetic-openai-gpt4")

#### Scenario: License attribution
- **WHEN** using teacher LLM output
- **THEN** set license to "synthetic-generated" (no copyright restrictions)

#### Scenario: Task type
- **WHEN** generating from natural language
- **THEN** set task_type to "NL_TO_DOT"

### Requirement: Diversity Scoring
The generator SHALL measure and optimize for dataset diversity.

#### Scenario: Domain distribution
- **WHEN** generating dataset
- **THEN** ensure balanced representation across domains (game AI, protocols, workflows, etc.)

#### Scenario: Complexity distribution
- **WHEN** generating examples
- **THEN** ensure mix of simple (2-5 nodes), medium (6-10 nodes), complex (11+ nodes)

#### Scenario: Feature coverage
- **WHEN** reviewing generated dataset
- **THEN** track coverage of DOT features (subgraphs, clusters, styling, labels)

#### Scenario: Diversity report
- **WHEN** generation completes
- **THEN** output diversity statistics (domains, complexity, features)

### Requirement: Configuration Management
The generator SHALL support flexible configuration via environment variables and config files.

#### Scenario: API key configuration
- **WHEN** user sets OPENAI_API_KEY environment variable
- **THEN** use it for GPT-4 generations

#### Scenario: Provider selection
- **WHEN** user sets PREFERRED_PROVIDER config
- **THEN** prioritize that provider for generation

#### Scenario: Generation parameters
- **WHEN** user sets TARGET_COUNT and MAX_COMPLEXITY
- **THEN** generate that many examples with specified complexity limit

#### Scenario: Config file validation
- **WHEN** loading config file
- **THEN** validate all required fields and raise clear errors for missing values

### Requirement: Semantic Validation (LLM-as-Judge)
The generator SHALL optionally use a validation LLM to check if DOT matches prompt.

#### Scenario: Enable semantic validation
- **WHEN** user enables --validate-semantics flag
- **THEN** use cheaper LLM (GPT-3.5 or Gemini Flash) to verify each generation

#### Scenario: Validation prompt
- **WHEN** validating DOT
- **THEN** ask: "Does this DOT graph represent [original prompt]? Answer yes/no and explain."

#### Scenario: Failed semantic check
- **WHEN** validation LLM says "no"
- **THEN** log the reason and regenerate

#### Scenario: Validation budget
- **WHEN** semantic validation is enabled
- **THEN** estimate additional API costs and warn user

### Requirement: Error Handling and Logging
The generator SHALL provide detailed logging and graceful error recovery.

#### Scenario: API timeout
- **WHEN** LLM API call times out
- **THEN** retry with exponential backoff (max 3 attempts)

#### Scenario: Rate limiting
- **WHEN** API returns rate limit error
- **THEN** wait specified time and retry

#### Scenario: Detailed logging
- **WHEN** generation runs
- **THEN** log all attempts, successes, failures with timestamps and error messages

#### Scenario: Error summary
- **WHEN** generation completes
- **THEN** output summary of errors grouped by type

### Requirement: Command-Line Interface
The generator SHALL provide a CLI for batch generation with flexible options.

#### Scenario: Basic usage
- **WHEN** user runs `python -m generators.synthetic_generator --count 100`
- **THEN** generate 100 synthetic pairs using default provider

#### Scenario: Provider selection
- **WHEN** user specifies `--provider openai` or `--provider gemini`
- **THEN** use that specific provider

#### Scenario: Domain filtering
- **WHEN** user specifies `--domains game-ai,protocols`
- **THEN** only generate from those domain templates

#### Scenario: Dry run
- **WHEN** user passes `--dry-run`
- **THEN** show what would be generated (costs, prompts) without calling APIs

#### Scenario: Resume generation
- **WHEN** user passes `--resume`
- **THEN** continue from previous incomplete generation run

### Requirement: Cost Tracking
The generator SHALL track and report API usage costs.

#### Scenario: Cost calculation
- **WHEN** making API calls
- **THEN** track tokens used and calculate cost based on provider pricing

#### Scenario: Budget limit
- **WHEN** user sets --max-cost flag
- **THEN** stop generation when budget is reached

#### Scenario: Cost report
- **WHEN** generation completes
- **THEN** output total cost breakdown by provider and model

#### Scenario: Cost estimation
- **WHEN** starting generation
- **THEN** estimate total cost before making API calls
