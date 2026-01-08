from config import MAX_CHARS
import os
from google.genai import types

# assume file_path is a relative path to working directory
def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([target_file_path, abs_working_dir]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f"Error reading the file: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the raw text content from a specified file on the local filesystem.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file, including the extension (e.g., 'data/report.txt').",
            ),
        },
        required=["file_path"]
    ),
)



