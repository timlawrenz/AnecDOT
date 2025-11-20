"""
QLoRA training script for AnecDOT.

Trains a small language model to generate DOT graphs from text/code descriptions.
"""

import os
import yaml
import torch
from pathlib import Path
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from dataset import AnecDOTDataset
from eval import compute_metrics, evaluate_generation
import argparse


def load_config(config_path: str = "training/config.yaml"):
    """Load training configuration."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def setup_model_and_tokenizer(config):
    """Initialize model with QLoRA configuration."""
    
    # BitsAndBytes config for 4-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config["load_in_4bit"],
        bnb_4bit_compute_dtype=getattr(torch, config["bnb_4bit_compute_dtype"]),
        bnb_4bit_quant_type=config["bnb_4bit_quant_type"],
        bnb_4bit_use_double_quant=True
    )
    
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        config["model_name"],
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Prepare for k-bit training
    model = prepare_model_for_kbit_training(model)
    
    # LoRA config
    lora_config = LoraConfig(
        r=config["lora_r"],
        lora_alpha=config["lora_alpha"],
        lora_dropout=config["lora_dropout"],
        target_modules=config["lora_target_modules"],
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        config["model_name"],
        trust_remote_code=True
    )
    
    # Set pad token if not present
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = model.config.eos_token_id
    
    return model, tokenizer


def tokenize_function(examples, tokenizer, max_length):
    """Tokenize examples for training."""
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=max_length,
        padding="max_length"
    )


def main(config_path: str = "training/config.yaml"):
    """Main training loop."""
    
    # Load config
    config = load_config(config_path)
    print(f"Loaded config from {config_path}")
    print(f"Model: {config['model_name']}")
    
    # Load dataset
    print("\nLoading dataset...")
    dataset_loader = AnecDOTDataset(seed=config["seed"])
    stats = dataset_loader.get_statistics()
    print(f"Dataset stats: {stats}")
    
    datasets = dataset_loader.create_dataset(
        train_val_split=config["train_val_split"]
    )
    
    # Setup model and tokenizer
    print("\nSetting up model and tokenizer...")
    model, tokenizer = setup_model_and_tokenizer(config)
    
    # Tokenize datasets
    print("\nTokenizing datasets...")
    tokenized_train = datasets["train"].map(
        lambda x: tokenize_function(x, tokenizer, config["max_seq_length"]),
        batched=True,
        remove_columns=datasets["train"].column_names
    )
    
    tokenized_val = datasets["validation"].map(
        lambda x: tokenize_function(x, tokenizer, config["max_seq_length"]),
        batched=True,
        remove_columns=datasets["validation"].column_names
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config["output_dir"],
        num_train_epochs=config["num_train_epochs"],
        per_device_train_batch_size=config["per_device_train_batch_size"],
        gradient_accumulation_steps=config["gradient_accumulation_steps"],
        learning_rate=config["learning_rate"],
        warmup_ratio=config["warmup_ratio"],
        lr_scheduler_type=config["lr_scheduler_type"],
        weight_decay=config["weight_decay"],
        max_grad_norm=config["max_grad_norm"],
        logging_steps=config["logging_steps"],
        save_steps=config["save_steps"],
        save_total_limit=config["save_total_limit"],
        evaluation_strategy=config["evaluation_strategy"],
        eval_steps=config["eval_steps"],
        fp16=True,
        report_to="none",  # Disable wandb/tensorboard for now
        seed=config["seed"]
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )
    
    # Train
    print("\nStarting training...")
    print(f"Total training examples: {len(tokenized_train)}")
    print(f"Total validation examples: {len(tokenized_val)}")
    print(f"Effective batch size: {config['per_device_train_batch_size'] * config['gradient_accumulation_steps']}")
    
    trainer.train()
    
    # Save final model
    print("\nSaving final model...")
    trainer.save_model(os.path.join(config["output_dir"], "final"))
    tokenizer.save_pretrained(os.path.join(config["output_dir"], "final"))
    
    # Final evaluation
    print("\nFinal evaluation...")
    eval_results = trainer.evaluate()
    print(f"Validation loss: {eval_results['eval_loss']:.4f}")
    
    # Sample generation
    if config.get("generate_samples_during_eval", False):
        print("\nGenerating sample outputs...")
        val_samples = datasets["validation"].select(range(min(config["num_eval_samples"], len(datasets["validation"]))))
        
        for i, sample in enumerate(val_samples):
            print(f"\n--- Sample {i+1} ---")
            print(f"Input: {sample['input_text'][:100]}...")
            
            prompt = f"<|system|>\nYou are a DOT graph generator. Convert the given input into a valid DOT graph representation.\n<|user|>\n{sample['input_text']}\n<|assistant|>\n"
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.7, do_sample=True)
            generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            print(f"Generated: {generated[len(prompt):200]}...")
    
    print("\nTraining complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train AnecDOT model with QLoRA")
    parser.add_argument("--config", type=str, default="training/config.yaml", help="Path to config file")
    args = parser.parse_args()
    
    main(args.config)
