### 1\. Overall Project Setup & Core Structure

As an AI specializing in Python development and agent architectures, help me set up the initial project structure for a 'Dev Agent' that operates via a Command Line Interface (CLI). This agent will heavily feature Human-in-the-Loop interactions.

The agent will use **BAML** for LLM interactions and a **local LLM** (like Ollama, compatible with OpenAI API).

**Here's what I need:**

1.  **Project Structure:**
    * A root directory named `dev_agent_cli`.
    * `src/`: Contains the main Python source code.
        * `src/cli.py`: The entry point for the CLI, handling command parsing (using `typer`).
        * `src/agent_core.py`: The core logic of the Dev Agent, orchestrating BAML calls, tool execution, and human interactions.
        * `src/tools/`: Directory for Python functions that act as tools.
            * `src/tools/file_manager.py`: For file I/O operations.
            * `src/tools/human_interaction.py`: **Crucially, for Human-in-the-Loop tools.**
        * `src/memory/`: Directory for memory management (`short_term_memory.py`). (Long-term memory is optional for now).
    * `baml_src/`: Contains BAML definitions (.baml files) for LLM functions and types.
        * `baml_src/config.baml`: BAML configuration for LLM providers.
        * `baml_src/functions.baml`: BAML functions for core agent operations (intent classification, planning, **and human interaction calls**).
        * `baml_src/types.baml`: BAML type definitions.
    * `tests/`: For unit and integration tests.
    * `data/`: For temporary data, like session files.
    * `.env.example`: Template for environment variables.
    * `requirements.txt`: Python dependencies.
    * `README.md`: Basic project description.

2.  **Initial CLI Setup (`src/cli.py`):**
    * Use `typer` for command-line parsing.
    * Define a basic `main` function.
    * Create a placeholder command: `dev_agent hello` that prints "Hello from Dev Agent!".

3.  **Basic Agent Core (`src/agent_core.py`):**
    * A class `DevAgent` with an `__init__` method that takes a `session_id`.
    * Initialize `ShortTermMemory` and an instance of `HumanInteractionTools` (from `src/tools/human_interaction.py`).
    * Placeholder method: `process_request(self, user_input: str)`.

4.  **Initial BAML Configuration (`baml_src/config.baml`):**
    * Define an LLM provider pointing to a local Ollama instance (e.g., `http://localhost:11434/v1`).
    * Specify `provider="openai"` and a dummy `api_key`.
    * Set a default model (e.g., `llama3`).

5.  **Initial BAML Function (`baml_src/functions.baml`):**
    * Define a simple BAML function, `EchoUserMessage(message: string) -> string`, which reflects the input message.

6.  **Basic Human Interaction Tool (`src/tools/human_interaction.py`):**
    * A class `HumanInteractionTools` with an `__init__` method.
    * A method `confirm_action(self, prompt_message: str) -> bool` that asks the user for a yes/no confirmation via CLI. Use `questionary` or basic `input()`.
    * Add a simple print statement for when it's called.

7.  **BAML Definition for Confirmation Tool (`baml_src/functions.baml`):**
    * Define a BAML function `AskForConfirmation(message: string) -> bool {}`.
    * This function should be callable by the LLM to request user confirmation.

8.  **`requirements.txt`:** List initial dependencies like `typer`, `baml-lib`, `python-dotenv`, `questionary`.

9.  **`README.md`:** A brief description, installation instructions (mentioning Ollama setup), and how to run the `hello` command.

Provide all the code snippets for these files, ensuring they are functional as a basic starting point.

---

### 2. Basic File Management Tools & Enhanced Human Interaction

As an AI assistant, I need you to implement basic file management tools and enhance the human interaction tools for my 'Dev Agent'. These tools will be called by the Agent Core based on LLM's decisions, enabling the agent to navigate and manipulate the file system.

**Here's what I need:**

