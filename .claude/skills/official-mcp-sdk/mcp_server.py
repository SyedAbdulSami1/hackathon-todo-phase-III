"""
Official MCP SDK Implementation for Task Management

This module implements the required MCP tools for task management:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task
"""

from modelcontextprotocol import ProtocolServer
from modelcontextprotocol.types import Tool, ToolResult
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Task(BaseModel):
    """Represents a task in the system"""
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

class TaskManager:
    """Manages tasks in memory - in production, this would use a database"""

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Task:
        """Add a new task to the system"""
        if not user_id or not title:
            raise ValueError("user_id and title are required")

        task = Task(
            id=self._next_id,
            user_id=user_id,
            title=title,
            description=description
        )

        self._tasks[self._next_id] = task
        self._next_id += 1

        logger.info(f"Added task {task.id} for user {user_id}: {title}")
        return task

    def get_tasks(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        """Retrieve tasks for a specific user with optional status filter"""
        user_tasks = [task for task in self._tasks.values() if task.user_id == user_id]

        if status == "pending":
            user_tasks = [task for task in user_tasks if not task.completed]
        elif status == "completed":
            user_tasks = [task for task in user_tasks if task.completed]

        logger.info(f"Retrieved {len(user_tasks)} tasks for user {user_id} with status={status}")
        return user_tasks

    def update_task(self, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task"""
        task = self._tasks.get(task_id)

        if not task:
            logger.warning(f"Task {task_id} not found for update")
            return None

        if task.user_id != user_id:
            logger.warning(f"Unauthorized access attempt to task {task_id} by user {user_id}")
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        logger.info(f"Updated task {task_id} for user {user_id}")
        return task

    def complete_task(self, user_id: str, task_id: int) -> Optional[Task]:
        """Mark a task as completed"""
        task = self._tasks.get(task_id)

        if not task:
            logger.warning(f"Task {task_id} not found for completion")
            return None

        if task.user_id != user_id:
            logger.warning(f"Unauthorized completion attempt to task {task_id} by user {user_id}")
            return None

        task.completed = True
        logger.info(f"Completed task {task_id} for user {user_id}")
        return task

    def delete_task(self, user_id: str, task_id: int) -> Optional[Task]:
        """Delete a task"""
        task = self._tasks.get(task_id)

        if not task:
            logger.warning(f"Task {task_id} not found for deletion")
            return None

        if task.user_id != user_id:
            logger.warning(f"Unauthorized deletion attempt to task {task_id} by user {user_id}")
            return None

        del self._tasks[task_id]
        logger.info(f"Deleted task {task_id} for user {user_id}")
        return task

# Initialize task manager
task_manager = TaskManager()

# Create the MCP server
server = ProtocolServer("Task Management MCP Server")

@server.handler(name="add_task")
async def add_task_handler(params: Dict[str, Any]) -> ToolResult:
    """
    Tool: add_task
    Purpose: Create a new task
    Parameters: user_id (string, required), title (string, required), description (string, optional)
    Returns: task_id, status, title
    """
    try:
        user_id = params.get("user_id")
        title = params.get("title")
        description = params.get("description", "")

        if not user_id or not title:
            return ToolResult(
                content=json.dumps({
                    "error": "user_id and title are required"
                }),
                is_error=True
            )

        task = task_manager.add_task(user_id, title, description)

        result = {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }

        logger.info(f"Successfully added task: {result}")
        return ToolResult(content=json.dumps(result))

    except Exception as e:
        logger.error(f"Error in add_task: {str(e)}")
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler(name="list_tasks")
async def list_tasks_handler(params: Dict[str, Any]) -> ToolResult:
    """
    Tool: list_tasks
    Purpose: Retrieve tasks from the list
    Parameters: user_id (string, required), status (string, optional: "all", "pending", "completed")
    Returns: Array of task objects
    """
    try:
        user_id = params.get("user_id")
        status = params.get("status", "all")

        if not user_id:
            return ToolResult(
                content=json.dumps({
                    "error": "user_id is required"
                }),
                is_error=True
            )

        tasks = task_manager.get_tasks(user_id, status)

        result = [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
            for task in tasks
        ]

        logger.info(f"Returning {len(result)} tasks for user {user_id}")
        return ToolResult(content=json.dumps(result))

    except Exception as e:
        logger.error(f"Error in list_tasks: {str(e)}")
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler(name="complete_task")
async def complete_task_handler(params: Dict[str, Any]) -> ToolResult:
    """
    Tool: complete_task
    Purpose: Mark a task as complete
    Parameters: user_id (string, required), task_id (integer, required)
    Returns: task_id, status, title
    """
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")

        if not user_id or task_id is None:
            return ToolResult(
                content=json.dumps({
                    "error": "user_id and task_id are required"
                }),
                is_error=True
            )

        task = task_manager.complete_task(user_id, task_id)

        if not task:
            return ToolResult(
                content=json.dumps({
                    "error": f"Task with id {task_id} not found or unauthorized"
                }),
                is_error=True
            )

        result = {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }

        logger.info(f"Successfully completed task: {result}")
        return ToolResult(content=json.dumps(result))

    except Exception as e:
        logger.error(f"Error in complete_task: {str(e)}")
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler(name="delete_task")
async def delete_task_handler(params: Dict[str, Any]) -> ToolResult:
    """
    Tool: delete_task
    Purpose: Remove a task from the list
    Parameters: user_id (string, required), task_id (integer, required)
    Returns: task_id, status, title
    """
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")

        if not user_id or task_id is None:
            return ToolResult(
                content=json.dumps({
                    "error": "user_id and task_id are required"
                }),
                is_error=True
            )

        task = task_manager.delete_task(user_id, task_id)

        if not task:
            return ToolResult(
                content=json.dumps({
                    "error": f"Task with id {task_id} not found or unauthorized"
                }),
                is_error=True
            )

        result = {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }

        logger.info(f"Successfully deleted task: {result}")
        return ToolResult(content=json.dumps(result))

    except Exception as e:
        logger.error(f"Error in delete_task: {str(e)}")
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler(name="update_task")
async def update_task_handler(params: Dict[str, Any]) -> ToolResult:
    """
    Tool: update_task
    Purpose: Modify task title or description
    Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
    Returns: task_id, status, title
    """
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")
        new_title = params.get("title")
        new_description = params.get("description")

        if not user_id or task_id is None:
            return ToolResult(
                content=json.dumps({
                    "error": "user_id and task_id are required"
                }),
                is_error=True
            )

        task = task_manager.update_task(user_id, task_id, new_title, new_description)

        if not task:
            return ToolResult(
                content=json.dumps({
                    "error": f"Task with id {task_id} not found or unauthorized"
                }),
                is_error=True
            )

        result = {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }

        logger.info(f"Successfully updated task: {result}")
        return ToolResult(content=json.dumps(result))

    except Exception as e:
        logger.error(f"Error in update_task: {str(e)}")
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

if __name__ == "__main__":
    # Run the server
    logger.info("Starting Task Management MCP Server...")
    server.run()