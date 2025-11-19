# Change: Add Synthetic Generation Pipeline for Dataset Augmentation

## Why

The current dataset (58 pairs) provides foundational coverage of DOT syntax and FSM patterns, but lacks:
- **Diversity**: Limited domains (mostly traffic lights, workflows, simple state machines)
- **Complexity**: Few examples with advanced DOT features (subgraphs, clusters, complex styling)
- **Scale**: Need 200-500+ pairs for effective fine-tuning
- **Edge cases**: Missing error-prone patterns that base models struggle with

Teacher LLMs (GPT-4, Gemini 1.5 Pro) can generate valid DOT graphs from natural language prompts, providing:
- Rapid dataset expansion
- Controlled complexity progression
- Domain diversity (game AI, protocols, workflows, etc.)
- Augmentation of underrepresented patterns

Without synthetic data, we're bottlenecked by:
- Manual curation time for finding/extracting real examples
- Limited FSM repository availability
- Lack of coverage for specific DOT syntax we want to teach

## What Changes

- Create synthetic generation pipeline using teacher LLMs
- Implement prompt engineering for diverse DOT graph generation
- Add quality filtering: Graphviz validation + semantic checks
- Generate 100-200 high-quality synthetic (NL → DOT) pairs
- Track provenance: `source: synthetic-gpt4` or `source: synthetic-gemini`

**Target Domains:**
- Game AI state machines (combat, dialogue, inventory)
- Network protocols (TCP, HTTP, WebSocket)
- Workflow automation (CI/CD, approval processes)
- UI navigation flows
- Robotics behaviors
- Database transactions

**Quality Controls:**
- All DOT must compile with Graphviz
- Semantic validation (does DOT match prompt?)
- Deduplication against existing dataset
- Diversity scoring (avoid repetitive patterns)

## Impact

**New Capability:**
- `synthetic-generator` - Teacher LLM pipeline for DOT generation

**Affected Code:**
- `generators/` - New directory for synthetic data generation
- `data/synthetic-stream.jsonl` - New output file
- `common/quality_filter.py` - Semantic validation utilities
- `.env.example` - API key configuration template

**Dataset Impact:**
- Current: 58 pairs (44 real + 14 FSM)
- After Phase I.3: 158-258 pairs (+ 100-200 synthetic)
- Task distribution: Primarily NL_TO_DOT
- Increased domain diversity and complexity

**Risk Assessment:**
- **Synthetic bias**: Teacher LLM patterns may differ from human-written DOT
- **Cost**: API calls to GPT-4/Gemini ($10-50 estimated)
- **Quality variance**: Some generations may be low quality
- **Overfitting risk**: Model may learn teacher LLM style instead of DOT semantics
- **Mitigation**: Mix synthetic with real data (max 70% synthetic), strict validation

**Benefits:**
- Rapid dataset expansion
- Controlled complexity and diversity
- Fill gaps in current dataset coverage
- Cost-effective compared to manual annotation
