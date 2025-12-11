# GitHub Enterprise SOP Compliance Rollout

**Status:** 🟢 Active
**Rollout Period:** [Start Date] - [End Date]
**Last Updated:** [Date]

---

## 📋 Quick Links

- [Compliance Scorecard]([LINK]) - View your repo's compliance status
- [Actions & Exceptions]([LINK]) - Request exceptions or track remediation
- [Release Views]([LINK]) - Version tracking and deployment manifests
- [Enablement Playbook]([LINK]) - Training materials and quick reference
- [FAQ]([LINK]) - Common questions

---

## 🎯 Role-Specific Guides

### 👥 [For Repository Owners & Administrators](#repo-owners)
**Action Required** - Review your repos and ensure compliance

### ✍️ [For Contributors & Writers](#contributors)
**What's Changing** - Updated workflows and processes

### 👀 [For Readers & Users](#readers)
**For Your Information** - High-level overview

---

# 👥 For Repository Owners & Administrators {#repo-owners}

## ⚠️ Action Required

Your repositories need to comply with new GitHub Enterprise SOP standards. Review the [Compliance Scorecard]([LINK]) and take action.

## 📊 What's Changing

### 1. Default Branch: `main` Required
- All repos must use `main` as default branch
- Exceptions documented in [Actions & Exceptions]([LINK])

### 2. Branch Protections
**Scope**: Multi-contributor repos only (single-contributor repos exempt)

- ✅ PR required for all changes (enforced via GitHub rulesets)
- ✅ 1-2 reviewers required (enforced via GitHub rulesets)
- ✅ Required status checks must pass (enforced via GitHub rulesets)
- ✅ Force push/deletion restricted (enforced via GitHub rulesets)
- ✅ Linear history (squash/rebase) (enforced via GitHub rulesets)

**Enforcement**: GitHub organization rulesets automatically prevent violations. Single-contributor repos are exempt to avoid friction for solo work.

### 3. Branch Naming
- ✅ Allowed: `feature/*`, `bugfix/*`, `hotfix/*`, `backport/*`
- ❌ Disallowed: `release/*`, `v*` branches (non-IaC)

### 4. Standard Files Required
- `LICENSE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/` (bug_report.md, feature_request.md)

**Note**: These will be retroactively added to existing repos via automated PRs, and included by default in all new repos via repository template.

### 5. CI/CD (Non-IaC)
- PR workflows: Build/test/scan only
- Tag workflows: Build/package/publish (`vX.Y.Z`)
- ❌ No branch-based deployments

## ✅ Your Action Items

**Week 1:**
- [ ] Review [Compliance Scorecard]([LINK])
- [ ] Request exceptions if needed
- [ ] Update default branch to `main`

**Week 1-2:**
- [ ] Add missing standard files
- [ ] Update CI/CD workflows
- [ ] Clean up stale branches (>90 days)
- [ ] Configure branch protections

**Week 2:**
- [ ] Test tag-based releases
- [ ] Verify required checks
- [ ] Review exception requests

## 📅 Timeline

| Week | Activities |
|------|-----------|
| **Week 1** | Audit complete, Scorecard published, Exceptions open |
| **Week 2** | Rulesets enabled (audit mode), Standard files PRs |
| **Week 2-3** | Branch standardization, CI/CD updates |
| **Week 3-4** | Tag workflows, Release migration |
| **Week 4** | Full enforcement, Validation |

## 🔄 Exception Request Process

1. Go to [Actions & Exceptions]([LINK])
2. Create new entry:
   - Type: "Exception"
   - Repository: Full name
   - Description: Why needed
   - Alternative: Proposed approach
3. Assign to compliance team
4. Wait for approval (1-2 business days)

**Common Exceptions:**
- Default branch name (e.g., `rcode` uses `master`)
- Release branches (IaC repos)
- Reviewer count (small repos)

## 📚 Resources

- [Compliance Scorecard]([LINK])
- [SOP Documentation]([LINK])
- [Exception Request]([LINK])
- [Enablement Playbook]([LINK])

## 💬 Support

