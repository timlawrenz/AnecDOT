"""DOT code validation using Graphviz compiler.

Reusable validation component used by all data streams (documentation, logic,
synthetic) and Phase II training validation. Ensures syntactic correctness
using the official Graphviz compiler.
"""

from dataclasses import dataclass
from typing import Optional, List, Callable
import subprocess
import shutil
import hashlib
import time
import platform
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed


class GraphvizNotFoundError(Exception):
    """Raised when Graphviz dot command is not found."""
    
    def __init__(self):
        system = platform.system()
        if system == "Linux":
            install_cmd = "sudo apt-get install graphviz"
        elif system == "Darwin":
            install_cmd = "brew install graphviz"
        elif system == "Windows":
            install_cmd = "choco install graphviz or download from graphviz.org"
        else:
            install_cmd = "See graphviz.org for installation instructions"
        
        super().__init__(
            f"Graphviz 'dot' command not found in PATH.\n"
            f"Install with: {install_cmd}"
        )


@dataclass
class ValidationResult:
    """Result of DOT code validation.
    
    Attributes:
        is_valid: True if DOT code compiled successfully
        error_message: Compiler error message (if validation failed)
        validation_method: Method used ("graphviz_compiler")
        compiler_version: Graphviz version string
        validation_duration: Time taken in seconds
    """
    
    is_valid: bool
    error_message: Optional[str] = None
    validation_method: str = "graphviz_compiler"
    compiler_version: Optional[str] = None
    validation_duration: float = 0.0
    
    def to_schema_status(self) -> str:
        """Convert to schema verification_status enum."""
        return "passed_compiler" if self.is_valid else "failed_compiler"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "is_valid": self.is_valid,
            "error_message": self.error_message,
            "validation_method": self.validation_method,
            "compiler_version": self.compiler_version,
            "validation_duration": self.validation_duration,
        }


# Global cache for validation results (LRU with max 1000 entries)
@lru_cache(maxsize=1000)
def _cached_validate(dot_code_hash: str, dot_code: str, timeout: int, strict: bool) -> ValidationResult:
    """Internal cached validation function."""
    return _validate_impl(dot_code, timeout, strict)


def validate_dot(
    dot_code: str,
    timeout: int = 10,
    strict: bool = False,
    use_cache: bool = True,
    output_format: str = "png"
) -> ValidationResult:
    """Validate DOT code using Graphviz compiler.
    
    Args:
        dot_code: DOT code string to validate
        timeout: Maximum seconds to wait for compilation (default: 10)
        strict: Treat warnings as errors (default: False)
        use_cache: Enable LRU caching of results (default: True)
        output_format: Graphviz output format to test (default: "png")
        
    Returns:
        ValidationResult with compilation status and diagnostics
        
    Raises:
        GraphvizNotFoundError: If dot command not found in PATH
    """
    # Check for empty input
    if not dot_code or not dot_code.strip():
        return ValidationResult(
            is_valid=False,
            error_message="Empty DOT code provided"
        )
    
    # Check size limit (10MB)
    if len(dot_code.encode('utf-8')) > 10 * 1024 * 1024:
        return ValidationResult(
            is_valid=False,
            error_message="DOT code exceeds maximum size limit (10MB)"
        )
    
    # Use cache if enabled
    if use_cache:
        dot_hash = hashlib.sha256(dot_code.encode('utf-8')).hexdigest()
        return _cached_validate(dot_hash, dot_code, timeout, strict)
    
    return _validate_impl(dot_code, timeout, strict, output_format)


def _validate_impl(
    dot_code: str,
    timeout: int,
    strict: bool,
    output_format: str = "png"
) -> ValidationResult:
    """Internal implementation of validation."""
    start_time = time.time()
    
    # Check if dot command exists
    dot_path = shutil.which("dot")
    if not dot_path:
        raise GraphvizNotFoundError()
    
    # Get compiler version
    compiler_version = _get_compiler_version()
    
    # Platform-specific null device
    null_device = "NUL" if platform.system() == "Windows" else "/dev/null"
    
    # Run dot compiler
    try:
        result = subprocess.run(
            ["dot", f"-T{output_format}", "-o", null_device],
            input=dot_code.encode('utf-8'),
            capture_output=True,
            timeout=timeout,
            check=False
        )
        
        duration = time.time() - start_time
        
        # Check for errors or warnings
        stderr = result.stderr.decode('utf-8', errors='replace')
        
        if result.returncode != 0:
            return ValidationResult(
                is_valid=False,
                error_message=stderr.strip() if stderr else f"Compilation failed with exit code {result.returncode}",
                compiler_version=compiler_version,
                validation_duration=duration
            )
        
        if strict and stderr:
            return ValidationResult(
                is_valid=False,
                error_message=f"Warnings treated as errors (strict mode): {stderr.strip()}",
                compiler_version=compiler_version,
                validation_duration=duration
            )
        
        return ValidationResult(
            is_valid=True,
            compiler_version=compiler_version,
            validation_duration=duration
        )
        
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return ValidationResult(
            is_valid=False,
            error_message=f"Compilation timeout after {timeout} seconds",
            compiler_version=compiler_version,
            validation_duration=duration
        )
    except Exception as e:
        duration = time.time() - start_time
        return ValidationResult(
            is_valid=False,
            error_message=f"Unexpected error: {str(e)}",
            compiler_version=compiler_version,
            validation_duration=duration
        )


def validate_batch(
    dot_codes: List[str],
    parallel: bool = False,
    max_workers: int = 4,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    **kwargs
) -> List[ValidationResult]:
    """Validate multiple DOT code samples.
    
    Args:
        dot_codes: List of DOT code strings
        parallel: Use parallel validation (default: False)
        max_workers: Number of parallel workers (default: 4)
        progress_callback: Optional callback(current, total) for progress
        **kwargs: Additional args passed to validate_dot()
        
    Returns:
        List of ValidationResult in same order as input
    """
    results = [None] * len(dot_codes)
    
    if parallel:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(validate_dot, code, **kwargs): idx
                for idx, code in enumerate(dot_codes)
            }
            
            completed = 0
            for future in as_completed(futures):
                idx = futures[future]
                results[idx] = future.result()
                completed += 1
                
                if progress_callback:
                    progress_callback(completed, len(dot_codes))
    else:
        for idx, code in enumerate(dot_codes):
            results[idx] = validate_dot(code, **kwargs)
            
            if progress_callback:
                progress_callback(idx + 1, len(dot_codes))
    
    return results


def get_cache_stats() -> dict:
    """Get LRU cache statistics.
    
    Returns:
        Dictionary with hits, misses, size, maxsize
    """
    info = _cached_validate.cache_info()
    return {
        "hits": info.hits,
        "misses": info.misses,
        "size": info.currsize,
        "maxsize": info.maxsize,
        "hit_rate": info.hits / (info.hits + info.misses) if (info.hits + info.misses) > 0 else 0.0
    }


def clear_cache():
    """Clear the validation cache."""
    _cached_validate.cache_clear()


def _get_compiler_version() -> Optional[str]:
    """Get Graphviz compiler version."""
    try:
        result = subprocess.run(
            ["dot", "-V"],
            capture_output=True,
            timeout=5,
            check=False
        )
        # dot -V outputs to stderr
        version = result.stderr.decode('utf-8', errors='replace').strip()
        return version if version else None
    except Exception:
        return None
