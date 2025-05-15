# main.py

def main():
    from src.cmd.cli import execute
    execute()

if __name__ == "__main__":
    # This handles running the script directly
    import sys
    import os
    
    # Add the project root directory to Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    main()