"""
Comprehensive extractor for automata-lib: DFA, NFA, PDA, TM examples
Generates both (code, dot) pairs from test files and documentation.
"""

import os
import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM

output_dir = project_root / "data" / "raw" / "automata_comprehensive"
output_dir.mkdir(parents=True, exist_ok=True)

examples = []

# NFA Examples
print("=== Extracting NFA Examples ===")

# NFA 001: Basic ab*
nfa_ab_star = NFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': {'q1'}},
        'q1': {'b': {'q1'}, '': {'q2'}},
    },
    initial_state='q0',
    final_states={'q2'}
)
examples.append(("nfa", "ab_star", nfa_ab_star, "NFA accepting strings starting with 'a' followed by zero or more 'b's"))

# NFA 002: Multiple epsilon transitions
nfa_epsilon = NFA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'': {'q1', 'q2'}},
        'q1': {'a': {'q3'}},
        'q2': {'b': {'q3'}},
    },
    initial_state='q0',
    final_states={'q3'}
)
examples.append(("nfa", "epsilon_branches", nfa_epsilon, "NFA with epsilon transitions branching to accept 'a' or 'b'"))

# NFA 003: Union pattern (a|b)*c
nfa_union = NFA(
    states={'q0', 'q1'},
    input_symbols={'a', 'b', 'c'},
    transitions={
        'q0': {'a': {'q0'}, 'b': {'q0'}, 'c': {'q1'}},
    },
    initial_state='q0',
    final_states={'q1'}
)
examples.append(("nfa", "union_star_c", nfa_union, "NFA accepting any combination of 'a' or 'b' followed by 'c'"))

# NFA 004: Nondeterministic choice
nfa_choice = NFA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
        'q1': {'1': {'q2'}},
        'q2': {'0': {'q3'}},
    },
    initial_state='q0',
    final_states={'q3'}
)
examples.append(("nfa", "nondeterministic_010", nfa_choice, "NFA accepting strings containing '010' as a substring (nondeterministic)"))

print("=== Extracting PDA Examples ===")

# DPDA 001: Balanced parentheses
dpda_parens = DPDA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'(', ')'},
    stack_symbols={'0', 'x'},
    transitions={
        'q0': {
            '': {'0': {('q2', '')}},
        },
        'q1': {
            '(': {'0': {('q1', ('x', '0'))}},
            ')': {'x': {('q1', '')}},
            '': {'0': {('q2', ('0',))}},
        },
        'q2': {},
    },
    initial_state='q0',
    initial_stack_symbol='0',
    final_states={'q2'},
    acceptance_mode='both'
)
examples.append(("dpda", "balanced_parens", dpda_parens, "DPDA accepting balanced parentheses"))

# DPDA 002: Equal a's and b's  
dpda_equal = DPDA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'a', 'b'},
    stack_symbols={'0', 'A', 'B'},
    transitions={
        'q0': {
            '': {'0': {('q3', '')}},
            'a': {'0': {('q1', ('A', '0'))}},
            'b': {'0': {('q2', ('B', '0'))}},
        },
        'q1': {
            'a': {
                '0': {('q1', ('A', '0'))},
                'A': {('q1', ('A', 'A'))},
            },
            'b': {
                'A': {('q1', '')},
            },
            '': {'0': {('q3', ('0',))}},
        },
        'q2': {
            'a': {
                'B': {('q2', '')},
            },
            'b': {
                '0': {('q2', ('B', '0'))},
                'B': {('q2', ('B', 'B'))},
            },
            '': {'0': {('q3', ('0',))}},
        },
        'q3': {},
    },
    initial_state='q0',
    initial_stack_symbol='0',
    final_states={'q3'},
    acceptance_mode='both'
)
examples.append(("dpda", "equal_ab", dpda_equal, "DPDA accepting strings with equal number of a's and b's"))

print("=== Extracting Turing Machine Examples ===")

# DTM 001: Palindrome checker
dtm_palindrome = DTM(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'qf'},
    input_symbols={'a', 'b'},
    tape_symbols={'a', 'b', 'x', '.'},
    transitions={
        'q0': {
            'a': ('q1', 'x', 'R'),
            'b': ('q2', 'x', 'R'),
            'x': ('q0', 'x', 'R'),
            '.': ('qf', '.', 'N'),
        },
        'q1': {
            'a': ('q1', 'a', 'R'),
            'b': ('q1', 'b', 'R'),
            '.': ('q3', '.', 'L'),
        },
        'q2': {
            'a': ('q2', 'a', 'R'),
            'b': ('q2', 'b', 'R'),
            '.': ('q4', '.', 'L'),
        },
        'q3': {
            'a': ('q0', 'x', 'L'),
            'x': ('q3', 'x', 'L'),
        },
        'q4': {
            'b': ('q0', 'x', 'L'),
            'x': ('q4', 'x', 'L'),
        },
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'qf'}
)
examples.append(("dtm", "palindrome", dtm_palindrome, "Turing Machine accepting palindromes over {a, b}"))

# DTM 002: Binary increment
dtm_increment = DTM(
    states={'q0', 'q1', 'qf'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    transitions={
        'q0': {
            '0': ('q0', '0', 'R'),
            '1': ('q0', '1', 'R'),
            '.': ('q1', '.', 'L'),
        },
        'q1': {
            '0': ('qf', '1', 'N'),
            '1': ('q1', '0', 'L'),
            '.': ('qf', '1', 'R'),
        },
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'qf'}
)
examples.append(("dtm", "binary_increment", dtm_increment, "Turing Machine incrementing binary numbers"))

# Generate outputs
print("\n=== Generating Outputs ===")
count = 0

for automaton_type, name, automaton, description in examples:
    example_dir = output_dir / f"{automaton_type}_{name}"
    example_dir.mkdir(exist_ok=True)
    
    # Save description
    desc_file = example_dir / "description.txt"
    desc_file.write_text(description)
    
    # Save code
    code_file = example_dir / "code.py"
    code_lines = [
        f"from automata.{automaton_type[:2]}.{automaton_type[:3] if automaton_type.startswith('d') else automaton_type[:3]} import {automaton.__class__.__name__}",
        "",
        f"# {description}",
        f"{name} = {repr(automaton)}",
    ]
    code_file.write_text("\n".join(code_lines))
    
    # Generate and save DOT
    try:
        dot_data = automaton.show_diagram(return_str=True)
        dot_file = example_dir / "diagram.dot"
        dot_file.write_text(dot_data)
        
        # Save metadata
        meta_file = example_dir / "metadata.txt"
        meta_file.write_text(f"type: {automaton_type}\nstates: {len(automaton.states)}\n")
        
        print(f"  ✓ Saved {automaton_type}_{name}")
        count += 1
    except Exception as e:
        print(f"  ✗ Failed {automaton_type}_{name}: {e}")

print(f"\n{'='*70}")
print(f"Extracted {count} comprehensive automata examples")
print(f"{'='*70}")
