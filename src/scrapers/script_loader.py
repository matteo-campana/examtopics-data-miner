def load_js_script(script_path):
    """Load JavaScript from a file"""
    try:
        with open(script_path, "r") as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Failed to load script from {script_path}, error: {str(e)}")
