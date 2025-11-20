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
    # Try to find DOT graph between common delimiters
    patterns = [
        r'```dot\n(.*?)```',
        r'```\n(digraph.*?)```',
        r'```\n(graph.*?)```',
        r'(digraph\s+\w*\s*{.*?})',
        r'(graph\s+\w*\s*{.*?})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # If no delimiters, try to find raw digraph/graph
    if response.strip().startswith(('digraph', 'graph')):
        return response.strip()
    
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
