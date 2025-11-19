"""
Enhanced FSM extractor that extracts natural language descriptions.

Extracts both code-to-DOT and NL-to-DOT pairs from FSM files with docstrings.
"""

import ast
from pathlib import Path
from typing import Optional


def extract_module_docstring(file_path: Path) -> Optional[str]:
    """Extract the module-level docstring from a Python file.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Module docstring if present, None otherwise
    """
    try:
        source = file_path.read_text(encoding='utf-8')
        tree = ast.parse(source)
        
        # Get module docstring
        docstring = ast.get_docstring(tree)
        
        if docstring:
            # Clean up the docstring
            # Remove excessive whitespace and formatting markers
            lines = docstring.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # Skip lines that are just separators
                if line.strip() and not all(c in '-=' for c in line.strip()):
                    cleaned_lines.append(line.strip())
            
            # Join and clean
            cleaned = ' '.join(cleaned_lines)
            # Remove multiple spaces
            cleaned = ' '.join(cleaned.split())
            
            return cleaned
        
        return None
        
    except Exception:
        return None


def extract_class_docstring(source_code: str, class_name: str) -> Optional[str]:
    """Extract docstring from a specific class in source code.
    
    Args:
        source_code: Python source code
        class_name: Name of class to find
        
    Returns:
        Class docstring if present
    """
    try:
        tree = ast.parse(source_code)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return ast.get_docstring(node)
        
        return None
        
    except Exception:
        return None


def generate_nl_description_from_code(source_code: str, class_name: Optional[str] = None) -> str:
    """Generate a natural language description from FSM code structure.
    
    This creates a basic NL description by analyzing the code structure.
    
    Args:
        source_code: FSM source code
        class_name: Optional class name
        
    Returns:
        Natural language description
    """
    try:
        tree = ast.parse(source_code)
        
        states = []
        transitions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Found a class, analyze it
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        # Look for State assignments
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                state_name = target.id
                                # Check if it's a State
                                if isinstance(item.value, ast.Call):
                                    if hasattr(item.value.func, 'id') and item.value.func.id == 'State':
                                        states.append(state_name)
        
        if states and class_name:
            state_list = ', '.join(states[:-1]) + f' and {states[-1]}' if len(states) > 1 else states[0]
            return f"Create a state machine called {class_name} with states: {state_list}."
        elif states:
            state_list = ', '.join(states[:-1]) + f' and {states[-1]}' if len(states) > 1 else states[0]
            return f"Create a state machine with states: {state_list}."
        else:
            return "Create a state machine."
            
    except Exception:
        return "Create a state machine."


if __name__ == '__main__':
    # Test with our examples
    import sys
    examples_dir = Path('/tmp/fsm-repos/python-statemachine/tests/examples')
    
    for py_file in examples_dir.glob('*.py'):
        if py_file.name.startswith('_'):
            continue
            
        print(f"\n{'='*70}")
        print(f"File: {py_file.name}")
        print('='*70)
        
        docstring = extract_module_docstring(py_file)
        if docstring:
            print(f"Module docstring:\n{docstring}\n")
        else:
            print("No module docstring found\n")
