"""
LangGraph workflow creation
"""

from langgraph.graph import StateGraph, START, END
from state import JiraState
from nodes import (
    fetch_user_info,
    fetch_sprints,
    fetch_tickets_agile,
    process_tickets,
    generate_release_doc
)


def create_jira_graph():
    """
    Create the LangGraph workflow for fetching JIRA tickets
    """
    # Initialize the graph
    workflow = StateGraph(JiraState)

    # Add nodes
    workflow.add_node("fetch_user_info", fetch_user_info)
    workflow.add_node("fetch_sprints", fetch_sprints)
    workflow.add_node("fetch_tickets_agile", fetch_tickets_agile)
    workflow.add_node("process_tickets", process_tickets)
    workflow.add_node("generate_release_doc", generate_release_doc)

    # Add edges
    workflow.add_edge(START, "fetch_user_info")
    workflow.add_edge("fetch_user_info", "fetch_sprints")
    workflow.add_edge("fetch_sprints", "fetch_tickets_agile")
    workflow.add_edge("fetch_tickets_agile", "process_tickets")
    workflow.add_edge("process_tickets", "generate_release_doc")
    workflow.add_edge("generate_release_doc", END)

    # Compile the graph
    app = workflow.compile()

    return app
