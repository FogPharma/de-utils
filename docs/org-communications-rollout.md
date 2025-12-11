# GitHub Enterprise SOP Compliance - Organizational Communications

**Status:** Ready for Distribution
**Created:** [Date]

---

## What Are Git and GitHub?

**Git** is a distributed software version control system that tracks changes to code over time, allowing developers to work collaboratively, maintain history, and manage different versions of their work.

**GitHub** is a cloud-based platform built on Git that provides hosting for code repositories, collaboration tools (like Pull Requests), and automation capabilities (like GitHub Actions). Together, they form the foundation of modern software development workflows, enabling teams to write, review, test, and deploy code safely and efficiently.

---

## Problem Statement: Why Standardization and Control?

As our organization has grown, our GitHub repositories have developed inconsistent practices, creating operational risks and inefficiencies. Without standardized workflows, we face:

**Security Risks:**
- Unprotected branches allow direct pushes to production code, bypassing review processes
- Missing security policies and unclear reporting procedures increase vulnerability exposure
- Inconsistent access controls create compliance gaps

**Operational Risks:**
- Arbitrary and inconsistent naming makes it difficult to understand repository state and find relevant work
- Mixed deployment strategies create confusion and increase deployment errors
- Missing standard files (LICENSE, SECURITY.md, CONTRIBUTING.md) reduce clarity and slow onboarding

**Efficiency Losses:**
- Manual enforcement of policies requires constant monitoring and intervention
- Inconsistent automation patterns make it difficult to understand what runs when
- Lack of automated compliance checking means issues are discovered late, if at all

## Why This Matters

Our organization's success depends on software, and we've reached a scale where standardized practices are essential:

* **Scale**: With hundreds of repositories and a growing team, consistent workflows reduce confusion and enable efficient collaboration. You shouldn't have to learn different processes for each repository.

* **External Collaboration**: We work with external partners and contractors who need clear standards to contribute effectively. Standardized practices make collaboration smoother.

* **AI-Assisted Development**: AI tools generate code that must fit our standards. Consistent patterns help AI produce code that integrates seamlessly with our codebase.

* **Automated Enforcement**: Most requirements are enforced automatically by GitHub configuration, so you don't need to remember complex rules—GitHub prevents violations automatically, reducing your cognitive load.

* **Quality and Security**: Required reviews and automated checks catch issues early, improving code quality and security without requiring you to remember every rule.

## The Solution: Configuration and Automation

To address these challenges while minimizing burden on developers, we're implementing:

1. **Organization-Level Configuration**: Using GitHub's built-in rulesets and organization settings to establish and automatically enforce policies (branch naming, protections, PR requirements) so violations are prevented rather than detected after the fact.

2. **Automated Compliance Auditing**: Automated tools that continuously monitor repositories and identify gaps, reducing the need for manual checks.

3. **Automated Remediation**: Where possible, automated processes create Pull Requests for missing files, clean up stale branches, standardize configurations, and notify responsible individuals

4. **Exception-Based Flexibility**: A clear exception process for legitimate deviations, tracked and managed through our Notion database.

This approach means that **most compliance requirements are enforced automatically through configuration**, requiring minimal ongoing effort from developers. Audits serve primarily to identify one-time migration needs and monitor areas that cannot be fully automated (like workflow file content).

---

## What This Means for Me: Responsibilities by Role

| Responsibility | Readers | Contributors | Owners/Admins |
|----------------|---------|--------------|---------------|
| **No action required** | ✅ | | |
| **Follow branch naming conventions** (`feature/*`, `bugfix/*`, `hotfix/*`, `backport/*`) | | ✅ | ✅ |
| **Use Pull Requests** (multi-contributor repos only) | | ✅ | ✅ |
| **Use tags for releases** (`vX.Y.Z`) | | ✅ | ✅ |
| **Fix CI failures** before merge | | ✅ | ✅ |
| **Review automated PRs** for standard files | | | ✅ |
| **Request exceptions** if needed | | | ✅ |
| **Monitor compliance scorecard** | | | ✅ |
| **Update CI/CD workflows** (where applicable) | | | ✅ |
| **Configure required status checks** | | | ✅ |


