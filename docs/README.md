# Documentation

This directory contains detailed documentation for each GitHub CLI alias in the DE-Utils collection.

## Available Aliases

### [gh prs-md](./gh-prs-md.md)
Display open pull requests across multiple repositories in markdown format.

**Quick Start:**
```bash
export GH_REPOS="repo1 repo2 repo3"
gh prs-md
```

### [gh recent-commits](./gh-recent-commits.md)
Show recent commits from the last 7 days, filtered by author and grouped by repository.

**Quick Start:**
```bash
export GH_REPOS="repo1 repo2 repo3"
export COMMIT_AUTHOR="your-username"
gh recent-commits
```

## First-Time Setup Guide

If you're new to these tools, follow these steps:

### 1. Prerequisites

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

### 2. Authenticate with GitHub

```bash
gh auth login
```

### 3. Install the Scripts

```bash
# Clone or download this repository
git clone <repository-url>
cd de-utils

# Install scripts
mkdir -p ~/.local/bin
cp src/* ~/.local/bin/
chmod +x ~/.local/bin/gh-*

# Add to PATH if not already there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

### 4. Configure GitHub CLI Aliases

```bash
# Add both aliases
gh alias set prs-md '!GITHUB_TOKEN="${GH_GEI_TOKEN:-$GITHUB_TOKEN}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-prs-md'
gh alias set recent-commits '!GITHUB_TOKEN="${GH_GEI_TOKEN:-$GITHUB_TOKEN}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-recent-commits'
```

### 5. Configure Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Required: List of repositories to query
export GH_REPOS="your-org/repo1 your-org/repo2 repo3"

# Required for recent-commits: Your author name(s)
export COMMIT_AUTHOR="your-github-username"

# Optional: Enable debug output
# export DEBUG=1
```

### 6. Test the Setup

```bash
# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc

# Test the aliases
gh prs-md
gh recent-commits
```

## Common Configuration Patterns

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

### Multiple Author Names

If you commit under different names or emails:

```bash
export COMMIT_AUTHOR="username|Real Name|email@domain.com"
```

## Troubleshooting

### Quick Diagnostics

```bash
# Check if tools are installed
which gh jq

# Check authentication
gh auth status

# Check environment variables
echo "GH_REPOS: $GH_REPOS"
echo "COMMIT_AUTHOR: $COMMIT_AUTHOR"

# Test repository access
gh repo view your-org/your-repo
```

### Common Issues

1. **"command not found: gh"** - Install GitHub CLI
2. **"command not found: jq"** - Install jq JSON processor
3. **"set GH_REPOS"** - Set the GH_REPOS environment variable
4. **Authentication errors** - Run `gh auth login`
5. **No commits found** - Check your COMMIT_AUTHOR matches your commit author name exactly

## Getting Help

- **Detailed documentation**: Read the individual alias documentation files
- **GitHub CLI help**: `gh --help` or `gh <command> --help`
- **Debug mode**: Set `DEBUG=1` to see detailed execution information
- **Test individual components**: Use `gh api` commands to test repository access

## Contributing

To contribute improvements or report issues:

1. Test your changes with debug mode enabled
2. Update documentation if you modify functionality
3. Ensure compatibility with both macOS and Linux
4. Test with multiple repository configurations
