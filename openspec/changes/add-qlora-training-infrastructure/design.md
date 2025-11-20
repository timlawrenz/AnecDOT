# Design: QLoRA Training Infrastructure

## Context
We have ~160 training pairs: 92 extracted from statemachine_cat repository and 68 from synthetic generation streams (diverse graph types, logic extraction, documentation). This is enough to test viability - not enough to expect production-quality results, but sufficient to measure if fine-tuning improves DOT generation over base models.

## Goals / Non-Goals

**Goals:**
- Prove end-to-end pipeline viability with current dataset size
- Efficient training on consumer GPU (QLoRA for memory efficiency)
- Minimal infrastructure to get first training results
- Clear success/failure criteria

**Non-Goals:**
- Production-ready training pipeline
- Distributed training or multi-GPU support
- Extensive hyperparameter optimization
- Advanced evaluation metrics

## Decisions

### Model Selection
**Decision:** Start with small instruction-tuned models (2-3B parameters)
- **Options considered:**
  - Gemma-2B-it: Good instruction following, 2B parameters
  - Phi-2: 2.7B parameters, strong code generation
  - Qwen2.5-1.5B: Smallest viable option
- **Rationale:** Gemma3:27b for synthetic generation ≠ training target. Smaller models train faster, validate concept, can scale up later.

### Training Approach
**Decision:** QLoRA (4-bit quantization + LoRA adapters)
- **Why:** Reduces memory footprint by ~4x, enables training on consumer GPUs
- **LoRA config:** r=16, alpha=32, target modules: q_proj, v_proj (conservative start)

### Data Format
**Decision:** Instruction-tuning format with system prompt
```
<system>You are a DOT graph generator.</system>
<user>{natural language or code description}</user>
<assistant>{DOT graph}</assistant>
```
- **Alternatives:** 
  - Plain concatenation: Less structured
  - Chat templates: More complex, unnecessary for proof-of-concept
- **Rationale:** Clear role separation, matches instruction-tuned model training

### Success Criteria
**What proves viability?**
1. Training loss decreases consistently
2. Model generates syntactically valid DOT after training
3. Generated DOT matches input semantics (basic cases)
4. Training completes without OOM on available GPU

**What indicates failure?**
- Model only memorizes training examples (overfitting)
- Generated DOT is syntactically invalid
- No improvement over base model

## Risks / Trade-offs

**Risk:** Dataset too small for meaningful fine-tuning
- **Mitigation:** Use data augmentation, track validation metrics, expand dataset if needed

**Risk:** Model overfits to limited examples
- **Mitigation:** Early stopping, validation split, focus on diversity over quantity

**Trade-off:** Small model may have limited capacity
- **Accepted:** Good enough for proof-of-concept, can scale later

## Implementation Notes

### Directory Structure
```
training/
├── train.py           # Main training script
├── config.yaml        # Hyperparameters
├── dataset.py         # Data loading and preprocessing
├── eval.py            # Evaluation utilities
└── README.md          # Usage documentation
```

### Hyperparameters (starting point)
```yaml
model: google/gemma-2b-it
quantization: 4bit
lora_r: 16
lora_alpha: 32
learning_rate: 2e-4
batch_size: 4
gradient_accumulation: 4  # effective batch 16
epochs: 3-5
warmup_ratio: 0.1
```

### Dependencies
- transformers >= 4.36.0
- peft >= 0.7.0
- bitsandbytes >= 0.41.0
- accelerate >= 0.25.0
- datasets >= 2.16.0

## Open Questions
- Should we train separate models for (code→DOT) vs (NL→DOT)?
- What's the minimum dataset size for viable results?
- How do we handle diverse graph types (FSM, flowchart, network, etc.)?
