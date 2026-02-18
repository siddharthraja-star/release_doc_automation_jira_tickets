"""
Fetch user information from JIRA
"""

import requests
from state import JiraState


def fetch_user_info(state: JiraState) -> JiraState:
    """
    Fetch current user information to verify authentication
    """
    print("👤 Fetching current user information...\n")

    try:
        base_url = state['jira_url'].rstrip('/')
        url = f"{base_url}/rest/api/3/myself"

        headers = {
            "Accept": "application/json",
        }

        auth = (state['email'], state['api_key'])

        # Make GET request to fetch user info
        response = requests.get(url, headers=headers, auth=auth)

        print(f"User API Status: {response.status_code}")
        print(f"User API URL: {url}")

        if response.status_code == 200:
            user_data = response.json()

            print(f"\n{'='*80}")
            print("✅ AUTHENTICATION SUCCESSFUL")
            print(f"{'='*80}")
            print(f"Account ID: {user_data.get('accountId', 'N/A')}")
            print(f"Display Name: {user_data.get('displayName', 'N/A')}")
            print(f"Email: {user_data.get('emailAddress', 'N/A')}")
            print(f"Account Type: {user_data.get('accountType', 'N/A')}")
            print(f"Active: {user_data.get('active', 'N/A')}")
            print(f"{'='*80}\n")

            return {
                **state,
                "user_info": user_data,
                "status": "success"
            }
        else:
            error_msg = f"Failed to fetch user info: {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return {
                **state,
                "user_info": {},
                "status": "error",
                "error": error_msg
            }

    except Exception as e:
        error_msg = f"Exception occurred: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            **state,
            "user_info": {},
            "status": "error",
            "error": error_msg
        }
