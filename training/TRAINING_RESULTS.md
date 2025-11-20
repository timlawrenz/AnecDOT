# Training Results: Phase II.1 - QLoRA Fine-tuning Proof-of-Concept

**Date:** 2025-01-20  
**Model:** google/gemma-2b-it  
**Dataset:** 153 pairs (137 train, 16 validation)  
**Technique:** QLoRA (4-bit quantization + LoRA adapters)

## Executive Summary

✅ **SUCCESS**: Fine-tuning significantly improved DOT graph generation capability.

- **Base Model Performance**: 0/16 valid DOT graphs (0%)
- **Fine-tuned Model Performance**: 9/16 valid DOT graphs (56.2%)
- **Statistical Significance**: z-score = 3.54 (p < 0.001)

**Conclusion:** 160 training pairs are sufficient to teach a 2B parameter model to generate valid DOT syntax with statistically significant improvement.

---

## Training Configuration

### Model Setup
```yaml
Base Model: google/gemma-2b-it (2B parameters)
Quantization: 4-bit NF4
LoRA Configuration:
  - r: 16
  - alpha: 32
  - dropout: 0.05
  - target_modules: [q_proj, v_proj, k_proj, o_proj]
  - trainable_params: 3,686,400 (0.147% of total)
```

### Training Hyperparameters
```yaml
Learning Rate: 2.0e-4
Epochs: 5
Batch Size: 4 per device
Gradient Accumulation: 4 steps (effective batch size: 16)
Warmup Ratio: 0.1
LR Scheduler: cosine
Weight Decay: 0.01
Max Sequence Length: 512
```

### Dataset
```
Total Pairs: 153 (filtered from 160)
Sources:
  - statemachine_cat: 92 pairs
  - attribute_docs: 31 pairs
  - graphviz_gallery: 13 pairs
  - logic extraction: 7 pairs
  - synthetic generation: 10 pairs

Split: 90/10 train/validation
  - Training: 137 examples
  - Validation: 16 examples
```

---

## Training Metrics

### Loss Progression
```
Epoch 1: loss=2.7155, lr=1.95e-4
Epoch 2: loss=1.5798, lr=1.45e-4
Epoch 3: loss=1.0886, lr=6.91e-5
Epoch 4: loss=0.9065, lr=1.09e-5
Epoch 5: Final

Average Training Loss: 1.498
Training Time: 75 seconds (~1.25 minutes)
Throughput: 9.08 samples/second
```

**Loss Reduction:** 2.72 → 0.91 (66% decrease)

---

## Evaluation Results

### Quantitative Metrics

| Metric | Base Model | Fine-tuned Model | Improvement |
|--------|-----------|-----------------|-------------|
| Valid DOT Graphs | 0/16 (0.0%) | 9/16 (56.2%) | +56.2% |
| Invalid Syntax | 0/16 | 7/16 | - |
| No DOT Found | 16/16 | 0/16 | -100% |

### Statistical Analysis
- **Sample Size:** 16 validation examples
- **Z-score:** 3.54
- **P-value:** < 0.001 (highly significant)
- **Result:** Fine-tuning produced statistically significant improvement

### Qualitative Observations

**Base Model Behavior:**
- Generated Python code, prose explanations, or irrelevant content
- No understanding of DOT syntax
- 0% success rate on DOT generation task

**Fine-tuned Model Behavior:**
- Consistently attempted DOT graph generation (16/16)
- Successfully generated valid DOT syntax (9/16)
- Failures primarily due to:
  - Incomplete graphs (missing closing braces)
  - Complex nested structures
  - Attribute formatting errors

---

## Critical Learnings

### 1. Chat Template Format is Critical

**Initial Attempt (FAILED):**
- Used generic format: `<|system|><|user|><|assistant|>`
- Result: 0/16 valid (worse than base model)
- Loss decreased but outputs were gibberish

**Second Attempt (SUCCESS):**
- Used Gemma's native format: `<start_of_turn>user...<end_of_turn><start_of_turn>model...`
- Result: 9/16 valid (56% success rate)
- **Lesson:** Always use model's native chat template for instruction tuning

### 2. Dataset Size Sufficiency

**Finding:** 160 pairs sufficient for proof-of-concept
- Large enough to demonstrate viability
- Too small for production-quality results
- Validation set (16 examples) adequate for statistical significance testing

**Recommendation:** Scale to 250-350 pairs for improved performance

### 3. Model Capacity vs Task Complexity

