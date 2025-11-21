#!/usr/bin/env python3
"""
Regenerate training dataset with improved prompts (Phase II.2.6).

This script:
1. Loads all existing training pairs
2. Updates input prompts with new instruction format
3. Keeps output DOT unchanged
4. Saves to new stream files
5. Preserves metadata (sources, etc.)
"""

import json
from pathlib import Path
from typing import List, Dict
import sys

# Add training directory to path
sys.path.insert(0, str(Path(__file__).parent))
from improved_prompts_v2 import format_prompt


def load_existing_pairs() -> List[Dict]:
    """Load all existing training pairs from all sources."""
    
    data_dir = Path("data")
    pairs = []
    
    # Load from JSONL streams
    stream_files = [
        "logic-stream.jsonl",
        "documentation-stream.jsonl",
        "attribute-docs-stream.jsonl",
        "synthetic-stream.jsonl",
        "error-correction-stream.jsonl"
    ]
    
    for stream_file in stream_files:
        stream_path = data_dir / stream_file
        if not stream_path.exists():
            print(f"Skipping {stream_file} (not found)")
            continue
        
        print(f"Loading {stream_file}...")
        with open(stream_path) as f:
            for line in f:
                try:
                    pair = json.loads(line)
                    pairs.append(pair)
                except json.JSONDecodeError:
                    continue
    
    # Load from statemachine_cat pairs.json
    pairs_json = data_dir / "training/statemachine_cat/pairs.json"
    if pairs_json.exists():
        print(f"Loading {pairs_json}...")
        with open(pairs_json) as f:
            sc_data = json.load(f)
            for item in sc_data:
                pairs.append({
                    "input_text": item.get("code", ""),
                    "output_dot": item.get("dot", ""),
                    "source": "statemachine_cat",
                    "task_type": "code_to_dot"
                })
    
    print(f"\nTotal pairs loaded: {len(pairs)}")
    return pairs


def classify_task_type(pair: Dict) -> str:
    """Determine task type from pair metadata."""
    
    source = pair.get("source", "")
    
    # Error correction pairs
    if source.startswith("synthetic_error_from_"):
        return "error_correction"
    
    # Code to DOT pairs
    if source in ["statemachine_cat", "pytransitions/transitions", "Quentin18/fsmdot"]:
        return "code_to_dot"
    
    # Check if input looks like code
    input_text = pair.get("input_text", "") or ""
    if any(keyword in input_text for keyword in ["class ", "def ", "import ", "from "]):
        return "code_to_dot"
    
    # Default to natural language
    return "nl_to_dot"


def update_pair_prompts(pairs: List[Dict]) -> List[Dict]:
    """Update prompts in all pairs with new instruction format."""
    
    updated = []
    stats = {"nl_to_dot": 0, "code_to_dot": 0, "error_correction": 0}
    
    for pair in pairs:
        task_type = classify_task_type(pair)
        stats[task_type] += 1
        
        # Get original input
        original_input = pair.get("input_text", "") or ""
        
        # Skip pairs with no input
        if not original_input.strip():
            continue
        
        # Apply new prompt format
        new_input = format_prompt(original_input, task_type)
        
        # Create updated pair
        updated_pair = {
            "input_text": new_input,
            "output_dot": pair.get("output_dot", ""),
            "source": pair.get("source", "unknown"),
            "task_type": task_type
        }
        
        updated.append(updated_pair)
    
    print(f"\nTask type distribution:")
    for task_type, count in stats.items():
        print(f"  {task_type}: {count}")
    
    return updated


def save_updated_pairs(pairs: List[Dict], output_path: Path):
    """Save updated pairs to JSONL."""
    
    print(f"\nSaving {len(pairs)} pairs to {output_path}...")
    
    with open(output_path, 'w') as f:
        for pair in pairs:
            f.write(json.dumps(pair) + '\n')
    
    print(f"✓ Saved to {output_path}")


def main():
    """Main function."""
    
    print("="*70)
    print("REGENERATING TRAINING DATA WITH IMPROVED PROMPTS (Phase II.2.6)")
    print("="*70)
    print()
    
    # Load existing pairs
    pairs = load_existing_pairs()
    
    if not pairs:
        print("ERROR: No pairs loaded!")
        return
    
    # Update prompts
    updated_pairs = update_pair_prompts(pairs)
    
    # Save to new file
    output_dir = Path("data")
    output_path = output_dir / "all-pairs-v2.jsonl"
    save_updated_pairs(updated_pairs, output_path)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Original pairs: {len(pairs)}")
    print(f"Updated pairs:  {len(updated_pairs)}")
    print(f"Output file:    {output_path}")
    print("\nNext steps:")
    print("  1. Update dataset.py to use all-pairs-v2.jsonl")
    print("  2. Run training: python3 training/train.py")
    print("  3. Evaluate: python3 training/evaluate_model.py")
    print("  4. Regenerate showcase: python3 training/generate_showcase.py")
    print("="*70)


if __name__ == "__main__":
    main()
