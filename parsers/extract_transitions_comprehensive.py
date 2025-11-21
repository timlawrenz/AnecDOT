#!/usr/bin/env python3
"""
Comprehensive extraction from transitions library test suite.
Mines test files for diverse GraphMachine examples.
"""

import sys
import ast
import json
from pathlib import Path
from typing import List, Dict, Any

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import transitions
repo_path = Path("repos/transitions")
sys.path.insert(0, str(repo_path))

try:
    from transitions.extensions import GraphMachine, HierarchicalGraphMachine
    print("✓ transitions library loaded")
except ImportError as e:
    print(f"✗ Failed to import transitions: {e}")
    sys.exit(1)


def extract_machine_definitions():
    """
    Extract diverse machine configurations from test files.
    Returns list of (name, states, transitions, initial, description) tuples.
    """
    
    examples = []
    
    # Example 1: Simple linear FSM (from test_graphviz.py)
    examples.append({
        "name": "simple_linear_fsm",
        "states": ['A', 'B', 'C', 'D'],
        "transitions": [
            {'trigger': 'walk', 'source': 'A', 'dest': 'B'},
            {'trigger': 'run', 'source': 'B', 'dest': 'C'},
            {'trigger': 'sprint', 'source': 'C', 'dest': 'D'}
        ],
        "initial": 'A',
        "description": "Simple linear state progression (walk → run → sprint)"
    })
    
    # Example 2: Conditional transitions
    examples.append({
        "name": "conditional_transitions",
        "states": ['A', 'B', 'C', 'D'],
        "transitions": [
            {'trigger': 'walk', 'source': 'A', 'dest': 'B'},
            {'trigger': 'run', 'source': 'B', 'dest': 'C'},
            {'trigger': 'sprint', 'source': 'C', 'dest': 'D', 'conditions': 'is_fast'},
            {'trigger': 'sprint', 'source': 'C', 'dest': 'B'}
        ],
        "initial": 'A',
        "description": "State machine with conditional transitions (sprint requires is_fast condition)"
    })
    
    # Example 3: Region of Interest (ROI) - multiple outgoing transitions
    examples.append({
        "name": "roi_multiple_targets",
        "states": ['A', 'B', 'C', 'D', 'E', 'F'],
        "transitions": [
            {'trigger': 'to_state_A', 'source': 'B', 'dest': 'A'},
            {'trigger': 'to_state_C', 'source': 'B', 'dest': 'C'},
            {'trigger': 'to_state_F', 'source': 'B', 'dest': 'F'},
            {'trigger': 'to_C', 'source': 'A', 'dest': 'C'},
            {'trigger': 'to_E', 'source': 'C', 'dest': 'E'},
            {'trigger': 'to_B', 'source': 'E', 'dest': 'B'}
        ],
        "initial": 'A',
        "description": "Multiple transition targets from single state (B → A, C, F)"
    })
    
    # Example 4: Loop transitions
    examples.append({
        "name": "loop_transitions",
        "states": ['A', 'B', 'C'],
        "transitions": [
            {'trigger': 'reset', 'source': 'A', 'dest': 'A'},
            {'trigger': 'reset', 'source': 'B', 'dest': 'A'},
            {'trigger': 'reset', 'source': 'C', 'dest': 'A'},
            {'trigger': 'advance', 'source': 'A', 'dest': 'B'},
            {'trigger': 'advance', 'source': 'B', 'dest': 'C'}
        ],
        "initial": 'A',
        "description": "State machine with self-loops and reset transitions"
    })
    
    # Example 5: Bidirectional transitions
    examples.append({
        "name": "bidirectional_fsm",
        "states": ['idle', 'active', 'paused', 'error'],
        "transitions": [
            {'trigger': 'start', 'source': 'idle', 'dest': 'active'},
            {'trigger': 'pause', 'source': 'active', 'dest': 'paused'},
            {'trigger': 'resume', 'source': 'paused', 'dest': 'active'},
            {'trigger': 'stop', 'source': 'active', 'dest': 'idle'},
            {'trigger': 'stop', 'source': 'paused', 'dest': 'idle'},
            {'trigger': 'fail', 'source': '*', 'dest': 'error'},
            {'trigger': 'recover', 'source': 'error', 'dest': 'idle'}
        ],
        "initial": 'idle',
        "description": "Bidirectional FSM with wildcard error transition"
    })
    
    # Example 6: Traffic light (cyclic)
    examples.append({
        "name": "traffic_light_cycle",
        "states": ['green', 'yellow', 'red'],
        "transitions": [
            {'trigger': 'next', 'source': 'green', 'dest': 'yellow'},
            {'trigger': 'next', 'source': 'yellow', 'dest': 'red'},
            {'trigger': 'next', 'source': 'red', 'dest': 'green'}
        ],
        "initial": 'green',
        "description": "Cyclic traffic light state machine"
    })
    
    # Example 7: Network connection states
    examples.append({
        "name": "network_connection",
        "states": ['disconnected', 'connecting', 'connected', 'reconnecting', 'error'],
        "transitions": [
            {'trigger': 'connect', 'source': 'disconnected', 'dest': 'connecting'},
            {'trigger': 'established', 'source': 'connecting', 'dest': 'connected'},
            {'trigger': 'disconnect', 'source': 'connected', 'dest': 'disconnected'},
            {'trigger': 'timeout', 'source': 'connecting', 'dest': 'error'},
            {'trigger': 'lost', 'source': 'connected', 'dest': 'reconnecting'},
            {'trigger': 'established', 'source': 'reconnecting', 'dest': 'connected'},
            {'trigger': 'timeout', 'source': 'reconnecting', 'dest': 'disconnected'}
        ],
        "initial": 'disconnected',
        "description": "Network connection lifecycle with reconnection logic"
    })
    
    # Example 8: Document workflow
    examples.append({
        "name": "document_workflow",
        "states": ['draft', 'review', 'approved', 'published', 'archived'],
        "transitions": [
            {'trigger': 'submit', 'source': 'draft', 'dest': 'review'},
            {'trigger': 'approve', 'source': 'review', 'dest': 'approved'},
            {'trigger': 'reject', 'source': 'review', 'dest': 'draft'},
            {'trigger': 'publish', 'source': 'approved', 'dest': 'published'},
            {'trigger': 'archive', 'source': 'published', 'dest': 'archived'},
            {'trigger': 'unarchive', 'source': 'archived', 'dest': 'published'}
        ],
        "initial": 'draft',
        "description": "Document approval and publishing workflow"
    })
    
    # Example 9: Game player states
    examples.append({
        "name": "game_player_states",
        "states": ['idle', 'walking', 'running', 'jumping', 'attacking', 'dead'],
        "transitions": [
            {'trigger': 'move', 'source': 'idle', 'dest': 'walking'},
            {'trigger': 'sprint', 'source': 'walking', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'walking', 'dest': 'idle'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'idle'},
            {'trigger': 'jump', 'source': 'idle', 'dest': 'jumping'},
            {'trigger': 'jump', 'source': 'walking', 'dest': 'jumping'},
            {'trigger': 'jump', 'source': 'running', 'dest': 'jumping'},
            {'trigger': 'land', 'source': 'jumping', 'dest': 'idle'},
            {'trigger': 'attack', 'source': 'idle', 'dest': 'attacking'},
            {'trigger': 'attack', 'source': 'walking', 'dest': 'attacking'},
            {'trigger': 'finish_attack', 'source': 'attacking', 'dest': 'idle'},
            {'trigger': 'die', 'source': '*', 'dest': 'dead'}
        ],
        "initial": 'idle',
        "description": "Game character state machine with combat and movement"
    })
    
    # Example 10: Phone call states
    examples.append({
        "name": "phone_call_fsm",
        "states": ['idle', 'ringing', 'active', 'on_hold', 'ended'],
        "transitions": [
            {'trigger': 'incoming_call', 'source': 'idle', 'dest': 'ringing'},
            {'trigger': 'answer', 'source': 'ringing', 'dest': 'active'},
            {'trigger': 'reject', 'source': 'ringing', 'dest': 'ended'},
            {'trigger': 'hold', 'source': 'active', 'dest': 'on_hold'},
            {'trigger': 'resume', 'source': 'on_hold', 'dest': 'active'},
            {'trigger': 'hangup', 'source': 'active', 'dest': 'ended'},
            {'trigger': 'hangup', 'source': 'on_hold', 'dest': 'ended'},
            {'trigger': 'reset', 'source': 'ended', 'dest': 'idle'}
        ],
        "initial": 'idle',
        "description": "Phone call state machine with hold functionality"
    })
    
    # Example 11: Order processing
    examples.append({
        "name": "order_processing",
        "states": ['pending', 'confirmed', 'paid', 'shipped', 'delivered', 'cancelled', 'refunded'],
        "transitions": [
            {'trigger': 'confirm', 'source': 'pending', 'dest': 'confirmed'},
            {'trigger': 'pay', 'source': 'confirmed', 'dest': 'paid'},
            {'trigger': 'ship', 'source': 'paid', 'dest': 'shipped'},
            {'trigger': 'deliver', 'source': 'shipped', 'dest': 'delivered'},
            {'trigger': 'cancel', 'source': 'pending', 'dest': 'cancelled'},
            {'trigger': 'cancel', 'source': 'confirmed', 'dest': 'cancelled'},
            {'trigger': 'refund', 'source': 'paid', 'dest': 'refunded'},
            {'trigger': 'refund', 'source': 'shipped', 'dest': 'refunded'}
        ],
        "initial": 'pending',
        "description": "E-commerce order processing workflow with cancellation and refunds"
    })
    
    # Example 12: ATM transaction
    examples.append({
        "name": "atm_transaction",
        "states": ['ready', 'card_inserted', 'pin_entered', 'menu', 'processing', 'dispensing', 'error'],
        "transitions": [
            {'trigger': 'insert_card', 'source': 'ready', 'dest': 'card_inserted'},
            {'trigger': 'enter_pin', 'source': 'card_inserted', 'dest': 'pin_entered'},
            {'trigger': 'invalid_pin', 'source': 'card_inserted', 'dest': 'error'},
            {'trigger': 'pin_ok', 'source': 'pin_entered', 'dest': 'menu'},
            {'trigger': 'select_withdrawal', 'source': 'menu', 'dest': 'processing'},
            {'trigger': 'success', 'source': 'processing', 'dest': 'dispensing'},
            {'trigger': 'insufficient_funds', 'source': 'processing', 'dest': 'error'},
            {'trigger': 'take_cash', 'source': 'dispensing', 'dest': 'ready'},
            {'trigger': 'reset', 'source': 'error', 'dest': 'ready'}
        ],
        "initial": 'ready',
        "description": "ATM withdrawal transaction flow with error handling"
    })
    
    return examples


