import os
import sys
import inspect
from dotenv import load_dotenv

sys.path.append(os.path.join(os.getcwd(), 'backend'))
load_dotenv('backend/.env')

from tools.registry import mcp

for name, tool in mcp._tool_manager._tools.items():
    is_run_async = inspect.iscoroutinefunction(tool.run)
    print("Tool:", name)
    print("Is run async?", is_run_async)
