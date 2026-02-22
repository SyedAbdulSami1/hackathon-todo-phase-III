---
name: Official MCP SDK Development
description: This skill should be used when the user asks to "create an MCP server with task management tools", "build MCP tools for task CRUD operations", "implement task management via MCP", "create tools for add_task, list_tasks, complete_task, delete_task, update_task", "implement MCP protocol for task management", "deploy task management MCP server", "create AI tools for task management", or mentions MCP server, Model Context Protocol, MCP tools, task management, or task CRUD operations.
version: 1.0.0
---

# Official MCP SDK Development Guide

This skill provides comprehensive guidance for building Model Context Protocol (MCP) servers and clients using the Official MCP SDK, specifically focused on task management tools.

## Core Concepts

MCP (Model Context Protocol) enables LLMs to interact with your data and services through three main capabilities:

- **Tools**: Functions that LLMs can call to perform actions
- **Resources**: Data that LLMs can read (files, APIs, databases)
- **Prompts**: Reusable prompt templates with arguments
- **Context**: Access to logging, progress reporting, and LLM sampling

## Installation

```bash
pip install @modelcontextprotocol/python
```

## Project Structure

```
project/
├── server.py              # Main MCP server with task management
├── tools/                 # Task management tool definitions
│   ├── __init__.py
│   ├── task_operations.py # add_task, list_tasks, complete_task, etc.
│   └── database.py        # Database connection layer
├── resources/             # Resource definitions
│   ├── __init__.py
│   └── task_data.py       # Task-related resources
├── prompts/               # Prompt templates
│   ├── __init__.py
│   └── task_templates.py  # Task-related prompts
└── requirements.txt
```

## Basic Server Setup with Task Management

```python
from modelcontextprotocol import ProtocolServer
from modelcontextprotocol.types import Tool, ToolResult
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json

# Create the server
server = ProtocolServer("Task Management Server")

# Task model
class Task(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False

# In-memory storage (for demonstration - use a database in production)
tasks_db: Dict[int, Task] = {}
next_task_id = 1

# Tool: add_task
# Purpose: Create a new task
# Parameters: user_id (string, required), title (string, required), description (string, optional)
# Returns: task_id, status, title
@server.handler
async def add_task_handler(params: Dict[str, Any]) -> ToolResult:
    global next_task_id

    user_id = params.get("user_id")
    title = params.get("title")
    description = params.get("description", "")

    if not user_id or not title:
        return ToolResult(
            content=json.dumps({"error": "user_id and title are required"}),
            is_error=True
        )

    task = Task(
        id=next_task_id,
        user_id=user_id,
        title=title,
        description=description,
        completed=False
    )

    tasks_db[next_task_id] = task
    task_id = next_task_id
    next_task_id += 1

    return ToolResult(content=json.dumps({
        "task_id": task_id,
        "status": "created",
        "title": title
    }))

# Tool: list_tasks
# Purpose: Retrieve tasks from the list
# Parameters: user_id (string, required), status (string, optional: "all", "pending", "completed")
# Returns: Array of task objects
@server.handler
async def list_tasks_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    status_filter = params.get("status", "all")

    if not user_id:
        return ToolResult(
            content=json.dumps({"error": "user_id is required"}),
            is_error=True
        )

    user_tasks = [task for task in tasks_db.values() if task.user_id == user_id]

    if status_filter == "pending":
        user_tasks = [task for task in user_tasks if not task.completed]
    elif status_filter == "completed":
        user_tasks = [task for task in user_tasks if task.completed]

    result = [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
        for task in user_tasks
    ]

    return ToolResult(content=json.dumps(result))

# Tool: complete_task
# Purpose: Mark a task as complete
# Parameters: user_id (string, required), task_id (integer, required)
# Returns: task_id, status, title
@server.handler
async def complete_task_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    task_id = params.get("task_id")

    if not user_id or task_id is None:
        return ToolResult(
            content=json.dumps({"error": "user_id and task_id are required"}),
            is_error=True
        )

    task = tasks_db.get(task_id)

    if not task:
        return ToolResult(
            content=json.dumps({"error": f"Task with id {task_id} not found"}),
            is_error=True
        )

    if task.user_id != user_id:
        return ToolResult(
            content=json.dumps({"error": "Unauthorized: task does not belong to user"}),
            is_error=True
        )

    task.completed = True

    return ToolResult(content=json.dumps({
        "task_id": task_id,
        "status": "completed",
        "title": task.title
    }))

# Tool: delete_task
# Purpose: Remove a task from the list
# Parameters: user_id (string, required), task_id (integer, required)
# Returns: task_id, status, title
@server.handler
async def delete_task_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    task_id = params.get("task_id")

    if not user_id or task_id is None:
        return ToolResult(
            content=json.dumps({"error": "user_id and task_id are required"}),
            is_error=True
        )

    task = tasks_db.get(task_id)

    if not task:
        return ToolResult(
            content=json.dumps({"error": f"Task with id {task_id} not found"}),
            is_error=True
        )

    if task.user_id != user_id:
        return ToolResult(
            content=json.dumps({"error": "Unauthorized: task does not belong to user"}),
            is_error=True
        )

    del tasks_db[task_id]

    return ToolResult(content=json.dumps({
        "task_id": task_id,
        "status": "deleted",
        "title": task.title
    }))

# Tool: update_task
# Purpose: Modify task title or description
# Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
# Returns: task_id, status, title
@server.handler
async def update_task_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    task_id = params.get("task_id")
    new_title = params.get("title")
    new_description = params.get("description")

    if not user_id or task_id is None:
        return ToolResult(
            content=json.dumps({"error": "user_id and task_id are required"}),
            is_error=True
        )

    task = tasks_db.get(task_id)

    if not task:
        return ToolResult(
            content=json.dumps({"error": f"Task with id {task_id} not found"}),
            is_error=True
        )

    if task.user_id != user_id:
        return ToolResult(
            content=json.dumps({"error": "Unauthorized: task does not belong to user"}),
            is_error=True
        )

    if new_title is not None:
        task.title = new_title

    if new_description is not None:
        task.description = new_description

    return ToolResult(content=json.dumps({
        "task_id": task_id,
        "status": "updated",
        "title": task.title
    }))

# Run the server
if __name__ == "__main__":
    server.run()
```

