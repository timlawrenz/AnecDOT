# AnecDOT QLoRA Training

Fine-tuning infrastructure for training small language models to generate DOT graphs from text/code descriptions.

## Overview

This directory contains the QLoRA (Quantized Low-Rank Adaptation) training pipeline for the AnecDOT project. It enables efficient fine-tuning of small LLMs on ~160 (text, DOT) pairs to validate the end-to-end pipeline.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

Required packages:
- `transformers` - Model loading and training
- `peft` - LoRA adapters
- `bitsandbytes` - 4-bit quantization
- `accelerate` - GPU optimization
- `datasets` - Data handling
- `torch` - PyTorch backend

### 2. Verify Data

```bash
python dataset.py
```

This should show:
- ~160 total training pairs
- Sources: statemachine_cat, synthetic, logic, documentation, attribute-docs
- Train/validation split details

### 3. Configure Training

Edit `config.yaml` to adjust hyperparameters:
- Model selection (default: `google/gemma-2b-it`)
- LoRA parameters (rank, alpha, target modules)
- Training settings (learning rate, batch size, epochs)

### 4. Run Training

```bash
python train.py
```

Training will:
- Load and tokenize datasets
- Initialize model with 4-bit quantization
- Apply LoRA adapters
- Train for configured epochs
- Save checkpoints to `outputs/`
- Generate evaluation samples

## Files

- **`train.py`** - Main training script
- **`dataset.py`** - Dataset loading and preprocessing
- **`eval.py`** - Evaluation utilities (DOT validation, metrics)
- **`config.yaml`** - Training configuration
- **`outputs/`** - Saved checkpoints and final model (created during training)

## Configuration

Key hyperparameters in `config.yaml`:

```yaml
# Model
model_name: "google/gemma-2b-it"
load_in_4bit: true

# LoRA
lora_r: 16              # Rank (higher = more capacity, slower)
lora_alpha: 32          # Scaling factor
lora_target_modules: ["q_proj", "v_proj", "k_proj", "o_proj"]

# Training
learning_rate: 2.0e-4
num_train_epochs: 5
per_device_train_batch_size: 4
gradient_accumulation_steps: 4  # Effective batch size: 16
```

## Expected Behavior

**Memory Usage:**
- 4-bit quantization: ~2-3GB VRAM for Gemma-2B
- LoRA adapters: minimal overhead (~10-50MB)
- Should fit on consumer GPUs (RTX 3060+, T4, etc.)

**Training Time:**
- ~160 examples, 5 epochs, batch size 16
- Estimated: 10-30 minutes depending on GPU

**Success Criteria:**
1. Training loss decreases consistently
2. Validation loss trends downward (not overfitting)
3. Generated DOT is syntactically valid
4. Model improves over base model baseline

## Data Format

Training pairs are loaded from:

1. **`data/training/statemachine_cat/pairs.json`** (92 pairs)
   ```json
   {
     "input_code": "FSM implementation code...",
     "output_dot": "digraph { ... }"
   }
   ```

2. **`data/*.jsonl` streams** (68 pairs)
   ```json
   {
     "input_text": "Description or code...",
     "output_dot": "digraph { ... }"
   }
   ```

Formatted as instruction-tuning prompts:
```
<|system|>
You are a DOT graph generator. Convert the given input into a valid DOT graph representation.
<|user|>
{input_text}
<|assistant|>
{output_dot}
```

## Evaluation

### During Training

- **Validation loss** logged every `eval_steps` (default: 50)
- **Sample generation** at evaluation steps (if enabled)
- **Checkpoints** saved every `save_steps` (default: 50)

### Post-Training

Run evaluation on validation set:

```python
from eval import evaluate_generation

# Load trained model
model = AutoModelForCausalLM.from_pretrained("outputs/final")
tokenizer = AutoTokenizer.from_pretrained("outputs/final")

# Evaluate on validation prompts
results = evaluate_generation(model, tokenizer, val_prompts)
print(f"Validity rate: {results['validity_rate']:.2%}")
```

### Metrics

- **Validation loss** - Primary training metric
- **DOT syntax validity** - Percentage of generated graphs that parse correctly
- **Visual inspection** - Sample outputs for semantic correctness

## Troubleshooting

**Out of Memory:**
- Reduce `per_device_train_batch_size` (try 2 or 1)
- Reduce `max_seq_length` (try 384 or 256)
- Use smaller model (try `Qwen2.5-1.5B` or `Phi-2`)

**Model not improving:**
- Check baseline: is base model already good at DOT?
- Increase epochs (try 10)
- Adjust learning rate (try 3e-4 or 1e-4)
- Verify data quality with `dataset.py`

**Training too slow:**
- Increase batch size if memory allows
- Reduce `max_seq_length`
- Use fewer evaluation steps

## Model Alternatives

If `gemma-2b-it` doesn't work well:

- **`microsoft/phi-2`** - 2.7B, strong code generation
- **`Qwen/Qwen2.5-1.5B-Instruct`** - Smallest viable option
- **`stabilityai/stablelm-2-zephyr-1_6b`** - 1.6B instruction-tuned

Change in `config.yaml`:
```yaml
model_name: "microsoft/phi-2"
```

## Next Steps

After training:

1. **Measure statistical significance** - Compare validation metrics to baseline
2. **Test generalization** - Try novel prompts not in training set
3. **Analyze failures** - Which graph types does it struggle with?
4. **Scale dataset** - If viable, expand to 250-350 pairs
5. **Optimize hyperparameters** - Grid search learning rate, LoRA rank, etc.

## References

- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [PEFT Documentation](https://huggingface.co/docs/peft)
- [Gemma Model Card](https://huggingface.co/google/gemma-2b-it)
