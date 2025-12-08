# Compliance Automation Setup Guide

Complete setup guide for GitHub Enterprise SOP Compliance automation.

## Prerequisites

- Python 3.12+
- GitHub token with repo read access (PAT or GitHub App)
- Notion integration token
- Access to create Notion databases

## Step 1: Install Dependencies

```bash
pip install -r src/compliance/requirements.txt
```

## Step 2: Configure GitHub Access

### Option A: GitHub App (Recommended for Higher Rate Limits)

GitHub Apps provide higher rate limits (15,000 requests/hour for Enterprise Cloud vs 5,000 for PATs), making them ideal for auditing large organizations.

1. **Get your GitHub App credentials:**
   - App ID: Found in your GitHub App settings (numeric ID like `1454949`)
   - Private Key: Download the `.pem` file from your GitHub App settings
   - Installation ID: Optional - can be auto-discovered, or find it at:
     `https://github.com/organizations/YOUR_ORG/settings/installations`

2. **Set environment variables:**
   ```bash
   export GITHUB_APP_ID="1454949"
   export GITHUB_APP_PRIVATE_KEY="/path/to/your-app-private-key.pem"
   # Installation ID is optional - will be auto-discovered if not set
   # export GITHUB_APP_INSTALLATION_ID="12345678"
   export GITHUB_ORG="FogPharma"
   ```

   **Note:** You can also set `GITHUB_APP_PRIVATE_KEY` to the PEM content directly (useful for CI/CD):
   ```bash
   export GITHUB_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
   MIIEpAIBAAKCAQEA...
   -----END RSA PRIVATE KEY-----"
   ```

### Option B: Personal Access Token

```bash
export GH_GEI_TOKEN="your_token_here"
# Or for GitHub Enterprise:
export GH_GEI_TOKEN="your_token_here"
export GITHUB_API_URL="https://your-github-enterprise-host/api/v3"
export GITHUB_ORG="FogPharma"
```

**Note:** The tool will automatically use GitHub App authentication if `GITHUB_APP_ID` and `GITHUB_APP_PRIVATE_KEY` are set, otherwise it falls back to PAT.

## Step 3: Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "New integration" (or use existing "Notion Automation" integration)
3. Name it "Notion Automation" (or use existing integration)
4. Select your workspace
5. Copy the **"Internal Integration Token"** (this is the API key, starts with `secret_`)

**Important:** Use the "Internal Integration Token" (API key), NOT the "Integration Secret" (which is for OAuth flows).

Set the token:

```bash
export NOTION_TOKEN="secret_your_integration_token_here"
```

The token should start with `secret_` and is used directly in API requests.

## Step 4: Create Notion Databases

### Option A: Using the Setup Script

1. Create a parent page in Notion (or use an existing page)
2. Get the page ID from the URL (the long hex string after the last `/`)
3. Run the setup script:

```bash
python -m src.compliance.setup_notion_dbs --parent-page-id YOUR_PAGE_ID
```

This will create all three databases and print their IDs.

### Option B: Manual Creation

Create three databases in Notion with the following properties:

#### Repos Scorecard Database

- **Name** (Title)
- **Compliance Score** (Number)
- **Default Branch** (Rich Text)
- **Archived** (Checkbox)
- **Archived At** (Date)
- **Primary Language** (Rich Text)
- **Primary Contributor** (Rich Text)
- **Contributors Count** (Number)
- **Last Commit Date** (Date)
- **Time Since Last Commit** (Rich Text)
- **Last Audit** (Date)
- **Status** (Select: Compliant, Needs Attention, Non-Compliant, Exception)
- **Owner** (Rich Text)
- **Repository URL** (URL)

#### Actions & Exceptions Database

- **Name** (Title)
- **Type** (Select: Exception, Action Item, Remediation)
- **Repository** (Rich Text)
- **Status** (Select: Open, In Progress, Resolved, Approved)
- **Owner** (Rich Text)
- **Due Date** (Date)
- **Description** (Rich Text)
- **Created** (Created Time)
- **Updated** (Last Edited Time)

#### Release Views Database

- **Name** (Title)
- **Product Version** (Rich Text)
- **Repository** (Rich Text)
- **Tag** (Rich Text)
- **Commit SHA** (Rich Text)
- **Package Version** (Rich Text)
- **Environment** (Select: staging, production, development)
- **Deployed At** (Date)
- **Last Updated** (Date)

## Step 5: Configure the Tool

1. Copy the example config:

```bash
cp src/compliance/config.yaml.example src/compliance/config.yaml
```

2. Edit `config.yaml`:

```yaml
github_org: "YourOrg"

notion:
  scorecard_db_id: "your_scorecard_database_id"
  actions_db_id: "your_actions_database_id"
  release_views_db_id: "your_release_views_database_id"

exceptions:
  default_branch:
    "YourOrg/rcode": "master"

  allow_release_branches:
    - "YourOrg/IaC-DataScience"
```

## Step 6: Test the Audit

Run a test audit on a single repository:

```bash
python -m src.compliance.audit --repo "YourOrg/test-repo" --dry-run
```

This will output JSON without syncing to Notion.

## Step 7: Run Full Audit

Audit all repositories and sync to Notion:

```bash
python -m src.compliance.audit --output audit-results.json
```

## Step 8: Set Up GitHub Actions (Optional)

The workflow file is already created at `.github/workflows/compliance-audit.yml`.

Add these secrets to your GitHub repository:

**For GitHub App authentication (recommended):**
- `GITHUB_APP_ID`: Your GitHub App ID
- `GITHUB_APP_PRIVATE_KEY`: Your private key (PEM content)
- `GITHUB_APP_INSTALLATION_ID`: Installation ID (optional)

**For Personal Access Token:**
- `GH_GEI_TOKEN`: Your GitHub token

**Common secrets:**
- `NOTION_TOKEN`: Your Notion integration token
- `NOTION_SCORECARD_DB_ID`: Your scorecard database ID
- `GITHUB_ORG`: Your GitHub organization name (if not in config)

The workflow will run daily at 2 AM UTC and can be triggered manually.

## Troubleshooting

### "GitHub token required" error

Make sure you've set either:
- `GH_GEI_TOKEN` or `GH_TOKEN` (for PAT), OR
- `GITHUB_APP_ID` + `GITHUB_APP_PRIVATE_KEY` (for GitHub App)

### "Failed to get installation token" error

- Verify your App ID is correct
- Ensure your private key is valid PEM format
- Check that the GitHub App is installed on your organization
- Verify the App has the necessary permissions (repository read access)

### Rate limiting

The tool automatically handles rate limits with retries and waiting. However:
- **GitHub App**: Provides 15,000 requests/hour (Enterprise Cloud)
- **Personal Access Token**: Provides 5,000 requests/hour

For large organizations, GitHub App authentication is recommended.

### "Notion token required" error

Set `NOTION_TOKEN` environment variable or use `--dry-run` to skip Notion sync.

### Notion API errors

- Ensure your integration has access to the databases
- Check that database IDs are correct
- Verify property names match exactly (case-sensitive)

## Next Steps

After setup, see the main plan document for:
- Creating organizational communications
- Setting up GitHub rulesets
- Standardizing repositories
- CI/CD alignment