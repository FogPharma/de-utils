#!/usr/bin/env python3
"""CLI for running compliance audits and syncing to Notion."""

import argparse
import json
import os
import signal
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .checks import ComplianceChecker
from .gh_api import GitHubAPI
from .notion_api import NotionAPI


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}

    # Try default location
    default_path = Path(__file__).parent / "config.yaml"
    if default_path.exists():
        with open(default_path, "r") as f:
            return yaml.safe_load(f) or {}

    return {}


class TimeoutError(Exception):
    """Raised when audit times out."""
    pass


def timeout_handler(signum, frame):
    """Handle timeout signal."""
    raise TimeoutError("Audit timed out after 15 minutes")


def audit_repo(
    gh_api: GitHubAPI,
    checker: ComplianceChecker,
    notion_api: Optional[NotionAPI],
    repo_name: str,
    scorecard_db_id: Optional[str] = None,
    progress: Optional[tuple[int, int]] = None,
    skip_recent_hours: Optional[int] = None,
    timeout_minutes: int = 30,
    include_properties: Optional[List[str]] = None,
    exclude_properties: Optional[List[str]] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """Audit a single repository.

    Args:
        gh_api: GitHub API client
        checker: Compliance checker
        notion_api: Optional Notion API client
        repo_name: Repository name
        scorecard_db_id: Optional Notion database ID for scorecard
        progress: Optional tuple of (current, total) for progress display
        skip_recent_hours: Skip if audited within this many hours (None = don't skip)
        timeout_minutes: Maximum time to spend auditing this repo (default: 30)
        include_properties: List of properties to include (None = all)
        exclude_properties: List of properties to exclude (None = none)
        min_score: Minimum compliance score to process (None = no minimum)
        max_score: Maximum compliance score to process (None = no maximum)

    Returns:
        Audit results dict, or None if skipped/timed out
    """
    # Set up timeout
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60

    def check_timeout():
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            raise TimeoutError(f"Audit timed out after {timeout_minutes} minutes")
    # Check if we should skip recently audited repos
    if skip_recent_hours and notion_api and scorecard_db_id:
        existing_page = notion_api.find_page_by_title(scorecard_db_id, repo_name)
        if existing_page:
            last_audit_prop = existing_page.get("properties", {}).get("Last Audit", {})
            last_audit_date = last_audit_prop.get("date", {}).get("start")
            if last_audit_date:
                try:
                    last_audit = datetime.fromisoformat(last_audit_date.replace("Z", "+00:00"))
                    hours_since_audit = (datetime.now(timezone.utc) - last_audit).total_seconds() / 3600
                    if hours_since_audit < skip_recent_hours:
                        # Progress handled by main thread in parallel mode
                        return None
                except (ValueError, AttributeError):
                    pass  # If we can't parse the date, proceed with audit

    if progress:
        current, total = progress
        print(f"[{current}/{total}] Auditing {repo_name}...", file=sys.stderr, end="", flush=True)
    else:
        print(f"Auditing {repo_name}...", file=sys.stderr, end="", flush=True)

    # Get repo data
    print(" [fetching repo data]", file=sys.stderr, end="", flush=True)
    repo_data = gh_api.get_repo(repo_name)
    full_name = repo_data.get("full_name", repo_name)
    default_branch = repo_data.get("default_branch", "main")
    archived = repo_data.get("archived", False)
    forked = repo_data.get("fork", False)

    # Helper function to check if property should be included
    def should_include_property(prop_name: str) -> bool:
        """Check if property should be included based on include/exclude lists."""
        if include_properties is not None:
            if prop_name not in include_properties:
                return False
        if exclude_properties is not None:
            if prop_name in exclude_properties:
                return False
        return True

    # Get languages
    primary_language = None
    if should_include_property("primary_language"):
        print(" [languages]", file=sys.stderr, end="", flush=True)
        languages = gh_api.get_repo_languages(repo_name)
        primary_language = checker.get_primary_language(languages)

    # Get latest commit
    last_commit_date = None
    time_since_last_commit = None
    if should_include_property("last_commit_date") or should_include_property("time_since_last_commit"):
        print(" [commits]", file=sys.stderr, end="", flush=True)
        check_timeout()
        latest_commit = gh_api.get_latest_commit(repo_name, default_branch)
        if latest_commit:
            commit_data = latest_commit.get("commit", {})
            author_data = commit_data.get("author", {})
            date_str = author_data.get("date")
            if date_str:
                try:
                    last_commit_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    time_since_last_commit = checker.humanize_time_since(last_commit_date)
                except (ValueError, AttributeError):
                    pass

    # Get contributors (only if needed)
    primary_contributor = None
    contributors_count = None
    if should_include_property("primary_contributor") or should_include_property("contributors_count"):
        print(" [contributors]", file=sys.stderr, end="", flush=True)
        check_timeout()
        if should_include_property("primary_contributor"):
            try:
                primary_contributor_result = checker.get_primary_contributor(repo_name)
                primary_contributor = primary_contributor_result[0] if primary_contributor_result else None
            except TimeoutError:
                print(f" ⚠ Timeout getting primary contributor", file=sys.stderr)
                primary_contributor = None
                raise  # Re-raise to exit audit

        check_timeout()
        if should_include_property("contributors_count"):
            try:
                contributors_count = checker.get_contributors_count(repo_name)
            except TimeoutError:
                print(f" ⚠ Timeout getting contributors count", file=sys.stderr)
                contributors_count = 0
                raise  # Re-raise to exit audit

    # Run compliance checks
    print(" [checks]", file=sys.stderr, end="", flush=True)
    check_timeout()
    default_branch_compliant, default_branch_msg = checker.check_default_branch(repo_data)
    branch_protection = checker.check_branch_protection(repo_name, default_branch)

    check_timeout()
    branches = gh_api.list_branches(repo_name)
    # Check if repo allows release branches (e.g., IaC repos)
    allow_release_branches = checker.config.get("allow_release_branches") or []
    allow_release = repo_name in allow_release_branches
    branch_naming = checker.check_branch_naming(branches, allow_release_branches=allow_release)

    check_timeout()
    standard_files = checker.check_standard_files(repo_name, default_branch)
    ci_patterns = checker.check_ci_patterns(repo_name)
    stale_branches = checker.check_stale_branches(branches)

    # Compile checks
    checks = {
        "default_branch_compliant": default_branch_compliant,
        "default_branch_message": default_branch_msg,
        "branch_protection": branch_protection,
        "branch_naming": branch_naming,
        "standard_files": standard_files,
        "ci_patterns": ci_patterns,
        "stale_branches": stale_branches,
    }

    # Compute score
    compliance_score = checker.compute_compliance_score(checks)

    # Check score thresholds
    if min_score is not None and compliance_score < min_score:
        if progress:
            current, total = progress
            print(f" [score {compliance_score:.1f} < {min_score}, skipping]", file=sys.stderr)
        return None
    if max_score is not None and compliance_score > max_score:
        if progress:
            current, total = progress
            print(f" [score {compliance_score:.1f} > {max_score}, skipping]", file=sys.stderr)
        return None

    # Build result
    result = {
        "repo": full_name,
        "name": repo_data.get("name", ""),
        "default_branch": default_branch,
        "archived": archived,
        "archived_at": repo_data.get("archived_at"),
        "forked": forked,
        "primary_language": primary_language,
        "primary_contributor": primary_contributor,
        "contributors_count": contributors_count,
        "last_commit_date": last_commit_date.isoformat() if last_commit_date else None,
        "time_since_last_commit": time_since_last_commit,
        "compliance_score": compliance_score,
        "checks": checks,
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Sync to Notion if configured
    if notion_api and scorecard_db_id:
        print(" [syncing]", file=sys.stderr, end="", flush=True)
        check_timeout()
        sync_to_notion(notion_api, scorecard_db_id, result, include_properties=include_properties, exclude_properties=exclude_properties)

    # Progress and score reporting handled by main thread in parallel mode
    if not progress:
        print(f" ✓ (score: {compliance_score:.1f})", file=sys.stderr)
    return result


def audit_repo_wrapper(
    args_tuple: tuple,
) -> tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    """Wrapper function for parallel execution of audit_repo.

    Args:
        args_tuple: Tuple of (repo_name, config_dict, org, scorecard_db_id, skip_hours,
                   timeout_minutes, include_properties, exclude_properties, min_score, max_score, dry_run)

    Returns:
        Tuple of (repo_name, result_dict, error_type) where error_type is None, 'timeout', or 'error'
    """
    (
        repo_name,
        config,
        org,
        scorecard_db_id,
        skip_hours,
        timeout_minutes,
        include_properties,
        exclude_properties,
        min_score,
        max_score,
        dry_run,
    ) = args_tuple

    # Create new API instances for this thread
    try:
        gh_api = GitHubAPI(org=org)
    except ValueError as e:
        return (repo_name, None, f"API init error: {e}")

    checker = ComplianceChecker(gh_api, config)

    notion_api = None
    if not dry_run:
        try:
            notion_api = NotionAPI()
        except ValueError:
            pass  # Notion not available, continue without sync

    try:
        result = audit_repo(
            gh_api,
            checker,
            notion_api,
            repo_name,
            scorecard_db_id,
            progress=None,  # Progress handled by main thread
            skip_recent_hours=skip_hours,
            timeout_minutes=timeout_minutes,
            include_properties=include_properties,
            exclude_properties=exclude_properties,
            min_score=min_score,
            max_score=max_score,
        )
        return (repo_name, result, None)
    except TimeoutError as e:
        return (repo_name, None, "timeout")
    except Exception as e:
        return (repo_name, None, f"error: {str(e)}")


def sync_to_notion(
    notion_api: NotionAPI,
    database_id: str,
    result: Dict[str, Any],
    include_properties: Optional[List[str]] = None,
    exclude_properties: Optional[List[str]] = None,
) -> None:
    """Sync audit result to Notion database.

    Args:
        notion_api: Notion API client
        database_id: Notion database ID
        result: Audit result dict
        include_properties: List of properties to include (None = all)
        exclude_properties: List of properties to exclude (None = none)
    """
    repo_name = result["repo"]

    # Check if page exists
    existing_page = notion_api.find_page_by_title(database_id, repo_name)

    # Property mapping: result key -> Notion property name
    property_mapping = {
        "primary_language": "Primary Language",
        "primary_contributor": "Primary Contributor",
        "contributors_count": "Contributors Count",
        "last_commit_date": "Last Commit Date",
        "time_since_last_commit": "Time Since Last Commit",
        "default_branch": "Default Branch",
        "archived": "Archived",
        "compliance_score": "Compliance Score",
    }

    def should_include_property(prop_key: str) -> bool:
        """Check if property should be included."""
        if include_properties is not None:
            if prop_key not in include_properties:
                return False
        if exclude_properties is not None:
            if prop_key in exclude_properties:
                return False
        return True

    # Build properties dict
    properties = {
        "Name": notion_api.property_text(repo_name),  # Always include Name
        "Last Audit": notion_api.property_date(datetime.fromisoformat(result["audit_timestamp"])),  # Always include Last Audit
    }

    # Add compliance score (always include for filtering)
    if should_include_property("compliance_score"):
        properties["Compliance Score"] = notion_api.property_number(result["compliance_score"])

    # Add other properties conditionally
    if should_include_property("default_branch"):
        properties["Default Branch"] = notion_api.property_rich_text(result["default_branch"])

    if should_include_property("archived"):
        properties["Archived"] = notion_api.property_checkbox(result["archived"])

    if should_include_property("forked"):
        properties["Forked"] = notion_api.property_checkbox(result.get("forked", False))

    if should_include_property("primary_language") and result.get("primary_language"):
        properties["Primary Language"] = notion_api.property_rich_text(result["primary_language"] or "Unknown")

    if should_include_property("primary_contributor") and result.get("primary_contributor") is not None:
        properties["Primary Contributor"] = notion_api.property_rich_text(result["primary_contributor"] or "Unknown")

    if should_include_property("contributors_count") and result.get("contributors_count") is not None:
        properties["Contributors Count"] = notion_api.property_number(result["contributors_count"])

    if should_include_property("last_commit_date") and result.get("last_commit_date"):
        properties["Last Commit Date"] = notion_api.property_date(datetime.fromisoformat(result["last_commit_date"]))

    if should_include_property("time_since_last_commit") and result.get("time_since_last_commit"):
        properties["Time Since Last Commit"] = notion_api.property_rich_text(result["time_since_last_commit"] or "Unknown")

    # Remove None values
    properties = {k: v for k, v in properties.items() if v is not None}

    if existing_page:
        notion_api.update_page(existing_page["id"], properties)
    else:
        notion_api.create_page(database_id, properties)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="GitHub Enterprise SOP Compliance Audit")
    parser.add_argument("--config", help="Path to config.yaml file")
    parser.add_argument("--org", help="GitHub organization (overrides config/env)")
    parser.add_argument("--repo", help="Single repository to audit (org/repo or just repo)")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--notion-db", help="Notion database ID for scorecard")
    parser.add_argument("--dry-run", action="store_true", help="Don't sync to Notion")
    parser.add_argument("--skip-recent-hours", type=int, default=24, help="Skip repos audited within this many hours (default: 24, 0 = don't skip)")
    parser.add_argument("--include-properties", help="Comma-separated list of properties to include (e.g., 'primary_contributor,contributors_count')")
    parser.add_argument("--exclude-properties", help="Comma-separated list of properties to exclude (e.g., 'primary_language,last_commit_date')")
    parser.add_argument("--min-score", type=float, help="Only process repos with compliance score >= this value")
    parser.add_argument("--max-score", type=float, help="Only process repos with compliance score <= this value")
    parser.add_argument("--contributor-window-days", type=int, help="Override contributor window days (default: from config or 365)")
    parser.add_argument("--primary-contributor-window-days", type=int, help="Override primary contributor window days (default: from config or 90)")
    parser.add_argument("--max-workers", type=int, default=4, help="Maximum number of parallel workers (default: 4)")

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)

    # Override window days if provided
    if args.contributor_window_days is not None:
        config["contributor_window_days"] = args.contributor_window_days
    if args.primary_contributor_window_days is not None:
        config["primary_contributor_window_days"] = args.primary_contributor_window_days

    # Initialize APIs
    try:
        gh_api = GitHubAPI(org=args.org or config.get("github_org"))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    checker = ComplianceChecker(gh_api, config)

    # Parse property lists
    include_properties = None
    if args.include_properties:
        include_properties = [p.strip() for p in args.include_properties.split(",")]

    exclude_properties = None
    if args.exclude_properties:
        exclude_properties = [p.strip() for p in args.exclude_properties.split(",")]

    notion_api = None
    if not args.dry_run:
        try:
            notion_api = NotionAPI()
        except ValueError:
            print("Warning: Notion token not found, skipping Notion sync", file=sys.stderr)

    scorecard_db_id = args.notion_db or config.get("notion", {}).get("scorecard_db_id")

    # Check rate limit status
    try:
        # Access the private method to check rate limits
        remaining, reset_time, limit_total = gh_api._check_rate_limit()
        reset_minutes = max((reset_time - int(time.time())) // 60, 0)
        print(f"GitHub API rate limit: {remaining}/{limit_total} remaining", file=sys.stderr)
        if reset_minutes > 0:
            print(f"Rate limit resets in ~{reset_minutes} minutes", file=sys.stderr)
    except Exception:
        pass  # Rate limit check failed, continue anyway

    # Audit repositories
    if args.repo:
        repos = [args.repo]
    else:
        print("Fetching repository list...", file=sys.stderr)
        repos_data = gh_api.list_org_repos()
        repos = [r.get("full_name", r.get("name", "")) for r in repos_data]
        print(f"Found {len(repos)} repositories to audit", file=sys.stderr)

    results = []
    errors = []
    skipped = []
    timed_out = []
    total = len(repos)
    skip_hours = args.skip_recent_hours if args.skip_recent_hours > 0 else None

    # Thread-safe progress counter
    progress_lock = threading.Lock()
    completed_count = [0]  # Use list to allow modification in nested function

    def update_progress(repo_name: str, status: str = ""):
        """Thread-safe progress update."""
        with progress_lock:
            completed_count[0] += 1
            current = completed_count[0]
            status_str = f" [{status}]" if status else ""
            print(f"[{current}/{total}] {repo_name}{status_str}", file=sys.stderr, flush=True)

    # Prepare arguments for parallel execution
    audit_args = [
        (
            repo,
            config,
            args.org or config.get("github_org"),
            scorecard_db_id,
            skip_hours,
            30,  # Timeout: 30 minutes per repository
            include_properties,
            exclude_properties,
            args.min_score,
            args.max_score,
            args.dry_run,
        )
        for repo in repos
    ]

    # Execute audits in parallel
    max_workers = args.max_workers
    print(f"Processing {total} repositories with {max_workers} parallel workers...", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_repo = {
            executor.submit(audit_repo_wrapper, args_tuple): args_tuple[0]
            for args_tuple in audit_args
        }

        # Process completed tasks as they finish
        for future in as_completed(future_to_repo):
            repo_name = future_to_repo[future]
            try:
                repo_name_result, result, error_type = future.result()

                if error_type == "timeout":
                    timed_out.append(repo_name_result)
                    update_progress(repo_name_result, "⏱ Timeout")
                elif error_type and error_type.startswith("error"):
                    errors.append(repo_name_result)
                    error_msg = error_type.split(":", 1)[1] if ":" in error_type else error_type
                    update_progress(repo_name_result, f"✗ Error: {error_msg}")
                elif result is None:
                    skipped.append(repo_name_result)
                    update_progress(repo_name_result, "Skipped")
                else:
                    results.append(result)
                    score = result.get("compliance_score", 0)
                    update_progress(repo_name_result, f"✓ (score: {score:.1f})")
            except Exception as e:
                errors.append(repo_name)
                update_progress(repo_name, f"✗ Exception: {e}")

    # Print summary
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Audit complete: {len(results)}/{total} repositories", file=sys.stderr)
    if skipped:
        print(f"Skipped (recent): {len(skipped)} repositories", file=sys.stderr)
    if timed_out:
        print(f"Timed out: {len(timed_out)} repositories", file=sys.stderr)
    if errors:
        print(f"Errors: {len(errors)} repositories failed", file=sys.stderr)
    if results:
        avg_score = sum(r["compliance_score"] for r in results) / len(results)
        print(f"Average compliance score: {avg_score:.1f}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    # Output results
    output = {
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "repos_audited": len(results),
        "results": results,
    }

    if args.output:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(output, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())

