import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        attempted_directory = os.path.abspath(working_directory)
    else:
        attempted_directory = os.path.abspath(os.path.join(working_directory, directory))

    # Ensure attempted_directory is inside working_directory
    if not attempted_directory.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.exists(attempted_directory):
        return f'Error: "{directory}" does not exist'

    if not os.path.isdir(attempted_directory):
        return f'Error: "{directory}" is not a directory'

    try:
        files = os.listdir(attempted_directory)
        return "\n".join([
            f" - {x}: file_size={os.path.getsize(os.path.join(attempted_directory, x))} bytes, is_dir={os.path.isdir(os.path.join(attempted_directory, x))}"
            for x in files
        ])
    except Exception as e:
        return f'Error: {e}'

# Define the function schema for use with Google GenAI
from google.genai import types
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)