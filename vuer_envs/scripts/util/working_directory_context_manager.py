import os
from contextlib import contextmanager


@contextmanager
def temporary_working_directory(new_directory):
    """Context manager to temporarily switch the current working directory."""
    original_directory = os.getcwd()
    try:
        os.chdir(new_directory)
        yield  # Control goes back to the code inside the `with` block
    finally:
        os.chdir(original_directory)  # Revert back to the original directory