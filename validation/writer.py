"""Atomic JSONL writer with deduplication support.

Provides safe, resumable writing of training data records with automatic
deduplication based on record IDs.
"""

import json
import os
from pathlib import Path
from typing import Set, Optional
from validation.schema import DataRecord


class JSONLWriter:
    """Atomic JSONL file writer with deduplication.
    
    Supports resume capability by loading existing IDs from the output file
    and skipping duplicates during writing.
    
    Attributes:
        output_path: Path to JSONL output file
        existing_ids: Set of IDs already present in file
    """
    
    def __init__(self, output_path: str):
        """Initialize writer.
        
        Args:
            output_path: Path to JSONL output file
        """
        self.output_path = Path(output_path)
        self.existing_ids: Set[str] = set()
        
        # Create parent directory if needed
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing IDs for resume capability
        if self.output_path.exists():
            self._load_existing_ids()
    
    def _load_existing_ids(self):
        """Load existing record IDs from output file."""
        try:
            with open(self.output_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            record = json.loads(line)
                            if 'id' in record:
                                self.existing_ids.add(record['id'])
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            # If we can't read the file, start fresh
            self.existing_ids = set()
    
    def is_duplicate(self, record_id: str) -> bool:
        """Check if record ID already exists.
        
        Args:
            record_id: Record ID to check
            
        Returns:
            True if ID already exists in output file
        """
        return record_id in self.existing_ids
    
    def append(self, record: DataRecord) -> bool:
        """Append record to JSONL file.
        
        Atomically appends a single line to the JSONL file. Skips duplicates
        based on record ID.
        
        Args:
            record: DataRecord to write
            
        Returns:
            True if record was written, False if skipped (duplicate)
            
        Raises:
            IOError: If write fails (e.g., disk full)
        """
        # Check for duplicate
        if self.is_duplicate(record.id):
            return False
        
        # Validate record
        is_valid, error = record.validate()
        if not is_valid:
            raise ValueError(f"Invalid record: {error}")
        
        # Atomic append (single line write)
        try:
            with open(self.output_path, 'a', encoding='utf-8') as f:
                f.write(record.to_json() + '\n')
            
            # Update existing IDs
            self.existing_ids.add(record.id)
            return True
            
        except IOError as e:
            if "No space left on device" in str(e):
                raise IOError(f"Disk full, cannot write to {self.output_path}")
            raise
    
    def count_existing(self) -> int:
        """Get count of existing records.
        
        Returns:
            Number of records already in file
        """
        return len(self.existing_ids)
    
    def get_output_path(self) -> Path:
        """Get output file path.
        
        Returns:
            Path object for output file
        """
        return self.output_path
