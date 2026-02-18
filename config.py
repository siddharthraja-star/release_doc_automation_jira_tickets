"""
Configuration settings for JIRA workflow
Loads from .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JIRA Configuration
JIRA_URL = os.getenv("JIRA_URL")
API_KEY = os.getenv("JIRA_API_KEY")
EMAIL = os.getenv("JIRA_EMAIL")
SPRINT_NAME = os.getenv("SPRINT_NAME")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LangSmith Configuration (Optional - for tracing)
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "jira-ticket-fetcher")

# Set LangSmith environment variables for tracing
if LANGCHAIN_TRACING_V2.lower() == "true":
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    if LANGCHAIN_API_KEY:
        os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    if LANGCHAIN_PROJECT:
        os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT

# Validate required environment variables
required_vars = {
    "JIRA_URL": JIRA_URL,
    "JIRA_API_KEY": API_KEY,
    "JIRA_EMAIL": EMAIL,
    "SPRINT_NAME": SPRINT_NAME,
    "OPENAI_API_KEY": OPENAI_API_KEY,
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}\n"
        f"Please create a .env file with all required variables. "
        f"See .env.example for template."
    )
