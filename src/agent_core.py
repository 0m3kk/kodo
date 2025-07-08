from baml_client.sync_client import b as baml_client
from baml_client.types import ReadFile, WriteFile, ListDirectoryContents, FindContentInFile, GetUserInput, ReviewAndConfirmChanges, CollectUserFeedback, RequestHumanIntervention, FinalAnswer, WebFetch, APIFetch
from .memory.short_term_memory import ShortTermMemory
from .tools.file_manager import FileManagerTools
from .tools.human_interaction import HumanInteractionTools
from .tools.response_provider import ResponseProviderTools
from .tools.web_fetch_tool import WebFetchTools
from .tools.api_fetch_tool import APIFetchTools
from html2text import html2text
from rich.console import Console
from rich.markdown import Markdown


class DevAgent:
    def __init__(self, session_id: str, max_loops: int = 10):
        self.session_id = session_id
        self.short_term_memory = ShortTermMemory(session_id)
        self.file_manager = FileManagerTools()
        self.human_interaction = HumanInteractionTools()
        self.response_provider = ResponseProviderTools()
        self.web_fetch_tool = WebFetchTools()
        self.api_fetch_tool = APIFetchTools()
        self.max_loops = max_loops
        self.console = Console()

    def _add_to_short_term_memory(self, action_log: str, tool_result: str):
        self.short_term_memory.add_entry(f"""---START---
{action_log}
Result: {tool_result}
---END---""")

    async def run(self, query: str):
        for i in range(self.max_loops):
            history = self.short_term_memory.get_history()
            tool_call = baml_client.Orchestrate(query=query, history=history)
            tool_result = None
            action_log = None

            if isinstance(tool_call, FinalAnswer):
                action_log = "Action: Provided final answer."
                if action_log:
                    self.console.print(Markdown(action_log))
                self.response_provider.final_answer(tool_call.answer)
                tool_result = tool_call.answer
                self._add_to_short_term_memory(action_log, tool_result)
                break
            elif isinstance(tool_call, ReadFile):
                action_log = f"Action: Read file: {tool_call.file_path}"
                content = self.file_manager.read_file(tool_call.file_path, tool_call.limit, tool_call.offset)
                tool_result = content
                if tool_call.limit and len(content) == tool_call.limit:
                    tool_result = "Note: The response was truncated. To get more data, you can use the 'offset' parameter in your next call." + tool_result
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, WriteFile):
                action_log = f"Action: Wrote to file: {tool_call.file_path}"
                success = self.file_manager.write_file(tool_call.file_path, tool_call.content)
                tool_result = "File saved successfully." if success else "Failed to save file."
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, ListDirectoryContents):
                action_log = f"Action: Listed directory: {tool_call.directory_path}"
                contents = self.file_manager.list_directory_contents(tool_call.directory_path)
                tool_result = "\n".join(contents)
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, FindContentInFile):
                action_log = f"Action: Searched for '{tool_call.search_query}' in file: {tool_call.file_path}"
                results = self.file_manager.find_content_in_file(tool_call.file_path, tool_call.search_query)
                tool_result = "\n".join(results)
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, GetUserInput):
                action_log = f"Action: Got user input for prompt: '{tool_call.prompt_message}'"
                user_input = self.human_interaction.get_user_text_input(tool_call.prompt_message)
                tool_result = user_input
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, ReviewAndConfirmChanges):
                action_log = f"Action: Review and confirm changes for: {tool_call.file_path}"
                success = self.human_interaction.review_and_confirm_changes(tool_call.file_path, tool_call.new_content)
                tool_result = "Changes applied." if success else "Changes rejected."
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, CollectUserFeedback):
                action_log = f"Action: Collected feedback for task {tool_call.task_id}"
                self.human_interaction.collect_feedback(tool_call.task_id, tool_call.feedback_type, tool_call.message)
                tool_result = "Feedback collected."
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, RequestHumanIntervention):
                action_log = f"Action: Requested human intervention for reason: '{tool_call.reason}'"
                user_input = self.human_interaction.request_human_intervention(tool_call.reason)
                tool_result = user_input
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, WebFetch):
                action_log = f"Action: Fetched content from URL: {tool_call.url}"
                content = await self.web_fetch_tool.fetch_page_content(tool_call.url, tool_call.limit, tool_call.offset, tool_call.convert_to_text)
                tool_result = content
                if tool_call.limit and len(content) == tool_call.limit:
                    tool_result = "Note: The response was truncated. To get more data, you can use the 'offset' parameter in your next call.\n" + tool_result
                self._add_to_short_term_memory(action_log, tool_result)
            elif isinstance(tool_call, APIFetch):
                action_log = f"Action: Fetched API data from URL: {tool_call.url}"
                content = self.api_fetch_tool.fetch_api_data(tool_call.url, tool_call.method, tool_call.headers, tool_call.data, tool_call.limit, tool_call.offset)
                tool_result = content
                if tool_call.limit and len(content) == tool_call.limit:
                    tool_result = "Note: The response was truncated. To get more data, you can use the 'offset' parameter in your next call." + tool_result
                self._add_to_short_term_memory(action_log, tool_result)
            else:
                tool_result = f"Unknown tool: {tool_call}"
                self.console.print(Markdown(tool_result))

            if action_log:
                self.console.print(Markdown(action_log.replace("Action:", "**[Agent Action]:**")))
        else:
            self.console.print(Markdown("Max loops reached. Exiting."))
