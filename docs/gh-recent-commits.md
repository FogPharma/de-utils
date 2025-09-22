# gh recent-commits

A GitHub CLI alias that displays recent commits from the last 7 days across multiple repositories, filtered by author and grouped by repository.

## Purpose

This tool helps developers track their recent work across multiple repositories. It provides a consolidated view of commits from the past week, making it easy to:

- Review your recent contributions across projects
- Generate status reports or standup summaries
- Track work across feature branches and repositories
- See commit activity filtered by specific authors

The tool searches all branches in each repository, not just the main branch, ensuring you don't miss commits on feature branches.

## Output Example

```markdown
### FogPharma/fog4j
- **6ed8f11** (2025-09-22) [feature/EN-1801_fog4j_reademe] docs: updated README — dvaron

### FogPharma/ML_models_production
- **abc1234** (2025-09-21) [main] fix: update model validation — Dave Varon
- **def5678** (2025-09-20) [feature/new-model] feat: add new ADMET model — varontron

### FogPharma/IaC-DataScience
- **123abcd** (2025-09-19) [hotfix/memory-fix] hotfix: increase batch memory to 64GB — dvaron
```

## Installation

### Prerequisites

- [GitHub CLI](https://cli.github.com/) installed and authenticated
- `jq` command-line JSON processor
- Standard Unix tools (`date`, `sed`, `cut`) - usually pre-installed
- Access to the repositories you want to query

### Step 1: Install the Script

```bash
# Create local bin directory if it doesn't exist
mkdir -p ~/.local/bin

# Copy the script to your local bin
cp src/gh-recent-commits ~/.local/bin/

# Make it executable
chmod +x ~/.local/bin/gh-recent-commits

# Ensure ~/.local/bin is in your PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

### Step 2: Configure GitHub CLI Alias

Add the alias to your GitHub CLI configuration:

```bash
# Option 1: Use gh CLI to add the alias
gh alias set recent-commits '!GITHUB_TOKEN="${GH_GEI_TOKEN:-$GITHUB_TOKEN}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-recent-commits'

# Option 2: Manually edit ~/.config/gh/config.yml
```

If editing manually, add this to your `~/.config/gh/config.yml`:

```yaml
aliases:
  recent-commits: '!GITHUB_TOKEN="${GH_GEI_TOKEN:-$GITHUB_TOKEN}" GH_TOKEN="${GH_GEI_TOKEN:-$GH_TOKEN}" ~/.local/bin/gh-recent-commits'
```

## Configuration

### Required: Set Repository List

The script requires the `GH_REPOS` environment variable to know which repositories to query:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export GH_REPOS="repo1 repo2 repo3"

# For repositories in different organizations:
export GH_REPOS="myorg/repo1 myorg/repo2 anotherorg/repo3"

# Example with actual repositories:
export GH_REPOS="fog4j ML_models_production IaC-DataScience fogpy"
```

**Note:** Repository names without a slash (/) are assumed to be under your default organization.

### Required: Set Author Filter

The script filters commits by author. You **must** configure this for your username:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export COMMIT_AUTHOR="your-github-username"

# If you use multiple names/emails in commits:
export COMMIT_AUTHOR="username1|Real Name|email@domain.com"

# Examples:
export COMMIT_AUTHOR="john_doe"
export COMMIT_AUTHOR="john_doe|John Doe|john@company.com"
```

**Important:** The author filter uses exact matching. Make sure your filter matches exactly how your name appears in commits.

### Optional: Authentication Configuration

The script uses GitHub tokens in this order of preference:

1. `GH_GEI_TOKEN` (GitHub Enterprise token)
2. `GITHUB_TOKEN` (standard GitHub token)
3. GitHub CLI's built-in authentication

Most users won't need to set these explicitly if GitHub CLI is properly authenticated.

### Optional: Debug Mode

Enable debug output to troubleshoot issues:

```bash
export DEBUG=1
```

## Usage

### Basic Usage

```bash
# Show your recent commits from the last 7 days
gh recent-commits
```

### Configuration Examples

```bash
# Show commits from a different user
COMMIT_AUTHOR="alice" gh recent-commits

# Show commits from multiple users
COMMIT_AUTHOR="alice|bob|charlie" gh recent-commits

# Query different repositories for this run
GH_REPOS="different-org/repo1 different-org/repo2" gh recent-commits

# Show all commits regardless of author (not recommended for large repos)
COMMIT_AUTHOR=".*" gh recent-commits

# Enable debug output
DEBUG=1 gh recent-commits
```

### Save Output to File

```bash
# Save to a file for documentation or sharing
gh recent-commits > my-recent-work-$(date +%Y%m%d).md
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

2. **"No commits in the last 7 days" (when you know you have commits)**
   ```bash
   # Check your author filter
   echo $COMMIT_AUTHOR
   # Make sure it matches your commit author name exactly
   
   # Test with a broader filter temporarily
   COMMIT_AUTHOR=".*" gh recent-commits
   ```

3. **Authentication errors**
   ```bash
   # Check GitHub CLI authentication
   gh auth status
   # If not authenticated:
   gh auth login
   ```

4. **Repository not found errors**
   - Verify repository names are correct
   - Ensure you have access to the repositories
   - Use full `org/repo` format for repositories outside your default org

### Debug Mode

Enable debug mode to see detailed information:

```bash
DEBUG=1 gh recent-commits
```

Debug output shows:
- Date range being searched
- Author filter being applied
- Each branch being processed
- API errors or issues
- Commits being skipped due to author filtering

### Finding Your Commit Author Name

If you're not sure what name to use in `COMMIT_AUTHOR`, check your recent commits:

```bash
# Check your recent commits in a specific repo
gh api repos/your-org/your-repo/commits --jq '.[0].commit.author.name'

# Or check locally
git log --oneline -n 5 --pretty=format:"%an"
```

## Customization

### Change Time Range

By default, the script looks for commits from the last 7 days. To change this, edit the script and modify this line:

```bash
SINCE_DATE=$(date -v-7d '+%Y-%m-%d' 2>/dev/null || date -d '7 days ago' '+%Y-%m-%d' 2>/dev/null)
```

Change `7d` or `7 days ago` to your preferred range (e.g., `14d`, `3 days ago`).

### Default Organization

If most of your repositories are in the same organization, you can modify the script to change the default organization assumption. Edit this line:

```bash
if [[ "$r" == */* ]]; then repo="$r"; else repo="YourOrg/$r"; fi
```

### Default Author Filter

To set a different default author filter (so you don't need to set `COMMIT_AUTHOR` every time), edit this line in the script:

```bash
COMMIT_AUTHOR=${COMMIT_AUTHOR:-"your-default-username"}
```

## Advanced Usage

### Multiple Author Patterns

The author filter supports regex patterns:

```bash
# Match multiple exact names
COMMIT_AUTHOR="john_doe|John Doe|j.doe@company.com"

# Match patterns (use carefully)
COMMIT_AUTHOR="john.*|.*doe.*"

# Match any commits from your organization's email domain
COMMIT_AUTHOR=".*@yourcompany\.com"
```

### Integration with Other Tools

```bash
# Generate a weekly report
echo "# Weekly Development Summary - $(date)" > weekly-report.md
gh recent-commits >> weekly-report.md

# Count your commits
gh recent-commits | grep -c "^- \*\*"

# Extract just commit messages for standup
gh recent-commits | grep -o "\] .* —" | sed 's/] //' | sed 's/ —//'
```

## Dependencies

- **GitHub CLI** (`gh`) - For API access and authentication
- **jq** - For JSON processing
- **Standard Unix tools** - `date`, `sed`, `cut` (usually pre-installed)

## Security Notes

- The script uses your GitHub CLI authentication
- No additional tokens or credentials are stored
- All API calls go through GitHub's official API endpoints
- Repository access is limited to what your GitHub account can access
- Author filtering is done locally after fetching commit data

## Performance Notes

- The script queries all branches in each repository
- For repositories with many branches or commits, this may take some time
- Results are not cached between runs
- Consider limiting `GH_REPOS` to actively developed repositories for better performance