1.  **`src/tools/file_manager.py`:**

      * **`FileManagerTools` Class:**
          * An `__init__` method.
          * **`read_file(self, file_path: str) -> str`:**
              * Reads the content of a given file path.
              * Handles `FileNotFoundError` and other `IOError` types gracefully, returning an informative error message prefixed with `ERROR:`.
              * Add a docstring.
          * **`write_file(self, file_path: str, content: str) -> bool`:**
              * Writes the given content to a file at the specified path.
              * Creates necessary parent directories if they don't exist.
              * Handles `IOError` types gracefully, returning `False` on failure and `True` on success.
              * Add docstring.
          * **`list_directory_contents(self, directory_path: str = ".") -> list[str]`:**
              * Lists all files and subdirectories within a given directory.
              * Excludes hidden files/directories (starting with `.`) and common ignored directories (e.g., `__pycache__`, `node_modules`, `.git`, `venv`, `dist`).
              * Handles `FileNotFoundError` and `NotADirectoryError` gracefully, returning an error message list if an error occurs.
              * Add docstring.
          * **`find_content_in_file(self, file_path: str, search_query: str) -> list[str]`:**
              * Reads the content of `file_path`.
              * Returns a list of lines that contain the `search_query` (case-insensitive).
              * If `file_path` is not found or cannot be read, return an appropriate error message list.
              * Add docstring.

2.  **Enhanced `src/tools/human_interaction.py`:**

      * **`HumanInteractionTools` Class:** (Continue adding methods to this class from the previous prompt)
          * **`confirm_action(self, prompt_message: str) -> bool`:** (Keep this)
              * Asks the user for confirmation via CLI (using `questionary.confirm`).
          * **`get_user_text_input(self, prompt_message: str) -> str`:**
              * Gets free-form text input from the user via CLI (using `questionary.text`).
              * Add docstring.
          * **`review_and_confirm_changes(self, file_path: str, new_content: str) -> bool`:**
              * This tool is specifically for reviewing proposed file changes.
              * It should read the existing content of `file_path`.
              * Compute and display a **diff** between the existing content and `new_content` to the user in a readable format (e.g., using `difflib`).
              * Then, it should ask the user to `confirm_action` whether to apply these changes.
              * Returns `True` if changes are confirmed and applied, `False` otherwise.
              * Add docstring.
          * **`collect_feedback(self, task_id: str, feedback_type: str, message: str) -> None`:**
              * Prints feedback to console and logs it to a simple `data/feedback.log` file.
              * Add docstring.
          * **`request_human_intervention(self, reason: str) -> str`:**
              * Pauses the agent, prints `reason`, and prompts the user for new instructions or a `continue` command.
              * Returns the user's input.
              * Add docstring.

3.  **BAML Function Definitions (`baml_src/functions.baml`):**

      * **`ReadFile(filePath: string) -> string {}`**
      * **`WriteFile(filePath: string, content: string) -> bool {}`**
      * **`ListDirectoryContents(directoryPath: string) -> list<string> {}`**
      * **`FindContentInFile(filePath: string, searchQuery: string) -> list<string> {}`**
      * **`GetUserInput(prompt: string) -> string {}`**
      * **`ReviewAndConfirmChanges(filePath: string, newContent: string) -> bool {}`**
      * **`CollectUserFeedback(taskId: string, feedbackType: string, feedbackMessage: string) -> void {}`**
      * **`RequestHumanIntervention(reason: string) -> string {}`**
      * Ensure all input/output types align with the Python functions.

4.  **Integration into `src/agent_core.py` (textual description):**

      * Describe how `DevAgent` would import and initialize `FileManagerTools` and `HumanInteractionTools`.
      * Explain how the agent would expose these tools for BAML's function calling mechanism.
      * Briefly describe the flow: LLM decides to call a tool -\> Agent Core executes the Python function -\> Result is handled. Specifically mention:
          * When LLM decides to `WriteFile`, Agent Core should interpose `ReviewAndConfirmChanges` tool first, passing the proposed content, and only if confirmed, proceed with `FileManagerTools.write_file`.

Provide the full Python code for `src/tools/file_manager.py` and the updated `src/tools/human_interaction.py`, and the BAML definitions for `baml_src/functions.baml`. Ensure `difflib` is mentioned as a dependency for `requirements.txt`.

-----

