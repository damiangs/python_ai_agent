import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_fp = os.path.abspath(os.path.join(abs_working_dir, file_path))

    # validate if filepatch is outside of the working directory
    if not target_fp.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # validate if the file path does not exists
    if not os.path.isfile(target_fp):
        return f'Error: File "{file_path}" not found.'

    # validate if it is a python file
    if not target_fp.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # run the Python file in a subprocess with timeout and capture output
        result = subprocess.run(
            [sys.executable, target_fp] + args,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        stdout_clean = result.stdout.strip()
        stderr_clean = result.stderr.strip()

        if stdout_clean:
            output_parts.append(f"STDOUT:\n\n{stdout_clean}")
        if stderr_clean:
            output_parts.append(f"STDERR:\n\n{stderr_clean}")

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
