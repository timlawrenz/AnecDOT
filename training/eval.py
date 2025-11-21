"""
Evaluation utilities for AnecDOT training.

Measures:
- Validation loss
- DOT syntax validity (via graphviz parsing)
- Sample generation quality
"""

import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
import re


def is_valid_dot_syntax(dot_string: str) -> bool:
    """Check if DOT string is syntactically valid using graphviz."""
    try:
        # Write to temp file and validate with dot
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as f:
            f.write(dot_string)
            temp_path = f.name
        
        result = subprocess.run(
            ['dot', '-Tsvg', temp_path],
            capture_output=True,
            timeout=5
        )
        
        Path(temp_path).unlink()
        return result.returncode == 0
        
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False


def extract_dot_from_response(response: str) -> Optional[str]:
    """Extract DOT graph from model response."""
    # Remove common prompt/response prefixes
    prefixes_to_remove = [
        "<start_of_turn>model",
        "<|assistant|>",
        "model\n",  # Gemma sometimes adds this
        "user\n",   # Remove user prefix too
    ]
    
    cleaned_response = response
    for prefix in prefixes_to_remove:
        if prefix in cleaned_response:
            # Take everything after the last occurrence
            cleaned_response = cleaned_response.split(prefix)[-1]
    
    # Try to find DOT graph between common delimiters
    patterns = [
        r'```dot\n(.*?)```',
        r'```\n(digraph.*?)```',
        r'```\n(graph.*?)```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, cleaned_response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # Find digraph/graph with balanced braces
    # Look for 'digraph' or 'graph' followed by balanced {}
    for start_pattern in [r'\bdigraph\b', r'\bgraph\b']:
        match = re.search(start_pattern, cleaned_response, re.IGNORECASE)
        if match:
            start_pos = match.start()
            # Find balanced braces starting from this position
            dot_candidate = extract_balanced_braces(cleaned_response[start_pos:])
            if dot_candidate:
                return dot_candidate
    
    return None


def extract_balanced_braces(text: str) -> Optional[str]:
    """Extract text with balanced braces starting with digraph/graph."""
    brace_count = 0
    start_idx = text.find('{')
    if start_idx == -1:
        return None
    
    for i in range(start_idx, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return text[:i+1].strip()
    
    return None


def evaluate_generation(
    model,
    tokenizer,
    prompts: List[str],
    max_length: int = 512,
    temperature: float = 0.7
) -> Dict:
    """Evaluate model generation on a set of prompts."""
    
    valid_count = 0
    total_count = len(prompts)
    generations = []
    
    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id
        )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract DOT from response
        dot_graph = extract_dot_from_response(generated_text)
        
        is_valid = False
        if dot_graph:
            is_valid = is_valid_dot_syntax(dot_graph)
            if is_valid:
                valid_count += 1
        
        generations.append({
            "prompt": prompt,
            "generated": generated_text,
            "extracted_dot": dot_graph,
            "is_valid": is_valid
        })
    
    return {
        "total": total_count,
        "valid_syntax": valid_count,
        "validity_rate": valid_count / total_count if total_count > 0 else 0,
        "generations": generations
    }


def compute_metrics(eval_pred):
    """Compute metrics for HuggingFace Trainer."""
    # This is called by the Trainer during evaluation
    # For now, we'll rely on the default loss metric
    # Custom metrics can be added here
    return {}


if __name__ == "__main__":
    # Test DOT validation
    valid_dot = """
    digraph test {
        A -> B;
        B -> C;
    }
    """
    
    invalid_dot = """
    digraph test {
        A -> B
        B -> C  // Missing semicolons
    """
    
    print("Testing DOT validation:")
    print(f"  Valid DOT: {is_valid_dot_syntax(valid_dot)}")
    print(f"  Invalid DOT: {is_valid_dot_syntax(invalid_dot)}")
    
    # Test extraction
    response_with_code_block = """Here's the graph:
    ```dot
    digraph example {
        X -> Y;
    }
    ```
    """
    
    print("\nTesting DOT extraction:")
    extracted = extract_dot_from_response(response_with_code_block)
    print(f"  Extracted: {extracted[:50] if extracted else 'None'}...")
