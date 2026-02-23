import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

# Try importing main
print("Trying to import main...")
try:
    import main
    print("  [OK] main imported successfully")
except Exception as e:
    print(f"  [FAIL] main import failed: {e}")

# Try importing routers
print("Trying to import routers...")
try:
    import routers
    print("  [OK] routers imported successfully")
except Exception as e:
    print(f"  [FAIL] routers import failed: {e}")

# Try importing db
print("Trying to import db...")
try:
    import db
    print("  [OK] db imported successfully")
except Exception as e:
    print(f"  [FAIL] db import failed: {e}")

# Try importing models
print("Trying to import models...")
try:
    import models
    print("  [OK] models imported successfully")
except Exception as e:
    print(f"  [FAIL] models import failed: {e}")

# Try importing models.conversation
print("Trying to import models.conversation...")
try:
    from models import Conversation
    print("  [OK] models.Conversation imported successfully")
except Exception as e:
    print(f"  [FAIL] models.Conversation import failed: {e}")

# Try importing models.message
print("Trying to import models.message...")
try:
    from models import Message
    print("  [OK] models.Message imported successfully")
except Exception as e:
    print(f"  [FAIL] models.Message import failed: {e}")

# Try importing models.SenderType
print("Trying to import models.SenderType...")
try:
    from models import SenderType
    print("  [OK] models.SenderType imported successfully")
except Exception as e:
    print(f"  [FAIL] models.SenderType import failed: {e}")

# Try importing models.MessageType
print("Trying to import models.MessageType...")
try:
    from models import MessageType
    print("  [OK] models.MessageType imported successfully")
except Exception as e:
    print(f"  [FAIL] models.MessageType import failed: {e}")

print("Import testing complete")
