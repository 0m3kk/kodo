from baml_client.sync_client import b as baml_client
from baml_client.types import (
    ReadFile,
    WriteFile,
    ListDirectoryContents,
    FindContentInFile,
    GetUserInput,
    ReviewAndConfirmChanges,
    CollectUserFeedback,
    RequestHumanIntervention,
    FinalAnswer,
    WebFetch,
    APIFetch,
)
from .memory.short_term_memory import ShortTermMemory
from .tools.file_manager import FileManagerTools
from .tools.human_interaction import HumanInteractionTools
from .tools.response_provider import ResponseProviderTools
from .tools.web_fetch_tool import WebFetchTools
from .tools.api_fetch_tool import APIFetchTools
from rich.console import Console
from rich.markdown import Markdown
import json


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

    def _add_to_short_term_memory(
        self, action: str, result: str, hint: str | None = None
    ):
        entry = {"action": action, "result": result}
        if hint:
            entry["hint"] = hint
        self.short_term_memory.add_entry(json.dumps(entry))

    async def run(self, query: str):
        for i in range(self.max_loops):
            history = self.short_term_memory.get_history()
            tool_call = baml_client.Orchestrate(query=query, history=history)
            result = None
            action = None

            if isinstance(tool_call, FinalAnswer):
                action = (
                    f"**[Agent Action]:** FinalAnswer\n- answer: `{tool_call.answer}`"
                )
                if action:
                    self.console.print(Markdown(action))
                self.response_provider.final_answer(tool_call.answer)
                result = tool_call.answer
                self._add_to_short_term_memory(action, result)
                break
            elif isinstance(tool_call, ReadFile):
                action = f"**[Agent Action]:** ReadFile\n- file_path: `{tool_call.file_path}`"
                if tool_call.limit is not None:
                    action += f"\n- limit: `{tool_call.limit}`"
                if tool_call.offset is not None:
                    action += f"\n- offset: `{tool_call.offset}`"
                content = self.file_manager.read_file(
                    tool_call.file_path, tool_call.limit, tool_call.offset
                )
                result = content
                hint = None
                if tool_call.limit and len(content) == tool_call.limit:
                    hint = "The response was truncated. To get more data, you can use the 'offset' parameter in your next call."
                self._add_to_short_term_memory(action, result, hint=hint)
            elif isinstance(tool_call, WriteFile):
                action = f"**[Agent Action]:** WriteFile\n- file_path: `{tool_call.file_path}`\n- content: `{tool_call.content[:100]}...`"
                success = self.file_manager.write_file(
                    tool_call.file_path, tool_call.content
                )
                result = (
                    "File saved successfully." if success else "Failed to save file."
                )
                self._add_to_short_term_memory(action, result)
            elif isinstance(tool_call, ListDirectoryContents):
                action = f"**[Agent Action]:** ListDirectoryContents\n- directory_path: `{tool_call.directory_path}`"
                contents = self.file_manager.list_directory_contents(
                    tool_call.directory_path
                )
                result = "\n".join(contents)
                self._add_to_short_term_memory(action, result)
            elif isinstance(tool_call, FindContentInFile):
                action = f"**[Agent Action]:** FindContentInFile\n- file_path: `{tool_call.file_path}`\n- search_query: `{tool_call.search_query}`"
                results = self.file_manager.find_content_in_file(
                    tool_call.file_path, tool_call.search_query
                )
                result = "\n".join(results)
                self._add_to_short_term_memory(action, result)
            elif isinstance(tool_call, GetUserInput):
                action = f"**[Agent Action]:** GetUserInput\n- prompt_message: `{tool_call.prompt_message}`"
                user_input = self.human_interaction.get_user_text_input(
                    tool_call.prompt_message
                )
                result = user_input
                self._add_to_short_term_memory(action, result)
            elif isinstance(tool_call, ReviewAndConfirmChanges):
                action = f"**[Agent Action]:** ReviewAndConfirmChanges\n- file_path: `{tool_call.file_path}`\n- new_content: `{tool_call.new_content[:100]}...`"
                success = self.human_interaction.review_and_confirm_changes(
                    tool_call.file_path, tool_call.new_content
                )
                result = "Changes applied." if success else "Changes rejected."
                self._add_to_short_term_memory(action, result)
            elif isinstance(tool_call, CollectUserFeedback):
                action = f"**[Agent Action]:** CollectUserFeedback\n- task_id: `{tool_call.task_id}`\n- feedback_type: `{tool_call.feedback_type}`\n- message: `{tool_call.message}`"
                self.human_interaction.collect_feedback(
                    tool_call.task_id, tool_call.feedback_type, tool_call.message
                )
                result = "Feedback collected."
                self._add_to_short_term_memory(action, result)
            elif isinstance(tool_call, RequestHumanIntervention):
                action = f"**[Agent Action]:** RequestHumanIntervention\n- reason: `{tool_call.reason}`"
                user_input = self.human_interaction.request_human_intervention(
                    tool_call.reason
                )
                result = user_input
                self._add_to_short_term_memory(action, result)
            elif isinstance(tool_call, WebFetch):
                action = f"**[Agent Action]:** WebFetch\n- url: `{tool_call.url}`"
                if tool_call.limit is not None:
                    action += f"\n- limit: `{tool_call.limit}`"
                if tool_call.offset is not None:
                    action += f"\n- offset: `{tool_call.offset}`"
                if tool_call.convert_to_text is not None:
                    action += f"\n- convert_to_text: `{tool_call.convert_to_text}`"
                content = await self.web_fetch_tool.fetch_page_content(
                    tool_call.url,
                    tool_call.limit,
                    tool_call.offset,
                    tool_call.convert_to_text,
                )
                result = content
                hint = None
                if tool_call.limit and len(content) == tool_call.limit:
                    hint = "The response was truncated. To get more data, you can use the 'offset' parameter in your next call."
                self._add_to_short_term_memory(action, result, hint=hint)
            elif isinstance(tool_call, APIFetch):
                action = f"**[Agent Action]:** APIFetch\n- url: `{tool_call.url}`"
                if tool_call.method is not None:
                    action += f"\n- method: `{tool_call.method}`"
                if tool_call.headers is not None:
                    action += f"\n- headers: `{tool_call.headers}`"
                if tool_call.data is not None:
                    action += f"\n- data: `{tool_call.data}`"
                if tool_call.limit is not None:
                    action += f"\n- limit: `{tool_call.limit}`"
                if tool_call.offset is not None:
                    action += f"\n- offset: `{tool_call.offset}`"
                content = self.api_fetch_tool.fetch_api_data(
                    tool_call.url,
                    tool_call.method,
                    tool_call.headers,
                    tool_call.data,
                    tool_call.limit,
                    tool_call.offset,
                )
                result = content
                hint = None
                if tool_call.limit and len(content) == tool_call.limit:
                    hint = "The response was truncated. To get more data, you can use the 'offset' parameter in your next call."
                self._add_to_short_term_memory(action, result, hint=hint)
            else:
                action = "**[Agent Action]:** Unknown Tool\n- tool_call: `{tool_call}`"
                self.console.print(Markdown(action))

            self.console.print(Markdown(action))

        else:
            self.console.print(Markdown("Max loops reached. Exiting."))