## MCP Tools Specification

The MCP server must expose the following tools for the AI agent:

### Tool: add_task
- **Purpose**: Create a new task
- **Parameters**: user_id (string, required), title (string, required), description (string, optional)
- **Returns**: task_id, status, title
- **Example Input**: {"user_id": "ziakhan", "title": "Buy groceries", "description": "Milk, eggs, bread"}
- **Example Output**: {"task_id": 5, "status": "created", "title": "Buy groceries"}

### Tool: list_tasks
- **Purpose**: Retrieve tasks from the list
- **Parameters**: user_id (string, required), status (string, optional: "all", "pending", "completed")
- **Returns**: Array of task objects
- **Example Input**: {"user_id": "ziakhan", "status": "pending"}
- **Example Output**: [{"id": 1, "title": "Buy groceries", "completed": false}, ...]

### Tool: complete_task
- **Purpose**: Mark a task as complete
- **Parameters**: user_id (string, required), task_id (integer, required)
- **Returns**: task_id, status, title
- **Example Input**: {"user_id": "ziakhan", "task_id": 3}
- **Example Output**: {"task_id": 3, "status": "completed", "title": "Call mom"}

### Tool: delete_task
- **Purpose**: Remove a task from the list
- **Parameters**: user_id (string, required), task_id (integer, required)
- **Returns**: task_id, status, title
- **Example Input**: {"user_id": "ziakhan", "task_id": 2}
- **Example Output**: {"task_id": 2, "status": "deleted", "title": "Old task"}

