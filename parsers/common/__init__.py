"""
Common utilities shared across parsers.

Re-exports validation utilities from the main validation module.
"""

from validation.dot_validator import DotValidator, ValidationResult

__all__ = ["DotValidator", "ValidationResult"]
