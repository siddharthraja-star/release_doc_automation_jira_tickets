"""
State definition for JIRA workflow
"""

from typing import TypedDict, List, Dict, Any


class JiraState(TypedDict):
    """State for the JIRA ticket fetching workflow"""
    jira_url: str
    api_key: str
    email: str
    user_info: Dict[str, Any]
    projects: List[Dict[str, Any]]
    sprints: List[Dict[str, Any]]
    tickets: List[Dict[str, Any]]
    error: str | None
    status: str
