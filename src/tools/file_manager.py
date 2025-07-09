import os
from pathlib import Path
import difflib
from .human_interaction import HumanInteractionTools
from rich.console import Console
from rich.syntax import Syntax


class FileManagerTools:
    """
    A class to manage file operations like reading, writing, and listing directory contents.
    """

    def __init__(self):
        """Initializes the FileManagerTools."""
        self.human_interaction = HumanInteractionTools()
        self.console = Console()

    def read_file(self, file_path: str, limit: int = -1, offset: int = 0) -> str:
        """
        Reads the content of a given file path after getting user approval.

        Args:
            file_path: The path to the file to read.

        Returns:
            The content of the file as a string, or an error message if it fails.
        """
        if not self.human_interaction.get_user_confirmation(
            f"Proceed with reading file: '{file_path}'?"
        ):
            return "INFO: File read operation was cancelled by the user."
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if offset > 0:
                content = content[offset:]
            if limit > -1:
                content = content[:limit]
            return content
        except FileNotFoundError:
            return f"ERROR: File not found at '{file_path}'."
        except IOError as e:
            return f"ERROR: Could not read file at '{file_path}': {e}"

    def write_file(self, file_path: str, content: str) -> bool:
        """
        Writes the given content to a file at the specified path after getting user approval.
        Shows a diff of the changes before asking for confirmation.
        Creates necessary parent directories if they don't exist.

        Args:
            file_path: The path to the file to write to.
            content: The content to write to the file.

        Returns:
            True if the write was successful, False otherwise.
        """
        try:
            original_content = ""
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    original_content = f.read()

            diff = list(
                difflib.unified_diff(
                    original_content.splitlines(keepends=True),
                    content.splitlines(keepends=True),
                    fromfile="original",
                    tofile="new",
                )
            )

            if not diff:
                print("No changes to apply.")
                return True

            print("The following changes are proposed:")
            syntax = Syntax("".join(diff), "diff", theme="monokai", line_numbers=True)
            self.console.print(syntax)

            if not self.human_interaction.get_user_confirmation(
                f"Apply changes to '{file_path}'?"
            ):
                return False

            # Create parent directories if they don't exist
            parent_dir = Path(file_path).parent
            os.makedirs(parent_dir, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except IOError as e:
            print(f"Error writing to file '{file_path}': {e}")
            return False

    def list_directory_contents(self, directory_path: str = ".") -> list[str]:
        """
        Lists all non-hidden files and subdirectories within a given directory.

        Excludes common ignored directories like '__pycache__', 'node_modules', '.git', 'venv', 'dist'.

        Args:
            directory_path: The path to the directory to list. Defaults to ".".

        Returns:
            A list of file and directory names, or a list with an error message if it fails.
        """
        ignored_dirs = {"__pycache__", "node_modules", ".git", ".venv", "venv", "dist"}
        try:
            if not os.path.isdir(directory_path):
                raise NotADirectoryError(
                    f"'{directory_path}' is not a valid directory."
                )

            entries = []
            for entry in os.listdir(directory_path):
                if not entry.startswith(".") and entry not in ignored_dirs:
                    entries.append(entry)
            return sorted(entries)
        except FileNotFoundError:
            return [f"ERROR: Directory not found at '{directory_path}'."]
        except NotADirectoryError:
            return [f"ERROR: Path '{directory_path}' is not a directory."]
        except Exception as e:
            return [f"ERROR: An unexpected error occurred: {e}"]

    def find_content_in_file(self, file_path: str, search_query: str) -> list[str]:
        """
        Reads the content of a file and returns lines containing the search query.

        Args:
            file_path: The path to the file to search within.
            search_query: The string to search for (case-insensitive).

        Returns:
            A list of lines containing the query, or a list with an error message.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            matching_lines = [
                line.strip() for line in lines if search_query.lower() in line.lower()
            ]
            return matching_lines
        except FileNotFoundError:
            return [f"ERROR: File not found at '{file_path}'."]
        except IOError as e:
            return [f"ERROR: Could not read file at '{file_path}': {e}"]
