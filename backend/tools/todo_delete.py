"""MCP tool for deleting todo tasks."""

from typing import Any, Dict
from tools.base import BaseMCPTool
from sqlmodel import Session
from models import Task
from db import engine


class TodoDeleteMCPTool(BaseMCPTool):
    """MCP tool to delete todo tasks."""

    @property
    def name(self) -> str:
        return "todo_delete_tool"

    @property
    def description(self) -> str:
        return "Delete a todo task by ID or title."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "The ID of the task to delete (either task_id or title required)"},
                "title": {"type": "string", "description": "The title of the task to delete (either task_id or title required)"}
            },
            "anyOf": [
                {"required": ["task_id"]},
                {"required": ["title"]}
            ]
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool to delete a task."""
        task_id = kwargs.get("task_id")
        title = kwargs.get("title")

        # In a real implementation, we'd need to get the user_id from context
        # For now, we'll use a placeholder user_id
        user_id = kwargs.get("user_id", 1)  # Placeholder user_id

        # Delete the task from the database
        with Session(engine) as session:
            if task_id:
                # Delete by ID
                task = session.get(Task, task_id)

                if not task:
                    return {
                        "success": False,
                        "message": f"Task with ID {task_id} not found"
                    }

                # Check that the task belongs to the user
                if task.user_id != user_id:
                    return {
                        "success": False,
                        "message": "Unauthorized: You can only delete your own tasks"
                    }

                session.delete(task)
                session.commit()

                return {
                    "success": True,
                    "message": f"Task with ID {task_id} deleted successfully"
                }
            elif title:
                # Delete by title (first matching task)
                task = session.query(Task).filter(Task.title == title, Task.user_id == user_id).first()

                if not task:
                    return {
                        "success": False,
                        "message": f"No task with title '{title}' found"
                    }

                session.delete(task)
                session.commit()

                return {
                    "success": True,
                    "message": f"Task '{title}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Either task_id or title must be provided"
                }
