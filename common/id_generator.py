"""Content-hash based ID generation for deduplication.

Generates deterministic IDs from DOT code content to enable automatic
deduplication across all data streams.
"""

import hashlib


def generate_id(output_dot: str, source_prefix: str = "") -> str:
    """Generate content-hash ID for a DOT code example.
    
    Uses SHA256 hash of the DOT code to create deterministic IDs. If the same
    DOT code appears in multiple sources, it will have the same hash, enabling
    global deduplication across all data streams.
    
    Args:
        output_dot: The DOT code to hash
        source_prefix: Optional source identifier (e.g., "graphviz-gallery")
        
    Returns:
        ID string in format "{source_prefix}-{hash}" or just "{hash}"
        
    Example:
        >>> generate_id("digraph { A -> B; }", "gallery")
        'gallery-a3f5b8c1d2e4f6a8'
    """
    # SHA256 hash of DOT code content
    content_hash = hashlib.sha256(output_dot.encode('utf-8')).hexdigest()
    
    # Use first 16 characters for reasonable collision resistance
    short_hash = content_hash[:16]
    
    if source_prefix:
        return f"{source_prefix}-{short_hash}"
    return short_hash


def extract_hash_from_id(id_string: str) -> str:
    """Extract the hash portion from an ID.
    
    Args:
        id_string: ID in format "{prefix}-{hash}" or just "{hash}"
        
    Returns:
        The hash portion of the ID
    """
    if '-' in id_string:
        return id_string.split('-', 1)[1]
    return id_string
