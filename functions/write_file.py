import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_fp = os.path.abspath(os.path.join(working_directory, file_path))

    # validate if the filepath is outside thw working directory
    if not target_fp.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        # if the filepath does not exist, create it
        os.makedirs(os.path.dirname(target_fp), exist_ok=True)

        with open(target_fp, "w", encoding="utf-8") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f'Error writing file "{file_path}": {e}'
