# Future Research Directions for AnecDOT

**Date:** 2025-11-21  
**Context:** Notes for extending AnecDOT to a wider study  
**Current Status:** Phase II.2 in progress (273 training pairs, Gemma-2B-IT)

---

## Alternative Base Models for Comparative Study

### High-Priority Candidates

#### 1. **Qwen3-4B-Instruct-2507** ⭐ RECOMMENDED
**HuggingFace:** `Qwen/Qwen3-4B-Instruct-2507`

**Why interesting:**
- **4B parameters** (2x current baseline)
- **Strong structured output performance**: MultiPL-E 76.8, LiveCodeBench 35.1
- **Excellent code understanding** → Better for CODE_TO_DOT tasks
- **256K context window** → Handles large/complex DOT graphs
- **Proven efficiency**: ~8GB VRAM, same infrastructure as Gemma-2B

**Expected improvement:**
- Phase II.2 (Gemma-2B): 56-65% → Qwen3-4B: **70-80%**

**Research value:**
- Tests hypothesis: Does 2x capacity improve structured syntax generation?
- Compares instruction-tuned models at different scales
- Validates if code-focused pretraining helps DOT generation

**Training config adjustments:**
```yaml
model_name: "Qwen/Qwen3-4B-Instruct-2507"
per_device_train_batch_size: 2  # Halve (larger model)
gradient_accumulation_steps: 8  # Double (maintain effective batch=16)
# Keep other hyperparameters same for fair comparison
```

---

#### 2. **VibeThinker-1.5B** ⚠️ EXPERIMENTAL
**HuggingFace:** `WeiboAI/VibeThinker-1.5B`

**Why interesting:**
- **Smaller than Gemma-2B** (1.5B vs 2B)
- **Exceptional reasoning**: AIME24 80.3 (beats 671B DeepSeek on math)
- **Novel training approach**: Spectrum-to-Signal Principle (diversity → focus)
- **Ultra cost-efficient**: $7,800 post-training cost

**Research questions:**
- Does step-by-step reasoning ability help structured syntax generation?
- Can reasoning-first models learn direct output without verbose explanations?
- Is diversity-driven training beneficial for syntax tasks?

**Risks:**
- Optimized for multi-step reasoning, not direct instruction following
- May generate verbose thinking instead of clean DOT syntax
- Weaker on general/broad tasks (GPQA-Diamond 46.7)

**Hypothesis to test:**
> "Reasoning models may struggle with syntax generation tasks that require 
> direct, structured output rather than step-by-step logical deduction."

**Training considerations:**
- May need different prompt engineering (suppress <think> blocks)
- Could benefit from post-processing to extract DOT from reasoning output
- Interesting as negative case study if it underperforms

---

### Medium-Priority Candidates

#### 3. **Phi-3-Mini-4K-Instruct** (3.8B)
**HuggingFace:** `microsoft/Phi-3-mini-4k-instruct`

**Why interesting:**
- Microsoft's highly optimized small model
- Strong benchmark performance for size
- Good at structured tasks
- Well-documented training process

**Research angle:** Compare tech company approaches (Google Gemma vs MS Phi vs Alibaba Qwen)

---

#### 4. **Llama-3.2-3B-Instruct**
**HuggingFace:** `meta-llama/Llama-3.2-3B-Instruct`

**Why interesting:**
- Meta's latest small model
- Strong baseline performance
- Open weights, permissive license
- Large community support

**Research angle:** Industry standard comparison point

---

## Experimental Training Approaches

### Multi-Model Ensemble Study

**Hypothesis:** Different models excel at different DOT graph types.

**Experiment design:**
1. Train Gemma-2B, Qwen3-4B, VibeThinker-1.5B on same dataset
2. Evaluate on categorized test sets:
   - Simple FSMs (2-5 states)
   - Complex FSMs (6-10 states, hierarchical)
   - Workflows (linear/branching)
   - Network diagrams
   - Dependency graphs
3. Analyze which model performs best on which category
4. Build ensemble: route tasks to best-fit model

**Metric:** Category-specific accuracy, not just overall

---

### Architecture Ablation Study

**Research question:** What architectural features matter most for DOT generation?

**Variables to test:**
- **Model size**: 1.5B → 2B → 4B → 7B
- **Pretraining focus**: General (Gemma) vs Code-focused (Qwen) vs Reasoning (VibeThinker)
- **Context length**: 4K vs 32K vs 256K
- **Attention mechanism**: Standard vs GQA (Grouped Query Attention)

**Expected finding:** Diminishing returns above 4B for simple syntax tasks

---

### Task-Specific Fine-tuning Strategies

**Experiment:** Compare different task formulations

1. **Direct generation** (current approach)
   - Input: "Create FSM for user login"
   - Output: Raw DOT code

