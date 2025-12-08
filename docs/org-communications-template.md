# Organizational Communications Template

Role-tailored communications for GitHub Enterprise SOP Compliance rollout.

## Overview

This document provides templates for communicating the compliance rollout to different GitHub roles:
- **Repo Owners/Admins**: Full details, responsibilities, exceptions process
- **Contributors/Writers**: What changes, how to work with new policies
- **Readers/Users**: High-level summary, where to find information

## Template: Repo Owners/Admins

### Subject: GitHub Enterprise SOP Compliance Rollout - Action Required

**To:** Repository owners and administrators
**Priority:** High
**Timeline:** [Start Date] - [End Date]

---

#### Summary

We are implementing GitHub Enterprise SOP compliance standards across all repositories. This ensures consistent development practices, improved security, and better release management.

#### What's Changing

1. **Default Branch Standardization**
   - All repos must use `main` as default branch (exceptions documented)
   - Existing repos with `master` or other defaults will be migrated

2. **Branch Protection Rules**
   - PR required for all changes to `main`
   - 1-2 reviewers required (depending on repo)
   - Required status checks must pass
   - Force push and branch deletion restricted

3. **Branch Naming Policy**
   - Allowed: `feature/*`, `bugfix/*`, `hotfix/*`, `backport/*`
   - Disallowed: `release/*`, `v*` branches (except IaC repos)
   - Auto-delete merged branches enabled

4. **Standard Files**
   - `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODEOWNERS` required
   - PR/Issue templates recommended

5. **CI/CD Alignment**
   - PR workflows: build/test/scan only
   - Tag workflows: build/package/publish/sign
   - Branch-based deployments removed

#### Your Responsibilities

- [ ] Review your repositories in the [Notion Scorecard]([LINK])
- [ ] Request exceptions if needed (see process below)
- [ ] Update default branch if not `main`
- [ ] Add missing standard files
- [ ] Review and update CI/CD workflows
- [ ] Clean up stale branches (>90 days)
- [ ] Ensure branch protections are configured

#### Timeline

- **Week 1**: Audit and baseline established
- **Week 2**: Rulesets enabled in audit mode, exceptions processed
- **Weeks 2-3**: Standard files and branch standardization
- **Weeks 3-5**: CI/CD alignment
- **Week 5**: Tag seeding and migration
- **Week 6**: Full enforcement and validation

#### Requesting Exceptions

Exceptions are tracked in [Notion Actions & Exceptions]([LINK]). To request:

1. Create a new entry in the Exceptions database
2. Specify repository and reason
3. Include proposed alternative approach
4. Assign to compliance team

Common exceptions:
- Default branch name (e.g., `rcode` uses `master`)
- Release branch policy (IaC repos)
- Reviewer count (small repos)

#### Resources

- [Compliance Scorecard]([LINK])
- [SOP Documentation]([LINK])
- [Exception Request Form]([LINK])
- [FAQ]([LINK])

#### Questions?

Contact: [compliance-team@example.com] or post in [#github-compliance]

---

## Template: Contributors/Writers

### Subject: GitHub Workflow Updates - What You Need to Know

**To:** All GitHub contributors
**Timeline:** Effective [Date]

---

#### Quick Summary

We're standardizing GitHub workflows across all repositories. Here's what changes for you:

#### What's New

**Branch Naming**
- ✅ Use: `feature/my-feature`, `bugfix/fix-name`, `hotfix/urgent-fix`
- ❌ Don't use: `feat/`, `fix/`, `release/`, `v1.2.3`

**Pull Requests**
- All changes to `main` require a PR
- 1-2 reviewers must approve
- All CI checks must pass
- Branches auto-delete after merge

**Releases**
- Releases are tag-based only (`vX.Y.Z`)
- No more `release/*` branches
- Tag creation triggers build/publish

#### What You Need to Do

1. **Update your branch names** if needed
2. **Create PRs** for all changes (no direct pushes to `main`)
3. **Wait for reviews** and CI checks before merging
4. **Use tags** for releases (not branches)

#### Common Workflows

**Starting a new feature:**
```bash
git checkout -b feature/my-feature
# ... make changes ...
git push origin feature/my-feature
# Create PR via GitHub UI
```

**Creating a release:**
```bash
git tag v1.2.3
git push origin v1.2.3
# CI automatically builds and publishes
```

**Backporting a fix:**
```bash
git checkout -b backport/1.1 main
# ... cherry-pick fix ...
git tag v1.1.1
git push origin v1.1.1
```

#### Resources

- [Contributing Guide]([LINK])
- [Branch Naming Policy]([LINK])
- [Release Process]([LINK])

#### Questions?

Ask in [#github-help] or check the [FAQ]([LINK])

---

## Template: Readers/Users

### Subject: GitHub Standards Update

**To:** All team members
**Timeline:** Rolling out over next 2 weeks

---

#### What's Happening

We're standardizing GitHub repository practices across the organization to improve security, consistency, and release management.

#### Key Changes

- Standardized branch naming and protection
- Tag-based releases
- Required code reviews
- Standard repository files

#### What This Means for You

- **If you read repos**: No action needed
- **If you contribute**: Follow new branch naming and PR process
- **If you own repos**: Review compliance status and request exceptions if needed

#### Where to Learn More

- [Compliance Dashboard]([LINK])
- [Quick Reference Guide]([LINK])
- [FAQ]([LINK])

#### Timeline

Full rollout: [Start Date] - [End Date]

Questions? Contact: [compliance-team@example.com]

---

## Distribution Checklist

- [ ] Create Notion page with full details
- [ ] Send email to repo owners/admins (use template above)
- [ ] Send email to contributors/writers (use template above)
- [ ] Post announcement in team chat/channel
- [ ] Update GitHub org profile with link to compliance page
- [ ] Create calendar invites for enablement sessions
- [ ] Add banner to internal portal (optional)
- [ ] Schedule follow-up reminders

## Customization Notes

Replace placeholders:
- `[LINK]`: Actual Notion/GitHub links
- `[Date]`: Actual dates
- `[compliance-team@example.com]`: Actual contact
- `[#github-compliance]`: Actual channel names

Adjust timeline based on your sprint schedule.

