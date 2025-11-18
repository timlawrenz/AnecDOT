"""Tests for JSONL schema module."""

import pytest
from datetime import datetime
from validation.schema import DataRecord, validate_record


def test_create_valid_record():
    """Test creating a valid DataRecord."""
    record = DataRecord(
        id="test-123",
        source="test_source",
        source_url="https://example.com",
        license="EPL-2.0",
        task_type="NL_TO_DOT",
        input_text="Create a graph",
        output_dot="digraph { A -> B; }",
        verification_status="passed_compiler",
        scraped_at=datetime.utcnow().isoformat() + 'Z'
    )
    
    is_valid, error = record.validate()
    assert is_valid is True
    assert error is None


def test_record_to_dict():
    """Test converting record to dictionary."""
    record = DataRecord(
        id="test-456",
        source="test",
        source_url="https://example.com",
        license="EPL-2.0",
        task_type="CODE_TO_DOT",
        input_text="def foo(): pass",
        output_dot="digraph {}",
        verification_status="passed_compiler",
        scraped_at="2025-11-18T17:00:00Z"
    )
    
    data = record.to_dict()
    assert data['id'] == "test-456"
    assert data['source'] == "test"
    assert data['task_type'] == "CODE_TO_DOT"


def test_record_to_json():
    """Test converting record to JSON string."""
    record = DataRecord(
        id="test-789",
        source="test",
        source_url="https://example.com",
        license="EPL-2.0",
        task_type="NL_TO_DOT",
        input_text="Test",
        output_dot="digraph {}",
        verification_status="passed_compiler",
        scraped_at="2025-11-18T17:00:00Z"
    )
    
    json_str = record.to_json()
    assert isinstance(json_str, str)
    assert '"id": "test-789"' in json_str


def test_record_from_dict():
    """Test creating record from dictionary."""
    data = {
        'id': 'test-dict',
        'source': 'test',
        'source_url': 'https://example.com',
        'license': 'EPL-2.0',
        'task_type': 'NL_TO_DOT',
        'input_text': 'Test input',
        'output_dot': 'digraph {}',
        'verification_status': 'passed_compiler',
        'scraped_at': '2025-11-18T17:00:00Z'
    }
    
    record = DataRecord.from_dict(data)
    assert record.id == 'test-dict'
    assert record.source == 'test'


def test_validate_invalid_task_type():
    """Test validation fails with invalid task_type."""
    record = DataRecord(
        id="test",
        source="test",
        source_url="https://example.com",
        license="EPL-2.0",
        task_type="INVALID_TYPE",
        input_text="Test",
        output_dot="digraph {}",
        verification_status="passed_compiler",
        scraped_at="2025-11-18T17:00:00Z"
    )
    
    is_valid, error = record.validate()
    assert is_valid is False
    assert "task_type" in error


def test_validate_invalid_verification_status():
    """Test validation fails with invalid verification_status."""
    record = DataRecord(
        id="test",
        source="test",
        source_url="https://example.com",
        license="EPL-2.0",
        task_type="NL_TO_DOT",
        input_text="Test",
        output_dot="digraph {}",
        verification_status="invalid_status",
        scraped_at="2025-11-18T17:00:00Z"
    )
    
    is_valid, error = record.validate()
    assert is_valid is False
    assert "verification_status" in error


def test_validate_empty_fields():
    """Test validation fails with empty required fields."""
    record = DataRecord(
        id="",  # Empty ID
        source="test",
        source_url="https://example.com",
        license="EPL-2.0",
        task_type="NL_TO_DOT",
        input_text="Test",
        output_dot="digraph {}",
        verification_status="passed_compiler",
        scraped_at="2025-11-18T17:00:00Z"
    )
    
    is_valid, error = record.validate()
    assert is_valid is False
    assert "id" in error


def test_validate_record_dict():
    """Test validate_record function with dictionary."""
    data = {
        'id': 'test',
        'source': 'test',
        'source_url': 'https://example.com',
        'license': 'EPL-2.0',
        'task_type': 'NL_TO_DOT',
        'input_text': 'Test',
        'output_dot': 'digraph {}',
        'verification_status': 'passed_compiler',
        'scraped_at': '2025-11-18T17:00:00Z'
    }
    
    is_valid, error = validate_record(data)
    assert is_valid is True


def test_validate_invalid_timestamp():
    """Test validation fails with invalid ISO 8601 timestamp."""
    record = DataRecord(
        id="test",
        source="test",
        source_url="https://example.com",
        license="EPL-2.0",
        task_type="NL_TO_DOT",
        input_text="Test",
        output_dot="digraph {}",
        verification_status="passed_compiler",
        scraped_at="not-a-timestamp"
    )
    
    is_valid, error = record.validate()
    assert is_valid is False
    assert "scraped_at" in error


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
