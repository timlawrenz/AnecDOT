# Project Context

## Purpose

AnecDOT (Graph-of-Thought: DOT as an Intermediate Reasoning Format) is a research project focused on teaching LLMs structural reasoning through Graphviz DOT language. 

**Primary Goals:**
1. Build a high-quality, syntactically verified dataset for training models to generate DOT graphs from natural language and code
2. Fine-tune small-to-mid-sized open models (Gemma 2 9B, Llama 3 8B) to outperform larger commercial models in generating valid, logical graph structures
3. Enable graph-based orchestration for multi-agent workflows where DOT output drives agentic task execution

**Mission:** All outputs (models, datasets, research findings) are intended for the public domain to advance LLM reasoning research.

## Tech Stack

### Data Pipeline (Phase I)
- **Python 3.10+** - Primary language for all tooling
- **Beautiful Soup 4 / lxml** - HTML scraping for Graphviz documentation
- **AST/tree-sitter** - Static code analysis for FSM library parsing
- **Graphviz** - DOT compiler for validation (`dot -Tpng`)
- **JSONL** - Training data format

### Model Training (Phase II)
- **PyTorch** - Deep learning framework
- **Transformers (HuggingFace)** - Model loading and inference
- **PEFT (Parameter-Efficient Fine-Tuning)** - QLoRA implementation
- **bitsandbytes** - 4-bit quantization for GPU efficiency
- **Accelerate** - Distributed training support
- **Weights & Biases / TensorBoard** - Experiment tracking

### Target Models
- Gemma 2 (9B)
- Llama 3 (8B)
- Other open-weights models with 7-13B parameters

### Validation & Evaluation
- **Graphviz CLI** - Syntactic validation
- **Gemini 1.5 Pro / GPT-4** - LLM-as-a-Judge for semantic evaluation
- **pytest** - Unit testing for parsers and validators

### Future (Phase III - Orchestrator)
- **NetworkX** - Graph traversal and topological sorting
- **Python subprocess** - Model execution coordination

## Project Conventions

### Code Style
- **PEP 8** compliance for all Python code
- **Type hints** required for all functions (use `typing` module)
- **Docstrings** using Google style for all public functions/classes
- **Line length:** 100 characters max
- **Import order:** stdlib, third-party, local (grouped and alphabetically sorted)
- **Linting:** Use `ruff` or `flake8` + `black` for formatting
- **Variable naming:**
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Architecture Patterns

#### Split-License Architecture
- **Repo A (The Factory)**: MIT/Apache-2.0 - Contains tooling, no data
- **Repo B (The Artifact)**: EPL-2.0 - Contains generated datasets

#### Data Pipeline Architecture
Three independent streams with consistent output schema:
1. **Documentation Stream** - Scrapes graphviz.org
2. **Logic Stream** - Extracts from FSM libraries
3. **Synthetic Stream** - Teacher LLM augmentation

Each stream must:
- Validate DOT syntax using `dot` compiler
- Output strict JSONL schema
- Track source and license metadata
- Support incremental processing and deduplication

#### Component Isolation
- Scrapers, parsers, validators are independent modules
- Each component has single responsibility
- Pipeline stages communicate via JSONL files
- No tight coupling between data sources

### Testing Strategy

#### Unit Tests
- All parsers and validators must have >90% coverage
- DOT syntax validation tests using known-good/known-bad examples
- Schema validation for JSONL output

#### Integration Tests
- End-to-end pipeline tests for each data stream
- Verify deduplication logic
- Test error handling and recovery

#### Validation Protocol
- **Syntactic Viability (Pass@1)**: Generate 1,000 graphs, validate with `dot -Tpng`
- **Semantic Alignment**: LLM-as-a-Judge evaluation
- Success criteria: >95% compilation rate for fine-tuned model

#### No Test Coverage Required For
- Documentation files (README, etc.)
- Experimental/exploratory scripts

### Git Workflow

#### Branching Strategy
- `main` - Stable, production-ready code
- `develop` - Integration branch for features
- `feature/<name>` - New features or data streams
- `fix/<name>` - Bug fixes
- `experiment/<name>` - Research experiments (may not merge)

