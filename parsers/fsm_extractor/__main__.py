"""
FSM Extractor - Command-line interface.

Extract (Code → DOT) training pairs from Python repositories containing
FSM library usage (python-statemachine, transitions).
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import List
from common.logging_config import setup_logger
from .detector import has_fsm_imports
from .extractor import FSMExtractor, write_training_pair


def scan_directory(directory: Path) -> List[Path]:
    """Scan directory for Python files with FSM imports.
    
    Args:
        directory: Directory to scan
        
    Returns:
        List of Python files containing FSM imports
    """
    python_files = []
    
    for py_file in directory.rglob("*.py"):
        # Skip common non-code directories
        if any(part in py_file.parts for part in ['__pycache__', '.git', '.tox', 'venv', 'env']):
            continue
        
        if has_fsm_imports(py_file):
            python_files.append(py_file)
    
    return python_files


def process_directory(directory: Path,
                     output_file: Path,
                     license_type: str,
                     dry_run: bool = False,
                     verbose: bool = False) -> dict:
    """Process a directory for FSM code extraction.
    
    Args:
        directory: Directory to process
        output_file: Output JSONL file path
        license_type: License of source code
        dry_run: If True, don't write output file
        verbose: If True, show detailed progress
        
    Returns:
        Statistics dictionary
    """
    logger = logging.getLogger(__name__)
    
    # Scan for candidate files
    logger.info(f"Scanning {directory} for FSM code...")
    python_files = scan_directory(directory)
    logger.info(f"Found {len(python_files)} Python files with FSM imports")
    
    if not python_files:
        return {
            'files_scanned': 0,
            'pairs_extracted': 0,
            'pairs_valid': 0,
            'pairs_invalid': 0
        }
    
    # Initialize extractor
    extractor = FSMExtractor()
    
    stats = {
        'files_scanned': 0,
        'pairs_extracted': 0,
        'pairs_valid': 0,
        'pairs_invalid': 0
    }
    
    # Process each file
    for py_file in python_files:
        stats['files_scanned'] += 1
        
        if verbose:
            logger.info(f"Processing {py_file.relative_to(directory)}...")
        
        try:
            for pair in extractor.extract_from_file(
                py_file,
                source_repo=directory.name,
                license_type=license_type
            ):
                stats['pairs_extracted'] += 1
                
                if pair.verification_status == "passed_compiler":
                    stats['pairs_valid'] += 1
                else:
                    stats['pairs_invalid'] += 1
                
                if verbose:
                    status = "✓" if pair.verification_status == "passed_compiler" else "✗"
                    logger.info(f"  {status} Extracted pair from {py_file.name}:{pair.source}")
                
                # Write to file (unless dry run)
                if not dry_run:
                    write_training_pair(pair, output_file)
        
        except Exception as e:
            logger.warning(f"Error processing {py_file}: {e}")
            continue
    
    return stats


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract DOT training pairs from FSM library code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process local directory
  python -m parsers.fsm_extractor --path /path/to/repo --license MIT

  # Process with custom output
  python -m parsers.fsm_extractor --path ./examples --license Apache-2.0 --output my-data.jsonl

  # Dry run to see what would be extracted
  python -m parsers.fsm_extractor --path ./test --license MIT --dry-run --verbose
        """
    )
    
    parser.add_argument(
        '--path',
        type=Path,
        required=True,
        help='Directory to scan for FSM code'
    )
    
    parser.add_argument(
        '--license',
        type=str,
        required=True,
        help='License type of source code (e.g., MIT, Apache-2.0)'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/logic-stream.jsonl'),
        help='Output JSONL file path (default: data/logic-stream.jsonl)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without writing output file'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed progress'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logger(name=__name__, level=log_level)
    logger = logging.getLogger(__name__)
    
    # Validate input
    if not args.path.exists():
        logger.error(f"Path does not exist: {args.path}")
        sys.exit(1)
    
    if not args.path.is_dir():
        logger.error(f"Path is not a directory: {args.path}")
        sys.exit(1)
    
    # Create output directory if needed
    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
    
    # Process directory
    logger.info(f"Starting FSM extraction from {args.path}")
    logger.info(f"License: {args.license}")
    logger.info(f"Output: {args.output if not args.dry_run else '(dry run - no output)'}")
    
    stats = process_directory(
        args.path,
        args.output,
        args.license,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    # Print summary
    print("\n" + "="*60)
    print("EXTRACTION SUMMARY")
    print("="*60)
    print(f"Files scanned:        {stats['files_scanned']}")
    print(f"Training pairs found: {stats['pairs_extracted']}")
    print(f"  Valid (compiled):   {stats['pairs_valid']}")
    print(f"  Invalid:            {stats['pairs_invalid']}")
    
    if stats['pairs_extracted'] > 0:
        success_rate = (stats['pairs_valid'] / stats['pairs_extracted']) * 100
        print(f"  Success rate:       {success_rate:.1f}%")
    
    if not args.dry_run and stats['pairs_extracted'] > 0:
        print(f"\nOutput written to: {args.output}")
    
    print("="*60)


if __name__ == '__main__':
    main()
