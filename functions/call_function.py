from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from google import genai
from google.genai import types

def call_function(function_call_part, verbose=False):

    # Manually add working_directory to kwargs
    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"

    #Check if verbose mode is enabled
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    #Map function names to actual functions
    function_map = {
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_file_content": get_file_content,
    }

    func = function_map.get(function_call_part.name)

    if func is None:
        return types.Content(
            role="tool",
            parts=[types.Part(function_response=types.FunctionResponse(response=f"Unknown function: {function_call_part.name}"))]
        )
    
    function_result = func(**kwargs)

    return types.Content(
        role="tool",
        parts=[types.Part(function_response=types.FunctionResponse(response={"output": function_result}))]
    )

    

