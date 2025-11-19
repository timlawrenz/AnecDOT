# AnecDOT: Graph-of-Thought Reasoning with DOT

> Teaching LLMs to think structurally through Graphviz DOT language

## Overview

AnecDOT is a research project exploring the use of DOT (Graphviz) as an intermediate reasoning format for Large Language Models. Instead of forcing LLMs to approach complex planning tasks linearly, we train specialized models to generate formal graph representations that capture dependencies, state transitions, and architectural structures.

This repository contains the **Factory** (Repo A) - the open-source tooling for dataset generation, model training, and validation. The generated datasets are maintained separately under EPL-2.0 licensing.

## Motivation

Current LLMs struggle with:
- **Long-horizon planning**: Multi-step tasks with complex dependencies
- **Structural reasoning**: Understanding relationships between components
- **State management**: Tracking transitions and flow control

By introducing DOT as an intermediate representation, we enable models to:
- Express complex logic as verifiable graph structures
- Separate architectural planning from implementation details
- Enable graph-based orchestration of multi-agent workflows

## Project Goals

1. **Phase I**: Build a high-quality dataset of `(Natural Language → DOT)` and `(Code → DOT)` pairs
2. **Phase II**: Fine-tune small-to-mid-sized models (Gemma 2 9B, Llama 3 8B) to generate syntactically valid and semantically accurate DOT graphs
3. **Future**: Enable graph-based orchestration where DOT output drives agentic workflows

## Architecture

### Dataset Generation (Phase I)

Three data streams feed the training pipeline:

#### 📚 Documentation Stream
- **Source**: Graphviz.org gallery, guides, and attribute references
- **Method**: HTML scraping of examples
- **Purpose**: Foundational syntax and attribute usage

#### 🔧 Logic Stream
- **Source**: Open-source FSM libraries (`python-statemachine`, `aasm`, etc.)
- **Method**: Static analysis + dynamic `.to_dot()` execution
- **Purpose**: Code-to-graph abstraction

#### 🤖 Synthetic Stream
- **Source**: Teacher LLMs (Gemini, Ollama) + seed prompts
- **Method**: Few-shot prompting with grounded examples + compiler verification
- **Purpose**: Dataset augmentation with diverse scenarios
- **Status**: ✅ Validated (10 examples, 100% success rate)

**Current Dataset Status (as of 2025-11-19):**
- Documentation Stream: 44 pairs (13 gallery + 31 attributes)
- Logic Stream: 14 pairs (7 CODE_TO_DOT + 7 NL_TO_DOT)
- Synthetic Stream: 10 pairs (validation batch)
- **Total: 68 training pairs** (100% validated)
- **Target: 250-350 pairs** before training

### Data Schema

```json
{
  "id": "unique_id_123",
  "source": "graphviz_gallery",
  "license": "EPL-2.0",
  "task_type": "NL_TO_DOT",
  "input_text": "Create a directed graph showing a login state machine...",
  "context_snippet": null,
  "output_dot": "digraph { Start -> Login; ... }",
  "verification_status": "passed_compiler"
}
```

### Model Training (Phase II)

- **Base Models**: Gemma 2 (9B), Llama 3 (8B)
- **Technique**: QLoRA (Quantized Low-Rank Adaptation)
- **Hardware**: Single 24GB VRAM GPU (e.g., RTX 4090)
- **Objective**: Causal Language Modeling optimized for DOT syntax

## Validation Metrics

### Syntactic Viability (Pass@1)
- Generate 1,000 graphs from unseen prompts
- Validate with `dot -Tpng > /dev/null`
- **Target**: >95% compilation success

### Semantic Alignment (LLM-as-a-Judge)
- Evaluate logical correctness with stronger model (Gemini 1.5 Pro)
- **Target**: Statistically significant improvement over base model

## Repository Structure

```
AnecDOT/
├── docs/               # Project documentation
│   └── initial-brief.md
├── scrapers/           # Data collection tools
├── parsers/            # FSM extraction and analysis
├── generators/         # Synthetic data generation
├── validation/         # DOT compiler verification
├── training/           # Fine-tuning scripts
└── orchestrator/       # Graph-based execution engine (future)
```

## Licensing & Public Domain Commitment

This repository (The Factory) is licensed under **MIT/Apache-2.0** for maximum reusability and unrestricted use.

Generated datasets (The Artifact) are maintained separately under **EPL-2.0** to comply with Graphviz documentation licensing.

**All outputs of this project—including trained models, datasets, and research findings—are intended for the public domain to further research, education, and open development.** Our goal is to advance the field of LLM reasoning and make these capabilities accessible to researchers, developers, and the broader AI community.

We believe that structural reasoning capabilities should be a public good, freely available for:
- 🎓 Academic research and education
- 🔬 Further experimentation and iteration
- 🛠️ Integration into open-source tools
- 🌍 Advancement of AI safety and interpretability

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/AnecDOT.git
cd AnecDOT

# Install Python dependencies
pip install -r requirements.txt

