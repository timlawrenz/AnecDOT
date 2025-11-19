#!/usr/bin/env python3
"""
Generate synthetic DOT graphs across multiple graph types.
This expands beyond just FSMs to include various graph structures.
"""

import ollama
import json
import os
import random
from pathlib import Path
from synthetic_graph_types import GRAPH_TYPES, get_prompt_for_type

def generate_synthetic_batch(
    output_dir: str = "data/synthetic_diverse",
    samples_per_type: int = 5,
    model: str = "gemma3:27b",
    temperature: float = 0.8
):
    """
    Generate synthetic graphs across all defined graph types.
    
    Args:
        output_dir: Where to save generated graphs
        samples_per_type: How many samples to generate per graph type
        model: Ollama model to use
        temperature: Generation temperature (higher = more creative)
    """
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    total_generated = 0
    failed = []
    
    for graph_type, info in GRAPH_TYPES.items():
        print(f"\n{'='*70}")
        print(f"Graph Type: {graph_type}")
        print(f"Description: {info['description']}")
        print('='*70)
        
        type_dir = output_path / graph_type
        type_dir.mkdir(exist_ok=True)
        
        patterns = info['patterns']
        
        for i in range(samples_per_type):
            # Use each pattern at least once, then repeat randomly
            if i < len(patterns):
                pattern = patterns[i]
            else:
                pattern = random.choice(patterns)
            
            print(f"\n[{i+1}/{samples_per_type}] Generating: {pattern}")
            
            try:
                prompt = get_prompt_for_type(graph_type, pattern)
                
                response = ollama.generate(
                    model=model,
                    prompt=prompt,
                    options={'temperature': temperature}
                )
                
                dot_code = response['response'].strip()
                
                # Extract DOT code if wrapped in markdown
                if '```' in dot_code:
                    parts = dot_code.split('```')
                    if len(parts) >= 2:
                        dot_code = parts[1]
                        if dot_code.startswith('dot'):
                            dot_code = dot_code[3:]
                        dot_code = dot_code.strip()
                
                # Validate it looks like DOT
                if not (dot_code.startswith('digraph') or dot_code.startswith('graph')):
                    print(f"  ⚠️  Warning: Doesn't look like DOT format")
                    failed.append({
                        'type': graph_type,
                        'pattern': pattern,
                        'reason': 'Invalid format'
                    })
                    continue
                
                # Save the graph
                filename = f"{graph_type}_{i:03d}"
                
                # Save DOT file
                dot_path = type_dir / f"{filename}.dot"
                with open(dot_path, 'w') as f:
                    f.write(dot_code)
                
                # Save metadata
                metadata = {
                    'graph_type': graph_type,
                    'pattern': pattern,
                    'description': info['description'],
                    'constraints': info['constraints'],
                    'model': model,
                    'temperature': temperature,
                    'nl_description': pattern
                }
                
                metadata_path = type_dir / f"{filename}.json"
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"  ✓ Saved to {filename}.dot ({len(dot_code)} chars)")
                total_generated += 1
                
            except Exception as e:
                print(f"  ✗ Failed: {e}")
                failed.append({
                    'type': graph_type,
                    'pattern': pattern,
                    'error': str(e)
                })
    
    # Summary
    print(f"\n{'='*70}")
    print(f"GENERATION SUMMARY")
    print('='*70)
    print(f"Total generated: {total_generated}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed generations:")
        for f in failed:
            print(f"  - {f['type']}: {f['pattern']}")
    
    # Save summary
    summary = {
        'total_generated': total_generated,
        'failed_count': len(failed),
        'failed_details': failed,
        'graph_types': list(GRAPH_TYPES.keys()),
        'samples_per_type': samples_per_type,
        'model': model
    }
    
    with open(output_path / 'generation_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary saved to {output_path / 'generation_summary.json'}")
    
    return summary


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate diverse synthetic DOT graphs")
    parser.add_argument('--output', default='data/synthetic_diverse', help='Output directory')
    parser.add_argument('--samples', type=int, default=5, help='Samples per graph type')
    parser.add_argument('--model', default='gemma3:27b', help='Ollama model to use')
    parser.add_argument('--temperature', type=float, default=0.8, help='Generation temperature')
    
    args = parser.parse_args()
    
    generate_synthetic_batch(
        output_dir=args.output,
        samples_per_type=args.samples,
        model=args.model,
        temperature=args.temperature
    )
