"""
Process and display fetched tickets
"""

from state import JiraState


def process_tickets(state: JiraState) -> JiraState:
    """
    Process and display the fetched tickets
    """
    print("\n" + "="*80)
    print("📋 JIRA TICKETS")
    print("="*80 + "\n")

    if state["status"] == "error":
        print(f"❌ Error: {state['error']}")
        return state

    tickets = state["tickets"]

    if not tickets:
        print("No tickets found.")
        return state

    for idx, ticket in enumerate(tickets, 1):
        key = ticket.get("key", "N/A")
        ticket_id = ticket.get("id", "N/A")
        fields = ticket.get("fields", {})

        summary = fields.get("summary", "No summary")
        description = fields.get("description", "No description")
        status = fields.get("status", {}).get("name", "Unknown")
        priority = fields.get("priority", {}).get("name", "None")
        issue_type = fields.get("issuetype", {}).get("name", "Unknown")
        project = fields.get("project", {}).get("key", "Unknown")
        assignee = fields.get("assignee")
        assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
        created = fields.get("created", "Unknown")

        # Format description - handle Atlassian Document Format (ADF)
        if isinstance(description, dict):
            # Description is in ADF format, extract plain text
            description_text = ""
            if "content" in description:
                for content_item in description.get("content", []):
                    if content_item.get("type") == "paragraph":
                        for text_item in content_item.get("content", []):
                            if text_item.get("type") == "text":
                                description_text += text_item.get("text", "")
                        description_text += "\n"
            description = description_text.strip() if description_text else "No description"
        elif not description:
            description = "No description"

        # Get sprint information - handle different sprint data formats
        sprint_name = "No Sprint"
        sprint_field = fields.get("sprint")

        # Debug: Print sprint field structure for first ticket
        if idx == 1 and sprint_field is not None:
            print(f"\n[DEBUG] Sprint field type: {type(sprint_field)}")
            print(f"[DEBUG] Sprint field value: {sprint_field}\n")

        if sprint_field:
            # Handle list of sprints (common in standard API)
            if isinstance(sprint_field, list) and len(sprint_field) > 0:
                if isinstance(sprint_field[0], dict):
                    sprint_name = sprint_field[0].get("name", "Unknown")
                else:
                    sprint_name = str(sprint_field[0])
            # Handle single sprint object (common in Agile API)
            elif isinstance(sprint_field, dict):
                sprint_name = sprint_field.get("name", "Unknown")
            # Handle string sprint name
            elif isinstance(sprint_field, str):
                sprint_name = sprint_field

        # If still no sprint, check custom fields
        if sprint_name == "No Sprint":
            for field_key, field_value in fields.items():
                if "sprint" in field_key.lower() and field_value:
                    if isinstance(field_value, list) and len(field_value) > 0:
                        sprint_name = field_value[0].get("name", "Unknown") if isinstance(field_value[0], dict) else str(field_value[0])
                        break
                    elif isinstance(field_value, dict):
                        sprint_name = field_value.get("name", "Unknown")
                        break

        print(f"{idx}. [{key}] (ID: {ticket_id}) {summary}")
        print(f"   Project: {project} | Type: {issue_type} | Status: {status} | Priority: {priority}")
        print(f"   Sprint: {sprint_name} | Assignee: {assignee_name}")
        print(f"   Created: {created}")

        # Print full description
        if description and description != "No description":
            print(f"   Description: {description}")
        else:
            print(f"   Description: No description")

        print("-" * 80)

    print(f"\nTotal tickets: {len(tickets)}")

    return state
