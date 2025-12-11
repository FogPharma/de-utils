# DE-Utils

Data Engineering utilities for workflow productivity.

## Overview

Tools for GitHub repository management and compliance:

- **`gh prs-md`** - Display open pull requests in markdown format with status, reviewers, and timing
- **`gh recent-commits`** - Show your recent commits from the last 7 days across all branches
- **`compliance`** - GitHub Enterprise SOP compliance auditing and tracking

All tools output clean markdown with clickable links and can save results to files for easy sharing.

## Quick Start

1. **Install prerequisites:** GitHub CLI (`gh`) and `jq`
2. **Copy scripts** from `src/` to `~/.local/bin/`
3. **Add GitHub CLI aliases** (see setup guides below)
4. **Configure repositories:** `export GH_REPOS="repo1 repo2 repo3"`
5. **Run the tools:** `gh prs-md` or `gh recent-commits`

## Sample Output

### Pull Requests (`gh prs-md`)
```
### FogPharma/my-repo
- [PR #42: Add new feature](https://github.com/FogPharma/my-repo/pull/42) — alice — feature/new-thing → main — opened 2d ago — REVIEW_REQUIRED — requested: @bob
```
or as rendered:
### FogPharma/my-repo
- [PR #42: Add new feature](https://github.com/FogPharma/my-repo/pull/42) — alice — feature/new-thing → main — opened 2d ago — REVIEW_REQUIRED — requested: @bob

### Recent Commits (`gh recent-commits`)
```
### FogPharma/my-repo
- **abc1234** (2025-09-22) [feature/new-thing] feat: add awesome feature — alice
```
or as rendered:
### FogPharma/my-repo
- **abc1234** (2025-09-22) [feature/new-thing] feat: add awesome feature — alice

## Documentation

### 🚀 First-Time Setup
- **[gh-prs-md Setup Guide](./docs/gh-prs-md-README.md)** - Install and configure the PR listing tool
- **[gh-recent-commits Setup Guide](./docs/gh-recent-commits-README.md)** - Install and configure the recent commits tool
- **[Compliance Setup Guide](./docs/compliance-setup.md)** - Install and configure compliance auditing

### 📖 Complete Guides
- **[gh-prs-md Complete Guide](./docs/gh-prs-md.md)** - Advanced features, customization, and troubleshooting
- **[gh-recent-commits Complete Guide](./docs/gh-recent-commits.md)** - Advanced filtering, performance tips, and integrations
- **[Compliance Implementation Summary](./docs/implementation-summary.md)** - Compliance automation overview
- **[Enablement Playbook](./docs/enablement-playbook.md)** - Training materials and quick reference

## Requirements

### For GitHub CLI Tools (`gh-prs-md`, `gh-recent-commits`)
- **GitHub CLI** (`gh`) - installed and authenticated
- **jq** - JSON processor
- **Standard Unix tools** - `date`, `sed`, `cut` (usually pre-installed)

### For Compliance Tools
- **Python 3.12+**
- **GitHub token** with repo read access
- **Notion integration token** (for Notion sync)
- See [Compliance Setup Guide](./docs/compliance-setup.md) for details


