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
