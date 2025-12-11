#!/usr/bin/env python3
"""Notion API client for compliance scorecard and tracking."""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import urllib3


class NotionAPI:
    """Notion API client for database operations."""

    def __init__(self, token: Optional[str] = None):
        """Initialize Notion API client.

        Args:
            token: Notion integration token (defaults to NOTION_TOKEN env var)
        """
        self.token = token or os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("Notion token required (NOTION_TOKEN env var)")

        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.http = urllib3.PoolManager()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Handle JSON body
        json_data = kwargs.pop("json", None)
        body = None
        if json_data:
            body = json.dumps(json_data).encode("utf-8")

        response = self.http.request(
            method,
            url,
            headers=self.headers,
            body=body,
            **kwargs
        )

        # Check status code
        if response.status >= 400:
            error_msg = response.data.decode("utf-8", errors="ignore")
            raise urllib3.exceptions.HTTPError(
                f"HTTP {response.status}: {error_msg}"
            )

        return json.loads(response.data.decode("utf-8"))

    def create_database(self, parent_page_id: str, title: str, properties: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Create a Notion database.

        Args:
            parent_page_id: Parent page ID
            title: Database title
            properties: Database properties schema
        """
        data = {
            "parent": {"page_id": parent_page_id},
            "title": [{"text": {"content": title}}],
            "properties": properties
        }
        return self._request("POST", "/databases", json=data)

    def query_database(self, database_id: str, filter_obj: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Query a Notion database.

        Args:
            database_id: Database ID
            filter_obj: Optional filter object
        """
        results = []
        has_more = True
        start_cursor = None

        while has_more:
            data = {}
            if filter_obj:
                data["filter"] = filter_obj
            if start_cursor:
                data["start_cursor"] = start_cursor

            response = self._request("POST", f"/databases/{database_id}/query", json=data)
            results.extend(response.get("results", []))
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")

        return results

    def create_page(self, database_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create a page in a database.

        Args:
            database_id: Database ID
            properties: Page properties
        """
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        return self._request("POST", "/pages", json=data)

    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Update a page in a database.

        Args:
            page_id: Page ID
            properties: Updated properties
        """
        data = {"properties": properties}
        return self._request("PATCH", f"/pages/{page_id}", json=data)

    def find_page_by_title(self, database_id: str, title: str) -> Optional[Dict[str, Any]]:
        """Find a page by title property.

        Args:
            database_id: Database ID
            title: Title to search for
        """
        filter_obj = {
            "property": "Name",
            "title": {"equals": title}
        }
        results = self.query_database(database_id, filter_obj=filter_obj)
        return results[0] if results else None

    @staticmethod
    def property_text(value: str) -> Dict[str, Any]:
        """Create a text property."""
        return {"title": [{"text": {"content": value}}]}

    @staticmethod
    def property_rich_text(value: str) -> Dict[str, Any]:
        """Create a rich text property."""
        return {"rich_text": [{"text": {"content": value}}]}

    @staticmethod
    def property_number(value: float) -> Dict[str, Any]:
        """Create a number property."""
        return {"number": value}

    @staticmethod
    def property_select(value: str) -> Dict[str, Any]:
        """Create a select property."""
        return {"select": {"name": value}}

    @staticmethod
    def property_multi_select(values: List[str]) -> Dict[str, Any]:
        """Create a multi-select property."""
        return {"multi_select": [{"name": v} for v in values]}

    @staticmethod
    def property_date(value: datetime) -> Dict[str, Any]:
        """Create a date property."""
        return {"date": {"start": value.isoformat()}}

    @staticmethod
    def property_checkbox(value: bool) -> Dict[str, Any]:
        """Create a checkbox property."""
        return {"checkbox": value}

    @staticmethod
    def property_url(value: str) -> Dict[str, Any]:
        """Create a URL property."""
        return {"url": value}
