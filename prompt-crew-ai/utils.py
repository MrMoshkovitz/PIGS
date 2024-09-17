
import logging

import os
import traceback
import linecache
import sys
import subprocess
class Utils:
    logger = None
    @staticmethod
    def initialize_logger(name='BackendLogger', level=logging.DEBUG, log_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')):
            
        """Initialize a logger with advanced debugging capabilities."""
        Utils.logger = logging.getLogger(name)
        Utils.logger.setLevel(level)

        # Create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        Utils.logger.addHandler(ch)

        return Utils.logger


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
        if Utils.logger is None:
            Utils.initialize_logger()
        
        logging.debug(f"Changing directory to {target_dir}")
        try:
            os.chdir(target_dir)
            Utils.logger.info(f"Changed directory to {target_dir}")
        except FileNotFoundError as e:
            error_details = Utils.get_error_details(e)
            Utils.logger.error(f"Directory {target_dir} not found. {error_details}")
            sys.exit(1)
        except Exception as e:
            error_details = Utils.get_error_details(e)
            Utils.logger.error(f"Failed to change directory. {error_details}")
            sys.exit(1)
                    

    @staticmethod
    def run_command(command):
        """Run a system command."""
        if Utils.logger is None:
            Utils.initialize_logger()
        
        try:
            subprocess.run(command, check=True)
            Utils.logger.info(f"Successfully ran command: {' '.join(command)}")
        except subprocess.CalledProcessError as e:
            error_details = Utils.get_error_details(e)
            Utils.logger.error(f"Command '{' '.join(command)}' failed. {error_details}")
            sys.exit(1)
        except Exception as e:
            error_details = Utils.get_error_details(e)
            Utils.logger.error(f"Failed to run command '{' '.join(command)}'. {error_details}")
            sys.exit(1)

    @staticmethod
    def install_frontend_dependencies(frontend_dir):
        """Install npm dependencies for the frontend if they are missing."""
        if Utils.logger is None:
            Utils.initialize_logger()
        logging.info("Installing frontend dependencies...")
        Utils.change_directory(frontend_dir)
        if not os.path.exists('node_modules'):
            Utils.logger.info("Frontend dependencies not found. Installing...")
            Utils.run_command(['npm', 'install'])
        else:
            Utils.logger.info("Frontend dependencies already installed.")

    @staticmethod
    def install_backend_dependencies(backend_dir):
        """Install Python dependencies for the backend if they are missing."""
        if Utils.logger is None:
            Utils.initialize_logger()
        logging.info("Installing backend dependencies...")
        Utils.change_directory(backend_dir)
        if os.path.exists('requirements.txt'):
            Utils.logger.info("Backend dependencies found. Installing...")
            Utils.run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        else:
            Utils.logger.warning("No requirements.txt found in the backend directory.")

    @staticmethod
    def run_frontend():
        """Start the frontend application."""
        if Utils.logger is None:
            Utils.initialize_logger()
        
        logging.info("Starting frontend application...")
        try:
            frontend_dir = os.path.dirname(os.path.abspath(__file__))
            Utils.logger.info(f"Starting frontend application in {frontend_dir}")
            
            Utils.install_frontend_dependencies(frontend_dir)
            
            # Check platform and run appropriate command
            command = ["npm.cmd", "start"] if sys.platform == "win32" else ["npm", "start"]
            Utils.logger.info(f"Running frontend command: {' '.join(command)}")
            Utils.run_command(command)
        except Exception as e:
            error_details = Utils.get_error_details(e)
            Utils.logger.error(f"Failed to run frontend application. {error_details}")
            sys.exit(1)

    @staticmethod
    def run_backend():
        """Start the backend application."""
        if Utils.logger is None:
            Utils.initialize_logger()
        
        logging.info("Starting backend application...")
        try:
            backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
            Utils.logger.info(f"Starting backend application in {backend_dir}")
            
            if not os.path.exists(backend_dir):
                raise FileNotFoundError(f"Backend directory not found at {backend_dir}")
            
            Utils.install_backend_dependencies(backend_dir)
            
            # Assuming you run your backend with python manage.py runserver or similar
            command = [sys.executable, "manage.py", "runserver"]
            Utils.logger.info(f"Running backend command: {' '.join(command)}")
            Utils.run_command(command)
        except FileNotFoundError as e:
            error_details = Utils.get_error_details(e)
            Utils.logger.error(f"Backend directory not found. {error_details}")
            sys.exit(1)
        except Exception as e:
            error_details = Utils.get_error_details(e)
            Utils.logger.error(f"Failed to run backend application. {error_details}")
            sys.exit(1)

