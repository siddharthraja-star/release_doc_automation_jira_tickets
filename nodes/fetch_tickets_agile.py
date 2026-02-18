"""
Fetch tickets using JIRA Agile REST API
"""

import requests
from state import JiraState
from config import SPRINT_NAME


def fetch_tickets_agile(state: JiraState) -> JiraState:
    """
    Fetch tickets using JIRA Agile REST API - Better for sprint data
    """
    print("🔍 Fetching tickets using Agile API...")

    try:
        base_url = state['jira_url'].rstrip('/')

        # Find the sprint ID from the fetched sprints
        sprint_id = None

        for sprint in state.get("sprints", []):
            if sprint.get("name") == SPRINT_NAME:
                sprint_id = sprint.get("id")
                break

        if not sprint_id:
            print(f"❌ Sprint '{SPRINT_NAME}' not found in fetched sprints")
            return {
                **state,
                "tickets": [],
                "status": "error",
                "error": f"Sprint '{SPRINT_NAME}' not found"
            }

        print(f"Found sprint ID: {sprint_id}")

        # Use Agile API to fetch issues for this sprint
        url = f"{base_url}/rest/agile/1.0/sprint/{sprint_id}/issue"

        headers = {
            "Accept": "application/json"
        }

        auth = (state['email'], state['api_key'])

        # Query parameters - Add JQL filter for Story type
        params = {
            "maxResults": 1000,  # Fetch up to 1000 tickets (JIRA API max)
            "fields": "summary,description,status,assignee,created,updated,priority,issuetype,project,sprint",
            "jql": "issuetype = 'Story'"
        }

        # Make GET request
        response = requests.get(url, headers=headers, auth=auth, params=params)

        print(f"Response Status: {response.status_code}")
        print(f"Request URL: {url}")

        if response.status_code == 200:
            data = response.json()

            print(f"✅ Successfully fetched data from JIRA Agile API")
            tickets = data.get("issues", [])

            print(f"✅ Successfully fetched {len(tickets)} tickets")

            # Debug: Print sprint data from first ticket
            if tickets:
                first_ticket_fields = tickets[0].get("fields", {})
                sprint_data = first_ticket_fields.get("sprint")

                print(f"\n🏃 Sprint data in first ticket:")
                if sprint_data:
                    print(f"  Sprint: {sprint_data}")
                else:
                    print(f"  No sprint field found. Available fields:")
                    for field_name in first_ticket_fields.keys():
                        print(f"    - {field_name}")
                print()

            return {
                **state,
                "tickets": tickets,
                "status": "success",
                "error": None
            }
        else:
            error_msg = f"Failed to fetch tickets: {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return {
                **state,
                "tickets": [],
                "status": "error",
                "error": error_msg
            }

    except Exception as e:
        error_msg = f"Exception occurred: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            **state,
            "tickets": [],
            "status": "error",
            "error": error_msg
        }
