# gh prs-md

A GitHub CLI alias that displays open pull requests across multiple repositories in a clean markdown format.

## Purpose

This tool helps developers quickly review the status of open pull requests across multiple repositories without having to navigate to each repository individually. It provides a consolidated view with:

- PR status (APPROVED, REVIEW_REQUIRED, CHANGES_REQUESTED, DRAFT)
- Author and requested reviewers
- Time since the PR was opened
- Branch information (source → target)
- Direct links to each PR

## Output Example

```markdown
### FogPharma/fog4j
- [PR #3: EN-1801: updating project readme](https://github.com/FogPharma/fog4j/pull/3) — tlincoln-parabilis — feature/EN-1801_fog4j_reademe → v1.4.2 — opened 2d 3h ago — APPROVED — requested: @jspeizer-parabilis (no review yet)

### FogPharma/ML_models_production
- [PR #540: new models for bcat](https://github.com/FogPharma/ML_models_production/pull/540) — nmathai-fog — new_models_bcat_sep25 → test — opened 2d 16h ago — REVIEW_REQUIRED — requested: @varontron (no review yet),@johnsantamariajr (no review yet)

### FogPharma/IaC-DataScience
- [PR #14: hotfix: EN-1836 increase batch memory to 64GB for v1.4.2](https://github.com/FogPharma/IaC-DataScience/pull/14) — varontron — hotfix/EN-1836_increase-batch-memory → v1.4.2 — opened 6h 22m ago — REVIEW_REQUIRED — requested: @jspeizer-parabilis (no review yet),@tlincoln-parabilis (no review yet)
```

## Installation

### Prerequisites

- [GitHub CLI](https://cli.github.com/) installed and authenticated
- `jq` command-line JSON processor
- Access to the repositories you want to query

### Step 1: Install the Script

```bash
# Create local bin directory if it doesn't exist
mkdir -p ~/.local/bin

# Copy the script to your local bin
cp src/gh-prs-md ~/.local/bin/

# Make it executable
chmod +x ~/.local/bin/gh-prs-md

# Ensure ~/.local/bin is in your PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

### Step 2: Configure GitHub CLI Alias

Add the alias to your GitHub CLI configuration:

```bash
# Option 1: Use gh CLI to add the alias
gh alias set prs-md '!GH_GEI_TOKEN="${GH_GEI_TOKEN:-}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-prs-md'

# Option 2: Manually edit ~/.config/gh/config.yml
```

If editing manually, add this to your `~/.config/gh/config.yml`:

```yaml
aliases:
  prs-md: '!GH_GEI_TOKEN="${GH_GEI_TOKEN:-}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-prs-md'
```

## Configuration

### Required: Set Repository List

The script requires the `GH_REPOS` environment variable to know which repositories to query:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export GH_REPOS="repo1 repo2 repo3"

# For repositories in different organizations:
export GH_REPOS="myorg/repo1 myorg/repo2 anotherporg/repo3"

# Example with actual repositories:
export GH_REPOS="fog4j ML_models_production IaC-DataScience"
```

**Note:** Repository names without a slash (/) are assumed to be under your default organization. Include the full `org/repo` format for repositories in different organizations.

### Optional: Authentication Configuration

The script uses GitHub tokens in this order of preference:

1. `GH_GEI_TOKEN` (GitHub Enterprise token)
2. `GH_TOKEN` (standard GitHub token)
3. GitHub CLI's built-in authentication

Most users won't need to set these explicitly if GitHub CLI is properly authenticated.

## Usage

### Basic Usage

```bash
# Display PRs for configured repositories
gh prs-md
```

### One-time Repository Override

```bash
# Query different repositories for this run only
GH_REPOS="different-org/repo1 different-org/repo2" gh prs-md
```

### Save Output to File

```bash
# Save to a file for sharing or documentation
gh prs-md > team-prs-$(date +%Y%m%d).md
```

## Troubleshooting

### Common Issues

1. **"set GH_REPOS" error**
   ```bash
   # Make sure GH_REPOS is set
   echo $GH_REPOS
   # If empty, set it:
   export GH_REPOS="your-repo1 your-repo2"
   ```

2. **Authentication errors**
   ```bash
   # Check GitHub CLI authentication
   gh auth status
   # If not authenticated:
   gh auth login
   ```

3. **Repository not found errors**
   - Verify repository names are correct
   - Ensure you have access to the repositories
   - Use full `org/repo` format for repositories outside your default org

4. **Command not found: jq**
   ```bash
   # Install jq
   # macOS:
   brew install jq
   # Ubuntu/Debian:
   sudo apt-get install jq
   # CentOS/RHEL:
   sudo yum install jq
   ```

### Debug Mode

The script doesn't have a built-in debug mode, but you can troubleshoot by:

```bash
# Test individual repository access
gh pr list --repo your-org/your-repo

# Check if environment variables are set
echo "GH_REPOS: $GH_REPOS"
echo "GH_GEI_TOKEN: ${GH_GEI_TOKEN:+SET}"
echo "GH_TOKEN: ${GH_TOKEN:+SET}"
```

## Customization

### Default Organization

If most of your repositories are in the same organization, you can modify the script to change the default organization assumption. Edit line 6 in the script:

```bash
if [[ "$r" == */* ]]; then repo="$r"; else repo="YourOrg/$r"; fi
```

### Output Format

The script outputs markdown by default. You can modify the output format by editing the `printf` and `echo` statements in the script to match your preferred format.

### Time Display

The script shows relative time (e.g., "2d 3h ago"). This is calculated using a custom function in the script and can be modified if you prefer different time formatting.

## Dependencies

- **GitHub CLI** (`gh`) - For API access and authentication
- **jq** - For JSON processing
- **Standard Unix tools** - `date`, `paste`, `head` (usually pre-installed)

## Security Notes

- The script uses your GitHub CLI authentication
- No additional tokens or credentials are stored
- All API calls go through GitHub's official API endpoints
- Repository access is limited to what your GitHub account can access
