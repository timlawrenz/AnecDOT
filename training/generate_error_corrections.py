#!/usr/bin/env python3
"""
Generate augmented dataset with error correction pairs.

Creates Phase II.2.5 dataset by:
1. Loading existing 273 training pairs
2. Generating 273 error correction pairs (1:1 ratio)
3. Creating new training stream with 546 total pairs

Expected improvement: 63% → 75-80% success rate
"""

import json
from pathlib import Path
from error_injection import augment_dataset_with_errors


def load_existing_dataset():
    """Load all existing training pairs."""
    
    data_dir = Path('data')
    stream_files = [
        'logic-stream.jsonl',
        'documentation-stream.jsonl',
        'attribute-docs-stream.jsonl',
        'synthetic-stream.jsonl',
    ]
    
    all_pairs = []
    
    for stream_file in stream_files:
        path = data_dir / stream_file
        if path.exists():
            with open(path) as f:
                for line in f:
                    try:
                        pair = json.loads(line)
                        all_pairs.append(pair)
                    except:
                        continue
    
    return all_pairs


def save_error_correction_stream(error_pairs: list, output_path: Path):
    """Save error correction pairs to JSONL."""
    
    with open(output_path, 'w') as f:
        for pair in error_pairs:
            f.write(json.dumps(pair) + '\n')
    
    print(f"✓ Saved {len(error_pairs)} pairs to {output_path}")


def generate_augmented_dataset():
    """Main function to generate augmented dataset."""
    
    print("=" * 70)
    print("PHASE II.2.5: ERROR CORRECTION DATA AUGMENTATION")
    print("=" * 70)
    
    # Load existing dataset
    print("\n1. Loading existing dataset...")
    original_pairs = load_existing_dataset()
    print(f"   Loaded {len(original_pairs)} original pairs")
    
    # Generate error correction pairs
    print("\n2. Generating error correction pairs...")
    error_pairs = augment_dataset_with_errors(
        original_pairs,
        augmentation_factor=1.0  # 1:1 ratio
    )
    
    # Save to new stream
    print("\n3. Saving error correction stream...")
    output_path = Path('data/error-correction-stream.jsonl')
    save_error_correction_stream(error_pairs, output_path)
    
    # Statistics
    print("\n" + "=" * 70)
    print("DATASET STATISTICS")
    print("=" * 70)
    print(f"Original pairs:        {len(original_pairs)}")
    print(f"Error correction:      {len(error_pairs)}")
    print(f"Total (Phase II.2.5):  {len(original_pairs) + len(error_pairs)}")
    print()
    
    # Breakdown by error type
    error_types = {}
    for pair in error_pairs:
        for error in pair.get('errors_injected', []):
            error_types[error] = error_types.get(error, 0) + 1
    
    print("Error types injected:")
    for error, count in sorted(error_types.items(), key=lambda x: -x[1]):
        print(f"  - {error}: {count}")
    
    # Sample pairs
    print("\n" + "=" * 70)
    print("SAMPLE ERROR CORRECTION PAIRS")
    print("=" * 70)
    
    for i, pair in enumerate(error_pairs[:3]):
        print(f"\nExample {i+1}:")
        print(f"Errors: {pair['errors_injected']}")
        print(f"Input (broken):")
        print(pair['broken_dot'][:200] + "..." if len(pair['broken_dot']) > 200 else pair['broken_dot'])
        print(f"\nOutput (fixed):")
        print(pair['output_dot'][:200] + "..." if len(pair['output_dot']) > 200 else pair['output_dot'])
        print("-" * 70)
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Review data/error-correction-stream.jsonl")
    print("2. Train Phase II.2.5 with 546 pairs:")
    print("   python3 training/train.py")
    print("3. Expected improvement: 63% → 75-80%")
    print()
    print("Training will use:")
    print("  - 273 original pairs (NL/Code → DOT)")
    print("  - 273 error correction pairs (Broken DOT → Fixed DOT)")
    print("  = Multi-task learning on both generation and correction")
    print("=" * 70)


if __name__ == "__main__":
    generate_augmented_dataset()
