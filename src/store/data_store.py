import json
import os

class DataStore:
    """
    Class responsible for reading and writing data to non-volatile storage
    """
    
    @staticmethod
    def read_file(file_path, encoding='utf-8'):
        """
        Read content from a file
        
        Args:
            file_path (str): Path to the file
            encoding (str): File encoding, defaults to utf-8
            
        Returns:
            str: Content of the file
            
        Raises:
            Exception: If there's an issue reading the file
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    @staticmethod
    def save_file(file_path, content, encoding='utf-8'):
        """
        Save content to a file
        
        Args:
            file_path (str): Path to the file
            content (str): Content to write
            encoding (str): File encoding, defaults to utf-8
            
        Raises:
            Exception: If there's an issue writing to the file
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding=encoding) as file:
                file.write(content)
        except Exception as e:
            raise Exception(f"Error writing to file {file_path}: {str(e)}")
    
    @staticmethod
    def read_json(file_path, encoding='utf-8'):
        """
        Read and parse JSON from a file
        
        Args:
            file_path (str): Path to the JSON file
            encoding (str): File encoding, defaults to utf-8
            
        Returns:
            dict: Parsed JSON content
        """
        content = DataStore.read_file(file_path, encoding)
        return json.loads(content)
    
    @staticmethod
    def save_json(file_path, data, encoding='utf-8', indent=4):
        """
        Save data as JSON to a file
        
        Args:
            file_path (str): Path to the file
            data: Data to be serialized to JSON
            encoding (str): File encoding, defaults to utf-8
            indent (int): JSON indentation level, defaults to 4
        """
        json_content = json.dumps(data, indent=indent)
        DataStore.save_file(file_path, json_content, encoding)
