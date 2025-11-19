"""
Batch extract training pairs from automata library test files.
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, 'data/raw/automata-caleb531')

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

# Collection of example automata from the test suite
EXAMPLE_AUTOMATA = []

# DFA examples from test_dfa.py
EXAMPLE_AUTOMATA.append({
    'name': 'simple_dfa',
    'description': 'DFA that accepts strings with odd number of 1s',
    'automaton': DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q0', '1': 'q2'},
            'q2': {'0': 'q2', '1': 'q1'}
        },
        initial_state='q0',
        final_states={'q1'}
    ),
    'code': '''DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)'''
})

EXAMPLE_AUTOMATA.append({
    'name': 'binary_multiples_dfa',
    'description': 'DFA that accepts binary strings divisible by 3',
    'automaton': DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q2', '1': 'q0'},
            'q2': {'0': 'q1', '1': 'q2'}
        },
        initial_state='q0',
        final_states={'q0'}
    ),
    'code': '''DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q2', '1': 'q0'},
        'q2': {'0': 'q1', '1': 'q2'}
    },
    initial_state='q0',
    final_states={'q0'}
)'''
})

EXAMPLE_AUTOMATA.append({
    'name': 'starts_with_zero',
    'description': 'DFA that accepts strings starting with 0',
    'automaton': DFA(
        states={'start', 'zero', 'one', 'dead'},
        input_symbols={'0', '1'},
        transitions={
            'start': {'0': 'zero', '1': 'one'},
            'zero': {'0': 'zero', '1': 'zero'},
            'one': {'0': 'one', '1': 'one'},
            'dead': {'0': 'dead', '1': 'dead'}
        },
        initial_state='start',
        final_states={'zero'}
    ),
    'code': '''DFA(
    states={'start', 'zero', 'one', 'dead'},
    input_symbols={'0', '1'},
    transitions={
        'start': {'0': 'zero', '1': 'one'},
        'zero': {'0': 'zero', '1': 'zero'},
        'one': {'0': 'one', '1': 'one'},
        'dead': {'0': 'dead', '1': 'dead'}
    },
    initial_state='start',
    final_states={'zero'}
)'''
})

EXAMPLE_AUTOMATA.append({
    'name': 'ends_with_one',
    'description': 'DFA that accepts strings ending with 1',
    'automaton': DFA(
        states={'s0', 's1'},
        input_symbols={'0', '1'},
        transitions={
            's0': {'0': 's0', '1': 's1'},
            's1': {'0': 's0', '1': 's1'}
        },
        initial_state='s0',
        final_states={'s1'}
    ),
    'code': '''DFA(
    states={'s0', 's1'},
    input_symbols={'0', '1'},
    transitions={
        's0': {'0': 's0', '1': 's1'},
        's1': {'0': 's0', '1': 's1'}
    },
    initial_state='s0',
    final_states={'s1'}
)'''
})

EXAMPLE_AUTOMATA.append({
    'name': 'contains_substring_01',
    'description': 'DFA that accepts strings containing substring 01',
    'automaton': DFA(
        states={'start', 'seen0', 'seen01'},
        input_symbols={'0', '1'},
        transitions={
            'start': {'0': 'seen0', '1': 'start'},
            'seen0': {'0': 'seen0', '1': 'seen01'},
            'seen01': {'0': 'seen01', '1': 'seen01'}
        },
        initial_state='start',
        final_states={'seen01'}
    ),
    'code': '''DFA(
    states={'start', 'seen0', 'seen01'},
    input_symbols={'0', '1'},
    transitions={
        'start': {'0': 'seen0', '1': 'start'},
        'seen0': {'0': 'seen0', '1': 'seen01'},
        'seen01': {'0': 'seen01', '1': 'seen01'}
    },
    initial_state='start',
    final_states={'seen01'}
)'''
})

# NFA examples
EXAMPLE_AUTOMATA.append({
    'name': 'simple_nfa',
    'description': 'NFA that accepts strings with second to last symbol being 1',
    'automaton': NFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': {'q0'}, '1': {'q0', 'q1'}},
            'q1': {'0': {'q2'}, '1': {'q2'}},
            'q2': {}
        },
        initial_state='q0',
        final_states={'q2'}
    ),
    'code': '''NFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': {'q0'}, '1': {'q0', 'q1'}},
        'q1': {'0': {'q2'}, '1': {'q2'}},
        'q2': {}
    },
    initial_state='q0',
    final_states={'q2'}
)'''
})

EXAMPLE_AUTOMATA.append({
    'name': 'nfa_with_epsilon',
    'description': 'NFA with epsilon transitions',
    'automaton': NFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': {'q1'}, '': {'q2'}},
            'q1': {'a': {'q1'}, 'b': {'q2'}},
            'q2': {}
        },
        initial_state='q0',
        final_states={'q2'}
    ),
    'code': '''NFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': {'q1'}, '': {'q2'}},
        'q1': {'a': {'q1'}, 'b': {'q2'}},
        'q2': {}
    },
    initial_state='q0',
    final_states={'q2'}
)'''
})

def extract_all():
    """Extract all training pairs."""
    pairs_code = []
    pairs_nl = []
    
    for example in EXAMPLE_AUTOMATA:
        try:
            # Generate DOT
            graph = example['automaton'].show_diagram()
            dot = graph.to_string()
            
            # Create code->dot pair
            pairs_code.append({
                'input': example['code'],
                'output': dot,
                'metadata': {
                    'source': 'automata-caleb531',
                    'type': 'code_to_dot',
                    'name': example['name']
                }
            })
            
            # Create nl->dot pair
            pairs_nl.append({
                'input': example['description'],
                'output': dot,
                'metadata': {
                    'source': 'automata-caleb531',
                    'type': 'nl_to_dot',
                    'name': example['name']
                }
            })
            
            print(f"✓ Extracted: {example['name']}")
            
        except Exception as e:
            print(f"✗ Failed {example['name']}: {e}")
    
    return pairs_code, pairs_nl

if __name__ == '__main__':
    print("Extracting automata library examples...\n")
    
    pairs_code, pairs_nl = extract_all()
    
    print(f"\n{'='*50}")
    print(f"Extracted {len(pairs_code)} code->dot pairs")
    print(f"Extracted {len(pairs_nl)} nl->dot pairs")
    print(f"Total: {len(pairs_code) + len(pairs_nl)} pairs")
    
    # Append to streams
    output_dir = Path('data')
    
    with open(output_dir / 'logic-stream.jsonl', 'a') as f:
        for pair in pairs_code:
            f.write(json.dumps(pair) + '\n')
    
    with open(output_dir / 'documentation-stream.jsonl', 'a') as f:
        for pair in pairs_nl:
            f.write(json.dumps(pair) + '\n')
    
    print(f"\nAppended to data streams")
    print(f"  logic-stream.jsonl: +{len(pairs_code)} pairs")
    print(f"  documentation-stream.jsonl: +{len(pairs_nl)} pairs")