### Tool: update_task
- **Purpose**: Modify task title or description
- **Parameters**: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
- **Returns**: task_id, status, title
- **Example Input**: {"user_id": "ziakhan", "task_id": 1, "title": "Buy groceries and fruits"}
- **Example Output**: {"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}

## Advanced Tool Implementation with Database

```python
from modelcontextprotocol import ProtocolServer
from modelcontextprotocol.types import Tool, ToolResult
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import sqlite3
from contextlib import contextmanager

class TaskManager:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    @contextmanager
    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> int:
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
                (user_id, title, description)
            )
            task_id = cursor.lastrowid
            conn.commit()
            return task_id

    def get_tasks(self, user_id: str, status: str = "all") -> List[Dict[str, Any]]:
        with self.get_db() as conn:
            query = "SELECT * FROM tasks WHERE user_id = ?"
            params = [user_id]

            if status == "pending":
                query += " AND completed = FALSE"
            elif status == "completed":
                query += " AND completed = TRUE"

            query += " ORDER BY created_at DESC"

            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "title": row["title"],
                    "description": row["description"],
                    "completed": bool(row["completed"]),
                    "created_at": row["created_at"]
                }
                for row in rows
            ]

    def update_task(self, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        with self.get_db() as conn:
            updates = []
            params = []

            if title is not None:
                updates.append("title = ?")
                params.append(title)

            if description is not None:
                updates.append("description = ?")
                params.append(description)

            if not updates:
                return False

            params.extend([user_id, task_id])
            query = f"UPDATE tasks SET {', '.join(updates)} WHERE user_id = ? AND id = ?"

            cursor = conn.cursor()
            cursor.execute(query, params)

            if cursor.rowcount == 0:
                return False

            conn.commit()
            return True

    def complete_task(self, user_id: str, task_id: int) -> bool:
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET completed = TRUE WHERE user_id = ? AND id = ?",
                (user_id, task_id)
            )

            if cursor.rowcount == 0:
                return False

            conn.commit()
            return True

    def delete_task(self, user_id: str, task_id: int) -> bool:
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tasks WHERE user_id = ? AND id = ?",
                (user_id, task_id)
            )

            if cursor.rowcount == 0:
                return False

            conn.commit()
            return True

# Initialize task manager
task_manager = TaskManager()

# Create the server
server = ProtocolServer("Database Task Management Server")

@server.handler
async def add_task_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    title = params.get("title")
    description = params.get("description", "")

    if not user_id or not title:
        return ToolResult(
            content=json.dumps({"error": "user_id and title are required"}),
            is_error=True
        )

    try:
        task_id = task_manager.add_task(user_id, title, description)

        return ToolResult(content=json.dumps({
            "task_id": task_id,
            "status": "created",
            "title": title
        }))
    except Exception as e:
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler
async def list_tasks_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    status_filter = params.get("status", "all")

    if not user_id:
        return ToolResult(
            content=json.dumps({"error": "user_id is required"}),
            is_error=True
        )

    try:
        tasks = task_manager.get_tasks(user_id, status_filter)

        return ToolResult(content=json.dumps(tasks))
    except Exception as e:
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler
async def complete_task_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    task_id = params.get("task_id")

    if not user_id or task_id is None:
        return ToolResult(
            content=json.dumps({"error": "user_id and task_id are required"}),
            is_error=True
        )

    try:
        success = task_manager.complete_task(user_id, task_id)

        if not success:
            return ToolResult(
                content=json.dumps({"error": f"Task with id {task_id} not found or unauthorized"}),
                is_error=True
            )

        # Get the task to return its title
        tasks = task_manager.get_tasks(user_id)
        task = next((t for t in tasks if t['id'] == task_id), None)

        if not task:
            return ToolResult(
                content=json.dumps({"error": "Task not found after update"}),
                is_error=True
            )

        return ToolResult(content=json.dumps({
            "task_id": task_id,
            "status": "completed",
            "title": task['title']
        }))
    except Exception as e:
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler
async def delete_task_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    task_id = params.get("task_id")

    if not user_id or task_id is None:
        return ToolResult(
            content=json.dumps({"error": "user_id and task_id are required"}),
            is_error=True
        )

    try:
        # Get the task to return its title
        tasks = task_manager.get_tasks(user_id)
        task = next((t for t in tasks if t['id'] == task_id), None)

        if not task:
            return ToolResult(
                content=json.dumps({"error": f"Task with id {task_id} not found or unauthorized"}),
                is_error=True
            )

        success = task_manager.delete_task(user_id, task_id)

        if not success:
            return ToolResult(
                content=json.dumps({"error": f"Failed to delete task with id {task_id}"}),
                is_error=True
            )

        return ToolResult(content=json.dumps({
            "task_id": task_id,
            "status": "deleted",
            "title": task['title']
        }))
    except Exception as e:
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

@server.handler
async def update_task_handler(params: Dict[str, Any]) -> ToolResult:
    user_id = params.get("user_id")
    task_id = params.get("task_id")
    new_title = params.get("title")
    new_description = params.get("description")

    if not user_id or task_id is None:
        return ToolResult(
            content=json.dumps({"error": "user_id and task_id are required"}),
            is_error=True
        )

    try:
        success = task_manager.update_task(user_id, task_id, new_title, new_description)

        if not success:
            return ToolResult(
                content=json.dumps({"error": f"Task with id {task_id} not found or unauthorized"}),
                is_error=True
            )

        # Get the updated task to return its title
        tasks = task_manager.get_tasks(user_id)
        task = next((t for t in tasks if t['id'] == task_id), None)

        if not task:
            return ToolResult(
                content=json.dumps({"error": "Task not found after update"}),
                is_error=True
            )

        return ToolResult(content=json.dumps({
            "task_id": task_id,
            "status": "updated",
            "title": task['title']
        }))
    except Exception as e:
        return ToolResult(
            content=json.dumps({"error": str(e)}),
            is_error=True
        )

if __name__ == "__main__":
    server.run()
```

## Running the Server

### STDIO Transport (Default)
```python
if __name__ == "__main__":
    server.run()  # Default: STDIO
```

### HTTP Transport
```python
if __name__ == "__main__":
    server.run(transport="http", host="0.0.0.0", port=8000)
```

## Client Usage Example

```python
import asyncio
from modelcontextprotocol import ProtocolClient
from modelcontextprotocol.types import ToolCall
import json

async def main():
    # Connect to the MCP server
    async with ProtocolClient("stdio://./server.py") as client:
        # Add a task
        result = await client.call_tool("add_task", {
            "user_id": "ziakhan",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        })
        print("Add task result:", json.loads(result.content))

        # List pending tasks
        result = await client.call_tool("list_tasks", {
            "user_id": "ziakhan",
            "status": "pending"
        })
        print("List tasks result:", json.loads(result.content))

        # Complete a task
        result = await client.call_tool("complete_task", {
            "user_id": "ziakhan",
            "task_id": 1
        })
        print("Complete task result:", json.loads(result.content))

        # Update a task
        result = await client.call_tool("update_task", {
            "user_id": "ziakhan",
            "task_id": 1,
            "title": "Updated task title"
        })
        print("Update task result:", json.loads(result.content))

asyncio.run(main())
```

## Best Practices

1. **Input Validation**: Always validate input parameters before processing
2. **Authentication**: Implement user authentication and authorization
3. **Error Handling**: Properly handle exceptions and return appropriate error messages
4. **Type Safety**: Use Pydantic models for complex data structures
5. **Database Transactions**: Use transactions for operations that modify multiple records
6. **Logging**: Log important operations and errors for debugging
7. **Rate Limiting**: Implement rate limiting to prevent abuse
8. **Testing**: Write comprehensive tests for all tools
9. **Security**: Sanitize inputs and prevent SQL injection
10. **Documentation**: Document all tools with clear examples

## Production Considerations

- Use a proper database (PostgreSQL, MySQL) instead of SQLite
- Implement proper authentication and authorization
- Add monitoring and logging
- Set up health checks
- Implement proper error recovery
- Add caching where appropriate
- Secure endpoints with authentication
- Monitor performance and optimize queries
- Implement backup and recovery procedures