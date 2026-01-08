import os

def format_file(folder_path):
    def get_format(filename):
        full_file_path = os.path.join(folder_path, filename)
        file_size = os.path.getsize(full_file_path)
        is_dir = os.path.isdir(full_file_path)
        return f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
    return get_format


def get_files_info(working_directory, directory="."):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        if os.path.commonpath([abs_working_directory, target_dir]) != abs_working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        file_str_list = map(format_file(target_dir), os.listdir(target_dir))
        return "\n".join(file_str_list)
    except Exception as e:
        return f"Error listing files: {e}"
