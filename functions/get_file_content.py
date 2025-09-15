import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_fp = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_fp.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_fp):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_fp, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if os.path.getsize(target_fp) > MAX_CHARS:
            return (
                file_content_string
                + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        else:
            return file_content_string

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