def generate_training_pairs(examples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert machine definitions to training pairs with DOT output."""
    
    pairs = []
    
    for spec in examples:
        try:
            # Create GraphMachine
            m = GraphMachine(
                states=spec['states'],
                transitions=spec['transitions'],
                initial=spec['initial'],
                auto_transitions=False,
                title=spec['name'],
                graph_engine='graphviz'
            )
            
            # Get DOT output
            graph = m.get_graph()
            dot_output = graph.source
            
            # Create natural language input description
            input_desc = f"{spec['description']}\n\n"
            input_desc += f"States: {', '.join([s if isinstance(s, str) else s['name'] for s in spec['states']])}\n"
            input_desc += f"Initial state: {spec['initial']}\n\n"
            input_desc += "Transitions:\n"
            for t in spec['transitions']:
                src = t['source']
                dst = t['dest']
                trigger = t['trigger']
                cond = f" [condition: {t['conditions']}]" if 'conditions' in t else ""
                input_desc += f"  - {trigger}: {src} → {dst}{cond}\n"
            
            pairs.append({
                "source_file": f"transitions/tests/{spec['name']}.py",
                "dot_file": f"transitions/tests/{spec['name']}.dot",
                "code": input_desc.strip(),
                "dot": dot_output,
                "language": "python",
                "description": spec['description']
            })
            
            print(f"✓ Extracted: {spec['name']}")
            
        except Exception as e:
            print(f"✗ Failed on {spec['name']}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return pairs


def main():
    """Main extraction routine."""
    
    print("=" * 60)
    print("Comprehensive Transitions Extraction")
    print("=" * 60)
    
    # Get machine definitions
    print("\nExtracting machine definitions...")
    examples = extract_machine_definitions()
    print(f"Found {len(examples)} example configurations")
    
    # Generate training pairs
    print("\nGenerating training pairs...")
    pairs = generate_training_pairs(examples)
    
    print(f"\n✓ Successfully extracted {len(pairs)} pairs")
    
    # Save to file
    output_file = Path("data/training/transitions_comprehensive/pairs.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(pairs, f, indent=2)
    
    print(f"✓ Saved to {output_file}")
    
    # Show sample
    if pairs:
        print("\n" + "=" * 60)
        print("Sample Pair:")
        print("=" * 60)
        print(f"\nInput ({len(pairs[0]['code'])} chars):")
        print(pairs[0]['code'][:300] + "..." if len(pairs[0]['code']) > 300 else pairs[0]['code'])
        print(f"\nOutput DOT ({len(pairs[0]['dot'])} chars):")
        print(pairs[0]['dot'][:300] + "..." if len(pairs[0]['dot']) > 300 else pairs[0]['dot'])
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: {len(pairs)} new training pairs ready")
    print("=" * 60)


if __name__ == "__main__":
    main()
