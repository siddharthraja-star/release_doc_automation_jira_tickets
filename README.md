# JIRA Ticket Fetcher

A LangGraph-based workflow to fetch JIRA tickets and generate release documentation using ChatGPT.

## Project Structure

```
jira/
├── main.py                      # Entry point
├── config.py                    # Configuration loader (uses .env)
├── state.py                     # JiraState TypedDict definition
├── graph.py                     # LangGraph workflow creation
├── .env                         # Environment variables (secrets)
├── .env.example                 # Template for .env file
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── docs/                        # Output files directory
│   ├── jira_tickets.json       # Raw ticket data (generated)
│   └── release_doc_*.md        # Release documentation (generated)
├── nodes/                       # Individual workflow nodes
│   ├── __init__.py             # Node exports
│   ├── fetch_user_info.py      # Authenticate and fetch user info
│   ├── fetch_sprints.py        # Fetch sprints for SPARK project
│   ├── fetch_tickets_agile.py  # Fetch tickets using Agile API
│   ├── process_tickets.py      # Display tickets in console
│   └── generate_release_doc.py # Generate release doc using ChatGPT
├── main_backup.py              # Original monolithic version (backup)
└── README.md                   # This file
```

## Workflow

The workflow executes the following nodes in sequence:

1. **fetch_user_info** - Authenticates and verifies user access
2. **fetch_sprints** - Fetches all sprints for the SPARK project
3. **fetch_tickets_agile** - Fetches Story tickets from the specified sprint
4. **process_tickets** - Displays tickets with details in the console
5. **generate_release_doc** - Generates a markdown release document using GPT-4o

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file**:
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

3. **Update `.env` with your values**:
   ```env
   JIRA_URL=https://your-instance.atlassian.net/
   JIRA_API_KEY=your-jira-api-key
   JIRA_EMAIL=your-email@example.com
   SPRINT_NAME=Your Sprint Name
   OPENAI_API_KEY=your-openai-api-key

   # Optional: LangSmith for tracing (get key from https://smith.langchain.com/)
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your-langsmith-api-key
   LANGCHAIN_PROJECT=jira-ticket-fetcher
   ```

## Configuration

All configuration is managed through the `.env` file:

**Required:**
- `JIRA_URL` - Your JIRA instance URL
- `JIRA_API_KEY` - Your JIRA API token
- `JIRA_EMAIL` - Your JIRA email
- `SPRINT_NAME` - Target sprint name
- `OPENAI_API_KEY` - Your OpenAI API key

**Optional (LangSmith Tracing):**
- `LANGCHAIN_TRACING_V2` - Enable tracing (true/false)
- `LANGCHAIN_API_KEY` - Your LangSmith API key
- `LANGCHAIN_PROJECT` - Project name for organizing traces

**Note**: Never commit `.env` to git. It's already in `.gitignore`.

## Usage

```bash
python main.py
```

## LangSmith Tracing (Optional)

LangSmith provides debugging, monitoring, and evaluation for LangGraph workflows.

**Enable tracing:**
1. Sign up at [https://smith.langchain.com/](https://smith.langchain.com/)
2. Get your API key from the settings
3. Update your `.env` file:
   ```env
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your-langsmith-api-key
   LANGCHAIN_PROJECT=jira-ticket-fetcher
   ```

**Benefits:**
- 🔍 **Trace each node** - See execution flow through the workflow
- ⏱️ **Monitor performance** - Track execution time for each step
- 🐛 **Debug issues** - View inputs/outputs for each node
- 📊 **Track API calls** - Monitor OpenAI and JIRA API usage

View traces at: [https://smith.langchain.com/](https://smith.langchain.com/)

## Output

All output files are saved in the `docs/` directory:
- Console output with ticket details
- `docs/jira_tickets.json` - Raw ticket data in JSON format
- `docs/release_doc_{sprint_name}.md` - Generated release documentation with clickable Jira links
