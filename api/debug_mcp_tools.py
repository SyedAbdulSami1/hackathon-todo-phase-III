import os
import sys
import inspect
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Load environment
load_dotenv('backend/.env')

try:
    from tools.registry import mcp
except ImportError as e:
    print("Import error:", e)
    sys.exit(1)

print("MCP Tools:", list(mcp._tool_manager._tools.keys()))

for name, tool in mcp._tool_manager._tools.items():
    print("\nTool:", name)
    print("Description:", getattr(tool, 'description', 'No description'))
    print("Type:", type(tool))
    
    # Try to see if it has a 'fn' attribute (the original function)
    # Check common attributes for FastMCP Tool objects
    fn = getattr(tool, 'func', getattr(tool, 'fn', getattr(tool, '_fn', None)))
    if fn:
        print("Original function found:", fn)
        try:
            print("Fn signature:", inspect.signature(fn))
        except: pass
    
    # Check 'run' method
    if hasattr(tool, 'run'):
        try:
            print("Run method signature:", inspect.signature(tool.run))
        except: pass
