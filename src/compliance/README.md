# GitHub Enterprise SOP Compliance Automation

Automated compliance auditing and tracking for GitHub Enterprise repositories.

## Overview

This tool audits GitHub repositories against SOP compliance policies and syncs results to Notion databases for tracking and reporting.

## Features

- **Automated Auditing**: Scans all repos in an organization for compliance
- **Comprehensive Checks**: Default branch, protections, naming, standard files, CI patterns, stale branches
- **Repository Metadata**: Primary language, contributors, last commit tracking
- **Notion Integration**: Syncs results to Notion databases for dashboards
- **Configurable**: YAML config for exceptions and settings
- **GitHub App Support**: Higher rate limits (15,000/hour) with automatic token management

## Installation

**Requirements:** Python 3.12+

```bash
# Install dependencies
pip install -r src/compliance/requirements.txt

# Or install in development mode
pip install -e .
```

## Configuration

1. Copy the example config:
   ```bash
   cp src/compliance/config.yaml.example src/compliance/config.yaml
   ```

2. Edit `config.yaml` with your settings:
   - GitHub organization name
   - Notion database IDs
   - Repository exceptions

3. Set environment variables:

   **Option A: GitHub App (Recommended for higher rate limits)**
   ```bash
   export GITHUB_APP_ID="your_app_id"
   export GITHUB_APP_PRIVATE_KEY="/path/to/private-key.pem"  # Or PEM content
   export GITHUB_APP_INSTALLATION_ID="installation_id"  # Optional, auto-discovered
   export NOTION_TOKEN="secret_your_integration_token"  # Internal Integration Token (API key)
   export GITHUB_ORG="your_org_name"  # Optional if in config.yaml
   ```

   **Option B: Personal Access Token**
   ```bash
   export GH_GEI_TOKEN="your_github_token"
   export NOTION_TOKEN="secret_your_integration_token"  # Internal Integration Token (API key)
   export GITHUB_ORG="your_org_name"  # Optional if in config.yaml
   ```

   The tool will automatically use GitHub App authentication if `GITHUB_APP_ID` and `GITHUB_APP_PRIVATE_KEY` are set, otherwise it falls back to PAT.

## Usage

### Audit all repositories

```bash
python -m src.compliance.audit
```

### Audit a single repository

```bash
python -m src.compliance.audit --repo "FogPharma/my-repo"
```

### Output to JSON file

```bash
python -m src.compliance.audit --output audit-results.json
```

### Dry run (no Notion sync)

```bash
python -m src.compliance.audit --dry-run
```

### Parallel Processing

Process multiple repositories in parallel for faster audits:

```bash
# Use 8 parallel workers (default: 4)
python -m src.compliance.audit --max-workers 8

# Combine with property filtering for optimal performance
python -m src.compliance.audit --max-workers 8 --exclude-properties "primary_contributor,contributors_count"
```

**Note**: Each worker creates its own API client instances. With GitHub App authentication, you get 15,000 requests/hour shared across all workers. The default of 4 workers balances speed with rate limit safety. Increase `--max-workers` for faster processing if you have sufficient rate limit headroom.

**Timeout**: Each repository has a 30-minute timeout (increased from 15 minutes) to handle large repositories with extensive commit history.

### Selective Property Updates

Update only specific properties to avoid expensive operations (like contributor analysis):

```bash
# Only update contributor metadata (skip other expensive operations)
python -m src.compliance.audit --include-properties "primary_contributor,contributors_count"

# Update everything except contributor analysis (faster)
python -m src.compliance.audit --exclude-properties "primary_contributor,contributors_count"

# Update only specific properties for repos with low scores
python -m src.compliance.audit --include-properties "primary_contributor,contributors_count" --max-score 50
```

Available property names:
- `primary_language`: Repository primary language
- `primary_contributor`: Most active contributor (last 90 days)
- `contributors_count`: Total unique contributors (last 365 days)
- `last_commit_date`: Date of last commit
- `time_since_last_commit`: Humanized time since last commit
- `default_branch`: Default branch name
- `archived`: Archive status
- `compliance_score`: Compliance score (always included for filtering)

