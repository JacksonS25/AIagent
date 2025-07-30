import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.call_function import call_function

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(1)
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    args = sys.argv[1:]

    user_prompt = " ".join(args)

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file,
            schema_get_file_content
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            )
    )

    if sys.argv[-1] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call, verbose=sys.argv[-1] == "--verbose")
            # Ensure result is types.Content and has function_response.response
            if (
                isinstance(result, types.Content)
                and hasattr(result.parts[0], "function_response")
                and hasattr(result.parts[0].function_response, "response")
                and result.parts[0].function_response.response
            ):
                if sys.argv[-1] == "--verbose":
                    print(f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception("FatalException: Function call failed or returned no response.")
        
    
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()