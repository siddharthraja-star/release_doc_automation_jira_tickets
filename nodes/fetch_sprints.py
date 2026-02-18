"""
Fetch sprints from JIRA
"""

import requests
from state import JiraState


def fetch_sprints(state: JiraState) -> JiraState:
    """
    Fetch all sprints for SPARK project
    """
    print("🏃 Fetching sprints for SPARK project...")

    try:
        base_url = state['jira_url'].rstrip('/')

        # First, get the board ID for SPARK project
        board_url = f"{base_url}/rest/agile/1.0/board"

        headers = {
            "Accept": "application/json",
        }

        auth = (state['email'], state['api_key'])

        # Get boards for SPARK project
        params = {"projectKeyOrId": "SPARK"}
        response = requests.get(board_url, headers=headers, auth=auth, params=params)

        print(f"Board API Status: {response.status_code}")

        if response.status_code != 200:
            error_msg = f"Failed to fetch boards: {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return {
                **state,
                "sprints": [],
                "status": "error",
                "error": error_msg
            }

        boards_data = response.json()
        boards = boards_data.get("values", [])

        if not boards:
            print("❌ No boards found for SPARK project")
            return {
                **state,
                "sprints": [],
                "status": "success"
            }

        # Get sprints from the first board
        board_id = boards[0].get("id")
        board_name = boards[0].get("name", "Unknown")
        print(f"Found board: {board_name} (ID: {board_id})")

        # Fetch sprints for this board
        sprint_url = f"{base_url}/rest/agile/1.0/board/{board_id}/sprint"
        sprint_response = requests.get(sprint_url, headers=headers, auth=auth)

        print(f"Sprint API Status: {sprint_response.status_code}")

        if sprint_response.status_code == 200:
            sprint_data = sprint_response.json()
            sprints = sprint_data.get("values", [])

            print(f"\n{'='*80}")
            print(f"🏃 AVAILABLE SPRINTS IN SPARK PROJECT ({len(sprints)} total)")
            print(f"{'='*80}\n")

            for idx, sprint in enumerate(sprints, 1):
                sprint_id = sprint.get("id", "N/A")
                sprint_name = sprint.get("name", "No name")
                sprint_state = sprint.get("state", "Unknown")
                print(f"{idx}. [{sprint_id}] {sprint_name} (State: {sprint_state})")

            print(f"\n{'='*80}\n")

            return {
                **state,
                "sprints": sprints,
                "status": "success"
            }
        else:
            error_msg = f"Failed to fetch sprints: {sprint_response.status_code} - {sprint_response.text}"
            print(f"❌ {error_msg}")
            return {
                **state,
                "sprints": [],
                "status": "error",
                "error": error_msg
            }

    except Exception as e:
        error_msg = f"Exception occurred: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            **state,
            "sprints": [],
            "status": "error",
            "error": error_msg
        }