### Score Threshold Filtering

Only process repositories within a score range:

```bash
# Only audit repos with scores below 50
python -m src.compliance.audit --max-score 50

# Only audit repos with scores above 80
python -m src.compliance.audit --min-score 80

# Audit repos with scores between 40 and 60
python -m src.compliance.audit --min-score 40 --max-score 60
```

### Override Historical Thresholds

Change the time windows for contributor analysis (useful for legacy repos):

```bash
# Use shorter windows for faster analysis
python -m src.compliance.audit --contributor-window-days 180 --primary-contributor-window-days 30

# Use longer windows for comprehensive analysis
python -m src.compliance.audit --contributor-window-days 730 --primary-contributor-window-days 180
```

Default values:
- `contributor_window_days`: 365 (from config or 365)
- `primary_contributor_window_days`: 90 (from config or 90)

## GitHub App Setup

For organizations with many repositories, using a GitHub App provides higher rate limits (15,000 requests/hour vs 5,000 for PATs).

### Getting Your GitHub App Credentials

1. **App ID**: Found in your GitHub App settings (numeric ID)
2. **Private Key**: Download the `.pem` file from your GitHub App settings
3. **Installation ID**: Optional - the tool can auto-discover this, or find it at:
   `https://github.com/organizations/YOUR_ORG/settings/installations`

### Setting Up the Private Key

You can provide the private key in two ways:

1. **File path**: Point to the `.pem` file
   ```bash
   export GITHUB_APP_PRIVATE_KEY="/path/to/your-app-private-key.pem"
   ```

2. **Direct content**: Set the PEM content directly (useful for CI/CD)
   ```bash
   export GITHUB_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
   ...
   -----END RSA PRIVATE KEY-----"
   ```

The tool automatically:
- Generates JWT tokens from the private key
- Exchanges JWT for installation tokens
- Refreshes tokens before expiration
- Falls back to PAT if App credentials aren't available

## Notion Database Setup

The tool expects Notion databases with specific properties. See the plan document for the full schema.

### Repos Scorecard Database Properties

- **Name** (Title): Repository full name
- **Compliance Score** (Number): 0-100 score
- **Default Branch** (Text): Default branch name
- **Archived** (Checkbox): Whether repo is archived
- **Primary Language** (Rich Text): Top language by bytes
- **Primary Contributor** (Rich Text): Top committer username
- **Contributors Count** (Number): Unique contributors count
- **Last Commit Date** (Date): ISO date of last commit
- **Time Since Last Commit** (Rich Text): Humanized duration
- **Last Audit** (Date): Audit timestamp

## GitHub Actions Workflow

Create `.github/workflows/compliance-audit.yml`:

```yaml
name: Compliance Audit

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r src/compliance/requirements.txt
      - run: |
          python -m src.compliance.audit \
            --output audit-results.json \
            --notion-db ${{ secrets.NOTION_SCORECARD_DB_ID }}
        env:
          # Option A: GitHub App (recommended)
          GITHUB_APP_ID: ${{ secrets.GITHUB_APP_ID }}
          GITHUB_APP_PRIVATE_KEY: ${{ secrets.GITHUB_APP_PRIVATE_KEY }}
          GITHUB_APP_INSTALLATION_ID: ${{ secrets.GITHUB_APP_INSTALLATION_ID }}
          # Option B: Personal Access Token
          # GH_GEI_TOKEN: ${{ secrets.GH_GEI_TOKEN }}
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
          GITHUB_ORG: ${{ secrets.GITHUB_ORG }}
```

## Rate Limiting

The tool automatically handles rate limits:
- **Proactive checking**: Monitors rate limit status before requests
- **Automatic retries**: Waits for rate limit reset when needed
- **GitHub App support**: Higher limits (15,000/hour) for Enterprise Cloud

For large organizations, GitHub App authentication is recommended to avoid rate limit issues.

## Development

```bash
# Run tests (when implemented)
pytest

# Format code
black src/compliance

# Lint
flake8 src/compliance
```

## License

See LICENSE file in repository root.