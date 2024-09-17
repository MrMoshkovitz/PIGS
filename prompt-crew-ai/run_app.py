# File: run_app.py

#* Import Libraries
from utils import GlobalUtils, FrontedUtils, BackendUtils
from threading import Thread

#* Initialize logger
logger = GlobalUtils.initialize_logger()

def main():
    if GlobalUtils.logger is None:
        GlobalUtils.initialize_logger()

    #* Start the application
    logger.info(f"Starting the application...")
    run_app()
    return

def run_app():
    if GlobalUtils.logger is None:
        GlobalUtils.initialize_logger()
    logger.info(f"Running the application...")
    logger.info(f"Creating Fronted & Backend Thread...")
    frontend_thread = Thread(target=FrontedUtils.run)
    backend_thread = Thread(target=BackendUtils.run)
    
    logger.info(f"Starting Frontend & Backend Thread...")
    frontend_thread.start()
    backend_thread.start()




if __name__ == "__main__":
    main()
