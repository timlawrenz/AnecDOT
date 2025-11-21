#!/usr/bin/env python3
"""
Generate visual comparison showcase for Phase II.2.5 results.

Creates a comprehensive table showing:
1. Test prompt
2. Base model output
3. Fine-tuned model output
4. Rendered SVG graphs (side-by-side)

This provides compelling visual evidence of the improvement.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
import torch
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Import improved prompts
sys.path.insert(0, str(Path(__file__).parent))
from improved_prompts_v2 import format_prompt


# Raw test prompts (will be formatted with instructions)
TEST_PROMPTS_RAW = [
    {
        "id": "simple_fsm",
        "category": "Simple FSM",
        "prompt": "Create a state machine for a traffic light with three states: Green, Yellow, and Red. Green transitions to Yellow, Yellow to Red, and Red back to Green."
    },
    {
        "id": "login_flow",
        "category": "Workflow",
        "prompt": "Design a login workflow state machine with states: LoggedOut, LoggingIn, LoggedIn, and Error. Include transitions for submit, success, failure, and logout."
    },
    {
        "id": "order_processing",
        "category": "Business Process",
        "prompt": "Create a state diagram for order processing: Pending → Processing → Shipped → Delivered. Include a Cancelled state that can be reached from Pending or Processing."
    },
    {
        "id": "door_lock",
        "category": "Simple FSM",
        "prompt": "Model a smart door lock with states: Locked, Unlocked, and Jammed. Include transitions for unlock (Locked→Unlocked), lock (Unlocked→Locked), and jam_detected (any→Jammed)."
    },
    {
        "id": "payment_gateway",
        "category": "Complex Workflow",
        "prompt": "Payment processing state machine: Initiated → Authorizing → Authorized → Capturing → Completed. Include Failed state reachable from Authorizing and Capturing."
    },
    {
        "id": "document_approval",
        "category": "Business Process",
        "prompt": "Document approval workflow: Draft → Review → Approved/Rejected. From Rejected, can go back to Draft for revision."
    },
    {
        "id": "media_player",
        "category": "Device Control",
        "prompt": "Media player state machine with states: Stopped, Playing, Paused. Include transitions: play, pause, stop, resume."
    },
    {
        "id": "network_connection",
        "category": "Network Protocol",
        "prompt": "TCP connection states: Closed → SynSent → Established → FinWait → Closed. Show the connection lifecycle."
    }
]

# Format all prompts with improved instruction format (Phase II.2.6)
TEST_PROMPTS = [
    {
        **item,
        "prompt": format_prompt(item["prompt"], "nl_to_dot")
    }
    for item in TEST_PROMPTS_RAW
]


def load_models():
    """Load base model and fine-tuned model."""
    
    base_model_name = "google/gemma-2b-it"
    adapter_path = "training/outputs/final"
    
    print("Loading models...")
    print(f"  Base model: {base_model_name}")
    print(f"  Fine-tuned adapter: {adapter_path}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    
    # Load base model
    print("\n  Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Load fine-tuned model
    print("  Loading fine-tuned model...")
    ft_base = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    ft_model = PeftModel.from_pretrained(ft_base, adapter_path)
    
    print("✓ Models loaded\n")
    
    return tokenizer, base_model, ft_model


def generate_dot(model, tokenizer, prompt: str, max_tokens: int = 512) -> str:
    """Generate DOT code from prompt using model."""
    
    # Format as chat message
    messages = [{"role": "user", "content": prompt}]
    input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # Tokenize
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract response (after the prompt)
    if "model" in generated:
        response = generated.split("model")[-1].strip()
    else:
        response = generated
    
    return response


def extract_dot(text: str) -> Optional[str]:
    """Extract DOT code from generated text."""
    
    import re
    
    # Try to find digraph block
    patterns = [
        r'(digraph\s+[^{]*\{[^}]*\})',
        r'(digraph\s+.*?\{.*?\})',
        r'```dot\s*(digraph.*?)```',
        r'```\s*(digraph.*?)```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            dot_code = match.group(1).strip()
            # Ensure it has balanced braces
            if dot_code.count('{') == dot_code.count('}'):
                return dot_code
    
    # If no match, check if entire text is DOT
    if text.strip().startswith('digraph'):
        return text.strip()
    
    return None


def validate_and_render_dot(dot_code: Optional[str], output_path: Path) -> bool:
    """Validate DOT syntax and render to SVG."""
    
    if not dot_code:
        return False
    
    try:
        # Write DOT to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as f:
            f.write(dot_code)
            temp_dot = f.name
        
        # Render to SVG
        result = subprocess.run(
            ['dot', '-Tsvg', temp_dot, '-o', str(output_path)],
            capture_output=True,
            timeout=5
        )
        
        # Clean up
        Path(temp_dot).unlink()
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"    Render error: {e}")
        return False


def save_raw_results(results: List[Dict], output_path: Path):
    """Save raw results to JSON for inspection."""
    
    # Create simplified version for JSON (remove model objects)
    json_results = []
    for r in results:
        json_results.append({
            'id': r['id'],
            'category': r['category'],
            'prompt': r['prompt'],
            'base_output': r['base_output'],
            'base_dot': r['base_dot'],
            'base_valid': r['base_valid'],
            'ft_output': r['ft_output'],
            'ft_dot': r['ft_dot'],
            'ft_valid': r['ft_valid'],
        })
    
    with open(output_path, 'w') as f:
        json.dump(json_results, f, indent=2)


def generate_comparison_table(results: List[Dict]) -> str:
    """Generate Markdown table with results."""
    
    md = "# Phase II.2.5 Visual Results Showcase\n\n"
    md += "**Date:** 2025-11-21  \n"
    md += "**Model:** google/gemma-2b-it  \n"
    md += "**Training:** Phase II.2.5 (450 pairs with error correction)  \n\n"
    md += "---\n\n"
    
    # Summary stats
    base_success = sum(1 for r in results if r['base_valid'])
    ft_success = sum(1 for r in results if r['ft_valid'])
    
    md += "## Summary\n\n"
    md += f"- **Test prompts:** {len(results)}\n"
    md += f"- **Base model success:** {base_success}/{len(results)} ({100*base_success/len(results):.1f}%)\n"
    md += f"- **Fine-tuned success:** {ft_success}/{len(results)} ({100*ft_success/len(results):.1f}%)\n"
    md += f"- **Improvement:** +{ft_success - base_success} examples\n\n"
    md += "---\n\n"
    
    # Individual results
    for i, result in enumerate(results, 1):
        md += f"## Test {i}: {result['category']}\n\n"
        
        # Prompt
        md += "### Prompt\n\n"
        md += f"> {result['prompt']}\n\n"
        
        # Base model result
        md += "### Base Model Output\n\n"
        if result['base_valid']:
            md += "✅ **Valid DOT generated**\n\n"
            md += "```dot\n"
            md += result['base_dot'] + "\n"
            md += "```\n\n"
            if result['base_svg']:
                md += f"![Base Model Graph]({result['base_svg']})\n\n"
        else:
            md += "❌ **Failed to generate valid DOT**\n\n"
            if result['base_output']:
                md += "<details>\n<summary>Raw output (click to expand)</summary>\n\n"
                md += "```\n"
                md += result['base_output']  # Full output, no truncation
                md += "\n```\n\n"
                md += "</details>\n\n"
        
        # Fine-tuned model result
        md += "### Fine-Tuned Model Output\n\n"
        if result['ft_valid']:
            md += "✅ **Valid DOT generated**\n\n"
            md += "```dot\n"
            md += result['ft_dot'] + "\n"
            md += "```\n\n"
            if result['ft_svg']:
                md += f"![Fine-Tuned Model Graph]({result['ft_svg']})\n\n"
        else:
            md += "❌ **Failed to generate valid DOT**\n\n"
            if result['ft_output']:
                md += "<details>\n<summary>Raw output (click to expand)</summary>\n\n"
                md += "```\n"
                md += result['ft_output']  # Full output, no truncation
                md += "\n```\n\n"
                md += "</details>\n\n"
        
        # Comparison
        md += "### Result\n\n"
        if result['base_valid'] and result['ft_valid']:
            md += "✅ **Both models succeeded** - Fine-tuned maintains quality\n\n"
        elif not result['base_valid'] and result['ft_valid']:
            md += "🎉 **Fine-tuned model succeeded where base failed!**\n\n"
        elif result['base_valid'] and not result['ft_valid']:
            md += "⚠️ **Regression** - Base succeeded but fine-tuned failed\n\n"
        else:
            md += "❌ **Both failed** - Challenging example\n\n"
        
        md += "---\n\n"
    
    return md


def main():
    """Main function to generate showcase."""
    
    print("=" * 70)
    print("PHASE II.2.5 VISUAL SHOWCASE GENERATOR")
    print("=" * 70)
    print()
    
    # Create output directory
    output_dir = Path("docs/showcase")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Load models
    tokenizer, base_model, ft_model = load_models()
    
    # Run tests
    results = []
    
    for i, test in enumerate(TEST_PROMPTS, 1):
        print(f"\n[{i}/{len(TEST_PROMPTS)}] Testing: {test['category']}")
        print(f"  Prompt: {test['prompt'][:60]}...")
        
        result = {
            'id': test['id'],
            'category': test['category'],
            'prompt': test['prompt'],
            'base_output': None,
            'base_dot': None,
            'base_valid': False,
            'base_svg': None,
            'ft_output': None,
            'ft_dot': None,
            'ft_valid': False,
            'ft_svg': None,
        }
        
        # Generate with base model
        print("  Generating with base model...")
        try:
            base_output = generate_dot(base_model, tokenizer, test['prompt'])
            result['base_output'] = base_output
            
            base_dot = extract_dot(base_output)
            result['base_dot'] = base_dot
            
            if base_dot:
                base_svg = output_dir / f"{test['id']}_base.svg"
                if validate_and_render_dot(base_dot, base_svg):
                    result['base_valid'] = True
                    result['base_svg'] = f"showcase/{test['id']}_base.svg"
                    print("    ✓ Valid DOT generated and rendered")
                else:
                    print("    ✗ DOT found but invalid syntax")
            else:
                print("    ✗ No DOT found in output")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        
        # Generate with fine-tuned model
        print("  Generating with fine-tuned model...")
        try:
            ft_output = generate_dot(ft_model, tokenizer, test['prompt'])
            result['ft_output'] = ft_output
            
            ft_dot = extract_dot(ft_output)
            result['ft_dot'] = ft_dot
            
            if ft_dot:
                ft_svg = output_dir / f"{test['id']}_finetuned.svg"
                if validate_and_render_dot(ft_dot, ft_svg):
                    result['ft_valid'] = True
                    result['ft_svg'] = f"showcase/{test['id']}_finetuned.svg"
                    print("    ✓ Valid DOT generated and rendered")
                else:
                    print("    ✗ DOT found but invalid syntax")
            else:
                print("    ✗ No DOT found in output")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        
        results.append(result)
    
    # Save raw results to JSON
    print("\n\nSaving raw results...")
    json_path = Path("docs/showcase_results.json")
    save_raw_results(results, json_path)
    print(f"✓ Saved raw data to: {json_path}")
    
    # Generate showcase markdown
    print("Generating showcase document...")
    showcase_md = generate_comparison_table(results)
    
    showcase_path = Path("docs/PHASE_II2.5_SHOWCASE.md")
    with open(showcase_path, 'w') as f:
        f.write(showcase_md)
    
    print(f"✓ Saved showcase to: {showcase_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    
    base_success = sum(1 for r in results if r['base_valid'])
    ft_success = sum(1 for r in results if r['ft_valid'])
    
    print(f"\nBase model:       {base_success}/{len(results)} ({100*base_success/len(results):.1f}%)")
    print(f"Fine-tuned:       {ft_success}/{len(results)} ({100*ft_success/len(results):.1f}%)")
    print(f"Improvement:      +{ft_success - base_success} examples")
    print(f"\nShowcase saved:   {showcase_path}")
    print(f"SVG graphs in:    {output_dir}/")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
