# DE-Utils

Developer Experience utilities and scripts for improving productivity.

## Contents

### GitHub CLI Extensions

Located in `src/`:

- **`gh-prs-md`** - Display open pull requests across multiple repositories in markdown format
- **`gh-recent-commits`** - Show recent commits from the last 7 days, filtered by author and grouped by repository

## GitHub CLI Scripts

### gh-prs-md

Displays open pull requests across multiple repositories with:
- PR status (APPROVED, REVIEW_REQUIRED, CHANGES_REQUESTED, DRAFT)
- Author and reviewers
- Time since opened
- Branch information

**Usage:**
```bash
export GH_REPOS="repo1 repo2 repo3"
gh prs-md
```

### gh-recent-commits

Shows recent commits from the last 7 days with:
- Multi-repository support
- Branch-aware searching
- Author filtering
- Clean markdown output with clickable links

**Usage:**
```bash
export GH_REPOS="repo1 repo2 repo3"
export COMMIT_AUTHOR="your_username"  # optional
gh recent-commits
```

## Installation

1. Copy scripts to your local bin directory:
   ```bash
   cp src/gh-prs-md ~/.local/bin/
   cp src/gh-recent-commits ~/.local/bin/
   chmod +x ~/.local/bin/gh-prs-md ~/.local/bin/gh-recent-commits
   ```

2. Add GitHub CLI aliases to `~/.config/gh/config.yml`:
   ```yaml
   aliases:
     prs-md: '!GITHUB_TOKEN="${GH_GEI_TOKEN:-$GITHUB_TOKEN}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-prs-md'
     recent-commits: '!GITHUB_TOKEN="${GH_GEI_TOKEN:-$GITHUB_TOKEN}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-recent-commits'
   ```

## Requirements

- GitHub CLI (`gh`)
- `jq` for JSON processing
- Standard Unix tools (`date`, `sed`, `cut`, `paste`)

## Configuration

Both scripts use the `GH_REPOS` environment variable to specify which repositories to query:

```bash
export GH_REPOS="org/repo1 org/repo2 repo3"  # repo3 assumes default org
```

For authentication, the scripts use GitHub tokens in this order of preference:
1. `GH_GEI_TOKEN` (if set)
2. `GITHUB_TOKEN` (fallback)

## Documentation

For setup instructions and detailed usage, see the [`docs/`](./docs/) directory:

### Quick Start Guides
- **[docs/gh-prs-md-README.md](./docs/gh-prs-md-README.md)** - First-time setup for PR listing tool
- **[docs/gh-recent-commits-README.md](./docs/gh-recent-commits-README.md)** - First-time setup for recent commits tool

### Complete Guides  
- **[docs/gh-prs-md.md](./docs/gh-prs-md.md)** - Complete guide for the PR listing tool
- **[docs/gh-recent-commits.md](./docs/gh-recent-commits.md)** - Complete guide for the recent commits tool

### Overview
- **[docs/README.md](./docs/README.md)** - Documentation overview and navigation

## License

MIT License - see individual script files for details.
