#!/usr/bin/env python3
"""
Extractor for caleb531/automata library examples.

Extracts DFA, NFA, and other automata examples from test files
and generates DOT representations using show_diagram().
"""

import os
import sys
import re
import ast
from pathlib import Path
from typing import List, Tuple, Optional

# Add automata to path
AUTOMATA_PATH = Path("/tmp/automata")
sys.path.insert(0, str(AUTOMATA_PATH))

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA


def extract_dfa_definitions(test_file: Path) -> List[Tuple[str, str, str]]:
    """
    Extract DFA definitions from test file.
    
    Returns list of (name, description, code) tuples.
    """
    content = test_file.read_text()
    
    definitions = []
    
    # Pattern: comment followed by variable_name = DFA(...)
    # Match multi-line comments and DFA definitions
    pattern = r'#\s*(.+?)\n\s*(\w+)\s*=\s*DFA\(((?:[^()]|\([^()]*\))*)\)'
    
    matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        description = match.group(1).strip()
        var_name = match.group(2)
        dfa_args = match.group(3)
        
        # Clean up description - handle multi-line comments
        desc_lines = [line.strip().lstrip('#').strip() 
                     for line in description.split('\n')]
        description = ' '.join(desc_lines)
        
        # Reconstruct full DFA code
        code = f"{var_name} = DFA({dfa_args})"
        
        definitions.append((var_name, description, code))
    
    return definitions


def execute_and_get_dot(code: str) -> Optional[str]:
    """
    Execute DFA code and call show_diagram() to get DOT output.
    """
    try:
        # Create namespace
        namespace = {
            'DFA': DFA,
            'NFA': NFA,
            'set': set,
            'frozendict': __import__('frozendict').frozendict,
        }
        
        # Execute the code
        exec(code, namespace)
        
        # Find the DFA variable (first non-builtin variable)
        dfa_var = None
        var_name = None
        for name, value in namespace.items():
            if isinstance(value, (DFA, NFA)) and not name.startswith('_'):
                dfa_var = value
                var_name = name
                break
        
        if dfa_var is None:
            return None
        
        # Get the diagram
        graph = dfa_var.show_diagram()
        
        # Convert to DOT string
        dot_str = graph.to_string()
        
        return dot_str
    
    except Exception as e:
        print(f"Error executing code: {e}", file=sys.stderr)
        return None


def save_pair(output_dir: Path, index: int, description: str, code: str, dot: str):
    """Save a (code, dot) pair with metadata."""
    pair_dir = output_dir / f"automata_{index:03d}"
    pair_dir.mkdir(parents=True, exist_ok=True)
    
    # Save description
    (pair_dir / "description.txt").write_text(description)
    
    # Save code
    (pair_dir / "code.py").write_text(code)
    
    # Save DOT
    (pair_dir / "diagram.dot").write_text(dot)
    
    # Save metadata
    metadata = f"""Source: caleb531/automata test suite
Type: DFA
Description: {description}
"""
    (pair_dir / "metadata.txt").write_text(metadata)


def main():
    """Main extraction function."""
    test_file = AUTOMATA_PATH / "tests" / "test_dfa.py"
    output_dir = Path("/home/tim/source/activity/AnecDOT/data/raw/automata_extraction")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting from {test_file}...")
    
    definitions = extract_dfa_definitions(test_file)
    print(f"Found {len(definitions)} DFA definitions")
    
    extracted_count = 0
    
    for i, (var_name, description, code) in enumerate(definitions, 1):
        print(f"\n[{i}/{len(definitions)}] Processing: {var_name}")
        print(f"  Description: {description[:60]}...")
        
        dot = execute_and_get_dot(code)
        
        if dot:
            save_pair(output_dir, extracted_count, description, code, dot)
            print(f"  ✓ Saved to automata_{extracted_count:03d}")
            extracted_count += 1
        else:
            print(f"  ✗ Failed to generate DOT")
    
    print(f"\n{'='*70}")
    print(f"Extraction complete!")
    print(f"Total extracted: {extracted_count} pairs")
    print(f"Output directory: {output_dir}")
    print(f"{'='*70}")
    
    return extracted_count


if __name__ == "__main__":
    count = main()
    sys.exit(0 if count > 0 else 1)
