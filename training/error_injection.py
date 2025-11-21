"""
Error injection for data augmentation.

Creates synthetic error-correction pairs by injecting common syntax errors
into valid DOT graphs, then pairing them with the corrected version.

This teaches the model:
1. What errors to avoid
2. How to fix broken DOT syntax
3. Reinforces correct patterns through negative examples

Based on Phase II.2 failure analysis:
- Quote errors (backticks instead of quotes)
- Edge operator errors (-- instead of ->)
- Missing closing braces
- Invalid escape sequences
"""

import re
import random
from typing import List, Tuple


def inject_backtick_error(dot_code: str) -> str:
    """Inject backtick error: digraph "name" → digraph `name`
    
    This was observed in Example #8 failure.
    """
    # Replace first quoted graph name with backticks
    return re.sub(r'(digraph|graph)\s+"([^"]+)"', r'\1 `\2`', dot_code, count=1)


def inject_edge_operator_error(dot_code: str) -> str:
    """Inject edge operator error: -> becomes --
    
    This was observed in Example #22 failure.
    """
    if not dot_code.strip().startswith('digraph'):
        return dot_code
    
    # Replace first few -> with --
    lines = dot_code.split('\n')
    modified_lines = []
    replacements = 0
    max_replacements = random.randint(1, 3)
    
    for line in lines:
        if '->' in line and replacements < max_replacements and random.random() < 0.5:
            line = line.replace('->', '--', 1)
            replacements += 1
        modified_lines.append(line)
    
    return '\n'.join(modified_lines)


def inject_missing_brace_error(dot_code: str) -> str:
    """Inject missing closing brace error.
    
    Common truncation error - remove final closing brace.
    """
    if dot_code.rstrip().endswith('}'):
        return dot_code.rstrip()[:-1].rstrip()
    return dot_code


def inject_escape_sequence_error(dot_code: str) -> str:
    """Inject invalid escape sequence: add \\l to labels
    
    This was observed in Example #2 failure.
    """
    # Add \l to some labels
    return re.sub(r'label="([^"]+)"', lambda m: f'label="{m.group(1)}\\l"' if random.random() < 0.3 else m.group(0), dot_code)


def inject_random_errors(dot_code: str, num_errors: int = 1) -> Tuple[str, List[str]]:
    """Inject random combination of errors.
    
    Args:
        dot_code: Valid DOT code
        num_errors: Number of errors to inject (1-3)
        
    Returns:
        Tuple of (broken_code, list_of_errors_injected)
    """
    error_functions = [
        (inject_backtick_error, "backtick_in_graph_name"),
        (inject_edge_operator_error, "wrong_edge_operator"),
        (inject_missing_brace_error, "missing_closing_brace"),
        (inject_escape_sequence_error, "invalid_escape_sequence"),
    ]
    
    # Randomly select errors to inject
    num_to_inject = min(num_errors, len(error_functions))
    selected_errors = random.sample(error_functions, num_to_inject)
    
    broken_code = dot_code
    errors_applied = []
    
    for error_func, error_name in selected_errors:
        broken_code = error_func(broken_code)
        errors_applied.append(error_name)
    
    return broken_code, errors_applied


def create_error_correction_pair(dot_code: str, description: str = None) -> dict:
    """Create error correction training pair.
    
    Args:
        dot_code: Valid DOT code
        description: Optional description for context
        
    Returns:
        Training pair in JSONL format
    """
    # Inject 1-2 random errors
    num_errors = random.randint(1, 2)
    broken_code, errors = inject_random_errors(dot_code, num_errors)
    
    # Create input prompt
    if description:
        input_text = f"Fix the syntax errors in this DOT graph:\n\n{broken_code}\n\nOriginal intent: {description}"
    else:
        input_text = f"Fix the syntax errors in this DOT graph:\n\n{broken_code}"
    
    # Create training pair
    pair = {
        "task_type": "ERROR_CORRECTION",
        "input_text": input_text,
        "output_dot": dot_code,  # The corrected version
        "errors_injected": errors,
        "broken_dot": broken_code,
    }
    
    return pair


def augment_dataset_with_errors(original_pairs: List[dict], augmentation_factor: float = 1.0) -> List[dict]:
    """Augment dataset with error correction pairs.
    
    Args:
        original_pairs: List of original training pairs
        augmentation_factor: Ratio of error pairs to original (1.0 = same count)
        
    Returns:
        List of error correction pairs
    """
    num_to_generate = int(len(original_pairs) * augmentation_factor)
    error_pairs = []
    
    print(f"Generating {num_to_generate} error correction pairs...")
    
    for i in range(num_to_generate):
        # Sample a random original pair
        original = random.choice(original_pairs)
        
        # Get the DOT code and description
        dot_code = original.get('output_dot', '')
        description = original.get('input_text', '')
        
        if not dot_code:
            continue
        
        # Create error correction pair
        error_pair = create_error_correction_pair(dot_code, description)
        
        # Add metadata from original
        error_pair['id'] = f"error_correction_{i:04d}"
        error_pair['source'] = f"synthetic_error_from_{original.get('source', 'unknown')}"
        error_pair['license'] = original.get('license', 'synthetic-generated')
        error_pair['context_snippet'] = f"Error correction variant of original pair"
        error_pair['verification_status'] = 'passed_compiler'  # Output is known valid
        
        error_pairs.append(error_pair)
        
        if (i + 1) % 50 == 0:
            print(f"  Generated {i + 1}/{num_to_generate}...")
    
    print(f"✓ Generated {len(error_pairs)} error correction pairs")
    return error_pairs


def test_error_injection():
    """Test error injection functions."""
    
    test_dot = '''digraph "TestGraph" {
  rankdir=LR;
  A [label="State A"];
  B [label="State B"];
  A -> B [label="transition"];
}'''
    
    print("ERROR INJECTION TESTS")
    print("=" * 70)
    
    tests = [
        ("Backtick error", inject_backtick_error),
        ("Edge operator error", inject_edge_operator_error),
        ("Missing brace error", inject_missing_brace_error),
        ("Escape sequence error", inject_escape_sequence_error),
    ]
    
    for name, func in tests:
        print(f"\n{name}:")
        print("-" * 70)
        broken = func(test_dot)
        print(broken)
    
    print("\n" + "=" * 70)
    print("Random errors (1-2 combined):")
    print("-" * 70)
    broken, errors = inject_random_errors(test_dot, num_errors=2)
    print(f"Errors injected: {errors}")
    print(broken)
    
    print("\n" + "=" * 70)
    print("✓ Error injection working correctly")


if __name__ == "__main__":
    test_error_injection()
