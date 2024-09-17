# # run_app.py
# import subprocess  # For running external commands
# import os  # For file and directory operations
# import sys  # For accessing system-specific parameters
# from threading import Thread  # For concurrent execution
# from utils import change_directory, run_command

# def change_directory(target_dir):
#     """Change the working directory to the target directory."""
#     try:
#         os.chdir(target_dir)
#     except FileNotFoundError:
#         print(f"Error: Directory {target_dir} not found.")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Error: Failed to change directory - {e}")
#         sys.exit(1)

# def run_command(command):
#     """Run a system command."""
#     try:
#         subprocess.run(command, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error: Command '{command}' failed with error {e}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Error: Failed to run command '{command}' - {e}")
#         sys.exit(1)

# def install_frontend_dependencies(frontend_dir):
#     """Install npm dependencies for the frontend if they are missing."""
#     change_directory(frontend_dir)
#     if not os.path.exists('node_modules'):
#         print("Frontend dependencies not found. Installing...")
#         run_command(['npm', 'install'])

# def install_backend_dependencies(backend_dir):
#     """Install Python dependencies for the backend if they are missing."""
#     change_directory(backend_dir)
#     if os.path.exists('requirements.txt'):
#         print("Backend dependencies found. Installing...")
#         run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# def run_frontend():
#     """Start the frontend application."""
#     frontend_dir = os.path.dirname(os.path.abspath(__file__))
    
#     install_frontend_dependencies(frontend_dir)
#     # Check platform and run appropriate command
#     command = ["npm.cmd", "start"] if sys.platform == "win32" else ["npm", "start"]
#     run_command(command)

# def run_backend():
#     """Start the backend application."""
#     backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
#     if not os.path.exists(backend_dir):
#         print(f"Error: Backend directory not found at {backend_dir}")
#         sys.exit(1)

    
#     install_backend_dependencies(backend_dir)
#     run_command([sys.executable, "main.py"])




# File: run_app.py

#* Import Libraries
from utils import Utils
from threading import Thread


def main():
    #* Initialize logger
    logger = Utils.initialize_logger()

    #* Start the application
    logger.info(f"Starting the application...")

    #* Create threads for frontend and backend
    frontend_thread = Thread(target=Utils.run_frontend)
    backend_thread = Thread(target=Utils.run_backend)

    #* Start the threads
    frontend_thread.start()
    backend_thread.start()

    return

if __name__ == "__main__":
    main()
