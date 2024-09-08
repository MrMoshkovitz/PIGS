# These lines import the necessary tools (called modules) that we'll use in our script
import subprocess  # This helps us run other programs or commands
import os  # This helps us work with files and folders
import sys  # This gives us information about the Python system we're using
from threading import Thread  # This lets us do multiple things at the same time in our script

# This function starts the frontend (the part of the app the user sees and interacts with)
def run_frontend():
    # First, we need to go to the right folder where our frontend code is
    frontend_dir = os.path.dirname(os.path.abspath(__file__))  # This finds the folder where this script is
    os.chdir(frontend_dir)  # This moves us into that folder
    
    # Now we start the frontend. The command is slightly different depending on if you're using Windows or not
    if sys.platform == "win32":  # This checks if we're on Windows
        subprocess.run(["npm.cmd", "start"], check=True)  # If we are, we use this command
    else:
        subprocess.run(["npm", "start"], check=True)  # If we're not (like on Mac or Linux), we use this command

# This function starts the backend (the part of the app that does the behind-the-scenes work)
def run_backend():
    # We need to go to the folder where our backend code is
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    # We check if the backend folder exists. If it doesn't, we stop and show an error.
    if not os.path.exists(backend_dir):
        print(f"Error: Backend directory not found at {backend_dir}")
        return
    
    os.chdir(backend_dir)  # If the folder exists, we move into it
    
    # Now we try to start the backend
    try:
        subprocess.run([sys.executable, "main.py"], check=True)  # This runs our main.py file with Python
    except subprocess.CalledProcessError as e:
        # If something goes wrong, we print out error information to help debug
        print(f"Backend error: {e}")
        if e.output:
            print(f"Backend output: {e.output}")

# This is where our script actually starts doing things
if __name__ == "__main__":
    # We create two separate threads. Think of threads like separate workers doing different jobs at the same time
    frontend_thread = Thread(target=run_frontend)  # This worker will run the frontend
    backend_thread = Thread(target=run_backend)    # This worker will run the backend

    # We tell both workers to start their jobs
    frontend_thread.start()
    backend_thread.start()

    try:
        # We wait for both workers to finish their jobs
        frontend_thread.join()
        backend_thread.join()
    except KeyboardInterrupt:
        # If the user presses Ctrl+C, we'll stop the program nicely
        print("Stopping the application...")
    except Exception as e:
        # If any other error happens, we'll print it out
        print(f"An error occurred: {e}")