# Details for Code Readers (non-developers)

We've summarized the changes above, but what impact on your work will it have?

## What This Means for You

**If you only read repositories or install software from our repos:**
- ✅ **No action needed** - You can continue using repos as before
- ✅ **Better documentation** - Standard files make repos easier to understand
- ✅ **More reliable releases** - Tag-based releases are more predictable
- ✅ **Consistent structure** - All repos follow the same patterns

**If you contribute code or own repositories, see sections below.**

---

# Details for Contributors

## What's Changing

### Branch Naming (Automatically Enforced)

**✅ Use These Patterns:**
- `feature/my-feature-name` - For new features
- `bugfix/fix-description` - For bug fixes
- `hotfix/urgent-fix-name` - For urgent production fixes
- `backport/version` - For backporting fixes (e.g., `backport/1.1`)

**❌ Don't Use:**
- `feat/` - Use `feature/` instead
- `fix/` - Use `bugfix/` instead
- `release/` - Use tags instead
- `v1.2.3` branches - Use tags instead
- Any other patterns not listed above

**Enforcement**: ✅ **Automated** - GitHub rulesets prevent creation of branches that don't match these patterns. You'll get an error if you try to create a non-compliant branch.

### Pull Request Process (Multi-Contributor Repos Only)

**Note**: These requirements apply only to repositories with multiple active contributors. Single-contributor repositories are exempt to avoid unnecessary friction for solo work and prototyping.

**For multi-contributor repositories, all changes to `main` require:**
1. Create a branch with proper naming (`feature/*`, `bugfix/*`, etc.) - enforced automatically
2. Make your changes and commit
3. Push the branch to GitHub
4. Create a Pull Request via GitHub UI - required automatically
5. Wait for review - 1-2 reviewers must approve (enforced automatically)
6. Wait for CI checks - All required checks must pass (enforced automatically)
7. Merge - Branch auto-deletes after merge (automatic)

**Enforcement**: GitHub organization rulesets automatically prevent violations. You cannot push directly to `main`, skip reviews, or merge with failing checks—GitHub blocks these actions automatically.

**Rationale**: PRs ensure code review, automated testing, and discussion before code is merged, improving quality and security. Automated enforcement means you don't have to remember these rules - GitHub prevents violations automatically.

### Releases (Automated Workflows)

**New Process:**
- Releases are **tag-based only** (no `release/*` branches) - ✅ **Enforced automatically**
- Create a tag: `git tag v1.2.3`
- Push tag: `git push origin v1.2.3`
- CI automatically builds, tests, and publishes - ✅ **Automated workflows** handle this

**Rationale**: Tag-based releases create immutable, versioned release points that are easier to track, roll back, and reproduce. Automated workflows handle the build/publish process once you create the tag.

## What You Need to Do

**Minimal Action Required**: Most requirements are enforced automatically through GitHub configuration. You primarily need to:

- **Follow branch naming conventions** - GitHub prevents creation of non-compliant branches automatically
- **Use Pull Requests** - Required automatically in multi-contributor repos (GitHub blocks direct pushes)
- **Use tags for releases** - GitHub prevents `release/*` branches automatically
- **Fix CI failures** - Required checks must pass before merge (enforced automatically)

**Optional**: Review the [Contributing Guide]([LINK]) and [Quick Reference Card]([LINK]) for detailed workflows. Most enforcement happens automatically—you don't need to remember complex rules.

## Do's and Don'ts

**✅ DO:**
- Use proper branch naming (`feature/*`, `bugfix/*`, etc.) - enforced automatically, but good practice
- Create PRs for all changes to multi-contributor repos - enforced automatically
- Wait for reviews before merging - enforced automatically
- Fix CI failures before requesting review - required automatically
- Use tags for releases (`vX.Y.Z`) - enforced automatically
- Keep your branches up to date with `main`

