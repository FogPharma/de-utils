# Release Manifest Structure

Structure for release orchestrator manifests (e.g., IaC-DataScience).

## Overview

Release manifests map product versions to specific repository tags or package versions, enabling side-by-side deployments of multiple product versions.

## Manifest Format

### YAML Format

```yaml
# release-manifest.yaml
version: "1.4"
created_at: "2025-01-15T10:00:00Z"
created_by: "platform-team"
environments:
  production:
    deployed_at: "2025-01-20T14:30:00Z"
    namespace: "prod-v1.4"
  staging:
    deployed_at: "2025-01-18T09:00:00Z"
    namespace: "staging-v1.4"

repositories:
  - name: "fogpy"
    tag: "v2.6.1"
    commit_sha: "abc123def456"
    package_version: "2.6.1"

  - name: "fogpy_utils"
    tag: "v1.4.2"
    commit_sha: "def456ghi789"
    package_version: "1.4.2"

  - name: "ML_model_dockers"
    tag: "v1.4.2"
    commit_sha: "ghi789jkl012"
    package_version: null  # Not a package

  - name: "chempipe-plugins"
    tag: "v3.1.0"
    commit_sha: "jkl012mno345"
    package_version: "3.1.0"

metadata:
  notes: "Production release with performance improvements"
  changelog_url: "https://github.com/org/repo/releases/tag/v1.4.0"
```

### JSON Format

```json
{
  "version": "1.4",
  "created_at": "2025-01-15T10:00:00Z",
  "created_by": "platform-team",
  "environments": {
    "production": {
      "deployed_at": "2025-01-20T14:30:00Z",
      "namespace": "prod-v1.4"
    },
    "staging": {
      "deployed_at": "2025-01-18T09:00:00Z",
      "namespace": "staging-v1.4"
    }
  },
  "repositories": [
    {
      "name": "fogpy",
      "tag": "v2.6.1",
      "commit_sha": "abc123def456",
      "package_version": "2.6.1"
    }
  ],
  "metadata": {
    "notes": "Production release",
    "changelog_url": "https://github.com/org/repo/releases/tag/v1.4.0"
  }
}
```

## Manifest Location

Store manifests in the release orchestrator repository (e.g., `IaC-DataScience`):

```
IaC-DataScience/
  manifests/
    v1.4.yaml
    v1.3.yaml
    v1.2.yaml
  README.md
```

## Notion Sync

The compliance automation can mirror manifests to Notion Release Views database:

- Each repository entry becomes a row
- Product version links related repos
- Deployment status tracked per environment

## Backport Process

1. Create PR to `release/<minor>` branch (e.g., `release/1.4`)
2. Update manifest with new tag versions
3. Merge PR
4. IaC pipeline consumes updated manifest
5. Notion Release Views updated automatically

## Validation

Manifests should be validated:
- All tags exist in respective repos
- Commit SHAs match tags
- Package versions match tags (if applicable)
- No circular dependencies

## Example: Creating a New Manifest

```bash
# 1. Identify current production versions
# 2. Create manifest file
cat > manifests/v1.5.yaml << EOF
version: "1.5"
created_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
created_by: "$USER"
repositories:
  - name: "fogpy"
    tag: "v2.7.0"
    commit_sha: "$(git rev-parse v2.7.0)"
EOF

# 3. Validate
python scripts/validate_manifest.py manifests/v1.5.yaml

# 4. Commit and create PR
git checkout -b release/1.5
git add manifests/v1.5.yaml
git commit -m "Add release manifest v1.5"
git push origin release/1.5
# Create PR
```

## Integration with Compliance Tool

The compliance audit can:
- Read manifests from IaC repo
- Validate tag existence
- Sync to Notion Release Views
- Track deployment status

See `src/compliance/release_views.py` for implementation (to be created).

