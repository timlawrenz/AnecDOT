"""
Parser for caleb531/automata library - extracts DFA/NFA/PDA examples from tests.
"""

import os
import re
import json
import ast
from pathlib import Path

def extract_automata_examples(repo_path):
    """Extract automata examples from test files."""
    examples = []
    test_dir = Path(repo_path) / "tests"
    
    for test_file in test_dir.glob("test_*.py"):
        content = test_file.read_text()
        
        # Look for DFA/NFA/PDA instantiations in tests
        examples.extend(extract_from_file(content, test_file.name))
    
    return examples

def extract_from_file(content, filename):
    """Extract automata definitions from a single file."""
    examples = []
    
    try:
        tree = ast.parse(content)
    except:
        return examples
    
    for node in ast.walk(tree):
        # Look for function calls creating automata (DFA, NFA, etc.)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ['from_dfa', 'from_nfa', 'show_diagram']:
                    # This might generate a diagram
                    example = extract_automaton_call(node, content)
                    if example:
                        examples.append({
                            'source': f'automata/{filename}',
                            'type': 'code',
                            **example
                        })
            elif isinstance(node.func, ast.Name):
                if node.func.id in ['DFA', 'NFA', 'GNFA', 'DPDA', 'NPDA']:
                    example = extract_automaton_call(node, content)
                    if example:
                        examples.append({
                            'source': f'automata/{filename}',
                            'type': 'code',
                            'automaton_type': node.func.id,
                            **example
                        })
    
    return examples

def extract_automaton_call(node, content):
    """Extract details from an automaton constructor call."""
    # Get the source code for this call
    try:
        # Simple approach: extract keyword arguments
        kwargs = {}
        for keyword in node.keywords:
            if keyword.arg:
                kwargs[keyword.arg] = ast.unparse(keyword.value) if hasattr(ast, 'unparse') else str(keyword.value)
        
        if 'states' in kwargs or 'input_symbols' in kwargs:
            return {
                'code': ast.unparse(node) if hasattr(ast, 'unparse') else None,
                'parameters': kwargs
            }
    except:
        pass
    
    return None

def create_dot_from_automaton(automaton_type, params):
    """Generate DOT representation from automaton parameters."""
    # This is a simplified generator - real implementation would execute the code
    # For now, we'll mark these for manual extraction
    return None

if __name__ == '__main__':
    repo_path = 'data/raw/automata-caleb531'
    examples = extract_automata_examples(repo_path)
    
    print(f"Found {len(examples)} automata examples")
    for ex in examples[:3]:
        print(f"\n{ex['source']}: {ex.get('automaton_type', 'unknown')}")
        if 'parameters' in ex:
            print(f"  Parameters: {list(ex['parameters'].keys())}")
