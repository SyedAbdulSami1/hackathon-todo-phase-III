"""MCP tool for marking tasks as complete/incomplete."""

from typing import Any, Dict
from tools.base import BaseMCPTool
from sqlmodel import Session
from models import Task
from db import engine


class TodoCompleteMCPTool(BaseMCPTool):
    """MCP tool to mark tasks as complete or incomplete."""

    @property
    def name(self) -> str:
        return "todo_complete_tool"

    @property
    def description(self) -> str:
        return "Mark a task as complete or incomplete."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "The ID of the task to update"},
                "complete": {"type": "boolean", "description": "True to mark as complete, False to mark as incomplete"}
            },
            "required": ["task_id", "complete"],
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool to mark a task as complete/incomplete."""
        task_id = kwargs.get("task_id")
        complete = kwargs.get("complete")

        # In a real implementation, we'd need to get the user_id from context
        # For now, we'll use a placeholder user_id
        user_id = kwargs.get("user_id", 1)  # Placeholder user_id

        # Update the task in the database
        with Session(engine) as session:
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
                    "message": "Unauthorized: You can only update your own tasks"
                }

            # Update the task status based on the complete flag
            if complete:
                task.status = "completed"
            else:
                # If it was completed, change back to pending; otherwise keep current status
                if task.status == "completed":
                    task.status = "pending"

            session.add(task)
            session.commit()
            session.refresh(task)

        status_text = "completed" if complete else "incomplete"
        return {
            "success": True,
            "message": f"Task '{task.title}' marked as {status_text}"
        }
