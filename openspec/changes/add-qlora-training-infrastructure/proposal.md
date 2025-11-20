# Change: Add QLoRA Training Infrastructure

## Why
To validate the complete AnecDOT pipeline (I.1 → II.3), we need infrastructure to fine-tune a small LLM on our extracted and synthetic DOT graph data. With ~160 training pairs, this tests whether our dataset quality and size are sufficient to measurably improve a model's DOT generation capabilities.

## What Changes
- Add QLoRA (Quantized Low-Rank Adaptation) training setup for efficient fine-tuning
- Implement training script with configurable hyperparameters
- Add dataset loading and preprocessing for (text, DOT) pairs
- Create minimal evaluation framework to measure training success
- Document model selection rationale and training approach

## Impact
- Affected specs: Creates new `training-infrastructure` capability
- Affected code: New `training/` directory with trainer, config, and evaluation scripts
- Dependencies: transformers, peft, bitsandbytes, accelerate, datasets
- Validates: Entire Phase I → Phase II pipeline before dataset expansion
