
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from app.server import app

print("\n=== REGISTERED ROUTES ===")
for route in app.routes:
    if hasattr(route, "path"):
        methods = ", ".join(route.methods) if hasattr(route, "methods") else "None"
        print(f"{methods} {route.path}")
    else:
        print(f"Mounted: {route.path!r}")
print("=========================\n")
