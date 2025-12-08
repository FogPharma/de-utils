# gh uncommitted-md - Setup Guide

A GitHub CLI alias that displays uncommitted changes and stashes across multiple local git repositories in markdown format.

## First-Time Setup

### Prerequisites

Install required tools:
```bash
# GitHub CLI (optional, only needed for the alias)
# macOS:
brew install gh
# Ubuntu/Debian:
sudo apt install gh
# Or download from: https://cli.github.com/

# Git (required)
# macOS:
brew install git
# Ubuntu/Debian:
sudo apt install git
```

### Step-by-Step Installation

#### 1. Install the Script

```bash
# Create local bin directory if it doesn't exist
mkdir -p ~/.local/bin

# Copy the script to your local bin
cp src/gh-uncommitted-md ~/.local/bin/

# Make it executable
chmod +x ~/.local/bin/gh-uncommitted-md

# Add to PATH if not already there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

#### 2. Configure GitHub CLI Alias

```bash
# The script automatically writes to PAPI/docs/uncommitted_changes.md
# and also outputs to stdout, so you can use it in pipes or aliases
gh alias set uncommitted-md '!~/.local/bin/gh-uncommitted-md'
```

**Alternative: Create a bash/zsh alias for more control:**
```bash
# Add to your ~/.bashrc or ~/.zshrc
alias uncommitted='gh uncommitted-md | tee ~/Documents/uncommitted-$(date +%Y%m%d).md'

# Usage after reloading shell:
uncommitted  # Shows output and saves to dated file
```

#### 3. Configure Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Required: List of repositories to check
export GH_REPOS="repo1 repo2 repo3"

# Examples:
export GH_REPOS="fog4j ML_models_production IaC-DataScience fogpy"

# Optional: Set base directory for repositories (defaults to ~/Documents/work)
export REPO_BASE_DIR="$HOME/Documents/work"
```

**Note:**
- Repository names should match the directory names in your `REPO_BASE_DIR`. The script extracts the repo name from `GH_REPOS` (handles both "org/repo" and "repo" formats).
- The script automatically writes output to `PAPI/docs/uncommitted_changes.md` (relative to `REPO_BASE_DIR`) while also outputting to stdout.

## Usage

### Basic Usage

```bash
# Display uncommitted changes and stashes for configured repositories
gh uncommitted-md
```

### One-time Repository Override

```bash
# Check different repositories for this run only
GH_REPOS="different-repo1 different-repo2" gh uncommitted-md
```

### Custom Base Directory

```bash
# Use a different base directory for this run
REPO_BASE_DIR="/path/to/repos" gh uncommitted-md
```

### Output File

The script automatically writes to `PAPI/docs/uncommitted_changes.md` (relative to your `REPO_BASE_DIR`). The output is also displayed on stdout, so you can still pipe it or redirect if needed:

```bash
# Output is automatically saved to PAPI/docs/uncommitted_changes.md
gh uncommitted-md

# You can also redirect to a different file if needed
gh uncommitted-md > custom-output.md
```

### Debug Mode

```bash
# Enable debug output to troubleshoot issues
DEBUG=1 gh uncommitted-md
```

## Sample Output

```
### fogpy
- **Branch:** main
- **Uncommitted changes:**
  - 3 modified, 1 added, 2 untracked
    - Modified: src/utils.py
    - Modified: tests/test_utils.py
    - Modified (staged): README.md
    - Added: new_feature.py
    - Untracked: temp_file.txt
    - Untracked: debug.log
- **Stashes:**
  - Total: 2 stash(es)
    - stash@{0}: [feature-branch] WIP: working on feature — 2024-01-15 14:30
    - stash@{1}: [main] experimental changes — 2024-01-14 09:15

### ML_models_production
- **Branch:** develop
- **Uncommitted changes:** None
- **Stashes:** None
```

## Troubleshooting

### Repository Not Found

If you see "Repository directory not found", check:
1. The repository name in `GH_REPOS` matches the directory name
2. The `REPO_BASE_DIR` is set correctly (defaults to `~/Documents/work`)
3. The directory actually exists

### Not a Git Repository

If you see "Not a git repository", ensure the directory contains a `.git` folder.

### Stash Dates Not Showing

The script tries multiple methods to extract stash dates. If dates don't appear:
1. Ensure your git version supports `git stash list --date=iso`
2. Check that stashes exist: `git stash list` in the repository

### Script Not Found

If you get "command not found":
1. Ensure `~/.local/bin` is in your PATH
2. Verify the script is executable: `chmod +x ~/.local/bin/gh-uncommitted-md`
3. Reload your shell configuration: `source ~/.bashrc` or `source ~/.zshrc`