2. **Chain-of-thought prompting**
   - Input: "Think step-by-step, then generate DOT"
   - Output: Reasoning + DOT

3. **Structured output with validation**
   - Fine-tune with compiler feedback in training loop
   - Reward valid DOT, penalize syntax errors

4. **Multi-stage generation**
   - Stage 1: Generate abstract graph structure (JSON)
   - Stage 2: Convert JSON → DOT syntax
   - Hypothesis: Easier to learn in stages

---

## Dataset Expansion Directions

### Scale to 1,000+ Pairs

**Current:** 273 pairs  
**Target:** 1,000-2,000 pairs

**Sources:**
1. **More FSM libraries** (50-100 repos): Django-FSM, XState, Robot Framework
2. **Academic datasets**: FSM course materials, textbooks, papers
3. **Industrial examples**: Workflow engines, state machines from real codebases
4. **Synthetic scaling**: Generate 300-500 diverse examples with Gemini/Claude

**Research value:**
- Test scaling laws for syntax learning
- Find data efficiency frontier (minimum pairs for 90%+ accuracy)
- Identify diminishing returns point

---

### Domain-Specific Subsets

Create specialized datasets and models:

1. **FSM-only model** (pure state machines)
2. **Workflow-only model** (CI/CD, business processes)
3. **Network-only model** (architecture diagrams)
4. **Generalist model** (all types)

**Hypothesis:** Specialists outperform generalists on their domain.

---

### Synthetic Data Quality Study

**Question:** How does synthetic data quality affect performance?

**Experiment:**
- Generate 100 pairs each with:
  - Gemini 1.5 Pro (high quality, expensive)
  - Gemini Flash (medium quality, cheap)
  - Ollama Gemma 27B (free, local)
  - Ollama DeepSeek R1 (reasoning-focused)
- Train separate models on each dataset
- Compare: Quality vs Quantity tradeoff

**Expected finding:** 50 high-quality pairs = 200 medium-quality pairs

---

## Evaluation & Benchmarking Extensions

### Beyond Syntactic Validity

**Current metric:** Pass@1 compilation rate (56% Phase II.1)

**New metrics to add:**

1. **Semantic correctness** (LLM-as-a-judge)
   - Does graph match intent?
   - Are transitions logical?
   - Correct graph type for task?

2. **Structural quality**
   - Graph complexity (nodes/edges)
   - Layout effectiveness
   - Style consistency

3. **Human evaluation**
   - Usefulness score
   - Clarity rating
   - Would-use-in-production?

4. **Downstream task performance**
   - Use generated DOT in actual workflow engines
   - Measure execution correctness

---

### Benchmark Dataset Creation

**Goal:** Standardized AnecDOT benchmark for community

**Components:**
- 100 held-out test examples (never seen in training)
- Difficulty tiers: Easy (2-3 states) → Hard (10+ states, hierarchical)
- Diverse domains: FSM, workflow, network, dependency
- Gold-standard reference DOT graphs
- Automated evaluation scripts

**Publication target:** Share on HuggingFace, Papers With Code

---

## Cross-Domain Applications

### 1. DOT → Natural Language (Reverse Task)

**Research question:** Can models trained for NL→DOT also do DOT→NL?

**Applications:**
- Graph documentation generation
- Code explanation
- Workflow description

**Experiment:** Test zero-shot reversal with instruction prompting

---

### 2. Multi-Format Conversion

Extend beyond DOT to other graph formats:

- **DOT ↔ Mermaid** (popular for markdown)
- **DOT ↔ PlantUML** (sequence diagrams)
- **DOT ↔ Cypher** (Neo4j graph queries)
- **DOT ↔ JSON/YAML** (structured data)

**Research value:** Test transfer learning across graph DSLs

---

### 3. Graph-Based Orchestration (Phase III)

**Original vision:** Use DOT output to drive agentic workflows

**Research directions:**
1. **Executable graphs**: DOT → Workflow engine (Temporal, Airflow)
2. **Agent coordination**: Each node = specialized agent
3. **Dynamic replanning**: Model generates updated graphs at runtime
4. **Error recovery**: Graph repairs when execution fails

**Ambitious goal:** End-to-end code generation via graph planning

---

## Publication & Dissemination

### Academic Paper Targets

**Title ideas:**
- "Teaching Small Language Models Structural Reasoning via DOT Graph Generation"
- "AnecDOT: Efficient Fine-Tuning for Graph Syntax Learning"
- "Comparing Model Architectures for Structured Output Generation Tasks"

**Venues:**
- **NeurIPS** (ML methods)
- **EMNLP/ACL** (NLP applications)
- **ICML** (model comparisons)
- **Workshop:** Code Generation, Structured Outputs

