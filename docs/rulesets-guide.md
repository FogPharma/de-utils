# GitHub Rulesets Implementation Guide

Guide for implementing organization-level rulesets for GitHub Enterprise SOP compliance.

## Overview

GitHub Rulesets allow organization-level policy enforcement. If unavailable, use per-repo branch protection rules.

## Ruleset Configuration

### Required Settings

1. **Pull Request Requirements**
   - Require pull request before merging: ✅ Enabled
   - Required number of reviewers: 1-2 (configurable per repo)
   - Dismiss stale reviews: ✅ Enabled
   - Require review from Code Owners: ✅ Enabled (if CODEOWNERS exists)

2. **Status Checks**
   - Require status checks to pass: ✅ Enabled
   - Require branches to be up to date: ✅ Enabled
   - Required status checks: (repo-specific)

3. **Branch Protection**
   - Require linear history: ✅ Enabled (optional, can be per-repo)
   - Require signed commits: ✅ Enabled (if org policy mandates)
   - Restrict force pushes: ✅ Enabled
   - Restrict branch deletion: ✅ Enabled

4. **Branch Naming**
   - Allowed patterns:
     - `feature/*`
     - `bugfix/*`
     - `hotfix/*`
     - `backport/*`
   - Blocked patterns:
     - `release/*` (except IaC repos)
     - `v*` (version branches)

5. **Auto-delete**
   - Delete head branches after merge: ✅ Enabled

## Implementation Steps

### Step 1: Create Audit Mode Ruleset

Start with a report-only ruleset to identify issues:

```yaml
name: "SOP Compliance - Audit Mode"
target: branches
enforcement: evaluate  # Report-only mode
conditions:
  ref_name:
    include:
      - "refs/heads/main"
      - "refs/heads/master"
rules:
  - type: pull_request
    parameters:
      required_approving_review_count: 1
      dismiss_stale_reviews_on_push: true
      require_code_owner_review: true
  - type: required_status_checks
    parameters:
      strict_required_status_checks_policy: true
  - type: non_fast_forward
  - type: deletion
```

### Step 2: Pilot on 5-10 Repos

Select low-risk, active repositories:
- Recent commits
- Active maintainers
- Standard workflows

Apply ruleset and monitor for 1 week.

### Step 3: Enable Enforcement

After validation, change enforcement to `active`:

```yaml
enforcement: active  # Full enforcement
```

### Step 4: Org-wide Rollout

Apply to all repositories except those with approved exceptions.

## Exceptions Process

Track exceptions in Notion Actions & Exceptions database:

1. **Default Branch Exception**
   - Repo: `FogPharma/rcode`
   - Reason: Legacy repo using `master`
   - Status: Approved

2. **Release Branch Exception**
   - Repo: `FogPharma/IaC-DataScience`
   - Reason: Manages release branches for versioned deployments
   - Status: Approved

3. **Reviewer Count Exception**
   - Repo: Small internal tool repos
   - Reason: Single maintainer
   - Status: Approved (1 reviewer instead of 2)

## GitHub API Implementation

### Create Ruleset (if API available)

```python
POST /orgs/{org}/rulesets
{
  "name": "SOP Compliance",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main", "refs/heads/master"]
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 1
      }
    }
  ]
}
```

### Fallback: Branch Protection API

If rulesets unavailable, use branch protection:

```python
PUT /repos/{owner}/{repo}/branches/{branch}/protection
{
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true
  },
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci/tests", "ci/lint"]
  },
  "enforce_admins": true,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

## Monitoring

Track ruleset coverage in Notion:
- Repos with rulesets applied
- Exceptions count
- Compliance score trends
- Issues reported

## Troubleshooting

**Issue**: Ruleset blocks legitimate workflows
**Solution**: Create exception, adjust ruleset conditions

**Issue**: Required checks not running
**Solution**: Verify workflow files, check branch names

**Issue**: Too many false positives
**Solution**: Review and refine conditions, add exceptions

## References

- [GitHub Rulesets Documentation](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/rules-for-repositories)
- [Branch Protection API](https://docs.github.com/en/rest/branches/branch-protection)

