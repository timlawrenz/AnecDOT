"""Tests for DOT validator module."""

import pytest
from validation.dot_validator import (
    validate_dot,
    validate_batch,
    GraphvizNotFoundError,
    get_cache_stats,
    clear_cache
)


def test_validate_valid_dot():
    """Test validation of syntactically correct DOT code."""
    dot_code = "digraph { A -> B; }"
    result = validate_dot(dot_code)
    
    assert result.is_valid is True
    assert result.error_message is None
    assert result.validation_method == "graphviz_compiler"
    assert result.compiler_version is not None
    assert result.validation_duration >= 0


def test_validate_invalid_dot():
    """Test validation of syntactically incorrect DOT code."""
    # Mixing directed and undirected edge syntax
    dot_code = "digraph { A -- B; }"
    result = validate_dot(dot_code)
    
    assert result.is_valid is False
    assert result.error_message is not None
    assert "syntax" in result.error_message.lower() or "error" in result.error_message.lower()


def test_validate_empty_dot():
    """Test validation of empty DOT code."""
    result = validate_dot("")
    
    assert result.is_valid is False
    assert "empty" in result.error_message.lower()


def test_validate_large_dot():
    """Test validation of DOT code exceeding size limit."""
    # Create DOT code > 10MB
    large_dot = "digraph { " + "A -> B; " * 1_000_000 + " }"
    result = validate_dot(large_dot)
    
    assert result.is_valid is False
    assert "size limit" in result.error_message.lower()


def test_validate_with_cache():
    """Test that caching works for duplicate validations."""
    clear_cache()
    
    dot_code = "digraph test { X -> Y; }"
    
    # First validation
    result1 = validate_dot(dot_code, use_cache=True)
    assert result1.is_valid is True
    
    # Second validation (should be cached)
    result2 = validate_dot(dot_code, use_cache=True)
    assert result2.is_valid is True
    
    # Check cache stats
    stats = get_cache_stats()
    assert stats['hits'] > 0


def test_validate_without_cache():
    """Test validation with caching disabled."""
    dot_code = "digraph nocache { A -> B; }"
    
    result = validate_dot(dot_code, use_cache=False)
    assert result.is_valid is True


def test_validate_batch():
    """Test batch validation of multiple DOT codes."""
    dot_codes = [
        "digraph { A -> B; }",
        "digraph { C -> D; }",
        "digraph { X -- Y; }",  # Invalid (mixing syntax)
    ]
    
    results = validate_batch(dot_codes)
    
    assert len(results) == 3
    assert results[0].is_valid is True
    assert results[1].is_valid is True
    assert results[2].is_valid is False


def test_validate_batch_parallel():
    """Test parallel batch validation."""
    dot_codes = [f"digraph {{ A{i} -> B{i}; }}" for i in range(10)]
    
    results = validate_batch(dot_codes, parallel=True, max_workers=4)
    
    assert len(results) == 10
    assert all(r.is_valid for r in results)


def test_schema_status_conversion():
    """Test conversion to schema verification_status."""
    valid_result = validate_dot("digraph { A -> B; }")
    assert valid_result.to_schema_status() == "passed_compiler"
    
    invalid_result = validate_dot("invalid dot code")
    assert invalid_result.to_schema_status() == "failed_compiler"


def test_timeout_handling():
    """Test that timeout works (using a large graph)."""
    # Create a very large graph that might timeout with short limit
    huge_graph = "digraph { " + "; ".join([f"N{i} -> N{i+1}" for i in range(100000)]) + "; }"
    
    result = validate_dot(huge_graph, timeout=1)
    # May timeout or succeed depending on system, but should not crash
    assert isinstance(result.is_valid, bool)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
