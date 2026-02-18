"""
Generate release documentation using ChatGPT
"""

from pathlib import Path
from openai import OpenAI
from state import JiraState
from config import OPENAI_API_KEY, SPRINT_NAME, JIRA_URL

# Get the project root directory (parent of nodes directory)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DOCS_DIR = PROJECT_ROOT / "docs"

# Ensure docs directory exists
DOCS_DIR.mkdir(exist_ok=True)


def generate_release_doc(state: JiraState) -> JiraState:
    """
    Generate release documentation using ChatGPT
    """
    print("\n" + "="*80)
    print("📝 GENERATING RELEASE DOCUMENTATION")
    print("="*80 + "\n")

    if state["status"] == "error":
        print(f"❌ Cannot generate release doc: {state['error']}")
        return state

    tickets = state["tickets"]

    if not tickets:
        print("No tickets to document.")
        return state

    try:
        # Format tickets data for ChatGPT
        tickets_data = []
        for ticket in tickets:
            key = ticket.get("key", "N/A")
            fields = ticket.get("fields", {})

            summary = fields.get("summary", "No summary")
            description = fields.get("description", "")
            assignee = fields.get("assignee")
            assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
            priority = fields.get("priority", {}).get("name", "None")
            status = fields.get("status", {}).get("name", "Unknown")

            # Handle ADF description format
            if isinstance(description, dict):
                description_text = ""
                if "content" in description:
                    for content_item in description.get("content", []):
                        if content_item.get("type") == "paragraph":
                            for text_item in content_item.get("content", []):
                                if text_item.get("type") == "text":
                                    description_text += text_item.get("text", "")
                            description_text += "\n"
                description = description_text.strip()

            tickets_data.append({
                "key": key,
                "summary": summary,
                "description": description,
                "assignee": assignee_name,
                "priority": priority,
                "status": status
            })

        # Create the prompt for ChatGPT
        jira_base_url = JIRA_URL.rstrip('/')
        prompt = f"""You are a technical documentation writer creating a release document for a sprint.

**IMPORTANT FORMAT REQUIREMENTS:**
Start with "* Change log" header, then list each ticket using this EXACT format with clickable links:

* Change log
1. [[TICKET-KEY]({jira_base_url}/browse/TICKET-KEY)] [Component Tags] Title
Description paragraph (2-3 sentences) explaining what the ticket accomplishes, the problem it solves, and its impact.

2. [[TICKET-KEY]({jira_base_url}/browse/TICKET-KEY)] [Component Tags] Title
Description paragraph...

**EXAMPLE:**
* Change log
1. [[SPARK-3352]({jira_base_url}/browse/SPARK-3352)] [JAMS] [ML] Preserve Original Character Names Throughout the Pipeline
Ensures that original character names are retained and propagated consistently across the entire ML pipeline. Prevents unintended renaming or loss of identity metadata between stages, improving traceability and output correctness.

**INSTRUCTIONS:**
1. Make the ticket key a clickable markdown link: [[TICKET-KEY]({jira_base_url}/browse/TICKET-KEY)]
2. Extract component tags from the summary (e.g., [JAMS], [ML], [Backend], [API])
3. Remove the tags from the title to avoid duplication
4. Write clear 2-3 sentence descriptions focusing on:
   - What the change accomplishes
   - What problem it solves
   - Impact on the system/users
5. Number entries sequentially (1, 2, 3...)
6. Keep the title concise and descriptive

**Here are the tickets to document:**

"""
        for idx, ticket in enumerate(tickets_data, 1):
            prompt += f"""
Ticket #{idx}:
Key: {ticket['key']}
Summary: {ticket['summary']}
Description: {ticket['description']}
Assignee: {ticket['assignee']}
Priority: {ticket['priority']}
Status: {ticket['status']}
---
"""

        prompt += """

**OUTPUT:**
Return ONLY the markdown-formatted change log starting with "* Change log". No additional commentary or explanations."""

        # Initialize OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)

        print("🤖 Calling ChatGPT to generate release documentation...")

        # Make API call using gpt-4o (128k context window)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a technical documentation writer specializing in clear, concise release notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=16000  # Increased to handle large sprints with many tickets
        )

        release_doc = response.choices[0].message.content

        # Save to markdown file in docs directory
        filename = f"release_doc_{SPRINT_NAME.replace(' ', '_').replace(':', '')}.md"
        filepath = DOCS_DIR / filename
        with open(filepath, "w") as f:
            f.write(f"# Release Documentation - {SPRINT_NAME}\n\n")
            f.write(release_doc)

        print(f"✅ Release documentation generated successfully!")
        print(f"📄 Saved to: {filepath}\n")

        # Print preview
        print("Preview:")
        print("-" * 80)
        print(release_doc[:500] + "..." if len(release_doc) > 500 else release_doc)
        print("-" * 80)

        return state

    except Exception as e:
        error_msg = f"Failed to generate release doc: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            **state,
            "error": error_msg
        }
