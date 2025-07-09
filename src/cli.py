import typer
import asyncio
import sys
from src.agent_core import DevAgent

app = typer.Typer()


@app.command()
def chat(
    max_loops: int = typer.Option(
        10,
        "--max-loops",
        "-l",
        help="The maximum number of loops to run the agent for.",
    )
):
    """
    Starts an interactive chat session with the Dev Agent.
    """
    agent = DevAgent(session_id="default_session", max_loops=max_loops)
    print("Welcome to the Dev Agent chat! Type 'exit' to end the session.")

    while True:
        try:
            query = input("> ")
            if query.lower() == "exit":
                print("Ending chat session.")
                break

            asyncio.run(agent.run(query))
        except KeyboardInterrupt:
            print("\nCaught Ctrl+C, exiting...")
            sys.exit(0)


if __name__ == "__main__":
    app()
