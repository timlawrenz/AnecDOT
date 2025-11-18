"""Summary statistics tracking for scraper runs.

Provides consistent metrics collection across all data streams for
comparability and monitoring.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class ScraperMetrics:
    """Statistics for a scraper run.
    
    Attributes:
        total_found: Total examples discovered
        total_scraped: Examples successfully extracted
        validation_passed: Examples that passed DOT validation
        validation_failed: Examples that failed DOT validation
        duplicates_skipped: Examples skipped due to duplicate IDs
        examples_written: Final count of examples written to output
        start_time: ISO 8601 start timestamp
        end_time: ISO 8601 end timestamp (None if not finished)
    """
    
    total_found: int = 0
    total_scraped: int = 0
    validation_passed: int = 0
    validation_failed: int = 0
    duplicates_skipped: int = 0
    examples_written: int = 0
    start_time: str = ""
    end_time: str = ""
    
    def __post_init__(self):
        if not self.start_time:
            self.start_time = datetime.utcnow().isoformat() + 'Z'
    
    def increment(self, metric: str, count: int = 1):
        """Increment a metric counter."""
        if hasattr(self, metric):
            setattr(self, metric, getattr(self, metric) + count)
    
    def finish(self):
        """Mark the run as finished with end timestamp."""
        self.end_time = datetime.utcnow().isoformat() + 'Z'
    
    def pass_rate(self) -> float:
        """Calculate validation pass rate as percentage."""
        total = self.validation_passed + self.validation_failed
        if total == 0:
            return 0.0
        return (self.validation_passed / total) * 100
    
    def duration_seconds(self) -> float:
        """Calculate run duration in seconds."""
        if not self.end_time:
            return 0.0
        start = datetime.fromisoformat(self.start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(self.end_time.replace('Z', '+00:00'))
        return (end - start).total_seconds()
    
    def summary(self) -> str:
        """Generate human-readable summary."""
        duration = self.duration_seconds()
        return f"""
Scraper Run Summary
===================
Total examples found:    {self.total_found}
Examples scraped:        {self.total_scraped}
Validation passed:       {self.validation_passed}
Validation failed:       {self.validation_failed}
Pass rate:               {self.pass_rate():.1f}%
Duplicates skipped:      {self.duplicates_skipped}
Examples written:        {self.examples_written}
Duration:                {duration:.1f}s
""".strip()
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), indent=2)
