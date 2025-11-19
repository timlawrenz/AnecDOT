"""
FSM DOT Extractor - Main module for extracting DOT from FSM libraries.

Coordinates static analysis, dynamic execution, and validation to produce
(Code → DOT) training pairs.
"""

import json
import hashlib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Iterator
from common.id_generator import generate_id
from validation.dot_validator import validate_dot, ValidationResult
from .detector import detect_fsm_patterns, FSMMatch
from .sandbox import FSMSandbox, DotExtractionResult


@dataclass
class TrainingPair:
    """A complete (Code → DOT) training pair.
    
    Matches the project JSONL schema with task_type: CODE_TO_DOT.
    """
    id: str
    source: str
    license: str
    task_type: str
    input_text: Optional[str]
    context_snippet: str
    output_dot: str
    verification_status: str


class FSMExtractor:
    """Extracts DOT training pairs from Python files containing FSM code."""
    
    def __init__(self, 
                 sandbox: Optional[FSMSandbox] = None,
                 max_context_chars: int = 2000):
        """Initialize extractor.
        
        Args:
            sandbox: Execution sandbox (creates default if None)
            max_context_chars: Maximum context snippet length
        """
        self.sandbox = sandbox or FSMSandbox(timeout=30)
        self.max_context_chars = max_context_chars
    
    def extract_from_file(self, 
                         file_path: Path,
                         source_repo: str,
                         license_type: str) -> Iterator[TrainingPair]:
        """Extract training pairs from a single Python file.
        
        Args:
            file_path: Path to Python source file
            source_repo: Repository name/URL for attribution
            license_type: License of source repository
            
        Yields:
            TrainingPair objects for each successfully extracted FSM
        """
        # Detect FSM patterns
        matches = detect_fsm_patterns(file_path)
        
        for match in matches:
            # Skip patterns without graph support
            if not match.has_graph_support:
                continue
            
            # Extract DOT using sandbox
            if match.library == "python-statemachine":
                result = self.sandbox.extract_dot_from_statemachine(match.source_code)
            elif match.library == "transitions":
                result = self.sandbox.extract_dot_from_transitions(match.source_code)
            else:
                continue
            
            if not result.success or not result.dot_output:
                continue
            
            # Validate DOT syntax
            validation = validate_dot(result.dot_output)
            
            # Prepare context snippet (truncate if needed)
            context = self._prepare_context(match.source_code)
            
            # Create training pair
            pair = TrainingPair(
                id=self._generate_pair_id(file_path, match),
                source=f"{source_repo}:{file_path.name}:{match.start_line}",
                license=license_type,
                task_type="CODE_TO_DOT",
                input_text=None,  # No natural language prompt for code-based extraction
                context_snippet=context,
                output_dot=result.dot_output,
                verification_status=validation.to_schema_status()
            )
            
            yield pair
    
    def _prepare_context(self, source_code: str) -> str:
        """Prepare context snippet with size limit.
        
        Args:
            source_code: Original FSM source code
            
        Returns:
            Truncated context if needed
        """
        if len(source_code) <= self.max_context_chars:
            return source_code
        
        # Truncate with ellipsis
        truncated = source_code[:self.max_context_chars - 10]
        # Try to truncate at line boundary
        last_newline = truncated.rfind('\n')
        if last_newline > self.max_context_chars * 0.8:
            truncated = truncated[:last_newline]
        
        return truncated + "\n# ..."
    
    def _generate_pair_id(self, file_path: Path, match: FSMMatch) -> str:
        """Generate unique ID for training pair.
        
        Args:
            file_path: Source file path
            match: FSM match information
            
        Returns:
            Unique identifier string
        """
        # Create stable hash from file path and line number
        unique_str = f"{file_path.name}:{match.start_line}:{match.library}"
        hash_suffix = hashlib.md5(unique_str.encode()).hexdigest()[:8]
        
        prefix = "logic_stream"
        return f"{prefix}_{hash_suffix}"


def write_training_pair(pair: TrainingPair, output_file: Path) -> None:
    """Write a training pair to JSONL file.
    
    Args:
        pair: Training pair to write
        output_file: Output JSONL file path
    """
    with output_file.open('a', encoding='utf-8') as f:
        json.dump(asdict(pair), f, ensure_ascii=False)
        f.write('\n')
