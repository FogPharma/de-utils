# gh prs-md - Setup Guide

A GitHub CLI alias that displays open pull requests across multiple repositories in markdown format.

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
cp src/gh-prs-md ~/.local/bin/

# Make it executable
chmod +x ~/.local/bin/gh-prs-md

# Add to PATH if not already there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

#### 3. Configure GitHub CLI Alias

```bash
# Basic alias (output to terminal only)
gh alias set prs-md '!GH_GEI_TOKEN="${GH_GEI_TOKEN:-}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-prs-md'

# Or alias with file output (recommended)
gh alias set prs-md '!GH_GEI_TOKEN="${GH_GEI_TOKEN:-}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-prs-md | tee ~/Documents/team-prs.md'
```

**Alternative: Create a bash/zsh alias for more control:**
```bash
# Add to your ~/.bashrc or ~/.zshrc
alias team-prs='gh prs-md | tee ~/Documents/team-prs-$(date +%Y%m%d).md'

# Usage after reloading shell:
team-prs  # Shows output and saves to dated file
```

#### 4. Configure Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Required: List of repositories to query
export GH_REPOS="your-org/repo1 your-org/repo2 repo3"

# Examples:
export GH_REPOS="fog4j ML_models_production IaC-DataScience"
export GH_REPOS="mycompany/frontend mycompany/backend mycompany/api"
```

#### 5. Test the Setup

```bash
# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc

# Test the alias
gh prs-md
```

## Configuration Examples

### Single Organization
If all your repositories are in the same organization:
```bash
export GH_REPOS="repo1 repo2 repo3 repo4"
# These will be interpreted as: your-org/repo1, your-org/repo2, etc.
```

### Multiple Organizations
For repositories across different organizations:
```bash
export GH_REPOS="org1/repo1 org2/repo2 personal-account/repo3"
```

### One-time Repository Override
```bash
# Query different repositories for this run only
GH_REPOS="different-org/repo1 different-org/repo2" gh prs-md
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

# Test repository access
gh repo view your-org/your-repo
```

## Usage

```bash
# Basic usage
gh prs-md

# Save to file (if not using tee in alias)
gh prs-md > team-prs-$(date +%Y%m%d).md

# Query specific repositories
GH_REPOS="repo1 repo2" gh prs-md

# Using the bash/zsh alias (if configured)
team-prs  # Shows output and saves to dated file
```

## Sample Output

When you run `gh prs-md`, you'll see output like this (when viewed as rendered markdown):

---

### FogPharma/fog4j
- [PR #3: EN-1801: updating project readme](https://github.com/FogPharma/fog4j/pull/3) — tlincoln-parabilis — feature/EN-1801_fog4j_reademe → v1.4.2 — opened 4d 18h ago — APPROVED — requested: @jspeizer-parabilis (no review yet)

### FogPharma/ML_models_production
- [PR #540: new models for bcat](https://github.com/FogPharma/ML_models_production/pull/540) — nmathai-fog — new_models_bcat_sep25 → test — opened 2d 16h ago — REVIEW_REQUIRED — requested: @varontron (no review yet),@johnsantamariajr (no review yet)
- [PR #536: Register model 1ca3626d5f9a1ecc4a5217c3c7438e5f by fkhalif on 20250918](https://github.com/FogPharma/ML_models_production/pull/536) — varontron — model-reg-20250918151653 → validation — opened 3d 19h ago — REVIEW_REQUIRED — no review requested

### FogPharma/ML_model_dockers
- No open PRs

### FogPharma/IaC-DataScience
- [PR #14: hotfix: EN-1836 increase batch memory to 64GB for v1.4.2](https://github.com/FogPharma/IaC-DataScience/pull/14) — varontron — hotfix/EN-1836_increase-batch-memory → v1.4.2 — opened 2d 21h ago — REVIEW_REQUIRED — requested: @jspeizer-parabilis (no review yet),@tlincoln-parabilis (no review yet)
- [PR #12: hotfix: EN-1656 peptide property calcs bugfix for v1.4.2](https://github.com/FogPharma/IaC-DataScience/pull/12) — varontron — hotfix/EN-1656_peptide-property-calcs-v1.4.2 → v1.4.2 — opened 2d 21h ago — REVIEW_REQUIRED — requested: @jspeizer-parabilis (no review yet),@tlincoln-parabilis (no review yet)

---

**Output Format Explained:**
- **Repository headers** with `### Organization/Repository`
- **Clickable PR links** with PR number and title
- **Author** who created the PR
- **Branch info** showing `source-branch → target-branch`
- **Time since opened** in human-readable format
- **Status** (APPROVED, REVIEW_REQUIRED, CHANGES_REQUESTED, DRAFT)
- **Requested reviewers** with their review status


## Common Issues

1. **"set GH_REPOS" error**
   ```bash
   # Make sure GH_REPOS is set
   echo $GH_REPOS
   # If empty, set it:
   export GH_REPOS="your-repo1 your-repo2"
   ```

2. **"command not found: gh"** - Install GitHub CLI
3. **"command not found: jq"** - Install jq JSON processor
4. **Authentication errors** - Run `gh auth login`
5. **Repository not found** - Check repository names and access permissions

---

For detailed usage information and advanced features, see [gh-prs-md.md](./gh-prs-md.md).