**❌ DON'T:**
- Push directly to `main` in multi-contributor repos - ✅ **Prevented automatically**
- Use non-compliant branch names (`feat/`, `fix/`, `release/*`) - ✅ **Prevented automatically**
- Merge your own PRs without review - ✅ **Prevented automatically**
- Merge PRs with failing CI checks - ✅ **Prevented automatically**
- Create `release/*` branches - ✅ **Prevented automatically**
- Deploy from branches - ✅ **Prevented automatically**
- Force push to `main` - ✅ **Prevented automatically**


# Details for Repository Owners & Administrators

## Policy Changes with Definitions and Rationale

### 1. Default Branch Standardization

**Requirement**: All repositories, going forward, must use `main` as the default branch

**Definition**: The default branch is the primary branch that serves as the base for all development work. It's the branch that's checked out by default when cloning a repository.

**Rationale**:
- Industry standard (replaced `master` for inclusivity)
- Consistency across all repositories improves developer experience
- Simplifies automation and tooling configuration
- Reduces confusion when switching between repositories

**Enforcement**:
- ✅ **Automated**: Organization setting ensures all NEW repositories automatically use `main`
- ⚠️ **Manual**: Existing repositories with `master` or other defaults require one-time migration or documented exceptions

**Exceptions**: Documented exceptions are allowed (e.g., legacy repos, `rcode` uses `master` for historical compatibility)

### 2. Branch Protection & Rulesets

**Scope**: These requirements apply only to **multi-contributor repositories** (repositories with more than one active contributor). Single-contributor repositories are exempt, as these rules would create unnecessary friction and could discourage the use of version control for prototypes and solo work.

**Terminology**:
- **Branch Protection**: GitHub settings that, for example, prevent direct pushes to protected branches, requiring Pull Requests instead
- **Rulesets**: Organization-level policies that enforce consistent rules across multiple repositories
- **Pull Request (PR)**: A mechanism for proposing changes, allowing code review and discussion before code is merged
- **Required Reviews**: Mandatory approval from one or more reviewers before code can be merged
- **Status Checks**: Automated tests, builds, and scans that must pass before a PR can be merged
- **Linear History**: A commit history without merge commits, achieved by squashing or rebasing PRs before merge
- **Signed Commits**: Cryptographically signed commits that verify the author's identity
- **Force Push**: Overwriting branch history, which can disrupt collaboration
- **Branch Deletion**: Deleting branches, which can cause data loss if done accidentally

**Requirements for Multi-Contributor Repositories**:
- **PR Required**: All changes to `main` must go through a Pull Request
- **Required Reviews**: 1-2 reviewers required (configurable per repository)
- **Required Status Checks**: All CI checks must pass before merge
- **Linear History**: No merge commits allowed (squash or rebase only)
- **Signed Commits**: Required (if organization policy mandates)
- **Restrictions**: Force push and branch deletion restricted on `main`

**Enforcement**:
- ✅ **GitHub Configuration**: Organization rulesets automatically enforce PR requirements, reviewer counts, required checks, and restrictions. Violations are prevented at the point of action—you cannot merge without meeting requirements.
- ✅ **Automated Auditing**: For repositories where GitHub rulesets cannot be applied (e.g., single-contributor repos that later gain contributors), automated compliance audits detect gaps and track remediation. These audits run nightly and update the Compliance Scorecard.
- ⚠️ **Manual Review**: Repository owners should periodically verify that protections are correctly configured, especially when repository ownership or contributor status changes.

**Rationale for Multi-Contributor Scope**: In repositories with multiple contributors, these protections are essential for:
- **Code Quality**: Peer review catches bugs and improves design
- **Knowledge Sharing**: PRs facilitate discussion and learning
- **Security**: Prevents accidental or malicious direct changes to production code
- **Collaboration**: Clear process reduces conflicts and coordination overhead

