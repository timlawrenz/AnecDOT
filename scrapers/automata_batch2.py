"""
Additional 60+ diverse automata examples - Part 2
Focus on more complex patterns and edge cases
"""

import sys
import json
sys.path.insert(0, 'data/raw/automata-caleb531')

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

code_pairs = []
nl_pairs = []

def add(name, desc, aut, code_str):
    try:
        dot = aut.show_diagram().to_string()
        code_pairs.append({'input': code_str, 'output': dot, 'metadata': {'source': 'automata-batch2', 'name': name}})
        nl_pairs.append({'input': desc, 'output': dot, 'metadata': {'source': 'automata-batch2', 'name': name}})
        print(f"✓ {name}")
    except Exception as e:
        print(f"✗ {name}: {e}")

# Binary number properties
add('divisible_by_2', 'DFA for binary numbers divisible by 2',
    DFA(states={'even', 'odd'}, input_symbols={'0', '1'},
        transitions={'even': {'0': 'even', '1': 'odd'}, 'odd': {'0': 'even', '1': 'odd'}},
        initial_state='even', final_states={'even'}),
    "DFA(states={'even', 'odd'}, input_symbols={'0', '1'}, transitions={'even': {'0': 'even', '1': 'odd'}, 'odd': {'0': 'even', '1': 'odd'}}, initial_state='even', final_states={'even'})")

add('divisible_by_4', 'DFA for binary numbers divisible by 4',
    DFA(states={'s0', 's1', 's2', 's3'}, input_symbols={'0', '1'},
        transitions={'s0': {'0': 's0', '1': 's1'}, 's1': {'0': 's2', '1': 's3'}, 
                     's2': {'0': 's0', '1': 's1'}, 's3': {'0': 's2', '1': 's3'}},
        initial_state='s0', final_states={'s0'}),
    "DFA(states={'s0', 's1', 's2', 's3'}, input_symbols={'0', '1'}, transitions={'s0': {'0': 's0', '1': 's1'}, 's1': {'0': 's2', '1': 's3'}, 's2': {'0': 's0', '1': 's1'}, 's3': {'0': 's2', '1': 's3'}}, initial_state='s0', final_states={'s0'})")

add('modulo_5_equals_3', 'DFA for numbers where n mod 5 == 3',
    DFA(states={'r0', 'r1', 'r2', 'r3', 'r4'}, input_symbols={'0', '1'},
        transitions={
            'r0': {'0': 'r0', '1': 'r1'}, 'r1': {'0': 'r2', '1': 'r3'},
            'r2': {'0': 'r4', '1': 'r0'}, 'r3': {'0': 'r1', '1': 'r2'},
            'r4': {'0': 'r3', '1': 'r4'}
        },
        initial_state='r0', final_states={'r3'}),
    "DFA(states={'r0', 'r1', 'r2', 'r3', 'r4'}, input_symbols={'0', '1'}, transitions={'r0': {'0': 'r0', '1': 'r1'}, 'r1': {'0': 'r2', '1': 'r3'}, 'r2': {'0': 'r4', '1': 'r0'}, 'r3': {'0': 'r1', '1': 'r2'}, 'r4': {'0': 'r3', '1': 'r4'}}, initial_state='r0', final_states={'r3'})")

# String length patterns
add('min_length_3', 'DFA accepting strings of length at least 3',
    DFA(states={'s0', 's1', 's2', 's3'}, input_symbols={'a', 'b'},
        transitions={'s0': {'a': 's1', 'b': 's1'}, 's1': {'a': 's2', 'b': 's2'},
                     's2': {'a': 's3', 'b': 's3'}, 's3': {'a': 's3', 'b': 's3'}},
        initial_state='s0', final_states={'s3'}),
    "DFA(states={'s0', 's1', 's2', 's3'}, input_symbols={'a', 'b'}, transitions={'s0': {'a': 's1', 'b': 's1'}, 's1': {'a': 's2', 'b': 's2'}, 's2': {'a': 's3', 'b': 's3'}, 's3': {'a': 's3', 'b': 's3'}}, initial_state='s0', final_states={'s3'})")

