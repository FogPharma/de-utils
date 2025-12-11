# GitHub Enterprise SOP Compliance - Action Items

**Status:** For Evaluation
**Created:** [Date]

---

## Overview: Push-Driven Automation

Most compliance work is **push-driven**—meaning organization administrators handle configurations, rulesets, automations, and notifications. This eliminates the need for repository owners, contributors, and readers to take manual action in most cases.

**What's Automated:**
- ✅ Organization-level rulesets enforce branch protections, PR requirements, and branch naming
- ✅ Default branch name (`main`) enforced for all new repositories
- ✅ Automated compliance auditing runs nightly
- ✅ Automated PRs created for missing standard files
- ✅ Automated branch cleanup (merged branches auto-delete)
- ✅ Automated notifications for compliance violations
- ✅ Compliance scorecard updated automatically

**What Requires Manual Action:**
- ⚠️ Review and merge automated PRs for standard files (one-time per repository)
- ⚠️ Request exceptions for legitimate deviations
- ⚠️ Update CI/CD workflows (where applicable)
- ⚠️ One-time migrations (default branch changes, branch renames)

---

## Organization Administrators

### Initial Setup (One-Time)

- [ ] Configure GitHub organization default branch name (`main`)
- [ ] Create and configure organization rulesets:
  - [ ] Branch naming patterns
  - [ ] Branch protections (PR required, reviewers, checks)
  - [ ] Linear history requirement
  - [ ] Force push/deletion restrictions
  - [ ] Auto-delete merged branches
- [ ] Set up repository template with standard files
- [ ] Configure automated compliance auditing (nightly runs)
- [ ] Set up automated PR creation for missing standard files
- [ ] Configure automated notifications (email/Slack)
- [ ] Create Notion databases (Scorecard, Actions/Exceptions, Release Views)
- [ ] Set up exception approval workflow

### Ongoing Operations

- [ ] Monitor compliance scorecard trends
- [ ] Review and approve exception requests
- [ ] Update rulesets based on feedback
- [ ] Maintain repository template
- [ ] Review and refine automation workflows
- [ ] Generate compliance reports (monthly/quarterly)

---

## Repository Owners & Administrators

### Initial Period (One-Time Actions)

**Week 1:**
- [ ] Review repositories in [Compliance Scorecard]([LINK]) - automated audits show current status
- [ ] Check compliance scores and identify gaps
- [ ] Request exceptions if repository has legitimate deviations (see exception process)

**Week 1-2:**
- [ ] Review and merge automated PRs for missing standard files (automated tools create these)
- [ ] Update default branch to `main` if not already (or request exception) - one-time migration
- [ ] Review automated stale branch cleanup reports and approve deletions
- [ ] Rename non-compliant branches (`feat/*` → `feature/*`, etc.) - one-time cleanup

**Week 2:**
- [ ] Verify branch protections are working (rulesets handle enforcement automatically, but verify)
- [ ] Ensure required status checks are configured per repository
- [ ] Test tag-based release workflow
- [ ] Review and approve exception requests from team members

### Ongoing (Minimal)

- [ ] Monitor compliance scorecard periodically (automated nightly updates)
- [ ] Address any compliance gaps identified in automated audits (if any)
- [ ] Keep standard files up to date (minimal maintenance)
- [ ] Review automated branch cleanup reports periodically

### CI/CD Workflows (Where Applicable)

**Note**: These actions only apply to repositories with CI/CD workflows. Many repositories may not have CI/CD.

- [ ] Review and update CI/CD workflows:
  - [ ] Ensure PR workflows only build/test/scan (no deployments)
  - [ ] Create tag workflows for releases (`vX.Y.Z`)
  - [ ] Remove branch-based deployments
- [ ] Test tag-based release workflow
- [ ] Verify required status checks are configured

---

## Contributors & Writers

### Initial Period (One-Time Actions)

