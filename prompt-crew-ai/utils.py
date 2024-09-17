
import logging

import os
import traceback
import linecache
import sys
import subprocess

class GlobalUtils:
    logger = None
    @staticmethod
    def initialize_logger(name='BackendLogger', level=logging.DEBUG, log_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')):
            
        """Initialize a logger with advanced debugging capabilities."""
        GlobalUtils.logger = logging.getLogger(name)
        GlobalUtils.logger.setLevel(level)

        # Create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        GlobalUtils.logger.addHandler(ch)

        return GlobalUtils.logger


    @staticmethod
    def get_error_details(e):
        """
        Extract detailed error information from an exception.
        
        Args:
        e (Exception): The caught exception

        Returns:
        str: A string containing function name, line number, and the exact line of code
        """
        tb = e.__traceback__
        frame = tb.tb_frame
        filename = frame.f_code.co_filename
        function_name = frame.f_code.co_name
        line_number = tb.tb_lineno
        line = linecache.getline(filename, line_number).strip()
        return f"Error in function '{function_name}' at line {line_number}: '{line}'"
    
    @staticmethod
    def change_directory(target_dir):
        """Change the working directory to the target directory."""
        if GlobalUtils.logger is None:
            GlobalUtils.initialize_logger()
        
        logging.debug(f"Changing directory to {target_dir}")
        try:
            os.chdir(target_dir)
            GlobalUtils.logger.info(f"Changed directory to {target_dir}")
        except FileNotFoundError as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Directory {target_dir} not found. {error_details}")
            sys.exit(1)
        except Exception as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Failed to change directory. {error_details}")
            sys.exit(1)
                    

    @staticmethod
    def run_command(command):
        """Run a system command."""
        if GlobalUtils.logger is None:
            GlobalUtils.initialize_logger()
        
        try:
            subprocess.run(command, check=True)
            GlobalUtils.logger.info(f"Successfully ran command: {' '.join(command)}")
        except subprocess.CalledProcessError as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Command '{' '.join(command)}' failed. {error_details}")
            sys.exit(1)
        except Exception as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Failed to run command '{' '.join(command)}'. {error_details}")
            sys.exit(1)




class FrontedUtils:
    @staticmethod
    def install_dependencies(frontend_dir):
        """Install frontend dependencies if they are missing."""
        if GlobalUtils.logger is None:
            GlobalUtils.initialize_logger()
        
        logging.info("Installing frontend dependencies...")
        GlobalUtils.change_directory(frontend_dir)
        if os.path.exists('package.json'):
            GlobalUtils.logger.info("Frontend dependencies found. Installing...")
            GlobalUtils.run_command(["npm", "install"])
        else:
            GlobalUtils.logger.warning("No package.json found in the frontend directory.")
    
    @staticmethod
    def run():
        """Start the frontend application."""
        if GlobalUtils.logger is None:
            GlobalUtils.initialize_logger()
        
        logging.info("Starting frontend application...")
        try:
            frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
            GlobalUtils.logger.info(f"Starting frontend application in File: {frontend_dir}")
            
            if not os.path.exists(frontend_dir):
                raise FileNotFoundError(f"Frontend directory not found at {frontend_dir}")
            
            FrontedUtils.install_frontend_dependencies(frontend_dir)
            
            # Assuming you run your frontend with npm start or similar
            command = ["npm", "start"]
            GlobalUtils.logger.info(f"Running frontend command: {' '.join(command)}")
            GlobalUtils.run_command(command)
        except FileNotFoundError as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Frontend directory not found. {error_details}")
            sys.exit(1)
        except Exception as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Failed to run frontend application. {error_details}")
            sys.exit(1)


class BackendUtils:
    @staticmethod
    def install_dependencies(backend_dir):
        """Install Python dependencies for the backend if they are missing."""
        if GlobalUtils.logger is None:
            GlobalUtils.initialize_logger()
        logging.info("Installing backend dependencies...")
        GlobalUtils.change_directory(backend_dir)
        if os.path.exists('requirements.txt'):
            GlobalUtils.logger.info("Backend dependencies found. Installing...")
            GlobalUtils.run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        else:
            GlobalUtils.logger.warning("No requirements.txt found in the backend directory.")


    @staticmethod
    def run():
        """Start the backend application."""
        if GlobalUtils.logger is None:
            GlobalUtils.initialize_logger()
        
        logging.info("Starting backend application...")
        try:
            backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
            GlobalUtils.logger.info(f"Starting backend application in File: {backend_dir}")
            
            if not os.path.exists(backend_dir):
                raise FileNotFoundError(f"Backend directory not found at {backend_dir}")
            
            GlobalUtils.install_backend_dependencies(backend_dir)
            
            # Assuming you run your backend with python manage.py runserver or similar
            command = [sys.executable, "manage.py", "runserver"]
            GlobalUtils.logger.info(f"Running backend command: {' '.join(command)}")
            GlobalUtils.run_command(command)
        except FileNotFoundError as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Backend directory not found. {error_details}")
            sys.exit(1)
        except Exception as e:
            error_details = GlobalUtils.get_error_details(e)
            GlobalUtils.logger.error(f"Failed to run backend application. {error_details}")
            sys.exit(1)
