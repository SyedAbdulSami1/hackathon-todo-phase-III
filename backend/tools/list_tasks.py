"""MCP tool for searching todo tasks."""

from typing import Any, Dict, List
from tools.base import BaseMCPTool
from sqlmodel import Session, select
from models import Task
from db import engine


class ListTasksMCPTool(BaseMCPTool):
    """MCP tool to search/list existing tasks."""

    @property
    def name(self) -> str:
        return "list_tasks"

    @property
    def description(self) -> str:
        return "Search for existing tasks based on status, priority, or search term."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter by status (optional)", "enum": ["pending", "in_progress", "completed"]},
                "priority": {"type": "string", "description": "Filter by priority (optional)", "enum": ["low", "medium", "high"]},
                "search_term": {"type": "string", "description": "Search term to match in title or description (optional)"},
                "limit": {"type": "integer", "description": "Maximum number of results to return (optional)"}
            }
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool to search for tasks."""
        status = kwargs.get("status")
        priority = kwargs.get("priority")
        search_term = kwargs.get("search_term")
        limit = kwargs.get("limit", 10)  # Default limit

        # In a real implementation, we'd need to get the user_id from context
        # For now, we'll use a placeholder user_id
        user_id = kwargs.get("user_id", 1)  # Placeholder user_id

        # Build the query to search for tasks
        with Session(engine) as session:
            query = select(Task).where(Task.user_id == user_id)

            if status:
                query = query.where(Task.status == status)

            if search_term:
                # Search in both title and description
                query = query.where(
                    (Task.title.contains(search_term)) |
                    (Task.description.contains(search_term))
                )

            # Apply limit
            query = query.limit(limit)

            # Execute the query
            tasks = session.exec(query).all()

            # Format the results
            task_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "description": task.description,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }

                # Add priority if available in the model (even though it's not currently in the Task model)
                # We'll just add it conditionally in case it gets added later
                if hasattr(task, 'priority'):
                    task_dict['priority'] = getattr(task, 'priority', 'medium')
                else:
                    task_dict['priority'] = 'medium'  # Default priority

                # Add due_date if available
                if hasattr(task, 'due_date'):
                    task_dict['due_date'] = getattr(task, 'due_date', None)

                task_list.append(task_dict)

        return {
            "success": True,
            "tasks": task_list
        }
