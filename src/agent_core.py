from baml_client.sync_client import b as baml_client
from baml_client.types import Tool
from .memory.short_term_memory import ShortTermMemory
from .tools.file_manager import FileManagerTools
from .tools.human_interaction import HumanInteractionTools

class DevAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.short_term_memory = ShortTermMemory(session_id)
        self.file_manager = FileManagerTools()
        self.human_interaction = HumanInteractionTools()

    async def run(self, query: str):
        history = self.short_term_memory.get_history()
        tool_call = baml_client.Orchestrate(query=query, history=history)

        match tool_call.name:
            case Tool.ReadFile:
                file_path = tool_call.args["filePath"]
                content = self.file_manager.read_file(file_path)
                self.short_term_memory.add_entry(f"Read file: {file_path}")
                print(content)
            case Tool.WriteFile:
                file_path = tool_call.args["filePath"]
                content = tool_call.args["content"]
                if self.file_manager.write_file(file_path, content):
                    self.short_term_memory.add_entry(f"Wrote to file: {file_path}")
                    print("File saved.")
            case Tool.ListDirectoryContents:
                directory_path = tool_call.args["directoryPath"]
                contents = self.file_manager.list_directory_contents(directory_path)
                self.short_term_memory.add_entry(f"Listed directory: {directory_path}")
                print("\n".join(contents))
            case Tool.FindContentInFile:
                file_path = tool_call.args["filePath"]
                search_query = tool_call.args["searchQuery"]
                results = self.file_manager.find_content_in_file(file_path, search_query)
                self.short_term_memory.add_entry(f"Searched for '{search_query}' in file: {file_path}")
                print("\n".join(results))
            case Tool.GetUserInput:
                prompt = tool_call.args["prompt"]
                user_input = self.human_interaction.get_user_text_input(prompt)
                self.short_term_memory.add_entry(f"Got user input for prompt: '{prompt}'")
                print(f"User input: {user_input}")
            case Tool.ReviewAndConfirmChanges:
                file_path = tool_call.args["filePath"]
                new_content = tool_call.args["newContent"]
                if self.human_interaction.review_and_confirm_changes(file_path, new_content):
                    self.short_term_memory.add_entry(f"Confirmed and applied changes to: {file_path}")
                    print("Changes applied.")
                else:
                    self.short_term_memory.add_entry(f"Rejected changes to: {file_path}")
                    print("Changes rejected.")
            case Tool.CollectUserFeedback:
                task_id = tool_call.args["taskId"]
                feedback_type = tool_call.args["feedbackType"]
                feedback_message = tool_call.args["feedbackMessage"]
                self.human_interaction.collect_feedback(task_id, feedback_type, feedback_message)
                self.short_term_memory.add_entry(f"Collected feedback for task {task_id}")
            case Tool.RequestHumanIntervention:
                reason = tool_call.args["reason"]
                user_input = self.human_interaction.request_human_intervention(reason)
                self.short_term_memory.add_entry(f"Requested human intervention for reason: '{reason}'")
                print(f"User input: {user_input}")
            case _:
                print(f"Unknown tool: {tool_call.name}")
