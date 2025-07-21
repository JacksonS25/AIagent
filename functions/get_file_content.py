import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        directory = os.path.abspath(working_directory)
        file = os.path.abspath(os.path.join(directory, file_path))

        if not file.startswith(directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(file, 'r') as f:
            content = f.read(MAX_CHARS)
        if len(content) == MAX_CHARS:
            content += f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: {e}'

# Define the function schema for use with Google GenAI
from google.genai import types
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to return content from within the working directory.",
            ),
        },
    ),
)