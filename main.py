"""
LangGraph workflow to fetch JIRA tickets using REST API
"""

import json
from pathlib import Path
from config import JIRA_URL, API_KEY, EMAIL
from graph import create_jira_graph

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
DOCS_DIR = SCRIPT_DIR / "docs"

# Ensure docs directory exists
DOCS_DIR.mkdir(exist_ok=True)


def main():
    """
    Main function to run the JIRA ticket fetching workflow
    """
    print("🚀 Starting JIRA Ticket Fetcher\n")

    # Create the graph
    app = create_jira_graph()

    # Initial state
    initial_state = {
        "jira_url": JIRA_URL,
        "api_key": API_KEY,
        "email": EMAIL,
        "user_info": {},
        "projects": [],
        "sprints": [],
        "tickets": [],
        "error": None,
        "status": "pending"
    }

    # Run the workflow
    final_state = app.invoke(initial_state)

    print("\n✅ Workflow completed!")

    # Optionally save tickets to JSON file
    if final_state["status"] == "success" and final_state["tickets"]:
        output_path = DOCS_DIR / "jira_tickets.json"
        with open(output_path, "w") as f:
            json.dump(final_state["tickets"], f, indent=2)
        print(f"💾 Tickets saved to {output_path}")


if __name__ == "__main__":
    main()
