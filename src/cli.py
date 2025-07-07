import typer
import asyncio
from src.agent_core import DevAgent

app = typer.Typer()

@app.command()
def run(query: str):
    """
    Runs the Dev Agent with the given query.
    """
    agent = DevAgent(session_id="default_session")
    asyncio.run(agent.run(query))

if __name__ == "__main__":
    app()