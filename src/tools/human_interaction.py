import questionary
import difflib


class HumanInteractionTools:
    """
    A class for handling human-in-the-loop interactions.
    """

    def __init__(self):
        """Initializes the HumanInteractionTools."""
        pass

    def get_user_confirmation(self, prompt_message: str) -> bool:
        """
        Asks the user for a yes/no confirmation via the CLI.

        Args:
            prompt_message: The message to display to the user.

        Returns:
            True if the user confirms, False otherwise.
        """
        return questionary.confirm(prompt_message).ask()

    def get_user_text_input(self, prompt_message: str) -> str:
        """
        Gets free-form text input from the user via the CLI.

        Args:
            prompt_message: The message to display to the user.

        Returns:
            The text input from the user.
        """
        return questionary.text(prompt_message).ask()

    def review_and_confirm_changes(self, file_path: str, new_content: str) -> bool:
        """
        Displays a diff of proposed changes and asks for user confirmation to apply them.

        Args:
            file_path: The path to the file to be modified.
            new_content: The proposed new content for the file.

        Returns:
            True if the user confirms and the changes are applied, False otherwise.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
        except FileNotFoundError:
            existing_content = ""

        diff = difflib.unified_diff(
            existing_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"Original: {file_path}",
            tofile=f"Proposed: {file_path}",
        )

        print("\nProposed changes:\n")
        for line in diff:
            print(line, end="")

        if self.get_user_confirmation("\nApply these changes?"):
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                return True
            except IOError as e:
                print(f"Error writing to file: {e}")
                return False
        return False

    def collect_feedback(self, task_id: str, feedback_type: str, message: str) -> None:
        """
        Logs feedback to the console and a file.

        Args:
            task_id: The ID of the task related to the feedback.
            feedback_type: The type of feedback (e.g., 'info', 'warning', 'error').
            message: The feedback message.
        """
        log_message = f"[{feedback_type.upper()}] Task {task_id}: {message}"
        print(log_message)
        with open("data/feedback.log", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

    def request_human_intervention(self, reason: str) -> str:
        """
        Pauses the agent and prompts the user for new instructions.

        Args:
            reason: The reason for requesting intervention.

        Returns:
            The user's input.
        """
        print(f"\nAgent paused: {reason}")
        return self.get_user_text_input(
            "Please provide new instructions or type 'continue':"
        )
