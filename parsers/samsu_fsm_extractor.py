#!/usr/bin/env python3
"""
Extractor for Samsu-F/finite_state_machines repository.
Extracts FSM definitions and generates DOT diagrams.
"""

import sys
from pathlib import Path

# Add the repo to path
sys.path.insert(0, "/tmp/finite_state_machines")

from fsm import Fsm

# Descriptions for each example
DESCRIPTIONS = {
    "divisible_by_4.fsm": "Finite state machine accepting decimal numbers divisible by 4",
    "even_binary.fsm": "Finite state machine accepting binary numbers with even number of ones",
    "even_number_of_ones.fsm": "Finite state machine accepting strings with even number of ones",
    "sorted_0-3.fsm": "Finite state machine accepting sorted sequences of digits 0-3",
    "sorted_0-3_fully_defined.fsm": "Finite state machine accepting sorted sequences of digits 0-3 (fully defined)",
    "sorted_0-3_fully_defined_wildcard.fsm": "Finite state machine accepting sorted sequences of digits 0-3 (with wildcards)",
    "sorted.fsm": "Finite state machine accepting sorted sequences",
    "sorted_fully_defined.fsm": "Finite state machine accepting sorted sequences (fully defined)",
    "suffix_00.fsm": "Finite state machine accepting strings ending with '00'",
}

output_dir = Path("/home/tim/source/activity/AnecDOT/data/raw/samsu_fsm_extraction")
output_dir.mkdir(parents=True, exist_ok=True)

example_dir = Path("/tmp/finite_state_machines/example_files")

extracted_count = 0

for fsm_file in sorted(example_dir.glob("*.fsm")):
    try:
        print(f"Processing {fsm_file.name}...")
        
        # Load the FSM
        fsm = Fsm(str(fsm_file))
        
        # Create output directory for this example
        example_name = fsm_file.stem
        pair_dir = output_dir / example_name
        pair_dir.mkdir(exist_ok=True)
        
        # Save description
        description = DESCRIPTIONS.get(fsm_file.name, f"Finite state machine from {fsm_file.name}")
        (pair_dir / "description.txt").write_text(description)
        
        # Save original FSM file as code
        (pair_dir / "code.fsm").write_text(fsm_file.read_text())
        
        # Generate and save DOT
        dot_content = fsm.to_dot(name=example_name)
        (pair_dir / "diagram.dot").write_text(dot_content)
        
        # Save metadata
        metadata = f"""Source: Samsu-F/finite_state_machines
File: {fsm_file.name}
Description: {description}
Type: Deterministic Finite Automaton
States: {len(fsm.states)}
"""
        (pair_dir / "metadata.txt").write_text(metadata)
        
        print(f"  ✓ Saved {example_name} ({len(fsm.states)} states)")
        extracted_count += 1
        
    except Exception as e:
        print(f"  ✗ Failed to process {fsm_file.name}: {e}")
        continue

print(f"\n{'='*70}")
print(f"Extracted {extracted_count} pairs from Samsu-F/finite_state_machines")
print(f"{'='*70}")
