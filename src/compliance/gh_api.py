#!/usr/bin/env python3
"""GitHub API client for compliance auditing."""

import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote, urlencode

import urllib3

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False


class GitHubAPI:
    """GitHub REST API client for compliance checks."""

    def __init__(self, token: Optional[str] = None, org: Optional[str] = None):
        """Initialize GitHub API client.

        Args:
            token: GitHub token (defaults to GH_TOKEN or GH_GEI_TOKEN env var)
                  Or use GitHub App: set GITHUB_APP_ID, GITHUB_APP_PRIVATE_KEY, GITHUB_APP_INSTALLATION_ID
            org: Organization name (defaults to GITHUB_ORG env var)
        """
        self.org = org or os.getenv("GITHUB_ORG")
        if not self.org:
            raise ValueError("GitHub organization required (GITHUB_ORG env var)")

        self.base_url = os.getenv("GITHUB_API_URL", "https://api.github.com")
        self.http = urllib3.PoolManager()  # Initialize early for GitHub App auth

        # Try GitHub App authentication first
        app_id = os.getenv("GITHUB_APP_ID")
        app_private_key = os.getenv("GITHUB_APP_PRIVATE_KEY")
        app_installation_id = os.getenv("GITHUB_APP_INSTALLATION_ID")

        if app_id and app_private_key and JWT_AVAILABLE:
            # Auto-discover installation ID if not provided
            if not app_installation_id:
                app_installation_id = self._find_installation_id(app_id, app_private_key)

            if app_installation_id:
                self.token = self._get_installation_token(app_id, app_private_key, app_installation_id)
                self.token_type = "app"
            else:
                # Fall back to PAT if installation not found
                self.token = token or os.getenv("GH_TOKEN") or os.getenv("GH_GEI_TOKEN")
                self.token_type = "pat"
        else:
            # Fall back to personal access token
            self.token = token or os.getenv("GH_TOKEN") or os.getenv("GH_GEI_TOKEN")
            if not self.token:
                raise ValueError(
                    "GitHub token required. Set GH_TOKEN/GH_GEI_TOKEN or "
                    "GITHUB_APP_ID + GITHUB_APP_PRIVATE_KEY + (optional) GITHUB_APP_INSTALLATION_ID"
                )
            self.token_type = "pat"

        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "de-utils-compliance/0.1.0"
        }
        self._installation_token_expires = None

    def _generate_app_jwt(self, app_id: str, private_key: str) -> str:
        """Generate JWT for GitHub App authentication.

        Args:
            app_id: GitHub App ID (numeric string)
            private_key: Private key in PEM format (can be file path or key string)

        Returns:
            JWT token string
        """
        if not JWT_AVAILABLE:
            raise ImportError("pyjwt and cryptography required for GitHub App authentication. Install with: pip install pyjwt cryptography")

        # Expand tilde in path if present
        if private_key.startswith("~"):
            private_key = os.path.expanduser(private_key)

        # Load private key if it's a file path
        if os.path.exists(private_key):
            with open(private_key, "r") as f:
                private_key = f.read()

        # Ensure private key has proper PEM headers if missing
        if not private_key.strip().startswith("-----BEGIN"):
            # Try to add headers if it's just the key content
            private_key = f"-----BEGIN RSA PRIVATE KEY-----\n{private_key}\n-----END RSA PRIVATE KEY-----"

        now = int(time.time())
        payload = {
            "iat": now - 60,  # Issued at time (1 minute ago to account for clock skew)
            "exp": now + (10 * 60),  # Expires in 10 minutes
            "iss": app_id  # Issuer (App ID)
        }

        return jwt.encode(payload, private_key, algorithm="RS256")

    def _find_installation_id(self, app_id: str, private_key: str) -> Optional[str]:
        """Find installation ID for the organization.

        Args:
            app_id: GitHub App ID
            private_key: Private key (PEM format or file path)

        Returns:
            Installation ID or None
        """
        jwt_token = self._generate_app_jwt(app_id, private_key)

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "de-utils-compliance/0.1.0"
        }

        # List all installations
        url = f"{self.base_url}/app/installations"
        response = self.http.request("GET", url, headers=headers)

        if response.status >= 400:
            return None

        installations = json.loads(response.data.decode("utf-8"))

        # Find installation for this organization
        for installation in installations:
            account = installation.get("account", {})
            if account.get("login", "").lower() == self.org.lower():
                return str(installation["id"])

        return None

    def _get_installation_token(self, app_id: str, private_key: str, installation_id: str) -> str:
        """Get installation token from GitHub App credentials.

        Args:
            app_id: GitHub App ID
            private_key: Private key (PEM format or file path)
            installation_id: Installation ID

        Returns:
            Installation token
        """
        jwt_token = self._generate_app_jwt(app_id, private_key)

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "de-utils-compliance/0.1.0"
        }

        url = f"{self.base_url}/app/installations/{installation_id}/access_tokens"
        response = self.http.request("POST", url, headers=headers)

        if response.status >= 400:
            error_msg = response.data.decode("utf-8", errors="ignore")
            raise urllib3.exceptions.HTTPError(
                f"Failed to get installation token: HTTP {response.status}: {error_msg}"
            )

        data = json.loads(response.data.decode("utf-8"))
        token = data["token"]
        expires_at = data.get("expires_at")

        # Store expiration time
        if expires_at:
            self._installation_token_expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))

        print(f"Using GitHub App installation token (expires: {expires_at})", file=sys.stderr)
        return token

    def _refresh_installation_token_if_needed(self):
        """Refresh installation token if it's expired or about to expire."""
        if self.token_type != "app":
            return

        should_refresh = False
        if self._installation_token_expires:
            # Refresh if expires in less than 5 minutes or already expired
            time_until_expiry = (self._installation_token_expires - datetime.now(timezone.utc)).total_seconds()
            if time_until_expiry < 300:  # 5 minutes
                should_refresh = True
        else:
            # No expiration time stored, refresh to be safe
            should_refresh = True

        if should_refresh:
            app_id = os.getenv("GITHUB_APP_ID")
            app_private_key = os.getenv("GITHUB_APP_PRIVATE_KEY")
            app_installation_id = os.getenv("GITHUB_APP_INSTALLATION_ID")

            if not app_installation_id:
                app_installation_id = self._find_installation_id(app_id, app_private_key)

            if app_id and app_private_key and app_installation_id:
                self.token = self._get_installation_token(app_id, app_private_key, app_installation_id)
                self.headers["Authorization"] = f"token {self.token}"

    def _check_rate_limit(self) -> tuple[int, int, int]:
        """Check current rate limit status.

        Returns:
            (remaining, reset_timestamp, limit_total)
        """
        try:
            data = self._request("GET", "/rate_limit")
            core = data.get("resources", {}).get("core", {})
            return core.get("remaining", 0), core.get("reset", 0), core.get("limit", 5000)
        except Exception:
            return 5000, 0, 5000  # Default fallback

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling and rate limit retry."""
        # Refresh installation token if needed
        self._refresh_installation_token_if_needed()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Handle query parameters
        params = kwargs.pop("params", {})
        if params:
            url += "?" + urlencode(params)

        # Handle JSON body
        json_data = kwargs.pop("json", None)
        body = None
        if json_data:
            body = json.dumps(json_data).encode("utf-8")
            headers = self.headers.copy()
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
        else:
            headers = self.headers

        max_retries = 3
        for attempt in range(max_retries):
            # Check rate limit before request (proactive)
            if attempt == 0:
                remaining, reset_time, limit_total = self._check_rate_limit()
                if remaining < 100:  # Getting low
                    wait_time = max(reset_time - int(time.time()) + 1, 0)
                    if wait_time > 0 and wait_time < 3600:  # Don't wait more than an hour
                        reset_minutes = wait_time // 60
                        reset_seconds = wait_time % 60
                        if reset_minutes > 0:
                            print(f"\n⚠️  Rate limit low ({remaining}/{limit_total} remaining). Waiting {reset_minutes}m {reset_seconds}s until reset...", file=sys.stderr, flush=True)
                        else:
                            print(f"\n⚠️  Rate limit low ({remaining}/{limit_total} remaining). Waiting {reset_seconds}s until reset...", file=sys.stderr, flush=True)
                        # Show countdown
                        for remaining_wait in range(wait_time, 0, -10):
                            if remaining_wait > 10:
                                print(f"   Waiting... {remaining_wait}s remaining", file=sys.stderr, end="\r", flush=True)
                                time.sleep(10)
                            else:
                                print(f"   Waiting... {remaining_wait}s remaining", file=sys.stderr, end="\r", flush=True)
                                time.sleep(remaining_wait)
                        print("   Rate limit reset, continuing...", file=sys.stderr)

            response = self.http.request(
                method,
                url,
                headers=headers,
                body=body,
                **kwargs
            )

            # Handle 401 Bad credentials (token expired)
            if response.status == 401:
                error_data = {}
                try:
                    error_data = json.loads(response.data.decode("utf-8", errors="ignore"))
                except:
                    pass

                if "Bad credentials" in str(error_data) and self.token_type == "app" and attempt < max_retries - 1:
                    print(f"\n⚠️  Token expired, refreshing...", file=sys.stderr, flush=True)
                    # Force refresh by clearing expiration
                    self._installation_token_expires = None
                    self._refresh_installation_token_if_needed()
                    # Update headers with new token
                    headers["Authorization"] = f"token {self.token}"
                    continue

            # Handle rate limiting (403 with rate limit)
            if response.status == 403:
                rate_limit_reset = response.headers.get("X-RateLimit-Reset")
                rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", "0")
                rate_limit_total = response.headers.get("X-RateLimit-Limit", "5000")
                error_data = {}
                try:
                    error_data = json.loads(response.data.decode("utf-8", errors="ignore"))
                except:
                    pass

                if rate_limit_reset and ("rate limit" in str(error_data).lower() or "API rate limit" in str(error_data)):
                    reset_time = int(rate_limit_reset)
                    wait_time = max(reset_time - int(time.time()) + 1, 1)
                    if attempt < max_retries - 1:
                        reset_minutes = wait_time // 60
                        reset_seconds = wait_time % 60
                        print(f"\n🚫 Rate limit exceeded ({rate_limit_remaining}/{rate_limit_total} remaining).", file=sys.stderr, flush=True)
                        if reset_minutes > 0:
                            print(f"   Backing off for {reset_minutes}m {reset_seconds}s until reset...", file=sys.stderr, flush=True)
                        else:
                            print(f"   Backing off for {reset_seconds}s until reset...", file=sys.stderr, flush=True)
                        # Show countdown
                        for remaining_wait in range(wait_time, 0, -10):
                            if remaining_wait > 10:
                                print(f"   Waiting... {remaining_wait}s remaining", file=sys.stderr, end="\r", flush=True)
                                time.sleep(10)
                            else:
                                print(f"   Waiting... {remaining_wait}s remaining", file=sys.stderr, end="\r", flush=True)
                                time.sleep(remaining_wait)
                        print("   Rate limit reset, retrying...", file=sys.stderr)
                        continue

            # Check status code
            if response.status >= 400:
                error_msg = response.data.decode("utf-8", errors="ignore")
                raise urllib3.exceptions.HTTPError(
                    f"HTTP {response.status}: {error_msg}"
                )

            return json.loads(response.data.decode("utf-8"))

        raise urllib3.exceptions.HTTPError("Max retries exceeded for rate limit")

    def _paginate(self, endpoint: str, max_items: Optional[int] = None, **kwargs) -> List[Dict[str, Any]]:
        """Paginate through API results.

        Args:
            endpoint: API endpoint
            max_items: Maximum number of items to return (None = no limit)
            **kwargs: Additional request parameters
        """
        results = []
        page = 1
        per_page = 100

        while True:
            # Check if we've hit the max items limit
            if max_items and len(results) >= max_items:
                return results[:max_items]

            params = kwargs.get("params", {})
            params.update({"page": page, "per_page": per_page})

            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            if params:
                url += "?" + urlencode(params)

            # Remove params from kwargs for urllib3
            request_kwargs = {k: v for k, v in kwargs.items() if k != "params"}

            response = self.http.request(
                "GET",
                url,
                headers=self.headers,
                **request_kwargs
            )

            if response.status >= 400:
                error_msg = response.data.decode("utf-8", errors="ignore")
                raise urllib3.exceptions.HTTPError(
                    f"HTTP {response.status}: {error_msg}"
                )

            data = json.loads(response.data.decode("utf-8"))
            if isinstance(data, list):
                results.extend(data)
                if len(data) < per_page:
                    break
            else:
                results.append(data)
                break

            page += 1

        return results

    def list_org_repos(self) -> List[Dict[str, Any]]:
        """List all repositories in the organization."""
        return self._paginate(f"/orgs/{self.org}/repos", params={"type": "all"})

    def get_repo(self, repo: str) -> Dict[str, Any]:
        """Get repository details.

        Args:
            repo: Repository name (org/repo or just repo)
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"
        return self._request("GET", f"/repos/{repo}")

    def get_repo_languages(self, repo: str) -> Dict[str, int]:
        """Get repository languages breakdown.

        Args:
            repo: Repository name (org/repo or just repo)
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"
        return self._request("GET", f"/repos/{repo}/languages")

    def get_repo_contributors(self, repo: str) -> List[Dict[str, Any]]:
        """Get repository contributors.

        Args:
            repo: Repository name (org/repo or just repo)
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"
        return self._paginate(f"/repos/{repo}/contributors", params={"anon": "1"})

    def get_repo_commits(self, repo: str, branch: Optional[str] = None, since: Optional[str] = None, max_commits: Optional[int] = 1000) -> List[Dict[str, Any]]:
        """Get repository commits.

        Args:
            repo: Repository name (org/repo or just repo)
            branch: Branch name (defaults to default branch)
            since: ISO 8601 timestamp for filtering commits
            max_commits: Maximum number of commits to fetch (default: 1000, None = no limit)
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"

        params = {}
        if branch:
            params["sha"] = branch
        if since:
            params["since"] = since

        return self._paginate(f"/repos/{repo}/commits", max_items=max_commits, params=params)

    def get_latest_commit(self, repo: str, branch: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get latest commit on a branch.

        Args:
            repo: Repository name (org/repo or just repo)
            branch: Branch name (defaults to default branch)
        """
        # Only need the first commit, so limit to 1
        commits = self.get_repo_commits(repo, branch=branch, max_commits=1)
        return commits[0] if commits else None

    def get_branch_protection(self, repo: str, branch: str) -> Optional[Dict[str, Any]]:
        """Get branch protection rules.

        Args:
            repo: Repository name (org/repo or just repo)
            branch: Branch name
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"

        try:
            return self._request("GET", f"/repos/{repo}/branches/{quote(branch)}/protection")
        except urllib3.exceptions.HTTPError as e:
            if "404" in str(e):
                return None  # Branch protection not configured
            if "403" in str(e) and "not accessible by integration" in str(e):
                # Permission denied - GitHub App doesn't have Pull requests permission
                return None  # Return None instead of failing
            raise

    def list_branches(self, repo: str) -> List[Dict[str, Any]]:
        """List all branches in repository.

        Args:
            repo: Repository name (org/repo or just repo)
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"
        return self._paginate(f"/repos/{repo}/branches")

    def get_file_contents(self, repo: str, path: str, ref: Optional[str] = None) -> Optional[str]:
        """Get file contents from repository.

        Args:
            repo: Repository name (org/repo or just repo)
            path: File path in repository
            ref: Git reference (branch/tag/commit SHA)
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"

        params = {}
        if ref:
            params["ref"] = ref

        try:
            response = self._request("GET", f"/repos/{repo}/contents/{quote(path)}", params=params)
            import base64
            return base64.b64decode(response["content"]).decode("utf-8")
        except urllib3.exceptions.HTTPError as e:
            if "404" in str(e):
                return None
            raise

    def list_workflows(self, repo: str) -> List[Dict[str, Any]]:
        """List GitHub Actions workflows.

        Args:
            repo: Repository name (org/repo or just repo)
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"
        return self._request("GET", f"/repos/{repo}/actions/workflows").get("workflows", [])

    def get_workflow_runs(self, repo: str, workflow_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get workflow runs.

        Args:
            repo: Repository name (org/repo or just repo)
            workflow_id: Optional workflow ID to filter by
        """
        if "/" not in repo:
            repo = f"{self.org}/{repo}"

        endpoint = f"/repos/{repo}/actions/runs"
        if workflow_id:
            endpoint = f"/repos/{repo}/actions/workflows/{workflow_id}/runs"

        return self._paginate(endpoint, params={"per_page": 100})