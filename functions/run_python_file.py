import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    """
    Executes a Python file at the specified path within the working directory.

    :param working_directory: The base directory where the file should be executed.
    :param file_path: The relative path of the Python file to execute.
    :param args: List of arguments to pass to the Python script.
    :return: Output from the script execution or an error message.
    """
    
    try:
        directory = os.path.abspath(working_directory)
        file = os.path.abspath(os.path.join(directory, file_path))

        if not file.startswith(directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file):
            return f'Error: File "{file_path}" not found.'

        if not file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(['python', file] + args, check=True, capture_output=True, timeout=30, cwd=directory, text=True)

        if result.returncode != 0:
            return f"Process exited with code {str(result.returncode)}"
        elif not result.stdout:
            return "No output produced."
        
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    
    except Exception as e:
        return f'Error: executing Python file: {e}'

# Define the function schema for use with Google GenAI
from google.genai import types
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file within the working directory with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run within the working directory. Must be a Python file.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python script.",
            ),
        },
    ),
)