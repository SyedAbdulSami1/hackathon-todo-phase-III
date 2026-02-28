"""MCP tool for creating new todo tasks."""

from typing import Any, Dict
from tools.base import BaseMCPTool
from sqlmodel import Session
from models import Task
from db import engine


class AddTaskMCPTool(BaseMCPTool):
    """MCP tool to create new todo tasks."""

    @property
    def name(self) -> str:
        return "add_task"

    @property
    def description(self) -> str:
        return "Create a new todo task with title, description, due date, and priority."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The title of the task"},
                "description": {"type": "string", "description": "The description of the task (optional)"},
                "due_date": {"type": "string", "description": "Due date for the task (optional)"},
                "priority": {"type": "string", "description": "Priority of the task (optional)", "enum": ["low", "medium", "high"]}
            },
            "required": ["title"],
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool to create a new task."""
        title = kwargs.get("title")
        description = kwargs.get("description")
        due_date = kwargs.get("due_date")
        priority = kwargs.get("priority", "medium")

        # In a real implementation, we'd need to get the user_id from context
        # For now, we'll use a placeholder user_id
        user_id = kwargs.get("user_id", 1)  # Placeholder user_id

        # Create the task in the database
        with Session(engine) as session:
            task = Task(
                title=title,
                description=description,
                status="pending",
                user_id=user_id
            )
            session.add(task)
            session.commit()
            session.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "message": f"Task '{title}' created successfully"
        }
