"""
Post-processing fixes for generated DOT graphs.

Based on Phase II.2 failure analysis, implements automatic corrections
for common syntax errors to improve success rate from 63% to ~70-74%.
"""

import re
from typing import Optional


def fix_common_syntax_errors(dot_code: str) -> str:
    """Apply common syntax error fixes to DOT code.
    
    Fixes:
    1. Backticks → quotes (digraph `name` → digraph "name")
    2. Escape sequence errors (\l misuse)
    3. Edge operator mistakes (-- → -> in digraph)
    4. Missing closing braces
    5. Quote mismatches
    
    Args:
        dot_code: Raw DOT code (possibly with syntax errors)
        
    Returns:
        Fixed DOT code
    """
    if not dot_code:
        return dot_code
    
    fixed = dot_code
    
    # Fix 1: Replace backticks with quotes in graph declaration
    # digraph `name` → digraph "name"
    fixed = re.sub(r'(digraph|graph)\s+`([^`]+)`', r'\1 "\2"', fixed)
    
    # Fix 2: Remove invalid \l escape sequences in labels
    # These should only appear at end of label for left-justification
    # Remove them if they appear mid-label or incorrectly
    fixed = re.sub(r'label="([^"]*?)\\l\s*"', r'label="\1"', fixed)
    
    # Fix 3: Replace undirected edges (--) with directed (->) in digraph
    if fixed.strip().startswith('digraph'):
        # Only fix -- that are edge operators, not in labels/strings
        # Look for pattern: identifier -- identifier
        fixed = re.sub(r'(\w+)\s+--\s+(\w+)', r'\1 -> \2', fixed)
        fixed = re.sub(r'("[\w\s]+")\s+--\s+("[\w\s]+")', r'\1 -> \2', fixed)
    
    # Fix 4: Add missing closing brace if needed
    if '{' in fixed and fixed.count('{') != fixed.count('}'):
        open_braces = fixed.count('{')
        close_braces = fixed.count('}')
        if open_braces > close_braces:
            # Add missing closing braces at end
            fixed += '\n' + '}' * (open_braces - close_braces)
    
    # Fix 5: Basic quote mismatch fixes
    # Count quotes, if odd number, try to close at end
    quote_count = fixed.count('"') - fixed.count('\\"')
    if quote_count % 2 != 0:
        # Add closing quote before last closing brace
        if fixed.rstrip().endswith('}'):
            fixed = fixed.rstrip()[:-1] + '"\n}'
    
    return fixed


def fix_html_label_errors(dot_code: str) -> str:
    """Fix common HTML label syntax errors.
    
    Fixes:
    1. Unclosed table tags
    2. Missing > in HTML-like labels
    3. Malformed table structures
    
    Args:
        dot_code: DOT code with potential HTML label errors
        
    Returns:
        Fixed DOT code
    """
    if not dot_code or '<table' not in dot_code.lower():
        return dot_code
    
    fixed = dot_code
    
    # Fix unclosed table tags
    # Count <table> vs </table>
    table_open = len(re.findall(r'<table[^>]*>', fixed, re.IGNORECASE))
    table_close = len(re.findall(r'</table>', fixed, re.IGNORECASE))
    
    if table_open > table_close:
        # Find positions where tables should be closed
        # Simple heuristic: add </table> before >] markers
        fixed = re.sub(r'(\s+>])', r'</table>\1', fixed, count=(table_open - table_close))
    
    return fixed


def postprocess_dot(dot_code: str) -> str:
    """Apply all post-processing fixes.
    
    Args:
        dot_code: Raw DOT code from model
        
    Returns:
        Fixed DOT code with better chance of being valid
    """
    if not dot_code:
        return dot_code
    
    # Apply fixes in sequence
    fixed = dot_code
    fixed = fix_common_syntax_errors(fixed)
    fixed = fix_html_label_errors(fixed)
    
    return fixed


def test_postprocessing():
    """Test post-processing on known failure patterns."""
    
    test_cases = [
        # Test 1: Backticks
        {
            'input': 'digraph `transitions` { a -> b; }',
            'expected': 'digraph "transitions" { a -> b; }',
            'name': 'Backtick replacement'
        },
        
        # Test 2: Wrong edge operator
        {
            'input': 'digraph G { a -- b; }',
            'expected': 'digraph G { a -> b; }',
            'name': 'Edge operator fix'
        },
        
        # Test 3: Missing closing brace
        {
            'input': 'digraph G { a -> b;',
            'expected': 'digraph G { a -> b;\n}',
            'name': 'Missing brace'
        },
        
        # Test 4: Invalid escape sequence
        {
            'input': 'digraph G { a [label="test\\l"]; }',
            'expected': 'digraph G { a [label="test"]; }',
            'name': 'Escape sequence fix'
        },
    ]
    
    print("Testing post-processing fixes...")
    print("=" * 70)
    
    passed = 0
    for test in test_cases:
        result = postprocess_dot(test['input'])
        if result.strip() == test['expected'].strip():
            print(f"✓ {test['name']}")
            passed += 1
        else:
            print(f"✗ {test['name']}")
            print(f"  Expected: {test['expected']}")
            print(f"  Got:      {result}")
    
    print("=" * 70)
    print(f"Passed: {passed}/{len(test_cases)}")
    
    return passed == len(test_cases)


if __name__ == "__main__":
    # Run tests
    success = test_postprocessing()
    exit(0 if success else 1)