**Rationale for Single-Contributor Exemption**: Requiring PRs and reviews in single-contributor repositories would:
- Create unnecessary friction for solo work, experiments, and personal projects
- Discourage the use of version control for small projects
- Add overhead without providing benefits (no one to review your own PRs)
- Slow down rapid iteration and prototyping

**Note**: If a single-contributor repository gains additional contributors, branch protections should be enabled at that time. Automated audits will flag repositories that have multiple contributors but lack protections. Also, single-contributor repositories will not be prohibited from engaging in these practices if the owner prefers to do so.

### 3. Branch Naming Policy

**Requirement**: Branches must follow standardized naming patterns that indicate the type of work being done.

**Allowed Patterns**:
- `feature/*` - New features or enhancements
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes
- `backport/*` - Backporting fixes to prior versions (e.g., `backport/1.1`)

**Disallowed Patterns** (for single-release repos):
- `release/*` - Use tags instead (see Release Process below)
- `v*` branches - Use tags instead (e.g., `v1.2.3` should be a tag, not a branch)

**Note**: Because a lot of our products are bespoke data analysis solutions and web applications and services designed for internal use, only the current version of a product is ever used "in production". This is contrary to what we are used to with publicly available commercial and open source software products and libraries, of which multiple versions are often available. **Disallowed Patterns** restrictions will only apply to repositories comprising single-release products. Commit **tags** are the appropriate method to annotate milestone commits of these products, i.e., releases.

**Rationale**:
- **Clarity**: Standardized naming makes it immediately clear what type of work a branch contains
- **Automation**: Consistent patterns enable automated workflows and tooling
- **Organization**: Makes it easier to find and manage related branches
- **Prevents Confusion**: Separates release branches (disallowed) from release tags (required)

**Enforcement**:
- ✅ **Automated**: Organization rulesets prevent creation of branches that don't match allowed patterns
- ✅ **Automated**: GitHub automatically blocks branch creation attempts that violate naming rules
- ⚠️ **Manual**: Existing non-compliant branches need one-time renaming (`feat/*` → `feature/*`)

**Auto-delete Merged Branches**:
- ✅ **Automated**: Organization rulesets automatically delete branches after they're merged, keeping repositories clean

