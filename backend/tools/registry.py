"""Official MCP Server implementation for Todo Task Tools."""

import os
import json
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select
from models import Task, TaskStatus
from db import engine

# Initialize FastMCP server (Official MCP SDK)
mcp = FastMCP("Todo MCP Server")

@mcp.tool()
def add_task(title: str, description: Optional[str] = None, user_id: str = "1") -> Dict[str, Any]:
    """Create a new task (Requirement #8.1)"""
    with Session(engine) as session:
        task = Task(
            title=title,
            description=description,
            status=TaskStatus.pending,
            user_id=int(user_id)
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "created", "title": task.title}

@mcp.tool()
def list_tasks(status: str = "all", user_id: str = "1") -> List[Dict[str, Any]]:
    """Retrieve tasks from the list (Requirement #8.2)"""
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == int(user_id))
        if status != "all":
            query = query.where(Task.status == status)
        
        tasks = session.exec(query).all()
        return [{"id": t.id, "title": t.title, "completed": t.status == "completed"} for t in tasks]

@mcp.tool()
def complete_task(task_id: int, user_id: str = "1") -> Dict[str, Any]:
    """Mark a task as complete (Requirement #8.3)"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or str(task.user_id) != str(user_id):
            return {"error": "Task not found"}
        
        task.status = TaskStatus.completed
        session.add(task)
        session.commit()
        return {"task_id": task.id, "status": "completed", "title": task.title}

@mcp.tool()
def delete_task(task_id: int, user_id: str = "1") -> Dict[str, Any]:
    """Remove a task from the list (Requirement #8.4)"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or str(task.user_id) != str(user_id):
            return {"error": "Task not found"}
        
        title = task.title
        session.delete(task)
        session.commit()
        return {"task_id": task_id, "status": "deleted", "title": title}

@mcp.tool()
def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None, user_id: str = "1") -> Dict[str, Any]:
    """Modify task title or description (Requirement #8.5)"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or str(task.user_id) != str(user_id):
            return {"error": "Task not found"}
        
        if title: task.title = title
        if description: task.description = description
        
        session.add(task)
        session.commit()
        return {"task_id": task.id, "status": "updated", "title": task.title}

class ToolRegistry:
    """Registry adapter for ChatAgent to use FastMCP tools."""
    
    def execute_tool(self, name: str, **kwargs) -> Any:
        # FastMCP tools can be accessed via the internal tool manager
        if name in mcp._tool_manager._tools:
            # Call the tool function directly
            return mcp._tool_manager._tools[name].run(**kwargs)
        return {"error": f"Tool {name} not found"}

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Convert FastMCP tools to OpenAI function format."""
        # Use internal _tools dict which is synchronous
        defs = []
        for name, tool in mcp._tool_manager._tools.items():
            # FastMCP tool parameters are already JSON schemas
            # But we need to match OpenAI's expected structure
            defs.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            })
        return defs

tool_registry = ToolRegistry()
