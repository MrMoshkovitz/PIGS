# run_app.py
import subprocess  # For running external commands
import os  # For file and directory operations
import sys  # For accessing system-specific parameters
from threading import Thread  # For concurrent execution


def change_directory(target_dir):
    """Change the working directory to the target directory."""
    try:
        os.chdir(target_dir)
    except FileNotFoundError:
        print(f"Error: Directory {target_dir} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to change directory - {e}")
        sys.exit(1)

def run_command(command):
    """Run a system command."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{command}' failed with error {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to run command '{command}' - {e}")
        sys.exit(1)

def run_frontend():
    """Start the frontend application."""
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    change_directory(frontend_dir)

    # Check platform and run appropriate command
    command = ["npm.cmd", "start"] if sys.platform == "win32" else ["npm", "start"]
    run_command(command)

def run_backend():
    """Start the backend application."""
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    if not os.path.exists(backend_dir):
        print(f"Error: Backend directory not found at {backend_dir}")
        sys.exit(1)

    change_directory(backend_dir)
    run_command([sys.executable, "main.py"])

if __name__ == "__main__":
    frontend_thread = Thread(target=run_frontend)
    backend_thread = Thread(target=run_backend)

    frontend_thread.start()
    backend_thread.start()

    frontend_thread.join()
    backend_thread.join()
