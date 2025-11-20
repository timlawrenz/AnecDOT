## ADDED Requirements

### Requirement: QLoRA Training Configuration
The system SHALL provide QLoRA training infrastructure to fine-tune small language models on (text, DOT) pairs with 4-bit quantization and LoRA adapters.

#### Scenario: Model loads with quantization
- **WHEN** training script initializes model with QLoRA config
- **THEN** model loads in 4-bit quantization
- **AND** LoRA adapters are attached to target modules
- **AND** memory usage is reduced vs full fine-tuning

#### Scenario: Training runs without OOM
- **WHEN** training executes with configured batch size and gradient accumulation
- **THEN** training completes without out-of-memory errors on available GPU

### Requirement: Dataset Loading and Preprocessing
The system SHALL load (text, DOT) pairs from data/ directory and format them for instruction-tuning.

#### Scenario: Pairs loaded from filesystem
- **WHEN** dataset loader runs
- **THEN** all JSON files in data/ are discovered
- **AND** (code, DOT) and (text, DOT) pairs are extracted
- **AND** data statistics are reported (count, avg lengths)

#### Scenario: Instruction format applied
- **WHEN** pairs are preprocessed for training
- **THEN** data is formatted with system/user/assistant roles
- **AND** tokenization respects model's sequence length
- **AND** train/validation split is applied (e.g., 90/10)

### Requirement: Training Execution
The system SHALL execute training loop with checkpointing, logging, and early stopping.

#### Scenario: Training progresses with logging
- **WHEN** training runs for configured epochs
- **THEN** loss metrics are logged per step
- **AND** learning rate schedule is applied
- **AND** GPU memory usage is tracked

#### Scenario: Checkpoints saved
- **WHEN** training completes epoch or reaches save interval
- **THEN** model checkpoint is saved to disk
- **AND** checkpoint includes LoRA adapters and training state

### Requirement: Basic Evaluation
The system SHALL evaluate model performance on validation set and sample generation quality.

#### Scenario: Validation loss computed
- **WHEN** evaluation runs on validation split
- **THEN** validation loss is computed
- **AND** loss trend indicates learning vs overfitting

#### Scenario: Sample generation validates syntax
- **WHEN** model generates DOT from test prompts
- **THEN** output is parseable DOT syntax
- **AND** generated graphs match input semantics (basic cases)

### Requirement: Documentation and Reproducibility
The system SHALL provide documentation for training setup, execution, and evaluation.

#### Scenario: Training can be reproduced
- **WHEN** user follows training README
- **THEN** dependencies are installable
- **AND** training script runs with provided config
- **AND** expected outputs are documented
