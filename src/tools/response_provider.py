class ResponseProviderTools:
    """
    A class for providing the final answer to the user.
    """

    def __init__(self):
        """Initializes the ResponseProviderTools."""
        pass

    def final_answer(self, answer: str) -> str:
        """
        Provides the final answer to the user.

        Args:
            answer: The final answer to be provided to the user.

        Returns:
            The final answer.
        """
        print(f"\n{answer}\n")
        return answer

