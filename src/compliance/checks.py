#!/usr/bin/env python3
"""Compliance policy checks and scoring."""

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from .gh_api import GitHubAPI


class ComplianceChecker:
    """Check repository compliance against SOP policies."""

    # Standard files that should exist
    STANDARD_FILES = ["LICENSE", "SECURITY.md", "CONTRIBUTING.md", "CODEOWNERS"]

    # Allowed branch name patterns
    ALLOWED_BRANCH_PATTERNS = [
        r"^feature/.*",
        r"^bugfix/.*",
        r"^hotfix/.*",
        r"^backport/.*",
    ]

    # Disallowed branch name patterns (for non-IaC repos)
    DISALLOWED_BRANCH_PATTERNS = [
        r"^release/.*",
        r"^v\d+\.\d+.*",
    ]

    # Bot patterns to exclude from contributor counts
    BOT_PATTERNS = [
        r".*\[bot\]$",
        r".*bot$",
        r"^dependabot",
        r"^renovate",
    ]

    def __init__(self, gh_api: GitHubAPI, config: Optional[Dict[str, Any]] = None):
        """Initialize compliance checker.

        Args:
            gh_api: GitHub API client
            config: Configuration dict with exceptions and settings
        """
        self.gh_api = gh_api
        self.config = config or {}
        self.exceptions = self.config.get("exceptions") or {}
        self.contributor_window_days = self.config.get("contributor_window_days", 365)
        self.primary_contributor_window_days = self.config.get("primary_contributor_window_days", 90)

    def check_default_branch(self, repo_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if default branch is 'main' (with exceptions).

        Returns:
            (is_compliant, message)
        """
        default_branch = repo_data.get("default_branch", "")
        repo_name = repo_data.get("full_name", repo_data.get("name", ""))

        # Check exceptions
        default_branch_exceptions = self.exceptions.get("default_branch") or {}
        if repo_name in default_branch_exceptions:
            expected = self.exceptions["default_branch"][repo_name]
            if default_branch == expected:
                return True, f"Exception: default branch is '{expected}'"
            return False, f"Exception expects '{expected}' but found '{default_branch}'"

        if default_branch == "main":
            return True, "Default branch is 'main'"
        return False, f"Default branch is '{default_branch}', expected 'main'"

    def check_branch_protection(self, repo: str, branch: str) -> Dict[str, Any]:
        """Check branch protection rules.

        Returns:
            Dict with protection checks
        """
        protection = self.gh_api.get_branch_protection(repo, branch)

        if not protection:
            return {
                "protected": False,
                "requires_pr": False,
                "required_reviewers": 0,
                "required_checks": [],
                "linear_history": False,
                "signed_commits": False,
                "restrict_deletions": False,
                "restrict_force_push": False,
            }

        required_status_checks = protection.get("required_status_checks", {})
        enforce_admins = protection.get("enforce_admins", {})
        restrictions = protection.get("restrictions")
        required_pull_request_reviews = protection.get("required_pull_request_reviews", {})

        return {
            "protected": True,
            "requires_pr": protection.get("required_pull_request_reviews") is not None,
            "required_reviewers": required_pull_request_reviews.get("required_approving_review_count", 0),
            "required_checks": required_status_checks.get("contexts", []),
            "linear_history": protection.get("required_linear_history", {}).get("enabled", False),
            "signed_commits": protection.get("required_signatures", False),
            "restrict_deletions": restrictions is not None,
            "restrict_force_push": protection.get("allow_force_pushes", {}).get("enabled", False) is False,
        }

    def check_branch_naming(self, branches: List[Dict[str, Any]], allow_release_branches: bool = False) -> Dict[str, Any]:
        """Check branch naming compliance.

        Args:
            branches: List of branch dicts with 'name' key
            allow_release_branches: Whether release branches are allowed (e.g., for IaC repos)

        Returns:
            Dict with compliance info
        """
        violations = []
        allowed_patterns = self.ALLOWED_BRANCH_PATTERNS.copy()
        disallowed_patterns = self.DISALLOWED_BRANCH_PATTERNS.copy()

        if allow_release_branches:
            disallowed_patterns = [p for p in disallowed_patterns if not p.startswith("^release/")]

        for branch in branches:
            name = branch.get("name", "")
            if name in ["main", "master", "staging"]:
                continue

            # Check if matches allowed pattern
            matches_allowed = any(re.match(pattern, name) for pattern in allowed_patterns)

            # Check if matches disallowed pattern
            matches_disallowed = any(re.match(pattern, name) for pattern in disallowed_patterns)

            if matches_disallowed:
                violations.append(name)
            elif not matches_allowed:
                violations.append(name)

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "total_branches": len(branches),
        }

    def check_standard_files(self, repo: str, default_branch: str) -> Dict[str, Any]:
        """Check for standard files.

        Returns:
            Dict with file check results
        """
        found = []
        missing = []

        for filename in self.STANDARD_FILES:
            content = self.gh_api.get_file_contents(repo, filename, ref=default_branch)
            if content:
                found.append(filename)
            else:
                missing.append(filename)

        return {
            "found": found,
            "missing": missing,
            "compliant": len(missing) == 0,
        }

    def check_ci_patterns(self, repo: str) -> Dict[str, Any]:
        """Check CI/CD workflow patterns.

        Returns:
            Dict with CI pattern checks
        """
        workflows = self.gh_api.list_workflows(repo)

        pr_workflows = []
        tag_workflows = []
        branch_deploy_workflows = []

        for workflow in workflows:
            path = workflow.get("path", "")
            name = workflow.get("name", "")

            # Check workflow file contents (simplified - would need to parse YAML for full check)
            if "pull_request" in path.lower() or "pr" in name.lower():
                pr_workflows.append(name)
            if "tag" in path.lower() or "release" in name.lower():
                tag_workflows.append(name)
            if "deploy" in path.lower() and "branch" in path.lower():
                branch_deploy_workflows.append(name)

        return {
            "has_pr_workflows": len(pr_workflows) > 0,
            "has_tag_workflows": len(tag_workflows) > 0,
            "has_branch_deploys": len(branch_deploy_workflows) > 0,
            "pr_workflows": pr_workflows,
            "tag_workflows": tag_workflows,
            "branch_deploy_workflows": branch_deploy_workflows,
        }

    def check_stale_branches(self, branches: List[Dict[str, Any]], days: int = 90) -> Dict[str, Any]:
        """Check for stale branches.

        Args:
            branches: List of branch dicts
            days: Days threshold for staleness

        Returns:
            Dict with stale branch info
        """
        stale = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        for branch in branches:
            name = branch.get("name", "")
            if name in ["main", "master", "staging"]:
                continue

            commit = branch.get("commit", {})
            commit_date_str = commit.get("commit", {}).get("author", {}).get("date")
            if commit_date_str:
                try:
                    commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
                    if commit_date < cutoff:
                        stale.append({
                            "name": name,
                            "last_commit": commit_date_str,
                        })
                except (ValueError, AttributeError):
                    pass

        return {
            "stale_count": len(stale),
            "stale_branches": stale,
            "threshold_days": days,
        }

    def get_primary_language(self, languages: Dict[str, int]) -> Optional[str]:
        """Get primary language by bytes.

        Args:
            languages: Dict mapping language names to byte counts

        Returns:
            Primary language name or None
        """
        if not languages:
            return None
        return max(languages.items(), key=lambda x: x[1])[0]

    def get_primary_contributor(self, repo: str, window_days: Optional[int] = None) -> Optional[Tuple[str, int]]:
        """Get primary contributor by commit count.

        Args:
            repo: Repository name
            window_days: Days to look back (defaults to primary_contributor_window_days)

        Returns:
            Tuple of (username, commit_count) or None
        """
        window_days = window_days or self.primary_contributor_window_days
        since = (datetime.now(timezone.utc) - timedelta(days=window_days)).isoformat()

        try:
            # Limit to 1000 commits max to avoid timeout on large repos
            commits = self.gh_api.get_repo_commits(repo, since=since, max_commits=1000)
            contributor_counts = {}

            for commit in commits:
                author = commit.get("author")
                if not author:
                    continue

                login = author.get("login")
                if not login or self._is_bot(login):
                    continue

                contributor_counts[login] = contributor_counts.get(login, 0) + 1

            if not contributor_counts:
                # Fallback to longer window
                if window_days < self.contributor_window_days:
                    return self.get_primary_contributor(repo, self.contributor_window_days)
                return None

            primary = max(contributor_counts.items(), key=lambda x: x[1])
            return primary
        except Exception:
            return None

    def get_contributors_count(self, repo: str, window_days: Optional[int] = None) -> int:
        """Get count of unique contributors.

        Args:
            repo: Repository name
            window_days: Days to look back (defaults to contributor_window_days)

        Returns:
            Number of unique contributors
        """
        window_days = window_days or self.contributor_window_days
        since = (datetime.now(timezone.utc) - timedelta(days=window_days)).isoformat()

        try:
            # Limit to 1000 commits max to avoid timeout on large repos
            commits = self.gh_api.get_repo_commits(repo, since=since, max_commits=1000)
            contributors = set()

            for commit in commits:
                author = commit.get("author")
                if not author:
                    continue

                login = author.get("login")
                if login and not self._is_bot(login):
                    contributors.add(login)

            return len(contributors)
        except Exception:
            return 0

    def humanize_time_since(self, dt: datetime) -> str:
        """Humanize time since datetime.

        Args:
            dt: Datetime to compare against now

        Returns:
            Humanized string like "2y 3m 5d" or "3m 5d" or "5d"
        """
        now = datetime.now(timezone.utc)
        delta = now - dt

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = delta.days % 30

        parts = []
        if years > 0:
            parts.append(f"{years}y")
        if months > 0:
            parts.append(f"{months}m")
        if days > 0:
            parts.append(f"{days}d")

        return " ".join(parts) if parts else "0d"

    def compute_compliance_score(self, checks: Dict[str, Any]) -> float:
        """Compute overall compliance score (0-100).

        Args:
            checks: Dict of check results

        Returns:
            Score from 0 to 100
        """
        weights = {
            "default_branch": 10,
            "branch_protection": 20,
            "branch_naming": 10,
            "standard_files": 15,
            "ci_patterns": 15,
            "stale_branches": 10,
        }

        total_weight = sum(weights.values())
        score = 0

        # Default branch check
        if checks.get("default_branch_compliant", False):
            score += weights["default_branch"]

        # Branch protection
        protection = checks.get("branch_protection", {})
        if protection.get("protected"):
            score += weights["branch_protection"]
        elif protection.get("requires_pr"):
            score += weights["branch_protection"] * 0.5

        # Branch naming
        if checks.get("branch_naming", {}).get("compliant", False):
            score += weights["branch_naming"]

        # Standard files
        files_check = checks.get("standard_files", {})
        found_count = len(files_check.get("found", []))
        total_files = len(self.STANDARD_FILES)
        if total_files > 0:
            score += weights["standard_files"] * (found_count / total_files)

        # CI patterns (simplified)
        ci_check = checks.get("ci_patterns", {})
        if ci_check.get("has_pr_workflows") and not ci_check.get("has_branch_deploys"):
            score += weights["ci_patterns"]

        # Stale branches (penalty)
        stale_count = checks.get("stale_branches", {}).get("stale_count", 0)
        if stale_count == 0:
            score += weights["stale_branches"]
        elif stale_count < 5:
            score += weights["stale_branches"] * 0.5

        return round((score / total_weight) * 100, 1)

    def _is_bot(self, username: str) -> bool:
        """Check if username matches bot patterns."""
        return any(re.match(pattern, username, re.IGNORECASE) for pattern in self.BOT_PATTERNS)

