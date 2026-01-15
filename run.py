import uvicorn
import os
import sys

if __name__ == "__main__":
    # Get the absolute path of the current directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # Add to path and env so Windows reloader finds 'src'
    sys.path.append(root_dir)
    os.environ["PYTHONPATH"] = root_dir

    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)