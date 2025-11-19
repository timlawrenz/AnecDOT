"""
Extract training pairs from state-machine-cat test fixtures.
"""

import json
import os
from pathlib import Path
from typing import List, Dict

def extract_state_machine_cat_pairs(repo_path: str) -> List[Dict]:
    """Extract (code, dot) pairs from state-machine-cat fixtures."""
    fixtures_dir = Path(repo_path) / "test" / "render" / "fixtures"
    
    if not fixtures_dir.exists():
        print(f"Fixtures directory not found: {fixtures_dir}")
        return []
    
    pairs = []
    smcat_files = sorted(fixtures_dir.glob("*.smcat"))
    
    for smcat_file in smcat_files:
        dot_file = smcat_file.with_suffix(".dot")
        
        if not dot_file.exists():
            continue
        
        try:
            smcat_code = smcat_file.read_text(encoding='utf-8')
            dot_code = dot_file.read_text(encoding='utf-8')
            
            # Skip empty files
            if not smcat_code.strip() or not dot_code.strip():
                continue
            
            pair = {
                "source_file": str(smcat_file.relative_to(repo_path)),
                "dot_file": str(dot_file.relative_to(repo_path)),
                "code": smcat_code,
                "dot": dot_code,
                "language": "smcat",
                "description": f"State machine from {smcat_file.name}"
            }
            pairs.append(pair)
            
        except Exception as e:
            print(f"Error processing {smcat_file.name}: {e}")
            continue
    
    return pairs

def main():
    repo_path = "repos/state-machine-cat"
    output_dir = Path("data/training/statemachine_cat")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting pairs from {repo_path}...")
    pairs = extract_state_machine_cat_pairs(repo_path)
    
    print(f"\nExtracted {len(pairs)} pairs")
    
    # Save pairs
    output_file = output_dir / "pairs.json"
    with open(output_file, 'w') as f:
        json.dump(pairs, f, indent=2)
    
    print(f"Saved to {output_file}")
    
    # Show sample
    if pairs:
        print("\n=== Sample Pair ===")
        sample = pairs[len(pairs) // 2]
        print(f"Source: {sample['source_file']}")
        print(f"\nCode ({len(sample['code'])} chars):")
        print(sample['code'][:200])
        print(f"\nDOT ({len(sample['dot'])} chars):")
        print(sample['dot'][:200])

if __name__ == "__main__":
    main()