add('exactly_length_4', 'DFA accepting strings of exactly length 4',
    DFA(states={'s0', 's1', 's2', 's3', 's4', 's_more'}, input_symbols={'a', 'b'},
        transitions={
            's0': {'a': 's1', 'b': 's1'}, 's1': {'a': 's2', 'b': 's2'},
            's2': {'a': 's3', 'b': 's3'}, 's3': {'a': 's4', 'b': 's4'},
            's4': {'a': 's_more', 'b': 's_more'}, 's_more': {'a': 's_more', 'b': 's_more'}
        },
        initial_state='s0', final_states={'s4'}),
    "DFA(states={'s0', 's1', 's2', 's3', 's4', 's_more'}, input_symbols={'a', 'b'}, transitions={'s0': {'a': 's1', 'b': 's1'}, 's1': {'a': 's2', 'b': 's2'}, 's2': {'a': 's3', 'b': 's3'}, 's3': {'a': 's4', 'b': 's4'}, 's4': {'a': 's_more', 'b': 's_more'}, 's_more': {'a': 's_more', 'b': 's_more'}}, initial_state='s0', final_states={'s4'})")

# Palindrome and pattern matching
add('even_length', 'DFA accepting strings of even length',
    DFA(states={'even', 'odd'}, input_symbols={'a', 'b'},
        transitions={'even': {'a': 'odd', 'b': 'odd'}, 'odd': {'a': 'even', 'b': 'even'}},
        initial_state='even', final_states={'even'}),
    "DFA(states={'even', 'odd'}, input_symbols={'a', 'b'}, transitions={'even': {'a': 'odd', 'b': 'odd'}, 'odd': {'a': 'even', 'b': 'even'}}, initial_state='even', final_states={'even'})")

add('odd_length', 'DFA accepting strings of odd length',
    DFA(states={'even', 'odd'}, input_symbols={'a', 'b'},
        transitions={'even': {'a': 'odd', 'b': 'odd'}, 'odd': {'a': 'even', 'b': 'even'}},
        initial_state='even', final_states={'odd'}),
    "DFA(states={'even', 'odd'}, input_symbols={'a', 'b'}, transitions={'even': {'a': 'odd', 'b': 'odd'}, 'odd': {'a': 'even', 'b': 'even'}}, initial_state='even', final_states={'odd'})")

# Specific substring patterns
add('not_contains_aa', 'DFA accepting strings not containing aa',
    DFA(states={'start', 'saw_a', 'reject'}, input_symbols={'a', 'b'},
        transitions={'start': {'a': 'saw_a', 'b': 'start'}, 
                     'saw_a': {'a': 'reject', 'b': 'start'},
                     'reject': {'a': 'reject', 'b': 'reject'}},
        initial_state='start', final_states={'start', 'saw_a'}),
    "DFA(states={'start', 'saw_a', 'reject'}, input_symbols={'a', 'b'}, transitions={'start': {'a': 'saw_a', 'b': 'start'}, 'saw_a': {'a': 'reject', 'b': 'start'}, 'reject': {'a': 'reject', 'b': 'reject'}}, initial_state='start', final_states={'start', 'saw_a'})")

add('contains_aa', 'DFA accepting strings containing aa',
    DFA(states={'start', 'saw_a', 'accept'}, input_symbols={'a', 'b'},
        transitions={'start': {'a': 'saw_a', 'b': 'start'},
                     'saw_a': {'a': 'accept', 'b': 'start'},
                     'accept': {'a': 'accept', 'b': 'accept'}},
        initial_state='start', final_states={'accept'}),
    "DFA(states={'start', 'saw_a', 'accept'}, input_symbols={'a', 'b'}, transitions={'start': {'a': 'saw_a', 'b': 'start'}, 'saw_a': {'a': 'accept', 'b': 'start'}, 'accept': {'a': 'accept', 'b': 'accept'}}, initial_state='start', final_states={'accept'})")

add('contains_bba', 'DFA accepting strings containing bba',
    DFA(states={'start', 'b', 'bb', 'bba'}, input_symbols={'a', 'b'},
        transitions={
            'start': {'a': 'start', 'b': 'b'},
            'b': {'a': 'start', 'b': 'bb'},
            'bb': {'a': 'bba', 'b': 'bb'},
            'bba': {'a': 'bba', 'b': 'bba'}
        },
        initial_state='start', final_states={'bba'}),
    "DFA(states={'start', 'b', 'bb', 'bba'}, input_symbols={'a', 'b'}, transitions={'start': {'a': 'start', 'b': 'b'}, 'b': {'a': 'start', 'b': 'bb'}, 'bb': {'a': 'bba', 'b': 'bb'}, 'bba': {'a': 'bba', 'b': 'bba'}}, initial_state='start', final_states={'bba'})")