**Gemma-2B-IT Performance:**
- ✅ Learned basic DOT syntax structure
- ✅ Mastered `digraph {...}` format
- ✅ Generated node and edge declarations
- ⚠️ Struggled with complex nested subgraphs
- ⚠️ Occasional attribute formatting errors

**Recommendation:** Test larger models (7B-9B) for better complex graph handling

---

## Failure Analysis

### 7 Invalid DOT Graphs

**Common failure modes:**
1. **Incomplete graphs** (3/7): Missing closing braces or nodes
2. **Syntax errors** (2/7): Invalid attribute formatting
3. **Complex nesting** (2/7): Nested subgraphs with HTML-like labels

**Example failure:**
```
Input: Complex state machine with nested substates
Output: Correct structure but missing closing brace for subgraph
```

**Mitigation strategies:**
- More training epochs
- Larger model capacity
- More examples of complex nested structures

---

## Reproducibility

### Hardware
- GPU: Consumer-grade (8GB+ VRAM)
- Memory usage: ~2-3GB VRAM during training
- CPU: Any modern multi-core processor

### Software Environment
```
Python: 3.13
transformers: 4.x (latest)
peft: 0.7.0+
bitsandbytes: 0.41.0+
torch: 2.1.0+
accelerate: 0.25.0+
datasets: 2.16.0+
```

### Replication Steps
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify data
python3 training/verify_data.py
# Expected: 153 pairs

# 3. Train
python3 training/train.py
# Expected: ~75 seconds, loss 2.7 → 0.9

# 4. Evaluate
python3 training/evaluate_model.py
# Expected: 9/16 valid (56%)
```

---

## Comparison to Baselines

### vs Base Gemma-2B-IT
- **Improvement:** +56.2 percentage points
- **Significance:** z = 3.54, p < 0.001
- **Verdict:** Clear win for fine-tuning

### vs Synthetic Generation (Gemma-27B)
- Synthetic generator: ~100% valid DOT (teacher model)
- Fine-tuned 2B: 56% valid DOT
- **Note:** 2B model learned from teacher outputs, expected gap

---

## Cost-Benefit Analysis

### Training Costs
- **Time:** 75 seconds
- **Compute:** Single GPU, ~3GB VRAM
- **Energy:** Negligible (~0.01 kWh)
- **Total Cost:** < $0.01 on cloud GPU

### Benefits
- Validated end-to-end pipeline
- Proven approach viability
- Baseline for scaling experiments
- Reusable infrastructure

**ROI:** Extremely high for proof-of-concept phase

---

## Next Steps

### Immediate (Phase II.2)
- [ ] Scale dataset to 250-350 pairs
- [ ] Test larger models (Gemma-7B, Phi-3-7B)
- [ ] Increase training epochs (10-15)
- [ ] Implement better evaluation metrics (semantic correctness)

### Medium-term (Phase II.3)
- [ ] Add graph-specific validation (edge connectivity, node references)
- [ ] Evaluate on diverse graph types (FSM, flowchart, network, architecture)
- [ ] Compare multiple model architectures
- [ ] Implement ensemble approaches

### Long-term (Phase III)
- [ ] Deploy model for graph-based agentic workflows
- [ ] Integrate with DOT → execution pipeline
- [ ] Create public dataset and model release
- [ ] Benchmark against commercial alternatives

---

## Conclusions

**Primary Finding:** Fine-tuning small LLMs on DOT graph generation is viable and effective.

**Key Success Factors:**
1. Correct chat template formatting
2. Diverse training data (multiple graph types)
3. Adequate dataset size (~150+ pairs)
4. QLoRA for efficient training

**Limitations:**
- 56% success rate insufficient for production
- Model struggles with complex nested structures
- Small validation set limits detailed analysis

**Overall Assessment:** ✅ **Proof-of-concept successful**

The infrastructure, methodology, and approach are validated. Scaling to more data and larger models should yield production-ready results.

---

## References

- **Training Script:** `training/train.py`
- **Evaluation Script:** `training/evaluate_model.py`
- **Detailed Results:** `training/evaluation_results.json`
- **Model Checkpoint:** `training/outputs/final/`
- **OpenSpec Proposal:** `openspec/changes/add-qlora-training-infrastructure/`

## Acknowledgments

- QLoRA technique: Dettmers et al. (2023)
- Base model: Google Gemma team
- Graphviz: Open-source graph visualization community
- Dataset sources: statemachine_cat, graphviz.org, synthetic generation
