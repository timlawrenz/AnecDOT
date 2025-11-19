"""
DOT validation and JSONL output formatting.
"""

import subprocess
import tempfile
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class TrainingPair:
    """Training pair in AnecDOT schema."""
    id: str
    source: str
    license: str
    task_type: str
    input_text: str
    context_snippet: Optional[str]
    output_dot: str
    verification_status: str
    
    def to_jsonl(self) -> str:
        """Convert to JSONL format."""
        return json.dumps(asdict(self))


def validate_dot_syntax(dot_code: str) -> tuple[bool, Optional[str]]:
    """Validate DOT code using Graphviz compiler.
    
    Args:
        dot_code: DOT graph code to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as f:
            f.write(dot_code)
            dot_file = f.name
        
        result = subprocess.run(
            ['dot', '-Tpng', dot_file, '-o', '/dev/null'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        Path(dot_file).unlink()
        
        if result.returncode == 0:
            return True, None
        else:
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except FileNotFoundError:
        return False, "Graphviz not installed (dot command not found)"
    except Exception as e:
        return False, str(e)


def create_training_pair(
    prompt: str,
    dot_output: str,
    provider: str,
    model: str,
    validation_passed: bool
) -> TrainingPair:
    """Create a training pair from generation result.
    
    Args:
        prompt: Natural language input
        dot_output: Generated DOT code
        provider: Provider name (gemini, ollama)
        model: Model name
        validation_passed: Whether DOT compiled successfully
        
    Returns:
        TrainingPair ready for JSONL output
    """
    # Generate unique ID
    content = f"{prompt}{dot_output}"
    pair_id = f"synthetic_{hashlib.md5(content.encode()).hexdigest()[:8]}"
    
    # Source attribution
    source = f"synthetic-{provider}-{model}"
    
    return TrainingPair(
        id=pair_id,
        source=source,
        license="synthetic-generated",
        task_type="NL_TO_DOT",
        input_text=prompt,
        context_snippet=None,
        output_dot=dot_output,
        verification_status="passed_compiler" if validation_passed else "failed_compiler"
    )


def write_jsonl(pairs: list[TrainingPair], output_file: Path, append: bool = False):
    """Write training pairs to JSONL file.
    
    Args:
        pairs: List of training pairs
        output_file: Output file path
        append: If True, append to existing file
    """
    mode = 'a' if append else 'w'
    
    with open(output_file, mode) as f:
        for pair in pairs:
            f.write(pair.to_jsonl() + '\n')


def calculate_cost(tokens_used: Optional[dict], provider: str, model: str) -> float:
    """Calculate estimated API cost.
    
    Args:
        tokens_used: Dict with 'input' and 'output' token counts
        provider: Provider name
        model: Model name
        
    Returns:
        Estimated cost in USD
    """
    if provider == "ollama":
        return 0.0  # Local models are free
    
    if not tokens_used:
        return 0.0
    
    # Pricing per 1M tokens (Nov 2024)
    pricing = {
        "gemini-2.5-flash": {
            "input": 0.00001875,
            "output": 0.000075
        },
        "gemini-2.5-pro": {
            "input": 0.00125,
            "output": 0.005
        },
        "gemini-3-pro-preview": {
            "input": 0.00125,
            "output": 0.005
        }
    }
    
    if model not in pricing:
        return 0.0
    
    rates = pricing[model]
    cost = (
        (tokens_used.get("input", 0) / 1000) * rates["input"] +
        (tokens_used.get("output", 0) / 1000) * rates["output"]
    )
    
    return cost
