#!/usr/bin/env python3
"""Helper script to create Notion databases for compliance tracking."""

import argparse
import os
import sys

from .notion_api import NotionAPI


def create_scorecard_database(notion_api: NotionAPI, parent_page_id: str) -> str:
    """Create Repos Scorecard database.

    Args:
        notion_api: Notion API client
        parent_page_id: Parent page ID

    Returns:
        Database ID
    """
    properties = {
        "Name": {"title": {}},
        "Compliance Score": {"number": {}},
        "Default Branch": {"rich_text": {}},
        "Archived": {"checkbox": {}},
        "Archived At": {"date": {}},
        "Forked": {"checkbox": {}},
        "Primary Language": {"rich_text": {}},
        "Primary Contributor": {"rich_text": {}},
        "Contributors Count": {"number": {}},
        "Last Commit Date": {"date": {}},
        "Time Since Last Commit": {"rich_text": {}},
        "Last Audit": {"date": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Compliant", "color": "green"},
                    {"name": "Needs Attention", "color": "yellow"},
                    {"name": "Non-Compliant", "color": "red"},
                    {"name": "Exception", "color": "blue"},
                ]
            }
        },
        "Owner": {"rich_text": {}},
        "Repository URL": {"url": {}},
    }

    db = notion_api.create_database(parent_page_id, "Repos Scorecard", properties)
    print(f"Created Repos Scorecard database: {db['id']}")
    print(f"URL: {db.get('url', 'N/A')}")
    return db["id"]


def create_actions_database(notion_api: NotionAPI, parent_page_id: str) -> str:
    """Create Actions/Exceptions database.

    Args:
        notion_api: Notion API client
        parent_page_id: Parent page ID

    Returns:
        Database ID
    """
    properties = {
        "Name": {"title": {}},
        "Type": {
            "select": {
                "options": [
                    {"name": "Exception", "color": "blue"},
                    {"name": "Action Item", "color": "yellow"},
                    {"name": "Remediation", "color": "orange"},
                ]
            }
        },
        "Repository": {"rich_text": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Open", "color": "red"},
                    {"name": "In Progress", "color": "yellow"},
                    {"name": "Resolved", "color": "green"},
                    {"name": "Approved", "color": "blue"},
                ]
            }
        },
        "Owner": {"rich_text": {}},
        "Due Date": {"date": {}},
        "Description": {"rich_text": {}},
        "Created": {"created_time": {}},
        "Updated": {"last_edited_time": {}},
    }

    db = notion_api.create_database(parent_page_id, "Actions & Exceptions", properties)
    print(f"Created Actions & Exceptions database: {db['id']}")
    print(f"URL: {db.get('url', 'N/A')}")
    return db["id"]


def create_release_views_database(notion_api: NotionAPI, parent_page_id: str) -> str:
    """Create Release Views database.

    Args:
        notion_api: Notion API client
        parent_page_id: Parent page ID

    Returns:
        Database ID
    """
    properties = {
        "Name": {"title": {}},
        "Product Version": {"rich_text": {}},
        "Repository": {"rich_text": {}},
        "Tag": {"rich_text": {}},
        "Commit SHA": {"rich_text": {}},
        "Package Version": {"rich_text": {}},
        "Environment": {
            "select": {
                "options": [
                    {"name": "staging", "color": "yellow"},
                    {"name": "production", "color": "green"},
                    {"name": "development", "color": "blue"},
                ]
            }
        },
        "Deployed At": {"date": {}},
        "Last Updated": {"date": {}},
    }

    db = notion_api.create_database(parent_page_id, "Release Views", properties)
    print(f"Created Release Views database: {db['id']}")
    print(f"URL: {db.get('url', 'N/A')}")
    return db["id"]


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Create Notion databases for compliance tracking")
    parser.add_argument("--parent-page-id", required=True, help="Notion parent page ID")
    parser.add_argument("--scorecard-only", action="store_true", help="Create only scorecard database")
    parser.add_argument("--actions-only", action="store_true", help="Create only actions database")
    parser.add_argument("--release-views-only", action="store_true", help="Create only release views database")

    args = parser.parse_args()

    try:
        notion_api = NotionAPI()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    created = []

    if args.scorecard_only or (not args.actions_only and not args.release_views_only):
        db_id = create_scorecard_database(notion_api, args.parent_page_id)
        created.append(("Scorecard", db_id))

    if args.actions_only or (not args.scorecard_only and not args.release_views_only):
        db_id = create_actions_database(notion_api, args.parent_page_id)
        created.append(("Actions", db_id))

    if args.release_views_only or (not args.scorecard_only and not args.actions_only):
        db_id = create_release_views_database(notion_api, args.parent_page_id)
        created.append(("Release Views", db_id))

    print("\nDatabase IDs to add to config.yaml:")
    for name, db_id in created:
        print(f"  {name}: {db_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

