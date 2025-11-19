"""
FSM Extractor - Extract DOT training pairs from FSM libraries.

This module implements the Logic Stream data pipeline for extracting
(Code → DOT) training pairs from repositories using python-statemachine
and transitions libraries.
"""

from .detector import FSMDetector, FSMMatch, detect_fsm_patterns
from .sandbox import FSMSandbox, DotExtractionResult
from .extractor import FSMExtractor, TrainingPair, write_training_pair

__all__ = [
    "FSMDetector",
    "FSMMatch",
    "detect_fsm_patterns",
    "FSMSandbox",
    "DotExtractionResult",
    "FSMExtractor",
    "TrainingPair",
    "write_training_pair",
]
