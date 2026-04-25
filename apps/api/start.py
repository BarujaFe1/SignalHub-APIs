"""Start the FastAPI server with correct paths."""
import sys
import os

# Ensure correct Python paths
sys.path.insert(0, os.path.dirname(__file__))  # apps/api
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # project root

# Change to apps/api directory so .env relative paths work
os.chdir(os.path.dirname(__file__))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[os.path.dirname(__file__)],
    )