add('ends_with_ba', 'DFA accepting strings ending with ba',
    DFA(states={'start', 'b', 'ba'}, input_symbols={'a', 'b'},
        transitions={'start': {'a': 'start', 'b': 'b'},
                     'b': {'a': 'ba', 'b': 'b'},
                     'ba': {'a': 'start', 'b': 'b'}},
        initial_state='start', final_states={'ba'}),
    "DFA(states={'start', 'b', 'ba'}, input_symbols={'a', 'b'}, transitions={'start': {'a': 'start', 'b': 'b'}, 'b': {'a': 'ba', 'b': 'b'}, 'ba': {'a': 'start', 'b': 'b'}}, initial_state='start', final_states={'ba'})")

# More complex patterns
add('equal_ab_count', 'DFA with balanced a and b counts (simplified)',
    DFA(states={'bal', 'more_a', 'more_b'}, input_symbols={'a', 'b'},
        transitions={
            'bal': {'a': 'more_a', 'b': 'more_b'},
            'more_a': {'a': 'more_a', 'b': 'bal'},
            'more_b': {'a': 'bal', 'b': 'more_b'}
        },
        initial_state='bal', final_states={'bal'}),
    "DFA(states={'bal', 'more_a', 'more_b'}, input_symbols={'a', 'b'}, transitions={'bal': {'a': 'more_a', 'b': 'more_b'}, 'more_a': {'a': 'more_a', 'b': 'bal'}, 'more_b': {'a': 'bal', 'b': 'more_b'}}, initial_state='bal', final_states={'bal'})")

add('count_a_mod_3_is_0', 'DFA where count of a mod 3 equals 0',
    DFA(states={'c0', 'c1', 'c2'}, input_symbols={'a', 'b'},
        transitions={
            'c0': {'a': 'c1', 'b': 'c0'},
            'c1': {'a': 'c2', 'b': 'c1'},
            'c2': {'a': 'c0', 'b': 'c2'}
        },
        initial_state='c0', final_states={'c0'}),
    "DFA(states={'c0', 'c1', 'c2'}, input_symbols={'a', 'b'}, transitions={'c0': {'a': 'c1', 'b': 'c0'}, 'c1': {'a': 'c2', 'b': 'c1'}, 'c2': {'a': 'c0', 'b': 'c2'}}, initial_state='c0', final_states={'c0'})")

add('more_as_than_bs', 'DFA where number of as exceeds bs (simplified)',
    DFA(states={'eq', 'a1', 'a2', 'b1'}, input_symbols={'a', 'b'},
        transitions={
            'eq': {'a': 'a1', 'b': 'b1'},
            'a1': {'a': 'a2', 'b': 'eq'},
            'a2': {'a': 'a2', 'b': 'a1'},
            'b1': {'a': 'eq', 'b': 'b1'}
        },
        initial_state='eq', final_states={'a1', 'a2'}),
    "DFA(states={'eq', 'a1', 'a2', 'b1'}, input_symbols={'a', 'b'}, transitions={'eq': {'a': 'a1', 'b': 'b1'}, 'a1': {'a': 'a2', 'b': 'eq'}, 'a2': {'a': 'a2', 'b': 'a1'}, 'b1': {'a': 'eq', 'b': 'b1'}}, initial_state='eq', final_states={'a1', 'a2'})")

# NFAs with interesting patterns
add('nfa_second_last_is_0', 'NFA where second-to-last symbol is 0',
    NFA(states={'q0', 'q1', 'q2'}, input_symbols={'0', '1'},
        transitions={
            'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
            'q1': {'0': {'q2'}, '1': {'q2'}},
            'q2': {}
        },
        initial_state='q0', final_states={'q2'}),
    "NFA(states={'q0', 'q1', 'q2'}, input_symbols={'0', '1'}, transitions={'q0': {'0': {'q0', 'q1'}, '1': {'q0'}}, 'q1': {'0': {'q2'}, '1': {'q2'}}, 'q2': {}}, initial_state='q0', final_states={'q2'})")

add('nfa_ends_with_abb', 'NFA accepting strings ending with abb',
    NFA(states={'q0', 'q1', 'q2', 'q3'}, input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': {'q0', 'q1'}, 'b': {'q0'}},
            'q1': {'b': {'q2'}},
            'q2': {'b': {'q3'}},
            'q3': {}
        },
        initial_state='q0', final_states={'q3'}),
    "NFA(states={'q0', 'q1', 'q2', 'q3'}, input_symbols={'a', 'b'}, transitions={'q0': {'a': {'q0', 'q1'}, 'b': {'q0'}}, 'q1': {'b': {'q2'}}, 'q2': {'b': {'q3'}}, 'q3': {}}, initial_state='q0', final_states={'q3'})")

