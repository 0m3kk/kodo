from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

class ResponseProviderTools:
    """
    A class for providing the final answer to the user.
    """

    def __init__(self):
        """Initializes the ResponseProviderTools."""
        self.console = Console()

    def final_answer(self, answer: str) -> str:
        """
        Provides the final answer to the user.

        Args:
            answer: The final answer to be provided to the user.

        Returns:
            The final answer.
        """
        self.console.print(Panel(Markdown(answer), title="[bold green]Final Answer[/bold green]", border_style="green", expand=False))
        return answer