### 3\. Short-Term Memory (STM) & Agent Core Orchestration

As an AI expert in agent memory systems and orchestration, I need you to design and implement the short-term memory solution and demonstrate its integration into the Agent Core logic for my 'Dev Agent'. This will ensure conversational context is maintained and the agent can effectively use its basic file and human interaction tools.

**Here's what I need:**

1.  **`src/memory/short_term_memory.py`:**
    * **`ShortTermMemory` Class:**
        * An `__init__` method that takes a `session_id: str` and a `data_dir: str = "data/sessions"`.
        * `add_message(role: str, content: str)`: Adds a new message (e.g., "user", "assistant", "system", "tool_output", "thought") to the history. Store as a list of dictionaries, e.g., `{"role": role, "content": content}`.
        * `get_history() -> list[dict]`: Returns the current conversation history.
        * `clear_history()`: Resets the memory for the current session and associated file.
        * Implement simple persistence: `_save_to_file()` and `_load_from_file()`. Save/load to a JSON file (`<session_id>.json`) in the specified `data_dir`.
        * Add docstrings.

2.  **Enhanced `src/agent_core.py`:**
    * **`DevAgent` Class:**
        * Modify `__init__` to:
            * Initialize `ShortTermMemory` using the provided `session_id`.
            * Initialize `FileManagerTools` and `HumanInteractionTools`.
            * Store a dictionary mapping BAML function names (as strings) to their corresponding Python tool methods (e.g., `{"ReadFile": self.file_manager.read_file, "AskForConfirmation": self.human_interaction.confirm_action}`).
        * Add a helper method `_execute_tool(tool_call: dict) -> str`:
            * Takes a `ToolCall` dictionary (e.g., `{"tool_name": "ReadFile", "parameters": {"filePath": "test.txt"}}`).
            * Looks up the corresponding Python function.
            * Calls the Python function with the provided parameters.
            * Returns the string result of the tool's execution.
            * Handle potential errors during tool execution.
        * Modify `process_request(self, user_input: str) -> str`:
            * Add the `user_input` to STM (`"user"` role).
            * **Orchestration Logic:**
                * **Loop:** Continue processing until a "DONE" signal or explicit user intervention.
                * **Step 1: LLM Thought/Plan Generation (using BAML):**
                    * Use a BAML function (let's call it `GenerateAgentThought` - define this in `baml_src/functions.baml` later) that takes `user_input`, `STM.get_history()`, and the list of available tools.
                    * This BAML function should output a `Thought` (a BAML Type) containing:
                        * `thought_process: string`: LLM's reasoning.
                        * `action: Optional<ToolCall>`: The tool LLM decides to call, if any.
                        * `final_response: Optional<string>`: If LLM believes the task is complete.
                        * `should_ask_for_confirmation: bool`: If the *next intended action* is sensitive (e.g., write file).
                    * Add `thought_process` to STM (`"thought"` role).
                * **Step 2: Human Confirmation (if needed):**
                    * If `should_ask_for_confirmation` is true, call `self.human_interaction.confirm_action`.
                    * If user declines, add a message to STM and return.
                * **Step 3: Tool Execution:**
                    * If `action` is present, call `self._execute_tool(action)`.
                    * Add the tool's output to STM (`"tool_output"` role).
                * **Step 4: Handle Final Response:**
                    * If `final_response` is present, add it to STM (`"assistant"` role) and return it.
                * **Loop or Request Intervention:** If no final response and no action, or if an unexpected state, use `self.human_interaction.request_human_intervention`.
            * Demonstrate the flow for a simple request like "read the content of `example.py`" or "list files in current directory and then read `README.md`".

Provide the full Python code for `src/memory/short_term_memory.py` and the updated `src/agent_core.py` to illustrate the orchestration. Assume necessary imports for BAML functions and tools.

---

### 4. BAML Functions for Intent, Thought & Plan Generation (Basic Tools Focused)

As an AI fluent in BAML and LLM prompt engineering, help me define the core BAML functions for my 'Dev Agent' to understand user intent, generate a thought process, and plan actions. The agent will **only use the basic file management tools (`ReadFile`, `WriteFile`, `ListDirectoryContents`, `FindContentInFile`) and human interaction tools (`AskForConfirmation`, `GetUserInput`, `ReviewAndConfirmChanges`, `CollectUserFeedback`, `RequestHumanIntervention`).**

**Here's what I need:**

1.  **`baml_src/types.baml`:**

      * **`Intent` Enum:**
          * Define a BAML enum type `Intent` with values like `READ_FILE`, `WRITE_FILE`, `LIST_DIRECTORY`, `FIND_CONTENT`, `GET_USER_INPUT`, `REQUEST_INTERVENTION`, `GIVE_FEEDBACK`, `UNKNOWN`.
      * **`ToolCall` Type:** (Keep this)
          * Define a BAML type `ToolCall` representing a specific tool to be called:
              * `tool_name: string`: The name of the tool (must be one of the specified basic tools).
              * `parameters: map<string, string>`: A dictionary of key-value pairs for the tool's parameters.
      * **`Thought` Type:**
          * Define a BAML type `Thought` for the LLM's reasoning and action plan:
              * `thought_process: string`: The LLM's detailed reasoning steps, why it chose a tool, what it expects.
              * `action: Optional<ToolCall>`: The tool LLM decides to call, if any.
              * `final_response: Optional<string>`: A message to return to the user if the task is complete.
              * `should_ask_for_confirmation: bool`: Indicates if the *next immediate action* (if any `action` is present) requires explicit user confirmation (e.g., `WriteFile`). **The LLM should decide this based on the tool being called.**

2.  **`baml_src/functions.baml`:**

      * **`ClassifyUserIntent(user_query: string, available_tools: list<string>) -> Intent` Function:**
          * A BAML function to classify the `user_query` into one of the basic `Intent` types.
          * Guide the LLM to choose the most appropriate intent.
          * Provide few-shot examples for each basic intent (e.g., "read X", "show me files", "find Y in Z").
      * **`GenerateAgentThought(user_query: string, conversation_history: list<dict>, available_tools: list<string>) -> Thought` Function:**
          * This is the core planning function. Takes `user_query`, `conversation_history` (from STM), and a list of `available_tools` (string names).
          * **Prompt for the LLM:**
              * "You are an intelligent Dev Agent capable of using specific tools to assist a developer. Your goal is to fulfill the `user_query` by performing a series of steps."
              * "**Available Tools:** `ReadFile`, `WriteFile`, `ListDirectoryContents`, `FindContentInFile`, `AskForConfirmation`, `GetUserInput`, `ReviewAndConfirmChanges`, `CollectUserFeedback`, `RequestHumanIntervention`."
              * "Based on the `user_query` and `conversation_history`, decide your `thought_process`, the `action` to take, and if you can provide a `final_response`."
              * "**Safety First:** If your `action` involves `WriteFile` or `ReviewAndConfirmChanges`, you **must** set `should_ask_for_confirmation` to `true`. If `ReviewAndConfirmChanges` is chosen, also use `should_ask_for_confirmation`."
              * "If you need more information from the user or cannot proceed, consider `GetUserInput` or `RequestHumanIntervention`."
              * "Always provide a clear `thought_process` explaining your reasoning and next step."
              * "When the task is complete, provide a `final_response` and leave `action` as null."
              * Include few-shot examples demonstrating thought processes and tool calls for tasks like:
                  * "List files in the current directory." (Output: `Thought` with `ListDirectoryContents` action).
                  * "Read the content of `main.py`." (Output: `Thought` with `ReadFile` action).
                  * "Write 'hello world' to `new_file.txt`." (Output: `Thought` with `WriteFile` action and `should_ask_for_confirmation=true`).
                  * "Find 'import' in `utils.py`." (Output: `Thought` with `FindContentInFile` action).
                  * "Tell me about the project structure." (Output: `Thought` with `ListDirectoryContents` then `ReadFile` of `README.md` in subsequent turns).

Provide all the BAML code for `baml_src/types.baml` and `baml_src/functions.baml`, focusing on detailed prompts within the BAML function definitions to guide the LLM's behavior and tool usage.

-----
