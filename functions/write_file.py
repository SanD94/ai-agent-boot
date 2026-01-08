import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if abs_working_dir != os.path.commonpath([abs_working_dir, target_file_path]):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        
        target_dir_path = os.path.dirname(target_file_path)
        os.makedirs(target_dir_path, exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing the file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates a new file or overwrites an existing file with the specified content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file should be saved, including the filename and extension (e.g., 'scripts/data_processor.py').",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to be written into the file. For code files, this should include all necessary imports and logic.",
            )
        },
        required=["file_path", "content"]
    ),
)