**Note**: *Commits* in feature branches are *not immediately* deleted. When a squash merge occurs, all branch commits are combined into a single commit on the target branch, i.e., `main`. The individual commits from the feature branch become unreachable from branch history but remain in the repository for approximately 90 days (via Git's reflog) and are accessible through GitHub's PR history. After this period, Git's garbage collection may remove unreachable commits, but the squash commit (containing all changes) remains permanently in the repository history.

### 4. Standard Files Required

**Requirement**: All repositories must include standard documentation files

**Required Files**:
- `LICENSE` - License file defining how code can be used
- `SECURITY.md` - Security policy and vulnerability reporting procedures
- `CONTRIBUTING.md` - Contribution guidelines for developers
- `CODEOWNERS` - Code ownership and automatic review assignments
- `.github/pull_request_template.md` - Pull Request template
- `.github/ISSUE_TEMPLATE/` - Issue templates (bug_report.md, feature_request.md)

**Definitions**:
- **LICENSE**: Legal document specifying how others can use, modify, and distribute the code
- **SECURITY.md**: Defines security policies, supported versions, and how to report vulnerabilities
- **CONTRIBUTING.md**: Guidelines for how to contribute code, including coding standards, testing requirements, and PR process
- **CODEOWNERS**: File that automatically assigns reviewers based on file paths, ensuring the right people review changes
- **PR Templates**: Standardized Pull Request description format ensuring consistent information
- **Issue Templates**: Structured templates for bug reports and feature requests

**Deployment**:
- **Existing Repositories**: These template files will be retroactively added to all existing, active repositories.
- **New Repositories**: These files are included by default in the organization's repository template, so all new repositories created through GitHub will automatically include these templates without any additional action required.

**Rationale**:
- **Legal Compliance**: LICENSE clarifies legal usage rights
- **Security**: SECURITY.md provides clear vulnerability reporting path and security expectations
- **Onboarding**: CONTRIBUTING.md helps new contributors understand how to participate
- **Efficiency**: CODEOWNERS automates reviewer assignment, reducing manual coordination
- **Consistency**: Standard files ensure all repositories have essential information
- **PR Templates**: Standardize Pull Request descriptions, ensuring consistent information (description, testing, checklist) is provided, making reviews more efficient
- **Issue Templates**: Guide users to provide structured, complete information when reporting bugs or requesting features, reducing back-and-forth and improving issue quality

**Enforcement**:
- ⚠️ **Semi-Automated**: Automated tools create Pull Requests with standard files for missing files
- ⚠️ **Manual**: Repository owners must review and merge these PRs (one-time per repository)
- ✅ **Automated**: Compliance audits detect missing files and track remediation

### 5. CI/CD Alignment, where applicable

CI/CD is short for Continuous Integration/Continuous Delivery. It refers to a software operations workflow which comprises automated code analysis, testing, packaging, annotation, etc. In many cases it also includes deployment to production systems.

**PR Workflows**:
- **Definition**: Workflows triggered by Pull Request events
- **Requirement**: Build, test, and scan only (no deployments)
- **Rationale**: PR workflows validate code before merge; deployments should only happen from tagged releases

**Tag Workflows**:
- **Definition**: Workflows triggered by pushing version tags (e.g., `v1.2.3`)
- **Requirement**: Build, package, publish, sign, and scan artifacts/images
- **Tag Format**: `vX.Y.Z` (SemVer - Semantic Versioning)
- **Rationale**: Tags create immutable release points; tag-based deployments ensure reproducible, versioned releases

**Branch Deployments**:
- **Requirement**: Removed/disabled (deployments only from tags)
- **Rationale**: Branch-based deployments are unpredictable and difficult to roll back; tag-based deployments provide clear versioning

**Required Checks**:
- **Requirement**: Must be configured and passing before merge
- **Rationale**: Ensures code quality, security, and functionality before code enters the main branch

**Enforcement**:
- ✅ **Automated**: Organization rulesets enforce that required status checks must pass before merge
- ⚠️ **Manual**: Workflow file content must be reviewed and updated (cannot be enforced via rulesets)
- ✅ **Automated**: Compliance audits detect branch-based deployments and track remediation

### 6. Branch Hygiene

**Requirement**: Maintain clean repository branch structure

**Stale Branches**:
- **Definition**: Branches with no commits for >90 days
- **Requirement**: Flagged for deletion
- **Rationale**: Reduces clutter, improves repository navigation, and reduces security surface area

**Merged Branches**:
- **Requirement**: Auto-deleted after merge
- **Rationale**: Prevents accumulation of merged branches that serve no purpose

**Naming Conformance**:
- **Requirement**: Existing branches must follow naming conventions
- **Rationale**: Consistency improves repository organization and enables automation

**Enforcement**:
- ✅ **Automated**: Merged branches automatically deleted by rulesets
- ⚠️ **Semi-Automated**: Automated tools identify stale branches and can delete them (with approval)
- ⚠️ **Manual**: Existing non-compliant branches need one-time renaming

## Your Responsibilities

**Minimal Action Required**: Most compliance requirements are enforced automatically through GitHub organization rulesets, configuration, and automated processes. Your primary responsibilities are:

- **Review automated PRs** - Automated tools create PRs for missing standard files; you just need to review and merge (one-time per repository)
- **Request exceptions if needed** - If your repository has legitimate deviations from standards
- **Monitor compliance scorecard** - Automated audits run nightly and update the scorecard; review periodically to stay informed
- **Update CI/CD workflows** (where applicable) - Ensure PR workflows only build/test/scan, create tag workflows for releases
- **Configure required status checks** - Set up per repository

**Note**: Branch protections, PR requirements, branch naming, and most other requirements are enforced automatically by GitHub configuration. You don't need to manually configure these—they're applied organization-wide through rulesets.

## Do's and Don'ts for Repo Owners

**✅ DO:**
- Review automated compliance scorecard weekly (minimal effort, high visibility)
- Request exceptions early if needed (automated exception tracking in Notion)
- Review and merge automated PRs for standard files (one-time per repo)
- Verify branch protections are working (rulesets handle enforcement automatically)
- Test tag-based releases before cutover
- Communicate changes to your contributors
- Keep CODEOWNERS file current (enables automated reviewer assignment)

**❌ DON'T:**
- Ignore automated compliance scorecard warnings
- Push directly to `main` (rulesets prevent this automatically)
- Create `release/*` branches (rulesets prevent this automatically)
- Skip required checks or reviews (rulesets prevent merge without these)
- Leave stale branches undeleted (automated cleanup available)
- Deploy from branches (use tags - automated workflows handle tag-based deployments)


# Resources, Workflows, and FAQs

## How to Request Exceptions

Exceptions are tracked in the [Notion Actions & Exceptions Database]([LINK]). To request an exception:

1. **Navigate** to the Actions & Exceptions database in Notion
2. **Create** a new entry with:
   - **Type**: "Exception"
   - **Repository**: Full repo name (e.g., `FogPharma/rcode`)
   - **Description**: Clear explanation of why exception is needed
   - **Proposed Alternative**: What you'll do instead
   - **Owner**: Your name/team
3. **Assign** to compliance team
4. **Wait** for approval (typically 1-2 business days)

**Common Exception Types:**
- Default branch name (e.g., `rcode` uses `master`)
- Release branch policy (IaC repos may need `release/*` branches)
- Reviewer count (small repos may request 1 reviewer instead of 2)
- CI check requirements (legacy repos may need phased approach)

**Exception Criteria:**
- Must have legitimate technical or business justification
- Must propose alternative approach that maintains security/compliance
- Must be documented and tracked
- Subject to periodic review

## Where to Find SOPs and Dashboards

**Notion Resources:**
- [Compliance Scorecard]([LINK]) - Per-repo compliance status and scores (automated nightly updates)
- [Actions & Exceptions Database]([LINK]) - Track exceptions and remediation tasks
- [Release Views]([LINK]) - Version tracking and deployment manifests (if applicable)
- [SOP Documentation]([LINK]) - Detailed procedures and policies
- [Enablement Playbook]([LINK]) - Training materials and quick reference

**GitHub Resources:**
- [Organization Profile]([LINK]) - Link to compliance page
- [de-utils Repository]([LINK]) - Compliance automation code
- [Compliance Workflow]([LINK]) - Automated audit runs (nightly)

## Common Workflows

### Starting a New Feature

```bash
# 1. Update your local main
git checkout main
git pull origin main

# 2. Create feature branch (must match naming pattern - enforced automatically)
git checkout -b feature/my-awesome-feature

# 3. Make your changes
# ... edit files ...

# 4. Commit
git add .
git commit -m "feat: enter mordor undetected"

# 5. Push
git push origin feature/my-awesome-feature

# 6. Create PR via GitHub UI (required automatically)
# 7. Wait for review and CI checks (required automatically)
# 8. Merge when approved (branch auto-deletes automatically)
```

### Creating a Release

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create tag (must be vX.Y.Z format)
git tag -a v1.2.3 -m "Release v1.2.3"

# 3. Push tag
git push origin v1.2.3

# 4. CI automatically (automated workflows):
#    - Builds artifacts
#    - Runs tests
#    - Publishes packages/images
#    - Creates GitHub release
```

### Backporting a Fix

```bash
# 1. Identify commit to backport
git log --oneline  # Find commit SHA

# 2. Create backport branch (must match naming pattern)
git checkout -b backport/1.1 main

# 3. Cherry-pick commit
git cherry-pick <commit-sha>

# 4. Create tag
git tag v1.1.1

# 5. Push branch and tag
git push origin backport/1.1
git push origin v1.1.1

# 6. Create PR for backport branch (required automatically)
# 7. After tag is created, delete branch (or let auto-delete handle it)
git push origin --delete backport/1.1
```

### Fixing a Broken Build

```bash
# 1. Create hotfix branch (must match naming pattern)
git checkout -b hotfix/fix-build-error main

# 2. Fix the issue
# ... make changes ...

# 3. Commit and push
git add .
git commit -m "fix: resolve build error"
git push origin hotfix/fix-build-error

# 4. Create PR (expedited review for hotfixes)
# 5. Merge quickly after approval (required checks still enforced automatically)
# 6. Tag release if needed (automated workflows handle build/publish)
```

## Frequently Asked Questions

**Q: Can I push directly to main?**
A: No, not to a multi-contributor repo. All changes require a Pull Request. This is enforced automatically by GitHub rulesets - you'll get an error if you try.

**Q: What if I need to deploy urgently?**
A: Use a `hotfix/*` branch and request expedited review. Tag-based releases are faster than branch deployments once set up, and automated workflows handle the build/publish process.

**Q: Can I use `feat/` instead of `feature/`?**
A: No, use `feature/` to comply with the naming policy. GitHub rulesets prevent creation of branches that don't match allowed patterns.

**Q: How do I release without a release branch?**
A: Create a tag (`vX.Y.Z`) which triggers the release workflow automatically. Automated workflows handle build, test, and publish.

**Q: What if my PR is blocked by required checks?**
A: Fix the failing checks. If you believe a check is incorrectly configured, contact the repo owner or compliance team. Required checks are enforced automatically - you cannot merge until they pass.

**Q: Can I merge my own PR?**
A: Only if you have at least one other reviewer's approval. Self-approval is not allowed - this is enforced automatically by rulesets.

**Q: What happens to my old branches?**
A: Branches inactive >90 days will be flagged for deletion by automated audits. Merged branches auto-delete automatically after merge.

**Q: How do I know if my repo is compliant?**
A: Check the [Compliance Scorecard]([LINK]) in Notion - it's updated automatically nightly.

**Q: Do I need to remember all these rules?**
A: Most rules are enforced automatically by GitHub rulesets, so violations are prevented automatically. You mainly need to follow the branch naming conventions and use PRs/tags as described.

**Q: What about single-contributor repositories?**
A: Single-contributor repositories are exempt from PR requirements and branch protections. However, branch naming conventions still apply. If your repository gains additional contributors, branch protections should be enabled.

**Q: How do I request an exception?**
A: Create an entry in the [Notion Actions & Exceptions Database]([LINK]) with the repository name, reason for exception, and proposed alternative approach. The compliance team will review and approve (typically 1-2 business days).

## Resources

**Quick Reference:**
- [Branch Naming Policy]([LINK]) - Definitions and rationale
- [PR Process Guide]([LINK]) - Detailed workflow
- [Release Process]([LINK]) - Tag-based releases
- [Quick Reference Card]([LINK]) - One-page cheat sheet

**Detailed Documentation:**
- [Contributing Guide]([LINK]) - Complete contributor guide
- [Enablement Playbook]([LINK]) - Training materials
- [Compliance Scorecard]([LINK]) - Per-repo compliance status (automated nightly updates)
- [Actions & Exceptions Database]([LINK]) - Track exceptions and remediation tasks
- [SOP Documentation]([LINK]) - Detailed procedures and policies

## Questions?

**Support:**
- **Email**: [ds_app_support@parabilismed.com]
- **Office Hours**: [Every other Tuesday at Lunch in Nexus 229]

