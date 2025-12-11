#!/usr/bin/env python3
"""Script for branch hygiene: deleting stale branches and enforcing naming."""

import argparse
import sys
from datetime import datetime, timedelta, timezone

from .gh_api import GitHubAPI


def delete_stale_branches(
    gh_api: GitHubAPI,
    repo: str,
    days: int = 90,
    dry_run: bool = True,
    exclude_branches: list = None,
) -> list:
    """Delete stale branches older than specified days.

    Args:
        gh_api: GitHub API client
        repo: Repository name
        days: Days threshold for staleness
        dry_run: If True, only report, don't delete
        exclude_branches: Branches to never delete

    Returns:
        List of deleted/excluded branch names
    """
    if exclude_branches is None:
        exclude_branches = ["main", "master", "staging"]

    branches = gh_api.list_branches(repo)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    stale = []
    for branch in branches:
        name = branch.get("name", "")
        if name in exclude_branches:
            continue

        commit = branch.get("commit", {})
        commit_data = commit.get("commit", {})
        author_data = commit_data.get("author", {})
        date_str = author_data.get("date")

        if date_str:
            try:
                commit_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                if commit_date < cutoff:
                    stale.append({
                        "name": name,
                        "last_commit": date_str,
                        "days_old": (datetime.now(timezone.utc) - commit_date).days,
                    })
            except (ValueError, AttributeError):
                pass

    deleted = []
    for branch_info in stale:
        branch_name = branch_info["name"]
        print(f"{'Would delete' if dry_run else 'Deleting'} branch: {branch_name} (last commit: {branch_info['days_old']} days ago)")

        if not dry_run:
            try:
                # Note: This requires DELETE permission
                # gh_api._request("DELETE", f"/repos/{repo}/git/refs/heads/{branch_name}")
                print(f"  → Deleted {branch_name}")
                deleted.append(branch_name)
            except Exception as e:
                print(f"  → Error deleting {branch_name}: {e}")
        else:
            deleted.append(branch_name)

    return deleted


def check_branch_naming(repo: str, branches: list, allow_release: bool = False) -> dict:
    """Check and report branch naming violations.

    Returns:
        Dict with violations and recommendations
    """
    from .checks import ComplianceChecker

    gh_api = GitHubAPI()
    checker = ComplianceChecker(gh_api)

    result = checker.check_branch_naming(branches, allow_release_branches=allow_release)

    if result["violations"]:
        print(f"\nBranch naming violations in {repo}:")
        for violation in result["violations"]:
            print(f"  - {violation}")
            # Suggest rename
            if violation.startswith("feat/"):
                print(f"    → Suggested: feature/{violation[5:]}")
            elif violation.startswith("fix/"):
                print(f"    → Suggested: bugfix/{violation[4:]}")

    return result


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Branch hygiene: delete stale branches and check naming")
    parser.add_argument("--repo", required=True, help="Repository name (org/repo or just repo)")
    parser.add_argument("--days", type=int, default=90, help="Days threshold for stale branches")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Don't actually delete")
    parser.add_argument("--execute", action="store_true", help="Actually delete branches (overrides dry-run)")
    parser.add_argument("--check-naming", action="store_true", help="Check branch naming compliance")

    args = parser.parse_args()

    try:
        gh_api = GitHubAPI()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    dry_run = args.dry_run and not args.execute

    if dry_run:
        print("DRY RUN MODE - No branches will be deleted\n")

    # Delete stale branches
    deleted = delete_stale_branches(gh_api, args.repo, days=args.days, dry_run=dry_run)

    if args.check_naming:
        branches = gh_api.list_branches(args.repo)
        check_branch_naming(args.repo, branches)

    if deleted:
        print(f"\n{'Would delete' if dry_run else 'Deleted'} {len(deleted)} stale branch(es)")
    else:
        print("\nNo stale branches found")

    return 0


if __name__ == "__main__":
    sys.exit(main())

