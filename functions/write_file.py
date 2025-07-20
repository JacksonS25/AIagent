import os

def write_file(working_directory, file_path, content):
    """
    Writes content to a file at the specified path within the working directory.

    :param working_directory: The base directory where the file should be written.
    :param file_path: The relative path of the file to write.
    :param content: The content to write into the file.
    """

    try:
        directory = os.path.abspath(working_directory)
        file = os.path.abspath(os.path.join(directory, file_path))

        if not file.startswith(directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file):
            # Ensure the directory exists
            os.makedirs(directory, exist_ok=True)
        

        with open(file, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'
    