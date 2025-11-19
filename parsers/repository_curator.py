"""
Repository curator for FSM library extraction.

Helps find and curate GitHub repositories using python-statemachine
or transitions libraries for DOT extraction.
"""

import json
from pathlib import Path
from typing import List, Dict
import requests


def search_github_repos(query: str, max_results: int = 50) -> List[Dict]:
    """Search GitHub repositories using code search.
    
    Note: This uses the GitHub API which you can access via the MCP tools.
    For actual usage, use the github-mcp-server-search_code tool.
    """
    print(f"Search query: {query}")
    print(f"Max results: {max_results}")
    print("\nThis is a template - use GitHub MCP tools to actually search!")
    return []


def analyze_repository(repo_data: Dict) -> Dict:
    """Analyze a repository for suitability.
    
    Returns scoring metrics:
    - has_license: bool
    - license_ok: bool (OSI-approved)
    - size_score: int (0-10)
    - activity_score: int (0-10)
    - quality_score: int (0-10)
    """
    return {
        "name": repo_data.get("full_name", "unknown"),
        "url": repo_data.get("html_url", ""),
        "license": repo_data.get("license", {}).get("key", "unknown"),
        "stars": repo_data.get("stargazers_count", 0),
        "description": repo_data.get("description", ""),
        "language": repo_data.get("language", ""),
    }


def filter_by_license(repos: List[Dict]) -> List[Dict]:
    """Filter repositories to only OSI-approved licenses."""
    approved_licenses = {
        'mit', 'apache-2.0', 'bsd-2-clause', 'bsd-3-clause',
        'isc', 'mpl-2.0', 'lgpl-3.0', 'gpl-3.0'
    }
    
    filtered = []
    for repo in repos:
        license_key = repo.get('license', 'unknown').lower()
        if license_key in approved_licenses:
            filtered.append(repo)
    
    return filtered


def create_curated_list():
    """Generate a curated repository list for manual review."""
    
    # Recommended search queries
    queries = [
        "from statemachine import StateMachine language:Python",
        "from transitions.extensions import GraphMachine language:Python"
    ]
    
    print("=" * 70)
    print("FSM REPOSITORY CURATOR")
    print("=" * 70)
    print("\nRecommended GitHub Code Search Queries:")
    print()
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")
    
    print("\n" + "=" * 70)
    print("FILTERING CRITERIA")
    print("=" * 70)
    print("\n✓ OSI-Approved Licenses:")
    print("  - MIT, Apache-2.0, BSD-2/3-Clause, ISC, MPL-2.0")
    print("  - LGPL-3.0, GPL-3.0 (with attribution)")
    print("\n✗ Skip:")
    print("  - AGPL (copyleft concerns)")
    print("  - No license / Proprietary")
    print("  - Forks (use original)")
    
    print("\n" + "=" * 70)
    print("QUALITY INDICATORS")
    print("=" * 70)
    print("\n• Stars: >10 (shows usage)")
    print("• Size: >100 KB (real project, not toy example)")
    print("• Activity: Updated in last 2 years")
    print("• Files: Has examples/ or tests/ directories")
    print("• Documentation: Has README")
    
    print("\n" + "=" * 70)
    print("MANUAL CURATION WORKFLOW")
    print("=" * 70)
    print("""
1. Use GitHub MCP search tool to find repositories
2. Review each repository:
   - Check LICENSE file
   - Look for actual FSM usage (not just imports)
   - Verify it's not a tutorial/homework project
   - Check if repo is still maintained
3. Clone promising repositories locally
4. Run FSM extractor to see what you get
5. Keep successful repositories in a curated list
    """)
    
    return queries


if __name__ == '__main__':
    create_curated_list()
