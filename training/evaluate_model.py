#!/usr/bin/env python3
"""
Evaluate and compare base model vs fine-tuned model on validation set.

Usage:
    python evaluate_model.py
"""

import os
import json
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from dataset import AnecDOTDataset
from eval import is_valid_dot_syntax, extract_dot_from_response
import argparse


def load_base_model(model_name="google/gemma-2b-it"):
    """Load base model with quantization."""
    print(f"\nLoading base model: {model_name}")
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True
    )
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer


def load_finetuned_model(checkpoint_path="training/outputs/final"):
    """Load fine-tuned model."""
    print(f"\nLoading fine-tuned model from: {checkpoint_path}")
    
    # Load base model first
    base_model, tokenizer = load_base_model()
    
    # Load LoRA adapters
    model = PeftModel.from_pretrained(base_model, checkpoint_path)
    
    return model, tokenizer


def generate_dot(model, tokenizer, prompt, max_tokens=512, temperature=0.7):
    """Generate DOT graph from prompt."""
    # Use tokenizer's chat template if available
    if hasattr(tokenizer, 'apply_chat_template'):
        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    else:
        # Fallback to Gemma format
        formatted_prompt = f"<bos><start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the model's response
    if "<start_of_turn>model" in generated:
        generated = generated.split("<start_of_turn>model")[-1].strip()
    elif "<|assistant|>" in generated:
        generated = generated.split("<|assistant|>")[-1].strip()
    
    return generated


def evaluate_on_validation_set(model, tokenizer, val_examples, model_name="model"):
    """Evaluate model on validation examples."""
    results = []
    valid_count = 0
    
    print(f"\nEvaluating {model_name} on {len(val_examples)} validation examples...")
    
    for i, example in enumerate(val_examples):
        print(f"  [{i+1}/{len(val_examples)}] ", end="", flush=True)
        
        input_text = example["input_text"]
        expected_dot = example["output_dot"]
        
        # Generate
        generated = generate_dot(model, tokenizer, input_text)
        
        # Extract DOT
        extracted_dot = extract_dot_from_response(generated)
        
        # Validate
        is_valid = False
        if extracted_dot:
            is_valid = is_valid_dot_syntax(extracted_dot)
            if is_valid:
                valid_count += 1
                print("✓")
            else:
                print("✗ (invalid syntax)")
        else:
            print("✗ (no DOT found)")
        
        results.append({
            "input": input_text,
            "expected": expected_dot,
            "generated": generated,
            "extracted_dot": extracted_dot,
            "is_valid": is_valid,
            "source": example.get("source", "unknown")
        })
    
    validity_rate = valid_count / len(val_examples) if val_examples else 0
    
    print(f"\n{model_name} Results:")
    print(f"  Valid DOT graphs: {valid_count}/{len(val_examples)} ({validity_rate:.1%})")
    
    return results, validity_rate


def compare_models(base_results, ft_results):
    """Compare base model vs fine-tuned model results."""
    print("\n" + "="*70)
    print("COMPARISON: Base Model vs Fine-Tuned Model")
    print("="*70)
    
    base_valid = sum(1 for r in base_results if r["is_valid"])
    ft_valid = sum(1 for r in ft_results if r["is_valid"])
    
    n = len(base_results)
    base_rate = base_valid / n if n > 0 else 0
    ft_rate = ft_valid / n if n > 0 else 0
    
    improvement = ft_valid - base_valid
    improvement_pct = ((ft_rate - base_rate) / base_rate * 100) if base_rate > 0 else float('inf')
    
    print(f"\nValidation Set Size: {n} examples")
    print(f"\nBase Model:       {base_valid}/{n} valid ({base_rate:.1%})")
    print(f"Fine-Tuned Model: {ft_valid}/{n} valid ({ft_rate:.1%})")
    print(f"\nImprovement:      +{improvement} examples ({improvement_pct:+.1f}%)")
    
    # Statistical significance (simple binomial test approximation)
    if n >= 10:
        # Using normal approximation for binomial proportion test
        p_pooled = (base_valid + ft_valid) / (2 * n)
        se = (2 * p_pooled * (1 - p_pooled) / n) ** 0.5
        z_score = (ft_rate - base_rate) / se if se > 0 else 0
        
        print(f"\nApproximate z-score: {z_score:.2f}")
        if abs(z_score) > 1.96:
            print("Result: STATISTICALLY SIGNIFICANT (p < 0.05)")
        else:
            print("Result: Not statistically significant (p >= 0.05)")
    
    print("\n" + "="*70)


def save_results(base_results, ft_results, output_file="training/evaluation_results.json"):
    """Save detailed results to JSON."""
    results = {
        "validation_size": len(base_results),
        "base_model": {
            "valid_count": sum(1 for r in base_results if r["is_valid"]),
            "validity_rate": sum(1 for r in base_results if r["is_valid"]) / len(base_results),
            "examples": base_results
        },
        "finetuned_model": {
            "valid_count": sum(1 for r in ft_results if r["is_valid"]),
            "validity_rate": sum(1 for r in ft_results if r["is_valid"]) / len(ft_results),
            "examples": ft_results
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate base vs fine-tuned model")
    parser.add_argument("--base-only", action="store_true", help="Only evaluate base model")
    parser.add_argument("--ft-only", action="store_true", help="Only evaluate fine-tuned model")
    parser.add_argument("--num-examples", type=int, default=None, help="Limit number of validation examples")
    args = parser.parse_args()
    
    # Load validation data
    print("Loading validation dataset...")
    dataset_loader = AnecDOTDataset(seed=42)
    datasets = dataset_loader.create_dataset(train_val_split=0.9)
    val_dataset = datasets["validation"]
    
    # Limit examples if requested
    if args.num_examples:
        val_examples = list(val_dataset.select(range(min(args.num_examples, len(val_dataset)))))
    else:
        val_examples = list(val_dataset)
    
    print(f"Evaluating on {len(val_examples)} validation examples")
    
    # Evaluate base model
    if not args.ft_only:
        base_model, base_tokenizer = load_base_model()
        base_results, base_rate = evaluate_on_validation_set(
            base_model, base_tokenizer, val_examples, "Base Model"
        )
        del base_model  # Free memory
        torch.cuda.empty_cache()
    else:
        base_results = None
    
    # Evaluate fine-tuned model
    if not args.base_only:
        ft_model, ft_tokenizer = load_finetuned_model()
        ft_results, ft_rate = evaluate_on_validation_set(
            ft_model, ft_tokenizer, val_examples, "Fine-Tuned Model"
        )
    else:
        ft_results = None
    
    # Compare
    if base_results and ft_results:
        compare_models(base_results, ft_results)
        save_results(base_results, ft_results)
    elif base_results:
        print(f"\nBase model validity rate: {base_rate:.1%}")
    elif ft_results:
        print(f"\nFine-tuned model validity rate: {ft_rate:.1%}")


if __name__ == "__main__":
    main()
