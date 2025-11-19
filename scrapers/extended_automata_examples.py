"""
Extended automata examples for training data.
Add 50+ more diverse DFA/NFA examples.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, 'data/raw/automata-caleb531')

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

examples_code = []
examples_nl = []

def add_example(name, description, automaton, code):
    """Add both code and NL pairs for an automaton."""
    try:
        graph = automaton.show_diagram()
        dot = graph.to_string()
        
        examples_code.append({
            'input': code,
            'output': dot,
            'metadata': {'source': 'automata-extended', 'name': name, 'type': 'code_to_dot'}
        })
        
        examples_nl.append({
            'input': description,
            'output': dot,
            'metadata': {'source': 'automata-extended', 'name': name, 'type': 'nl_to_dot'}
        })
        
        print(f"✓ {name}")
        return True
    except Exception as e:
        print(f"✗ {name}: {e}")
        return False

# Simple pattern recognition DFAs
add_example(
    'even_zeros',
    'DFA accepting strings with even number of 0s',
    DFA(
        states={'even', 'odd'},
        input_symbols={'0', '1'},
        transitions={
            'even': {'0': 'odd', '1': 'even'},
            'odd': {'0': 'even', '1': 'odd'}
        },
        initial_state='even',
        final_states={'even'}
    ),
    "DFA(states={'even', 'odd'}, input_symbols={'0', '1'}, transitions={'even': {'0': 'odd', '1': 'even'}, 'odd': {'0': 'even', '1': 'odd'}}, initial_state='even', final_states={'even'})"
)

add_example(
    'even_ones',
    'DFA accepting strings with even number of 1s',
    DFA(
        states={'s0', 's1'},
        input_symbols={'0', '1'},
        transitions={
            's0': {'0': 's0', '1': 's1'},
            's1': {'0': 's1', '1': 's0'}
        },
        initial_state='s0',
        final_states={'s0'}
    ),
    "DFA(states={'s0', 's1'}, input_symbols={'0', '1'}, transitions={'s0': {'0': 's0', '1': 's1'}, 's1': {'0': 's1', '1': 's0'}}, initial_state='s0', final_states={'s0'})"
)

add_example(
    'starts_and_ends_same',
    'DFA accepting strings starting and ending with same symbol',
    DFA(
        states={'start', 'saw0', 'saw1', 'end0', 'end1'},
        input_symbols={'0', '1'},
        transitions={
            'start': {'0': 'saw0', '1': 'saw1'},
            'saw0': {'0': 'saw0', '1': 'saw0'},
            'saw1': {'0': 'saw1', '1': 'saw1'},
            'end0': {'0': 'end0', '1': 'end0'},
            'end1': {'0': 'end1', '1': 'end1'}
        },
        initial_state='start',
        final_states={'saw0', 'saw1'}
    ),
    "DFA(states={'start', 'saw0', 'saw1', 'end0', 'end1'}, input_symbols={'0', '1'}, transitions={'start': {'0': 'saw0', '1': 'saw1'}, 'saw0': {'0': 'saw0', '1': 'saw0'}, 'saw1': {'0': 'saw1', '1': 'saw1'}, 'end0': {'0': 'end0', '1': 'end0'}, 'end1': {'0': 'end1', '1': 'end1'}}, initial_state='start', final_states={'saw0', 'saw1'})"
)

add_example(
    'length_mod_3',
    'DFA accepting strings whose length is divisible by 3',
    DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': 'q1', 'b': 'q1'},
            'q1': {'a': 'q2', 'b': 'q2'},
            'q2': {'a': 'q0', 'b': 'q0'}
        },
        initial_state='q0',
        final_states={'q0'}
    ),
    "DFA(states={'q0', 'q1', 'q2'}, input_symbols={'a', 'b'}, transitions={'q0': {'a': 'q1', 'b': 'q1'}, 'q1': {'a': 'q2', 'b': 'q2'}, 'q2': {'a': 'q0', 'b': 'q0'}}, initial_state='q0', final_states={'q0'})"
)

add_example(
    'contains_01_or_10',
    'DFA accepting strings containing 01 or 10 as substring',
    DFA(
        states={'start', 'saw0', 'saw1', 'accept'},
        input_symbols={'0', '1'},
        transitions={
            'start': {'0': 'saw0', '1': 'saw1'},
            'saw0': {'0': 'saw0', '1': 'accept'},
            'saw1': {'0': 'accept', '1': 'saw1'},
            'accept': {'0': 'accept', '1': 'accept'}
        },
        initial_state='start',
        final_states={'accept'}
    ),
    "DFA(states={'start', 'saw0', 'saw1', 'accept'}, input_symbols={'0', '1'}, transitions={'start': {'0': 'saw0', '1': 'saw1'}, 'saw0': {'0': 'saw0', '1': 'accept'}, 'saw1': {'0': 'accept', '1': 'saw1'}, 'accept': {'0': 'accept', '1': 'accept'}}, initial_state='start', final_states={'accept'})"
)

add_example(
    'three_consecutive_ones',
    'DFA accepting strings with at least three consecutive 1s',
    DFA(
        states={'q0', 'q1', 'q2', 'q3'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q0', '1': 'q2'},
            'q2': {'0': 'q0', '1': 'q3'},
            'q3': {'0': 'q3', '1': 'q3'}
        },
        initial_state='q0',
        final_states={'q3'}
    ),
    "DFA(states={'q0', 'q1', 'q2', 'q3'}, input_symbols={'0', '1'}, transitions={'q0': {'0': 'q0', '1': 'q1'}, 'q1': {'0': 'q0', '1': 'q2'}, 'q2': {'0': 'q0', '1': 'q3'}, 'q3': {'0': 'q3', '1': 'q3'}}, initial_state='q0', final_states={'q3'})"
)

add_example(
    'no_consecutive_zeros',
    'DFA accepting strings with no two consecutive 0s',
    DFA(
        states={'ok', 'saw0', 'reject'},
        input_symbols={'0', '1'},
        transitions={
            'ok': {'0': 'saw0', '1': 'ok'},
            'saw0': {'0': 'reject', '1': 'ok'},
            'reject': {'0': 'reject', '1': 'reject'}
        },
        initial_state='ok',
        final_states={'ok', 'saw0'}
    ),
    "DFA(states={'ok', 'saw0', 'reject'}, input_symbols={'0', '1'}, transitions={'ok': {'0': 'saw0', '1': 'ok'}, 'saw0': {'0': 'reject', '1': 'ok'}, 'reject': {'0': 'reject', '1': 'reject'}}, initial_state='ok', final_states={'ok', 'saw0'})"
)

add_example(
    'alternate_01',
    'DFA accepting alternating 01 patterns',
    DFA(
        states={'start', 'saw0', 'saw01', 'reject'},
        input_symbols={'0', '1'},
        transitions={
            'start': {'0': 'saw0', '1': 'reject'},
            'saw0': {'0': 'reject', '1': 'saw01'},
            'saw01': {'0': 'saw0', '1': 'reject'},
            'reject': {'0': 'reject', '1': 'reject'}
        },
        initial_state='start',
        final_states={'saw01'}
    ),
    "DFA(states={'start', 'saw0', 'saw01', 'reject'}, input_symbols={'0', '1'}, transitions={'start': {'0': 'saw0', '1': 'reject'}, 'saw0': {'0': 'reject', '1': 'saw01'}, 'saw01': {'0': 'saw0', '1': 'reject'}, 'reject': {'0': 'reject', '1': 'reject'}}, initial_state='start', final_states={'saw01'})"
)

add_example(
    'exactly_two_ones',
    'DFA accepting strings with exactly two 1s',
    DFA(
        states={'zero', 'one', 'two', 'more'},
        input_symbols={'0', '1'},
        transitions={
            'zero': {'0': 'zero', '1': 'one'},
            'one': {'0': 'one', '1': 'two'},
            'two': {'0': 'two', '1': 'more'},
            'more': {'0': 'more', '1': 'more'}
        },
        initial_state='zero',
        final_states={'two'}
    ),
    "DFA(states={'zero', 'one', 'two', 'more'}, input_symbols={'0', '1'}, transitions={'zero': {'0': 'zero', '1': 'one'}, 'one': {'0': 'one', '1': 'two'}, 'two': {'0': 'two', '1': 'more'}, 'more': {'0': 'more', '1': 'more'}}, initial_state='zero', final_states={'two'})"
)

add_example(
    'at_least_two_ones',
    'DFA accepting strings with at least two 1s',
    DFA(
        states={'zero', 'one', 'two_plus'},
        input_symbols={'0', '1'},
        transitions={
            'zero': {'0': 'zero', '1': 'one'},
            'one': {'0': 'one', '1': 'two_plus'},
            'two_plus': {'0': 'two_plus', '1': 'two_plus'}
        },
        initial_state='zero',
        final_states={'two_plus'}
    ),
    "DFA(states={'zero', 'one', 'two_plus'}, input_symbols={'0', '1'}, transitions={'zero': {'0': 'zero', '1': 'one'}, 'one': {'0': 'one', '1': 'two_plus'}, 'two_plus': {'0': 'two_plus', '1': 'two_plus'}}, initial_state='zero', final_states={'two_plus'})"
)

# Alphabet-based DFAs
add_example(
    'contains_abc',
    'DFA accepting strings containing abc as substring',
    DFA(
        states={'start', 'a', 'ab', 'abc'},
        input_symbols={'a', 'b', 'c'},
        transitions={
            'start': {'a': 'a', 'b': 'start', 'c': 'start'},
            'a': {'a': 'a', 'b': 'ab', 'c': 'start'},
            'ab': {'a': 'a', 'b': 'start', 'c': 'abc'},
            'abc': {'a': 'abc', 'b': 'abc', 'c': 'abc'}
        },
        initial_state='start',
        final_states={'abc'}
    ),
    "DFA(states={'start', 'a', 'ab', 'abc'}, input_symbols={'a', 'b', 'c'}, transitions={'start': {'a': 'a', 'b': 'start', 'c': 'start'}, 'a': {'a': 'a', 'b': 'ab', 'c': 'start'}, 'ab': {'a': 'a', 'b': 'start', 'c': 'abc'}, 'abc': {'a': 'abc', 'b': 'abc', 'c': 'abc'}}, initial_state='start', final_states={'abc'})"
)

add_example(
    'ends_with_ab',
    'DFA accepting strings ending with ab',
    DFA(
        states={'start', 'a', 'ab'},
        input_symbols={'a', 'b'},
        transitions={
            'start': {'a': 'a', 'b': 'start'},
            'a': {'a': 'a', 'b': 'ab'},
            'ab': {'a': 'a', 'b': 'start'}
        },
        initial_state='start',
        final_states={'ab'}
    ),
    "DFA(states={'start', 'a', 'ab'}, input_symbols={'a', 'b'}, transitions={'start': {'a': 'a', 'b': 'start'}, 'a': {'a': 'a', 'b': 'ab'}, 'ab': {'a': 'a', 'b': 'start'}}, initial_state='start', final_states={'ab'})"
)

add_example(
    'starts_with_ab',
    'DFA accepting strings starting with ab',
    DFA(
        states={'start', 'a', 'ab', 'other'},
        input_symbols={'a', 'b'},
        transitions={
            'start': {'a': 'a', 'b': 'other'},
            'a': {'a': 'other', 'b': 'ab'},
            'ab': {'a': 'ab', 'b': 'ab'},
            'other': {'a': 'other', 'b': 'other'}
        },
        initial_state='start',
        final_states={'ab'}
    ),
    "DFA(states={'start', 'a', 'ab', 'other'}, input_symbols={'a', 'b'}, transitions={'start': {'a': 'a', 'b': 'other'}, 'a': {'a': 'other', 'b': 'ab'}, 'ab': {'a': 'ab', 'b': 'ab'}, 'other': {'a': 'other', 'b': 'other'}}, initial_state='start', final_states={'ab'})"
)

add_example(
    'third_symbol_is_a',
    'DFA accepting strings where third symbol is a',
    DFA(
        states={'s0', 's1', 's2', 'accept', 'reject'},
        input_symbols={'a', 'b'},
        transitions={
            's0': {'a': 's1', 'b': 's1'},
            's1': {'a': 's2', 'b': 's2'},
            's2': {'a': 'accept', 'b': 'reject'},
            'accept': {'a': 'accept', 'b': 'accept'},
            'reject': {'a': 'reject', 'b': 'reject'}
        },
        initial_state='s0',
        final_states={'accept'}
    ),
    "DFA(states={'s0', 's1', 's2', 'accept', 'reject'}, input_symbols={'a', 'b'}, transitions={'s0': {'a': 's1', 'b': 's1'}, 's1': {'a': 's2', 'b': 's2'}, 's2': {'a': 'accept', 'b': 'reject'}, 'accept': {'a': 'accept', 'b': 'accept'}, 'reject': {'a': 'reject', 'b': 'reject'}}, initial_state='s0', final_states={'accept'})"
)

# NFAs
add_example(
    'nfa_ends_with_01',
    'NFA accepting strings ending with 01',
    NFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
            'q1': {'1': {'q2'}},
            'q2': {}
        },
        initial_state='q0',
        final_states={'q2'}
    ),
    "NFA(states={'q0', 'q1', 'q2'}, input_symbols={'0', '1'}, transitions={'q0': {'0': {'q0', 'q1'}, '1': {'q0'}}, 'q1': {'1': {'q2'}}, 'q2': {}}, initial_state='q0', final_states={'q2'})"
)

add_example(
    'nfa_third_from_end_is_1',
    'NFA accepting strings where third symbol from end is 1',
    NFA(
        states={'q0', 'q1', 'q2', 'q3'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': {'q0'}, '1': {'q0', 'q1'}},
            'q1': {'0': {'q2'}, '1': {'q2'}},
            'q2': {'0': {'q3'}, '1': {'q3'}},
            'q3': {}
        },
        initial_state='q0',
        final_states={'q3'}
    ),
    "NFA(states={'q0', 'q1', 'q2', 'q3'}, input_symbols={'0', '1'}, transitions={'q0': {'0': {'q0'}, '1': {'q0', 'q1'}}, 'q1': {'0': {'q2'}, '1': {'q2'}}, 'q2': {'0': {'q3'}, '1': {'q3'}}, 'q3': {}}, initial_state='q0', final_states={'q3'})"
)

add_example(
    'nfa_contains_01',
    'NFA accepting strings containing 01',
    NFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
            'q1': {'1': {'q2'}},
            'q2': {'0': {'q2'}, '1': {'q2'}}
        },
        initial_state='q0',
        final_states={'q2'}
    ),
    "NFA(states={'q0', 'q1', 'q2'}, input_symbols={'0', '1'}, transitions={'q0': {'0': {'q0', 'q1'}, '1': {'q0'}}, 'q1': {'1': {'q2'}}, 'q2': {'0': {'q2'}, '1': {'q2'}}}, initial_state='q0', final_states={'q2'})"
)

add_example(
    'nfa_contains_aba',
    'NFA accepting strings containing aba as substring',
    NFA(
        states={'q0', 'q1', 'q2', 'q3'},
        input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': {'q0', 'q1'}, 'b': {'q0'}},
            'q1': {'b': {'q2'}},
            'q2': {'a': {'q3'}},
            'q3': {'a': {'q3'}, 'b': {'q3'}}
        },
        initial_state='q0',
        final_states={'q3'}
    ),
    "NFA(states={'q0', 'q1', 'q2', 'q3'}, input_symbols={'a', 'b'}, transitions={'q0': {'a': {'q0', 'q1'}, 'b': {'q0'}}, 'q1': {'b': {'q2'}}, 'q2': {'a': {'q3'}}, 'q3': {'a': {'q3'}, 'b': {'q3'}}}, initial_state='q0', final_states={'q3'})"
)

# Save results
print(f"\n{'='*50}")
print(f"Generated {len(examples_code)} code pairs")
print(f"Generated {len(examples_nl)} NL pairs")
print(f"Total: {len(examples_code) + len(examples_nl)} pairs")

with open('data/logic-stream.jsonl', 'a') as f:
    for ex in examples_code:
        f.write(json.dumps(ex) + '\n')

with open('data/documentation-stream.jsonl', 'a') as f:
    for ex in examples_nl:
        f.write(json.dumps(ex) + '\n')

print("\nAppended to streams!")