#### Commit Conventions
Follow Conventional Commits:
- `feat:` - New features or data pipeline additions
- `fix:` - Bug fixes
- `docs:` - Documentation updates
- `test:` - Test additions/modifications
- `refactor:` - Code refactoring
- `data:` - Dataset updates (in separate repo)
- `model:` - Training/model configuration changes

**Examples:**
- `feat: add graphviz gallery scraper`
- `fix: handle malformed DOT syntax in validator`
- `docs: update training protocol in openspec`
- `model: add QLoRA config for Gemma 2 9B`

#### Pull Request Requirements
- Descriptive title and summary
- Reference related issues
- Tests pass (if applicable)
- Code review from maintainer

## Domain Context

### DOT Language (Graphviz)
- **Graph types**: `graph` (undirected), `digraph` (directed)
- **Syntax strict rules**:
  - Undirected edges use `--`
  - Directed edges use `->`
  - Mixing these is a common hallucination error in base LLMs
- **Attributes**: `rankdir`, `label`, `shape`, `color`, etc.
- **Subgraphs**: Clustering using `subgraph cluster_name { }`
- **Compiler**: `dot` from Graphviz package validates syntax

### Finite State Machines (FSMs)
- Common pattern in source code: state transitions, event handling
- Libraries often provide `.to_dot()` or similar export methods
- Target libraries: `python-statemachine`, `transitions`, `aasm` (Ruby)

### LLM Fine-Tuning Concepts
- **QLoRA**: 4-bit quantization + LoRA adapters for memory-efficient training
- **Causal Language Modeling (CLM)**: Next-token prediction objective
- **Context window**: Balance between instruction length and DOT output
- **Evaluation**: Pass@1 (syntax), LLM-as-a-Judge (semantics)

### Graph-Based Reasoning
- Nodes represent tasks/states
- Edges represent dependencies/transitions
- Topological sort enables execution order
- Context injection: node outputs flow to dependent nodes

## Important Constraints

### Hardware Limitations
- Training must fit on single 24GB VRAM GPU (e.g., RTX 4090)
- QLoRA required for larger models (>7B parameters)
- Inference should be feasible on consumer hardware

### Licensing Compliance
- Graphviz documentation is EPL-2.0
- Generated datasets derived from EPL sources must be EPL-2.0
- Tooling repository (this repo) remains MIT/Apache-2.0
- **Never mix data into tooling repository**

### Quality Requirements
- All DOT outputs must pass `dot` compiler validation
- >95% Pass@1 target for fine-tuned models
- Strict JSONL schema adherence
- No duplicate training examples

### Public Domain Commitment
- All outputs intended for public research use
- No proprietary restrictions on models or datasets
- Maximize accessibility for academic and open-source communities

### Ethical Constraints
- Only scrape publicly available documentation
- Respect robots.txt and rate limits
- Properly attribute all data sources
- No generation of harmful content

## External Dependencies

### Data Sources
- **graphviz.org** - Official documentation, gallery, examples (EPL-2.0)
- **GitHub repositories** - Open-source FSM libraries for code-to-DOT pairs
- **Teacher LLMs** - Gemini/GPT-4 for synthetic data generation

### Model Repositories
- **HuggingFace Hub** - Base models (Gemma, Llama) and fine-tuned checkpoints
- **PEFT library** - QLoRA adapters

### Validation Services
- **Graphviz CLI** - Must be installed: `apt-get install graphviz`
- **Google AI Studio / OpenAI API** - For LLM-as-a-Judge evaluation

### Infrastructure
- **Git/GitHub** - Version control and collaboration
- **GPU access** - Local or cloud (e.g., Lambda Labs, RunPod)
- **Storage** - For datasets (separate repository)

### Python Package Dependencies
Core packages (to be defined in `requirements.txt`):
- `torch>=2.0`
- `transformers>=4.35`
- `peft>=0.7`
- `bitsandbytes>=0.41`
- `accelerate>=0.25`
- `beautifulsoup4>=4.12`
- `lxml>=4.9`
- `pytest>=7.4`
- `ruff` or `black` + `flake8`
