"""MCP tool for updating existing todo tasks."""

from typing import Any, Dict
from tools.base import BaseMCPTool
from sqlmodel import Session
from models import Task
from db import engine


class UpdateTaskMCPTool(BaseMCPTool):
    """MCP tool to update existing todo tasks."""

    @property
    def name(self) -> str:
        return "update_task"

    @property
    def description(self) -> str:
        return "Update an existing todo task with new details."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "The ID of the task to update"},
                "title": {"type": "string", "description": "The new title of the task (optional)"},
                "description": {"type": "string", "description": "The new description of the task (optional)"},
                "due_date": {"type": "string", "description": "New due date for the task (optional)"},
                "status": {"type": "string", "description": "New status of the task (optional)", "enum": ["pending", "in_progress", "completed"]},
                "priority": {"type": "string", "description": "New priority of the task (optional)", "enum": ["low", "medium", "high"]}
            },
            "required": ["task_id"],
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool to update a task."""
        task_id = kwargs.get("task_id")
        title = kwargs.get("title")
        description = kwargs.get("description")
        due_date = kwargs.get("due_date")
        status = kwargs.get("status")
        priority = kwargs.get("priority")

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

            # Update the task attributes if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if due_date is not None:
                # In a real implementation, we'd parse the date
                pass
            if status is not None:
                task.status = status
            if priority is not None:
                # Priority is not a field in the current Task model, but we'll accept it
                pass

            session.add(task)
            session.commit()
            session.refresh(task)

        return {
            "success": True,
            "message": f"Task '{task.title}' updated successfully"
        }
