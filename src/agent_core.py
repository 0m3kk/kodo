from baml_client.sync_client import b as baml_client
from baml_client.types import ReadFile, WriteFile, ListDirectoryContents, FindContentInFile, GetUserInput, ReviewAndConfirmChanges, CollectUserFeedback, RequestHumanIntervention, FinalAnswer, WebFetch, APIFetch
from .memory.short_term_memory import ShortTermMemory
from .tools.file_manager import FileManagerTools
from .tools.human_interaction import HumanInteractionTools
from .tools.response_provider import ResponseProviderTools
from .tools.web_fetch_tool import WebFetchTools
from .tools.api_fetch_tool import APIFetchTools


class DevAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.short_term_memory = ShortTermMemory(session_id)
        self.file_manager = FileManagerTools()
        self.human_interaction = HumanInteractionTools()
        self.response_provider = ResponseProviderTools()
        self.web_fetch_tool = WebFetchTools()
        self.api_fetch_tool = APIFetchTools()

    async def run(self, query: str):
        history = self.short_term_memory.get_history()
        tool_call = baml_client.Orchestrate(query=query, history=history)

        if isinstance(tool_call, ReadFile):
            content = self.file_manager.read_file(tool_call.file_path)
            self.short_term_memory.add_entry(f"Read file: {tool_call.file_path}")
            print(content)
        elif isinstance(tool_call, WriteFile):
            if self.file_manager.write_file(tool_call.file_path, tool_call.content):
                self.short_term_memory.add_entry(f"Wrote to file: {tool_call.file_path}")
                print("File saved.")
        elif isinstance(tool_call, ListDirectoryContents):
            contents = self.file_manager.list_directory_contents(tool_call.directory_path)
            self.short_term_memory.add_entry(f"Listed directory: {tool_call.directory_path}")
            print("".join(contents))
        elif isinstance(tool_call, FindContentInFile):
            results = self.file_manager.find_content_in_file(tool_call.file_path, tool_call.search_query)
            self.short_term_memory.add_entry(f"Searched for '{tool_call.search_query}' in file: {tool_call.file_path}")
            print("".join(results))
        elif isinstance(tool_call, GetUserInput):
            user_input = self.human_interaction.get_user_text_input(tool_call.prompt_message)
            self.short_term_memory.add_entry(f"Got user input for prompt: '{tool_call.prompt_message}'")
            print(f"User input: {user_input}")
        elif isinstance(tool_call, ReviewAndConfirmChanges):
            if self.human_interaction.review_and_confirm_changes(tool_call.file_path, tool_call.new_content):
                self.short_term_memory.add_entry(f"Confirmed and applied changes to: {tool_call.file_path}")
                print("Changes applied.")
            else:
                self.short_term_memory.add_entry(f"Rejected changes to: {tool_call.file_path}")
                print("Changes rejected.")
        elif isinstance(tool_call, CollectUserFeedback):
            self.human_interaction.collect_feedback(tool_call.task_id, tool_call.feedback_type, tool_call.message)
            self.short_term_memory.add_entry(f"Collected feedback for task {tool_call.task_id}")
        elif isinstance(tool_call, RequestHumanIntervention):
            user_input = self.human_interaction.request_human_intervention(tool_call.reason)
            self.short_term_memory.add_entry(f"Requested human intervention for reason: '{tool_call.reason}'")
            print(f"User input: {user_input}")
        elif isinstance(tool_call, FinalAnswer):
            self.response_provider.final_answer(tool_call.answer)
            self.short_term_memory.add_entry(f"Provided final answer: {tool_call.answer}")
        elif isinstance(tool_call, WebFetch):
            content = await self.web_fetch_tool.fetch_page_content(tool_call.url)
            self.short_term_memory.add_entry(f"Fetched content from URL: {tool_call.url}")
            print(content)
        elif isinstance(tool_call, APIFetch):
            content = self.api_fetch_tool.fetch_api_data(tool_call.url, tool_call.method, tool_call.headers, tool_call.data)
            self.short_term_memory.add_entry(f"Fetched API data from URL: {tool_call.url}")
            print(content)
        else:
            print(f"Unknown tool: {tool_call}")
