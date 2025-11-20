#!/usr/bin/env python3
"""
Extract FSM pairs from transitions library.
Finds state machine definitions and their DOT graph outputs.
"""

import sys
import subprocess
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Clone and extract from transitions
repo_path = Path("repos/transitions")

# Check if transitions is importable
try:
    sys.path.insert(0, str(repo_path))
    from transitions.extensions import GraphMachine
    import tempfile
    import json
    print("✓ transitions library loaded successfully")
except ImportError as e:
    print(f"✗ Failed to import transitions: {e}")
    print("  Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "graphviz"], check=False)
    from transitions.extensions import GraphMachine
    print("✓ dependencies installed")

# Test cases to extract
test_machines = [
    {
        "name": "simple_fsm",
        "states": ['A', 'B', 'C', 'D'],
        "transitions": [
            {'trigger': 'walk', 'source': 'A', 'dest': 'B'},
            {'trigger': 'run', 'source': 'B', 'dest': 'C'},
            {'trigger': 'sprint', 'source': 'C', 'dest': 'D'}
        ],
        "initial": 'A'
    },
    {
        "name": "conditional_fsm",
        "states": ['A', 'B', 'C'],
        "transitions": [
            {'trigger': 'go', 'source': 'A', 'dest': 'B', 'conditions': ['is_ready']},
            {'trigger': 'go', 'source': 'A', 'dest': 'C'},
            {'trigger': 'back', 'source': 'B', 'dest': 'A'},
            {'trigger': 'back', 'source': 'C', 'dest': 'A'}
        ],
        "initial": 'A'
    },
    {
        "name": "traffic_light",
        "states": ['green', 'yellow', 'red'],
        "transitions": [
            {'trigger': 'slow_down', 'source': 'green', 'dest': 'yellow'},
            {'trigger': 'stop', 'source': 'yellow', 'dest': 'red'},
            {'trigger': 'go', 'source': 'red', 'dest': 'green'}
        ],
        "initial": 'green'
    },
    {
        "name": "door_controller",
        "states": ['closed', 'opening', 'open', 'closing'],
        "transitions": [
            {'trigger': 'open_button', 'source': 'closed', 'dest': 'opening'},
            {'trigger': 'opened', 'source': 'opening', 'dest': 'open'},
            {'trigger': 'close_button', 'source': 'open', 'dest': 'closing'},
            {'trigger': 'closed_complete', 'source': 'closing', 'dest': 'closed'}
        ],
        "initial": 'closed'
    }
]

pairs = []

for spec in test_machines:
    try:
        # Create machine with graphviz engine explicitly
        m = GraphMachine(
            states=spec['states'],
            transitions=spec['transitions'],
            initial=spec['initial'],
            auto_transitions=False,
            title=spec['name'],
            graph_engine='graphviz'  # Force graphviz, not mermaid
        )
        
        # Get DOT graph
        graph = m.get_graph()
        dot_output = graph.source
        
        # Create input description
        input_desc = f"State machine: {spec['name']}\n"
        input_desc += f"States: {', '.join(spec['states'])}\n"
        input_desc += "Transitions:\n"
        for t in spec['transitions']:
            cond = f" [condition: {t['conditions']}]" if 'conditions' in t else ""
            input_desc += f"  - {t['trigger']}: {t['source']} → {t['dest']}{cond}\n"
        input_desc += f"Initial state: {spec['initial']}"
        
        pairs.append({
            "source_file": f"transitions/{spec['name']}.py",
            "dot_file": f"transitions/{spec['name']}.dot",
            "code": input_desc,
            "dot": dot_output,
            "language": "python",
            "description": f"transitions FSM: {spec['name']}"
        })
        
        print(f"✓ Extracted: {spec['name']}")
        
    except Exception as e:
        print(f"✗ Failed on {spec['name']}: {e}")
        continue

print(f"\n✓ Extracted {len(pairs)} pairs from transitions")

# Save pairs
output_file = Path("data/training/transitions/pairs.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(pairs, f, indent=2)

print(f"✓ Saved to {output_file}")
print(f"\nSample pair:")
print(f"Input: {pairs[0]['code'][:100]}...")
print(f"Output: {pairs[0]['dot'][:100]}...")
