# File: run_app.py

#* Import Libraries
from utils import Utils
from threading import Thread

#* Initialize logger
logger = Utils.initialize_logger()

def main():
    if Utils.logger is None:
        Utils.initialize_logger()

    #* Start the application
    logger.info(f"Starting the application...")
    run_app()
    return

def run_app():
    if Utils.logger is None:
        Utils.initialize_logger()
    logger.info(f"Running the application...")
    logger.info(f"Creating Fronted & Backend Thread...")
    frontend_thread = Thread(target=Utils.run_frontend)
    backend_thread = Thread(target=Utils.run_backend)
    
    logger.info(f"Starting Frontend & Backend Thread...")
    frontend_thread.start()
    backend_thread.start()




if __name__ == "__main__":
    main()
