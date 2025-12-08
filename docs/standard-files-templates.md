# Standard Files Templates

Templates for required repository files: LICENSE, SECURITY.md, CONTRIBUTING.md, CODEOWNERS.

## LICENSE

### MIT License Template

```text
MIT License

Copyright (c) [YEAR] [ORGANIZATION NAME]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## SECURITY.md

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities to [security@example.com].

Do not open public issues for security vulnerabilities.

We will respond within 48 hours and provide updates on the resolution timeline.

## Security Best Practices

- Keep dependencies up to date
- Use secrets management for sensitive data
- Follow least privilege principles
- Review code changes before merging
```

## CONTRIBUTING.md

```markdown
# Contributing Guide

Thank you for contributing! This document provides guidelines for contributing to this repository.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Commit with clear messages
5. Push and create a pull request

## Branch Naming

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes
- `backport/` - Backports to previous versions

## Pull Request Process

1. All changes require a pull request
2. At least one reviewer must approve
3. All CI checks must pass
4. Keep PRs focused and small when possible

## Code Style

- Follow language-specific style guides
- Add tests for new features
- Update documentation as needed

## Release Process

- Releases are tag-based: `vX.Y.Z`
- Tags trigger automated builds
- No `release/*` branches

## Questions?

Open an issue or contact maintainers.
```

## CODEOWNERS

```text
# Default owners for everything in the repo
* @org/team-name

# Specific file/directory owners
/docs/ @org/docs-team
/src/ @org/eng-team
/.github/ @org/platform-team

# Language-specific owners
*.py @org/python-team
*.js @org/frontend-team
*.ts @org/frontend-team

# Infrastructure
/terraform/ @org/infrastructure-team
/.github/workflows/ @org/platform-team
```

## PR Template (.github/pull_request_template.md)

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Tests added/updated
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
```

## Issue Template (.github/ISSUE_TEMPLATE/bug_report.md)

```markdown
---
name: Bug Report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''
---

## Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Version: [e.g. 1.2.3]
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.9]

## Additional Context
Any other relevant information
```

## Automation Script

Create PRs to add standard files:

```python
# Example: Use GitHub API to create PRs
# This would be implemented as a separate script
```

See `src/compliance/standard_files_pr.py` for implementation (to be created).