# Install Graphviz (required for validation)
# Linux:
sudo apt-get install graphviz

# macOS:
brew install graphviz

# Windows:
choco install graphviz
```

### Run the Graphviz Gallery Scraper

**Interactive TUI (Recommended):**
```bash
# Install Textual for TUI support
pip install textual

# Run interactive scraper
python3 -m scrapers.graphviz_gallery_tui
```

**Command-line interface:**
```bash
# Basic usage (outputs to ./data/documentation-stream.jsonl)
python3 -m scrapers.graphviz_gallery

# Custom output path
python3 -m scrapers.graphviz_gallery --output /path/to/output.jsonl

# Dry run (no output file)
python3 -m scrapers.graphviz_gallery --dry-run
```

### Run the FSM Library Parser

Extract (Code → DOT) and (NL → DOT) pairs from FSM libraries:

```bash
# Process a directory containing FSM code
python3 -m parsers.fsm_extractor \
  --path /path/to/repo \
  --license MIT \
  --output data/logic-stream.jsonl

# Dry run to preview extraction
python3 -m parsers.fsm_extractor \
  --path /path/to/repo \
  --license MIT \
  --dry-run \
  --verbose
```

**Supported FSM libraries:**
- `python-statemachine` - Detects StateMachine subclasses
- `transitions.extensions.GraphMachine` - Detects GraphMachine usage

**Output:**
- CODE_TO_DOT pairs: Python code → DOT graph
- NL_TO_DOT pairs: Natural language (from docstrings) → DOT graph

### Run the Synthetic Generator

Generate synthetic training pairs using teacher LLMs:

```bash
# Using local Ollama (free, no API key needed)
python3 -m generators.synthetic_generator \
  --provider ollama-gemma \
  --count 10 \
  --output data/synthetic-stream.jsonl

# Using Gemini API (requires GEMINI_API_KEY)
python3 -m generators.synthetic_generator \
  --provider gemini-flash \
  --count 10 \
  --output data/synthetic-stream.jsonl

# Dry run to see prompts
python3 -m generators.synthetic_generator \
  --provider ollama-gemma \
  --count 10 \
  --dry-run
```

**Supported providers:**
- `ollama-gemma` - Local gemma3:27b (free, requires Ollama)
- `ollama-deepseek` - Local deepseek-r1:32b (free, requires Ollama)
- `gemini-flash` - Gemini 2.5 Flash (cheapest cloud option)
- `gemini-pro` - Gemini 2.5 Pro (higher quality)
- `gemini-3` - Gemini 3 Pro Preview (latest)

### Run Tests

```bash
pytest tests/ -v
```

## Roadmap

- [x] **Phase I.1**: Implement documentation stream scraper ✅
  - [x] Gallery scraper (13 examples)
  - [x] Attribute docs scraper (31 examples)
  - [x] Total: 44 validated DOT examples
- [x] **Phase I.2**: Build FSM library parser ✅
  - [x] AST-based pattern detection
  - [x] Sandboxed DOT extraction
  - [x] Natural language pairing
  - [x] Total: 14 pairs (7 CODE_TO_DOT + 7 NL_TO_DOT)
- [x] **Phase I.3**: Validate synthetic generation pipeline ✅
  - [x] Multi-provider LLM support (Gemini, Ollama)
  - [x] Few-shot prompting with grounded examples
  - [x] Graphviz validation and JSONL output
  - [x] Validation: 10/10 success (100%), $0 cost with local models
  - [x] Ready for scaling to 30-50 synthetic pairs
- [ ] **Phase I.3.5**: Expand dataset to 250-350 pairs
  - [ ] Scale synthetic generation (20-40 more pairs)
  - [ ] Extract from 20-30 more FSM repositories
  - [ ] Scrape additional documentation sources
  - [ ] Target: 200-300 real + 30-50 synthetic
- [ ] **Phase I.4**: Validate and deduplicate dataset
- [ ] **Phase II.1**: Set up QLoRA training infrastructure
  - ⚠️ **Note**: Minimum 200-300 pairs recommended before training
  - Current dataset (68 pairs) suitable for infrastructure testing only
- [ ] **Phase II.2**: Fine-tune base models
- [ ] **Phase II.3**: Run validation benchmarks
- [ ] **Phase III**: Implement graph-based orchestrator

## Contributing

Contributions are welcome! This is an experimental research project exploring novel approaches to LLM reasoning. By contributing, you help advance publicly available research that benefits the entire community.

## Future Vision: The Orchestrator

Once models reliably generate DOT graphs, they become engines for **graph-based agentic workflows**:

1. Model generates a dependency graph (the plan)
2. Python orchestrator traverses the graph
3. Each node executes with context from predecessor nodes
4. Edges act as data pipelines between specialized models

This decouples the "Planner" (local DOT model) from "Workers" (coding models), enabling complex multi-step software generation on consumer hardware.

## References

- [Graphviz Documentation](https://graphviz.org/)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)

---

**Status**: 🚧 Early Research Phase | **Mission**: Building public-domain reasoning infrastructure for all
