"""
Extract training pairs from caleb531/automata library by executing test cases.
"""

import sys
import os
import json
import re
from pathlib import Path

# Add the automata library to path
sys.path.insert(0, 'data/raw/automata-caleb531')

try:
    from automata.fa.dfa import DFA
    from automata.fa.nfa import NFA
    from automata.fa.gnfa import GNFA
    from automata.pda.dpda import DPDA
    from automata.pda.npda import NPDA
except ImportError as e:
    print(f"Error importing automata: {e}")
    print("Make sure the repo is cloned and dependencies are installed")
    sys.exit(1)

def extract_test_examples():
    """Parse test files and extract automaton definitions."""
    test_dir = Path('data/raw/automata-caleb531/tests')
    examples = []
    
    # Read test files and extract DFA/NFA definitions
    dfa_tests = test_dir / 'test_dfa.py'
    nfa_tests = test_dir / 'test_nfa.py'
    
    if dfa_tests.exists():
        examples.extend(extract_dfa_examples(dfa_tests.read_text()))
    
    if nfa_tests.exists():
        examples.extend(extract_nfa_examples(nfa_tests.read_text()))
    
    return examples

def extract_dfa_examples(content):
    """Extract DFA examples from test file."""
    examples = []
    
    # Find DFA instantiations - look for specific test patterns
    # Pattern: self.dfa = DFA(...)
    pattern = r'(\w+)\s*=\s*DFA\s*\((.*?)\n\s*\)'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        var_name = match.group(1)
        params_str = match.group(2)
        
        try:
            # Try to extract structured parameters
            code = f"DFA({params_str}\n)"
            examples.append({
                'type': 'DFA',
                'var_name': var_name,
                'code': code,
                'params_str': params_str
            })
        except:
            pass
    
    return examples

def extract_nfa_examples(content):
    """Extract NFA examples from test file."""
    examples = []
    
    pattern = r'(\w+)\s*=\s*NFA\s*\((.*?)\n\s*\)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        var_name = match.group(1)
        params_str = match.group(2)
        
        try:
            code = f"NFA({params_str}\n)"
            examples.append({
                'type': 'NFA',
                'var_name': var_name,
                'code': code,
                'params_str': params_str
            })
        except:
            pass
    
    return examples

def generate_dot_from_code(automaton_code, automaton_type):
    """Execute automaton code and generate DOT."""
    try:
        # Create a namespace for execution
        namespace = {
            'DFA': DFA,
            'NFA': NFA,
            'GNFA': GNFA,
            'DPDA': DPDA,
            'NPDA': NPDA,
            'frozenset': frozenset,
            'set': set
        }
        
        # Execute the code to create the automaton
        exec(f"automaton = {automaton_code}", namespace)
        automaton = namespace['automaton']
        
        # Generate diagram and get DOT
        graph = automaton.show_diagram()
        dot_string = graph.to_string()
        
        return dot_string
    except Exception as e:
        print(f"Error generating DOT: {e}")
        return None

def extract_description_from_test(var_name, test_content):
    """Try to extract test documentation for natural language description."""
    # Look for comments or docstrings near the variable
    lines = test_content.split('\n')
    for i, line in enumerate(lines):
        if var_name in line:
            # Check previous lines for comments
            for j in range(max(0, i-5), i):
                if '#' in lines[j]:
                    return lines[j].split('#')[1].strip()
                if '"""' in lines[j] or "'''" in lines[j]:
                    return lines[j].strip('"""').strip("'''").strip()
    return None

if __name__ == '__main__':
    print("Extracting automata examples...")
    
    # For now, let's manually define a few working examples from the test files
    # Later we can make the parser more sophisticated
    
    # Simple DFA from the tests
    simple_dfa = DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q0', '1': 'q2'},
            'q2': {'0': 'q2', '1': 'q1'}
        },
        initial_state='q0',
        final_states={'q1'}
    )
    
    # Generate DOT
    graph = simple_dfa.show_diagram()
    dot = graph.to_string()
    
    print("Generated DOT:")
    print(dot)
    print("\n" + "="*50 + "\n")
    
    # Create training pair
    code = '''DFA(
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
    
    pair = {
        'input': code,
        'output': dot,
        'metadata': {
            'source': 'automata-caleb531/tests/test_dfa.py',
            'type': 'code_to_dot',
            'automaton_type': 'DFA'
        }
    }
    
    print("Training pair created successfully!")
    print(f"Input length: {len(code)} chars")
    print(f"Output length: {len(dot)} chars")