- [ ] Update branch names if using non-compliant patterns (one-time)
- [ ] Review [Contributing Guide]([LINK]) for updated workflows
- [ ] Bookmark [Quick Reference Card]([LINK])
- [ ] Attend enablement session (optional, calendar invite to follow)

### Ongoing (Minimal)

**Most requirements are enforced automatically—no action needed:**
- ✅ Branch naming enforced automatically (GitHub prevents non-compliant branches)
- ✅ PR requirements enforced automatically (GitHub blocks direct pushes)
- ✅ Required checks enforced automatically (cannot merge until checks pass)
- ✅ Branch auto-delete happens automatically after merge

**What you need to do:**
- Follow branch naming conventions (`feature/*`, `bugfix/*`, `hotfix/*`, `backport/*`)
- Create PRs for changes (required automatically in multi-contributor repos)
- Use tags for releases (`vX.Y.Z`) instead of `release/*` branches
- Fix CI failures before requesting review (required automatically)
- Keep branches up to date with `main`

---

## Readers & Users

### Action Required

**None** - No action required. You can continue using repositories as before. Standard files and improved workflows will make repositories easier to understand and use.

**Optional:**
- Review [Compliance Dashboard]([LINK]) to understand repository compliance status
- Check [Quick Reference Guide]([LINK]) if you plan to contribute

---

## Evaluation Notes

### Questions to Consider

1. **Automation Coverage**: Are there any compliance requirements that cannot be automated? If so, what manual actions are truly necessary?

2. **Exception Frequency**: How many repositories will need exceptions? Can we reduce this through better automation or clearer policies?

3. **CI/CD Scope**: How many repositories actually have CI/CD workflows? Should CI/CD requirements be optional for repos without CI/CD?

4. **Standard Files**: Can we make standard file PRs auto-merge for non-critical files? Which files truly require review?

5. **Notification Strategy**: What level of notification is appropriate? Should we notify on every violation or only on significant changes?

6. **Compliance Score Thresholds**: What compliance score thresholds trigger action? Should there be different thresholds for different repository types?

7. **Migration Support**: What level of support is needed for one-time migrations (default branch changes, branch renames)? Can we automate more of this?

8. **Ongoing Maintenance**: What ongoing maintenance is truly required vs. what can be fully automated?

### Automation Opportunities

**Potential Additional Automation:**
- Auto-merge standard file PRs for non-critical files (LICENSE, CONTRIBUTING.md)
- Automated default branch migration (with approval workflow)
- Automated branch renaming (`feat/*` → `feature/*`)
- Automated CI/CD workflow updates (create PRs with suggested changes)
- Automated exception approval for common cases (single-contributor repos, etc.)
- Automated compliance score alerts (only for significant changes)

### Risk Assessment

**Low Risk (Can Automate Aggressively):**
- Standard file additions (non-critical files)
- Branch naming enforcement
- PR requirements
- Branch protections

**Medium Risk (Requires Review):**
- Standard file additions (critical files like SECURITY.md, CODEOWNERS)
- Default branch migrations
- CI/CD workflow changes
- Exception approvals

**High Risk (Requires Careful Review):**
- Critical security policy changes
- Major workflow changes
- Breaking changes to existing processes

---

## Success Criteria

**Automation Success:**
- ≥90% of compliance requirements enforced automatically
- ≤10% of repositories require manual action
- ≤5% exception request rate
- ≤1 hour/month average time per repository owner

**User Experience Success:**
- Zero action required for 90%+ of users
- Clear, automated notifications when action is needed
- Self-service exception request process
- Minimal disruption to existing workflows

---

## Next Steps

1. **Review this document** with compliance team and stakeholders
2. **Evaluate automation opportunities** - identify what can be further automated
3. **Prioritize action items** - determine which are truly necessary vs. nice-to-have
4. **Refine automation strategy** - adjust based on evaluation
5. **Update communications** - ensure messaging reflects push-driven approach
6. **Implement automation** - build out automated processes before rollout

