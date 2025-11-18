"""JSONL data schema for AnecDOT training datasets.

This module defines the canonical schema for all data streams (documentation,
logic, synthetic). All scrapers must produce records conforming to this schema.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json


@dataclass
class DataRecord:
    """Training data record conforming to AnecDOT JSONL schema.
    
    All data streams (documentation, logic, synthetic) produce records with
    this schema. Fields marked Optional may be null depending on the source.
    
    Attributes:
        id: Unique identifier, format: "{source}-{content_hash}"
        source: Data stream identifier (e.g., "graphviz_gallery", "fsm_library")
        source_url: Full URL to original source (for attribution)
        license: License of source material (e.g., "EPL-2.0")
        task_type: Training task ("NL_TO_DOT" or "CODE_TO_DOT")
        input_text: Natural language instruction or source code
        context_snippet: Optional context (e.g., prior node output)
        output_dot: DOT code (exact formatting preserved)
        verification_status: Validation result ("passed_compiler", "failed_compiler")
        scraped_at: ISO 8601 timestamp of scraping
    """
    
    id: str
    source: str
    source_url: str
    license: str
    task_type: str
    input_text: str
    output_dot: str
    verification_status: str
    scraped_at: str
    context_snippet: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSONL serialization."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Serialize to JSON string (single line for JSONL)."""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: dict) -> "DataRecord":
        """Create DataRecord from dictionary."""
        return cls(**data)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate record fields.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields check
        if not self.id:
            return False, "id cannot be empty"
        if not self.source:
            return False, "source cannot be empty"
        if not self.source_url:
            return False, "source_url cannot be empty"
        if not self.license:
            return False, "license cannot be empty"
        if self.task_type not in ("NL_TO_DOT", "CODE_TO_DOT"):
            return False, f"task_type must be NL_TO_DOT or CODE_TO_DOT, got {self.task_type}"
        if not self.input_text:
            return False, "input_text cannot be empty"
        if not self.output_dot:
            return False, "output_dot cannot be empty"
        if self.verification_status not in ("passed_compiler", "failed_compiler"):
            return False, f"verification_status must be passed_compiler or failed_compiler, got {self.verification_status}"
        
        # ISO 8601 timestamp validation
        try:
            datetime.fromisoformat(self.scraped_at.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return False, f"scraped_at must be valid ISO 8601 timestamp, got {self.scraped_at}"
        
        return True, None


def validate_record(record: dict) -> tuple[bool, Optional[str]]:
    """Validate a dictionary against DataRecord schema.
    
    Args:
        record: Dictionary to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        dr = DataRecord.from_dict(record)
        return dr.validate()
    except TypeError as e:
        return False, f"Missing or invalid fields: {e}"
