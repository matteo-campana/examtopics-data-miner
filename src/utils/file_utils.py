import os
from store.data_store import DataStore


class FileUtils:
    def get_assets_folder_path(self):
        """Get the path to the assets folder"""
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets"
        )

    def get_output_folder_path(self):
        """Get the path to the output folder"""
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output"
        )

    def get_relative_path(self, absolute_path):
        """
        Convert absolute path to a relative path from the output folder

        Args:
            absolute_path (str): Absolute path to the file

        Returns:
            str: Relative path from the output folder
        """
        # Getting the common base path (project root)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        # Convert to relative path from project root
        if absolute_path.startswith(project_root):
            rel_path = os.path.relpath(absolute_path, project_root)
            # Convert from output folder perspective (one level up then to assets)
            return f"../{rel_path}".replace("\\", "/")

        return absolute_path

    def save_output(self, content, filename=None, input_filename=None):
        """
        Save markdown content to output folder

        Args:
            content (str): Content to save
            filename (str): Optional filename, defaults to input_filename + "_output.md"
            input_filename (str): Optional input filename to base output filename on
        """
        output_folder = self.get_output_folder_path()

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Default filename if none provided
        if not filename:
            if input_filename:
                # Extract base filename without extension
                base_input = os.path.splitext(os.path.basename(input_filename))[0]
                filename = f"{base_input}_output.md"
            else:
                filename = "exam_output.md"

        # Make sure filename has .md extension
        if not filename.endswith(".md"):
            filename += ".md"

        # Full path to output file
        output_path = os.path.join(output_folder, filename)

        # Check if file already exists and create unique filename
        counter = 1
        base_name, extension = os.path.splitext(filename)
        while os.path.exists(output_path):
            new_filename = f"{base_name}_{counter}{extension}"
            output_path = os.path.join(output_folder, new_filename)
            counter += 1

        try:
            # Use DataStore instead of direct file writing
            DataStore.save_file(output_path, content, encoding="utf-8")
            print(f"Output successfully saved to {output_path}")
        except Exception as e:
            print(f"Error saving output: {e}")
