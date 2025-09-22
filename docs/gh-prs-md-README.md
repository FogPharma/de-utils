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
# Add the alias
gh alias set prs-md '!GITHUB_TOKEN="${GH_GEI_TOKEN:-$GITHUB_TOKEN}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-prs-md'
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

### Common Issues

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

## Usage

```bash
# Basic usage
gh prs-md

# Save to file
gh prs-md > team-prs-$(date +%Y%m%d).md

# Query specific repositories
GH_REPOS="repo1 repo2" gh prs-md
```

For detailed usage information, see [gh-prs-md.md](./gh-prs-md.md).
