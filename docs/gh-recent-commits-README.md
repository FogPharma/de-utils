# gh recent-commits - Setup Guide

A GitHub CLI alias that displays recent commits from the last 7 days across multiple repositories, filtered by author.

## First-Time Setup

### Prerequisites

Install required tools:
```bash
# GitHub CLI
# macOS:
brew install gh
# Ubuntu/Debian:
sudo apt install gh
# Or download from: https://cli.github.com/

# jq (JSON processor)
# macOS:
brew install jq
# Ubuntu/Debian:
sudo apt install jq
# CentOS/RHEL:
sudo yum install jq
```

### Step-by-Step Installation

#### 1. Authenticate with GitHub

```bash
gh auth login
```

#### 2. Install the Script

```bash
# Create local bin directory if it doesn't exist
mkdir -p ~/.local/bin

# Copy the script to your local bin
cp src/gh-recent-commits ~/.local/bin/

# Make it executable
chmod +x ~/.local/bin/gh-recent-commits

# Add to PATH if not already there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

#### 3. Configure GitHub CLI Alias

```bash
# Basic alias (output to terminal only)
gh alias set recent-commits '!GH_GEI_TOKEN="${GH_GEI_TOKEN:-}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-recent-commits'

# Or alias with file output (recommended)
gh alias set recent-commits '!GH_GEI_TOKEN="${GH_GEI_TOKEN:-}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-recent-commits | tee ~/Documents/my-recent-work.md'
```

**Alternative: Create a bash/zsh alias for more control:**
```bash
# Add to your ~/.bashrc or ~/.zshrc
alias my-work='gh recent-commits | tee ~/Documents/my-work-$(date +%Y%m%d).md'
alias weekly-summary='gh recent-commits | tee ~/Documents/weekly-summary-$(date +%Y-W%U).md'

# Usage after reloading shell:
my-work        # Shows output and saves to dated file
weekly-summary # Shows output and saves to weekly file
```

#### 4. Configure Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Required: List of repositories to query
export GH_REPOS="your-org/repo1 your-org/repo2 repo3"

# Required: Your author name(s) - THIS IS CRITICAL
export COMMIT_AUTHOR="your-github-username"

# Examples:
export GH_REPOS="fog4j ML_models_production IaC-DataScience"
export COMMIT_AUTHOR="john_doe"

# If you use multiple names in commits:
export COMMIT_AUTHOR="john_doe|John Doe|john@company.com"
```

#### 5. Find Your Commit Author Name

**Important:** The author filter must match exactly how your name appears in commits.

```bash
# Check your recent commits in a specific repo
gh api repos/your-org/your-repo/commits --jq '.[0].commit.author.name'

# Or check locally
git log --oneline -n 5 --pretty=format:"%an"

# Set the filter based on what you find
export COMMIT_AUTHOR="YourActualCommitName"
```

#### 6. Test the Setup

```bash
# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc

# Test the alias
gh recent-commits

# If no results, try debug mode
DEBUG=1 gh recent-commits
```

## Configuration Examples

### Single Author
```bash
export COMMIT_AUTHOR="alice"
```

### Multiple Author Names
If you commit under different names:
```bash
export COMMIT_AUTHOR="alice|Alice Smith|alice@company.com"
```

### Single Organization
```bash
export GH_REPOS="repo1 repo2 repo3"
# Interpreted as: your-org/repo1, your-org/repo2, etc.
```

### Multiple Organizations
```bash
export GH_REPOS="org1/repo1 org2/repo2 personal/repo3"
```

### One-time Overrides
```bash
# Different author for this run
COMMIT_AUTHOR="bob" gh recent-commits

# Different repositories
GH_REPOS="other-org/repo1 other-org/repo2" gh recent-commits

# Show all authors (not recommended for large repos)
COMMIT_AUTHOR=".*" gh recent-commits
```

## Quick Diagnostics

### Check Installation
```bash
# Check if tools are installed
which gh jq

# Check authentication
gh auth status

# Check environment variables
echo "GH_REPOS: $GH_REPOS"
echo "COMMIT_AUTHOR: $COMMIT_AUTHOR"
```

## Usage

```bash
# Basic usage
gh recent-commits

# Debug mode
DEBUG=1 gh recent-commits

# Save to file (if not using tee in alias)
gh recent-commits > my-work-$(date +%Y%m%d).md

# Different author
COMMIT_AUTHOR="teammate" gh recent-commits

# Using bash/zsh aliases (if configured)
my-work        # Shows output and saves to dated file
weekly-summary # Shows output and saves to weekly file
```

## Sample Output

When you run `gh recent-commits`, you'll see output like this (when viewed as rendered markdown):

---

### FogPharma/fog4j
- **6ed8f11** (2025-09-22) [feature/EN-1801_fog4j_reademe] docs: updated README — dvaron

### FogPharma/ML_models_production
- **abc1234** (2025-09-21) [main] fix: update model validation logic — Dave Varon
- **def5678** (2025-09-20) [feature/new-admet-model] feat: add new ADMET model for liver toxicity — varontron
- **789abcd** (2025-09-19) [hotfix/validation-bug] hotfix: fix validation error in production — dvaron

### FogPharma/IaC-DataScience
- **123cdef** (2025-09-22) [hotfix/EN-1836_increase-batch-memory] hotfix: increase batch memory to 64GB — dvaron
- **456789a** (2025-09-21) [feature/peptide-props] feat: add peptide property calculations — Dave Varon

### FogPharma/ML_model_dockers
- No commits in the last 7 days

### FogPharma/fogpy
- **987fed1** (2025-09-20) [ci/EN-1778_sop_compliance] ci: update workflows for SOP compliance — varontron

---

**Output Format Explained:**
- **Repository headers** with `### Organization/Repository`
- **Short commit SHA** (first 7 characters, clickable in some terminals)
- **Date** in YYYY-MM-DD format
- **Branch name** in square brackets
- **Commit message** (first line only)
- **Author name** as it appears in the commit
- **"No commits" message** for repositories with no matching commits

**What gets filtered:**
- Only shows commits from the last 7 days
- Only shows commits by authors matching your `COMMIT_AUTHOR` filter
- Searches ALL branches, not just main/master
- Each commit may appear multiple times if it exists on multiple branches

## Debug Mode
Enable detailed output to troubleshoot:
```bash
DEBUG=1 gh recent-commits
```

Debug output shows:
- Date range being searched
- Author filter being applied
- Each branch being processed
- Commits being skipped and why

## Common Issues

1. **"set GH_REPOS" error**
   ```bash
   export GH_REPOS="your-repo1 your-repo2"
   ```

2. **"No commits in the last 7 days" (when you know you have commits)**
   ```bash
   # Check your author filter matches exactly
   echo $COMMIT_AUTHOR

   # Test with broader filter to see all commits
   COMMIT_AUTHOR=".*" gh recent-commits

   # Find your actual commit author name
   gh api repos/your-org/your-repo/commits --jq '.[0].commit.author.name'
   ```

3. **"command not found: gh"** - Install GitHub CLI
4. **"command not found: jq"** - Install jq JSON processor
5. **Authentication errors** - Run `gh auth login`

---
For detailed usage information and advanced features, see [gh-recent-commits.md](./gh-recent-commits.md).