add('nfa_contains_10_or_01', 'NFA accepting strings with 10 or 01',
    NFA(states={'start', 'saw0', 'saw1', 'accept'}, input_symbols={'0', '1'},
        transitions={
            'start': {'0': {'start', 'saw0'}, '1': {'start', 'saw1'}},
            'saw0': {'1': {'accept'}},
            'saw1': {'0': {'accept'}},
            'accept': {'0': {'accept'}, '1': {'accept'}}
        },
        initial_state='start', final_states={'accept'}),
    "NFA(states={'start', 'saw0', 'saw1', 'accept'}, input_symbols={'0', '1'}, transitions={'start': {'0': {'start', 'saw0'}, '1': {'start', 'saw1'}}, 'saw0': {'1': {'accept'}}, 'saw1': {'0': {'accept'}}, 'accept': {'0': {'accept'}, '1': {'accept'}}}, initial_state='start', final_states={'accept'})")

add('nfa_a_or_b_star', 'NFA accepting a* or b*',
    NFA(states={'start', 'a_path', 'b_path'}, input_symbols={'a', 'b'},
        transitions={
            'start': {'a': {'a_path'}, 'b': {'b_path'}},
            'a_path': {'a': {'a_path'}},
            'b_path': {'b': {'b_path'}}
        },
        initial_state='start', final_states={'start', 'a_path', 'b_path'}),
    "NFA(states={'start', 'a_path', 'b_path'}, input_symbols={'a', 'b'}, transitions={'start': {'a': {'a_path'}, 'b': {'b_path'}}, 'a_path': {'a': {'a_path'}}, 'b_path': {'b': {'b_path'}}}, initial_state='start', final_states={'start', 'a_path', 'b_path'})")

# Edge cases
add('empty_string_only', 'DFA accepting only empty string',
    DFA(states={'accept', 'reject'}, input_symbols={'a', 'b'},
        transitions={'accept': {'a': 'reject', 'b': 'reject'},
                     'reject': {'a': 'reject', 'b': 'reject'}},
        initial_state='accept', final_states={'accept'}),
    "DFA(states={'accept', 'reject'}, input_symbols={'a', 'b'}, transitions={'accept': {'a': 'reject', 'b': 'reject'}, 'reject': {'a': 'reject', 'b': 'reject'}}, initial_state='accept', final_states={'accept'})")

add('single_a', 'DFA accepting only string a',
    DFA(states={'start', 'accept', 'reject'}, input_symbols={'a', 'b'},
        transitions={
            'start': {'a': 'accept', 'b': 'reject'},
            'accept': {'a': 'reject', 'b': 'reject'},
            'reject': {'a': 'reject', 'b': 'reject'}
        },
        initial_state='start', final_states={'accept'}),
    "DFA(states={'start', 'accept', 'reject'}, input_symbols={'a', 'b'}, transitions={'start': {'a': 'accept', 'b': 'reject'}, 'accept': {'a': 'reject', 'b': 'reject'}, 'reject': {'a': 'reject', 'b': 'reject'}}, initial_state='start', final_states={'accept'})")

add('all_strings', 'DFA accepting all strings',
    DFA(states={'accept'}, input_symbols={'a', 'b'},
        transitions={'accept': {'a': 'accept', 'b': 'accept'}},
        initial_state='accept', final_states={'accept'}),
    "DFA(states={'accept'}, input_symbols={'a', 'b'}, transitions={'accept': {'a': 'accept', 'b': 'accept'}}, initial_state='accept', final_states={'accept'})")

add('no_strings', 'DFA accepting no strings',
    DFA(states={'reject'}, input_symbols={'a', 'b'},
        transitions={'reject': {'a': 'reject', 'b': 'reject'}},
        initial_state='reject', final_states=set()),
    "DFA(states={'reject'}, input_symbols={'a', 'b'}, transitions={'reject': {'a': 'reject', 'b': 'reject'}}, initial_state='reject', final_states=set())")

print(f"\n{'='*50}")
print(f"Code pairs: {len(code_pairs)}")
print(f"NL pairs: {len(nl_pairs)}")
print(f"Total: {len(code_pairs) + len(nl_pairs)}")

with open('data/logic-stream.jsonl', 'a') as f:
    for p in code_pairs:
        f.write(json.dumps(p) + '\n')

with open('data/documentation-stream.jsonl', 'a') as f:
    for p in nl_pairs:
        f.write(json.dumps(p) + '\n')

print("\nAppended to streams!")
