#!/usr/bin/env python3
"""
Quick test to verify data files are accessible and count pairs.
Run this before installing training dependencies.
"""

import json
from pathlib import Path

data_dir = Path("data")
total_pairs = 0

print("Checking AnecDOT training data...\n")

# Check pairs.json
pairs_file = data_dir / "training/statemachine_cat/pairs.json"
if pairs_file.exists():
    with open(pairs_file) as f:
        data = json.load(f)
        count = len(data)
        print(f"✓ pairs.json: {count} pairs")
        total_pairs += count
else:
    print(f"✗ pairs.json not found at {pairs_file}")

# Check JSONL streams
streams = {
    "synthetic-stream.jsonl": 0,
    "logic-stream.jsonl": 0,
    "documentation-stream.jsonl": 0,
    "attribute-docs-stream.jsonl": 0
}

for stream_name in streams:
    stream_path = data_dir / stream_name
    if stream_path.exists():
        with open(stream_path) as f:
            for line in f:
                try:
                    item = json.loads(line)
                    if "output_dot" in item or "dot" in item:
                        streams[stream_name] += 1
                except:
                    pass
        print(f"✓ {stream_name}: {streams[stream_name]} pairs")
        total_pairs += streams[stream_name]
    else:
        print(f"✗ {stream_name} not found")

print(f"\n{'='*50}")
print(f"Total training pairs available: {total_pairs}")
print(f"{'='*50}")

if total_pairs >= 150:
    print("✓ Sufficient data for training experiment")
elif total_pairs >= 100:
    print("⚠ Limited data - results may vary")
else:
    print("✗ Insufficient data - need at least 100 pairs")
