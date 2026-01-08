import subprocess
import os

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if abs_working_dir != os.path.commonpath([abs_working_dir, target_file_path]):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' 

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        filename = os.path.basename(target_file_path)
        _, ext = os.path.splitext(filename)
        if ext != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)


        task_res = subprocess.run(command, capture_output=True, text=True, timeout=30)

        if task_res.returncode != 0:
            return f"Process exited with code {task_res.returncode}"

        if not (task_res.stdout or task_res.stderr):
            return "No output produced"

        res = ""
        if task_res.stdout:
            res += "STDOUT:\n" + task_res.stdout

        if task_res.stderr:
            res += "STDERR:\n" + task_res.stderr

        return res
    except Exception as e:
        return f"Error: executing Python file: {e}"
