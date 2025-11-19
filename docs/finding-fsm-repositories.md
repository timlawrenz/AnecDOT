# Finding FSM Repositories on GitHub

This guide shows you how to find and curate GitHub repositories for FSM DOT extraction.

## Quick Start

### Method 1: Using GitHub MCP Tools (Recommended)

We have built-in GitHub search capabilities! Use these searches:

```python
# Search for python-statemachine usage
github-mcp-server-search_code(
    query="from statemachine import StateMachine language:Python",
    perPage=50
)

# Search for transitions GraphMachine usage
github-mcp-server-search_code(
    query="from transitions.extensions import GraphMachine language:Python",
    perPage=50
)
```

### Method 2: GitHub Web Interface

Visit GitHub and use these search queries:

**Python-statemachine:**
```
"from statemachine import StateMachine" language:Python
```

**Transitions:**
```
"from transitions.extensions import GraphMachine" language:Python
```

**Add filters:**
- `license:mit` OR `license:apache-2.0` OR `license:bsd`
- `size:>100` (skip tiny repos)
- Sort by: Stars

## Initial Search Results

From GitHub code search, we found **10,288 files** using python-statemachine!

### Promising Repositories Found:

Based on initial search (20 results), here are potential candidates:

| Repository | Description | License | Notes |
|------------|-------------|---------|-------|
| KRSSG/robocup | RoboCup SSL main codebase | ? | Robotics FSM usage |
| Recursing/MySubredditsBot | Telegram bot for Reddit | ? | Bot state management |
| game-lecture/2023-2DGP | 2D Game Programming course | ? | Educational examples |
| opencodeiiita/SwarmShot | Zombie survival game | ? | Game AI states |
| FlynnByReference/IEEE-Region-5-Contest | Robotics competition | ? | Robot FSM control |

**Action Required:** Check each repository's LICENSE file before extraction!

## Filtering Criteria

### ✅ **Include** repositories with:
- OSI-approved licenses (MIT, Apache-2.0, BSD, ISC, MPL-2.0)
- Real-world usage (not homework/tutorials)
- Active maintenance (updated in last 2 years)
- Multiple FSM examples
- Stars > 10 (quality indicator)

### ❌ **Skip** repositories with:
- AGPL license (copyleft concerns)
- No license / Proprietary
- Fork repositories (use original instead)
- Single toy example
- Tutorial/homework projects

## Recommended Workflow

### Step 1: Search & Collect

Use GitHub search to find 50-100 potential repositories:

```bash
# Using GitHub CLI (if available)
gh search repos --license=mit "python-statemachine" --json fullName,url,license > candidates.json

# Or use the MCP tools interactively
```

### Step 2: Manual Review

For each candidate repository:

1. **Check LICENSE file**
   ```bash
   curl https://raw.githubusercontent.com/OWNER/REPO/main/LICENSE
   ```

2. **Check for FSM usage**
   - Look for files with `StateMachine` or `GraphMachine`
   - Verify it's actual usage, not just imports
   - Check if examples/ or tests/ directories exist

3. **Assess quality**
   - Stars count (>10 preferred)
   - Last commit date (within 2 years)
   - README quality
   - Active issues/PRs

### Step 3: Create Curated List

Save approved repositories to a file:

```text
# repos-to-process.txt
https://github.com/owner1/repo1  # MIT - Robotics state machine
https://github.com/owner2/repo2  # Apache-2.0 - Workflow engine
https://github.com/owner3/repo3  # BSD-3 - Game AI
```

### Step 4: Clone & Extract

```bash
# Clone repositories
while read repo; do
  git clone "$repo" /tmp/fsm-repos/$(basename $repo)
done < repos-to-process.txt

# Run FSM extractor on each
for dir in /tmp/fsm-repos/*/; do
  python -m parsers.fsm_extractor \
    --path "$dir" \
    --license MIT \
    --output data/logic-stream.jsonl \
    --verbose
done
```

## Sample Curation Script

```python
"""Quick repository checker."""
import requests

def check_license(owner, repo):
    """Check repository license via GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/license"
    resp = requests.get(url)
    if resp.ok:
        return resp.json().get('license', {}).get('key')
    return None

# Check a repository
license_key = check_license("KRSSG", "robocup")
print(f"License: {license_key}")
```

## Expected Yield

Based on search results:

- **python-statemachine**: 10,288 code files found
- **Estimated repositories**: ~500-1000 unique repos
- **After filtering**: ~50-100 suitable repos
- **Expected training pairs**: 100-500 pairs

## Quality Targets

Our goal for Phase I.2:

- **Minimum**: 50 valid (Code → DOT) pairs
- **Target**: 100-200 pairs
- **Stretch**: 300-500 pairs
- **Compilation rate**: >90%

## Next Steps

1. ✅ Run GitHub code search (done)
2. ⏭️ Manual review of top 20 repositories
3. ⏭️ Check licenses and download
4. ⏭️ Run FSM extractor
5. ⏭️ Review output quality
6. ⏭️ Iterate and expand

## Resources

- [GitHub Code Search Syntax](https://docs.github.com/en/search-github/searching-on-github/searching-code)
- [OSI Approved Licenses](https://opensource.org/licenses)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api)

---

**Note**: Always respect repository licenses and rate limits. Attribute sources properly in the dataset.