- **Email**: [compliance-team@fogpharma.com]
- **Slack**: [#github-compliance]

---

# ✍️ For Contributors & Writers {#contributors}

## 🚀 What's Changing

### Branch Naming
**✅ Use:**
- `feature/my-feature`
- `bugfix/fix-name`
- `hotfix/urgent-fix`
- `backport/1.1`

**❌ Don't Use:**
- `feat/`, `fix/`, `release/`, `v1.2.3`

### Pull Requests
**Scope**: Multi-contributor repos only (single-contributor repos exempt)

- All changes to `main` require PR (enforced automatically)
- 1-2 reviewers must approve (enforced automatically)
- All CI checks must pass (enforced automatically)
- Branches auto-delete after merge (automatic)

### Releases
- Tag-based only (`vX.Y.Z`)
- No `release/*` branches
- Tag triggers build/publish

## 📝 Quick Workflows

### New Feature
```bash
git checkout -b feature/my-feature
# ... make changes ...
git push origin feature/my-feature
# Create PR via GitHub UI
```

### Release
```bash
git tag v1.2.3
git push origin v1.2.3
# CI automatically builds/publishes
```

### Backport
```bash
git checkout -b backport/1.1 main
git cherry-pick <commit-sha>
git tag v1.1.1
git push origin v1.1.1
```

## ✅ Do's and Don'ts

**✅ DO:**
- Use proper branch names
- Create PRs for all changes
- Wait for reviews
- Use tags for releases

**❌ DON'T:**
- Push directly to `main`
- Use non-compliant branch names
- Merge without review
- Create `release/*` branches

## 📚 Resources

- [Contributing Guide]([LINK])
- [Branch Naming Policy]([LINK])
- [Release Process]([LINK])
- [Quick Reference Card]([LINK])

## 💬 Support

- **Slack**: [#github-help]
- **Email**: [compliance-team@fogpharma.com]

---

# 👀 For Readers & Users {#readers}

## 📢 What's Happening

We're standardizing GitHub practices across the organization for better security, consistency, and release management.

## 🎯 Why Now?

Our organization's success depends on software, and we've reached a scale where standardized practices are essential:

**📈 Scale**: Hundreds of repositories, millions of lines of code, and a growing team require consistent workflows. What worked for small teams no longer scales.

**🤝 External Collaboration**: We work with vendors, contractors, and partners who need clear standards. Standardized practices enable effective collaboration.

**🤖 AI-Assisted Engineering**: AI tools generate code that must fit our standards. Consistent patterns help AI produce code that integrates seamlessly.

**⚙️ Automation**: Most requirements are enforced automatically via GitHub configuration—you don't need to remember rules, GitHub prevents violations automatically.

**🔒 Security & Quality**: At scale, automated quality gates catch issues before production, protecting both our codebase and our users.

## 🎯 Key Changes

- Standardized branch naming
- Tag-based releases
- Required code reviews
- Standard repository files
- Improved security

## 👤 What This Means

**If you only read repos:**
- ✅ No action needed
- ✅ Better documentation
- ✅ More reliable releases

**If you contribute:**
- 📝 See [Contributors Guide](#contributors) above

**If you own repos:**
- 🔧 See [Repo Owners Guide](#repo-owners) above

## 📅 Timeline

- **Week 1**: Policies announced
- **Week 2**: Enforcement begins
- **Week 2-3**: Tag workflows implemented
- **Week 3-4**: Full rollout complete

## 📚 Learn More

- [Compliance Dashboard]([LINK])
- [Quick Reference Guide]([LINK])
- [FAQ]([LINK])

## 💬 Questions?

- **Email**: [compliance-team@fogpharma.com]
- **Slack**: [#github-help]

---

## 📊 Rollout Status

| Phase | Status | Target Date |
|-------|--------|-------------|
| Baseline Audit | ✅ Complete | [Date] |
| Scorecard v1 | ✅ Published | [Date] |
| Rulesets (Audit Mode) | 🟡 In Progress | [Date] |
| Standard Files | 🟡 In Progress | [Date] |
| CI/CD Updates | ⏳ Pending | [Date] |
| Tag Workflows | ⏳ Pending | [Date] |
| Full Enforcement | ⏳ Pending | [Date] |

---

## 📈 Success Metrics

- **Compliance Score**: Target ≥80% repos compliant
- **Exception Requests**: Target <10% of repos
- **Standard Files**: Target 100% coverage
- **Branch Protections**: Target 100% enabled
- **Tag Releases**: Target ≥80% adoption

---

## 🔄 Updates

- **[Date]**: Initial rollout announcement
- **[Date]**: Scorecard v1 published
- **[Date]**: [Add updates as rollout progresses]

---

**Last Updated:** [Date]
**Next Review:** [Date]

