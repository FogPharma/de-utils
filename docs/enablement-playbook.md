# Enablement Playbook

Training materials and playbooks for GitHub Enterprise SOP Compliance.

## Quick Reference Card

### For Contributors

**Branch Naming**
- ✅ `feature/my-feature`
- ✅ `bugfix/fix-name`
- ✅ `hotfix/urgent-fix`
- ✅ `backport/1.1`
- ❌ `feat/`, `fix/`, `release/`, `v1.2.3`

**Pull Requests**
1. Create branch: `git checkout -b feature/my-feature`
2. Make changes and commit
3. Push: `git push origin feature/my-feature`
4. Create PR via GitHub UI
5. Wait for review and CI checks
6. Merge (branch auto-deletes)

**Releases**
- Create tag: `git tag v1.2.3`
- Push tag: `git push origin v1.2.3`
- CI automatically builds and publishes

### For Repo Owners

**Compliance Checklist**
- [ ] Default branch is `main` (or exception approved)
- [ ] Branch protection enabled
- [ ] Standard files present (LICENSE, SECURITY.md, CONTRIBUTING.md, CODEOWNERS)
- [ ] CI workflows configured (PR builds, tag releases)
- [ ] Stale branches cleaned up
- [ ] Compliance score > 80%

**Exception Request**
1. Go to Notion Actions & Exceptions
2. Create new entry
3. Fill in repository, reason, alternative
4. Assign to compliance team

## Common Scenarios

### Scenario 1: Starting a New Feature

```bash
# 1. Update main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-authentication

# 3. Make changes
# ... edit files ...

# 4. Commit
git add .
git commit -m "feat: add user authentication"

# 5. Push
git push origin feature/user-authentication

# 6. Create PR via GitHub UI
# 7. Wait for review
# 8. Merge when approved
```

### Scenario 2: Creating a Release

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create tag
git tag -a v1.2.3 -m "Release v1.2.3"

# 3. Push tag
git push origin v1.2.3

# 4. CI automatically:
#    - Builds artifacts
#    - Runs tests
#    - Publishes packages
#    - Creates GitHub release
```

### Scenario 3: Backporting a Fix

```bash
# 1. Identify commit to backport
git log --oneline  # Find commit SHA

# 2. Create backport branch
git checkout -b backport/1.1 main

# 3. Cherry-pick commit
git cherry-pick <commit-sha>

# 4. Create tag
git tag v1.1.1

# 5. Push
git push origin backport/1.1
git push origin v1.1.1

# 6. Delete branch after tag created
git push origin --delete backport/1.1
```

### Scenario 4: Fixing a Broken Build

```bash
# 1. Create hotfix branch
git checkout -b hotfix/fix-build-error main

# 2. Fix the issue
# ... make changes ...

# 3. Commit and push
git add .
git commit -m "fix: resolve build error"
git push origin hotfix/fix-build-error

# 4. Create PR
# 5. Merge quickly (hotfix)
# 6. Tag release if needed
```

## FAQ

**Q: Can I push directly to main?**
A: No, all changes require a PR.

**Q: What if I need to deploy urgently?**
A: Use hotfix branch and expedited review process.

**Q: Can I use `feat/` instead of `feature/`?**
A: No, use `feature/` to comply with naming policy.

**Q: How do I release without a release branch?**
A: Create a tag (`vX.Y.Z`) which triggers the release workflow.

**Q: What if my repo needs an exception?**
A: Request it in Notion Actions & Exceptions database.

**Q: How do I know my repo's compliance status?**
A: Check the Notion Scorecard database.

## Troubleshooting

**Problem**: PR blocked by required checks
**Solution**: Ensure CI workflows are passing, check workflow files

**Problem**: Can't push to main
**Solution**: Create a branch and PR instead

**Problem**: Branch naming rejected
**Solution**: Use allowed patterns: `feature/*`, `bugfix/*`, `hotfix/*`, `backport/*`

**Problem**: Tag not triggering release
**Solution**: Verify tag format (`vX.Y.Z`), check workflow triggers

## Resources

- [Compliance Scorecard]([LINK])
- [Contributing Guide]([LINK])
- [Release Process]([LINK])
- [Exception Request]([LINK])