**Key contributions:**
1. Novel task formulation (NL/Code → DOT)
2. Efficient dataset creation pipeline
3. QLoRA training methodology for syntax learning
4. Comparative analysis of model architectures
5. Open-source dataset + models

---

### Open-Source Release Strategy

**Components to release:**
1. **Dataset** (273+ pairs) → HuggingFace Datasets
2. **Models** (Gemma-2B, Qwen3-4B checkpoints) → HuggingFace Models
3. **Training code** (QLoRA pipeline) → GitHub
4. **Evaluation suite** → Python package
5. **Benchmark** (100 held-out tests) → Papers With Code

**License:**
- Code: MIT/Apache-2.0
- Dataset: EPL-2.0 (Graphviz compliance)
- Models: Per base model license

**Community building:**
- Blog post on methodology
- Tutorial notebooks
- Demo on HuggingFace Spaces
- Reddit/X/LinkedIn announcement

---

## Resource Requirements Estimate

### For Extended Study (All Models)

| Model | Training Time | VRAM | Cost (Cloud) | Priority |
|-------|--------------|------|--------------|----------|
| Gemma-2B (baseline) | 90s | 3GB | $0.01 | ✅ Done |
| Qwen3-4B | 150s | 5GB | $0.02 | ⭐ High |
| VibeThinker-1.5B | 60s | 2GB | $0.01 | ⚠️ Medium |
| Phi-3-Mini (3.8B) | 140s | 5GB | $0.02 | Medium |
| Llama-3.2-3B | 120s | 4GB | $0.02 | Low |

**Total for all models:** ~$0.10, <10 minutes compute

**With 1,000-pair dataset:**
- Training time: 3-5x longer (~300-450s per model)
- Still extremely affordable (<$1 total)

---

## Timeline Projection

### Conservative Roadmap

**Q1 2025:**
- ✅ Phase II.1 complete (Gemma-2B, 153 pairs, 56% success)
- ✅ Phase II.2 complete (Gemma-2B, 273 pairs, expected 60-65%)
- 🔄 Phase II.3: Qwen3-4B training (1 week)

**Q2 2025:**
- Expand dataset to 500 pairs (1 month)
- Multi-model comparison study (2 weeks)
- Evaluation framework development (2 weeks)

**Q3 2025:**
- Scale to 1,000 pairs (1 month)
- Advanced experiments (ensembles, ablations) (1 month)
- Paper writing (1 month)

**Q4 2025:**
- Paper submission (conference deadline)
- Open-source release preparation
- Community engagement

---

## Decision Points

### When to scale dataset?

**Trigger:** If Phase II.2 (273 pairs) shows >65% success
- Hypothesis validated: More data helps
- Scale to 500 pairs for next experiment

**If <60% success:**
- Try different base model first (Qwen3-4B)
- Data quality > quantity at this stage

---

### When to try VibeThinker?

**Trigger:** After Qwen3-4B results
- If Qwen3-4B achieves 75%+: Test if reasoning helps push to 85%+
- If Qwen3-4B underperforms: VibeThinker unlikely to help

---

### When to pursue publication?

**Minimum bar:**
- ≥3 models tested (Gemma, Qwen, +1)
- ≥500 training pairs
- ≥70% success rate (best model)
- Statistical significance demonstrated
- Novel insights about architecture/data

**Strong publication:**
- 5+ models tested
- 1,000+ pairs
- 85%+ success rate
- Ablation studies
- Benchmark dataset released
- Downstream application demonstrated

---

## Key Research Questions to Answer

1. **Scaling laws:** How does performance scale with model size (1.5B → 7B)?
2. **Data efficiency:** What's the minimum dataset size for 90% accuracy?
3. **Architecture matters:** Do code-focused models beat general models?
4. **Reasoning vs direct:** Does CoT help or hurt syntax generation?
5. **Domain transfer:** Can DOT knowledge transfer to other graph DSLs?
6. **Practical value:** Can generated DOT drive real workflows?

---

## Notes & References

**Model cards reviewed:**
- Qwen3-4B-Instruct-2507: [HuggingFace](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)
- VibeThinker-1.5B: [HuggingFace](https://huggingface.co/WeiboAI/VibeThinker-1.5B)

**Benchmarks to track:**
- MultiPL-E (code generation)
- LiveCodeBench (code reasoning)
- MMLU-Pro (general knowledge)
- ZebraLogic (structured reasoning)

**Community resources:**
- [Awesome-LLM-for-Code](https://github.com/codefuse-ai/Awesome-Code-LLM)
- [OpenCompass Leaderboard](https://opencompass.org.cn/)
- [HuggingFace Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)

---

**Status:** Living document  
**Last updated:** 2025-11-21  
**Next review:** After Phase II.2 results
