class Utils:
    @staticmethod
    def get_error_details(e):
        import traceback
        import linecache        

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
