class ReadFile {
  tool_name "read_file" @description("Reads the content of a given file path.")
  file_path string @description("The path to the file to read.")
}

class WriteFile {
  tool_name "write_file" @description("Writes the given content to a file at the specified path.")
  file_path string @description("The path to the file to write to.")
  content string @description("The content to write to the file.")
}

class ListDirectoryContents {
  tool_name "list_directory_contents" @description("Lists all non-hidden files and subdirectories within a given directory.")
  directory_path string @description("The path to the directory to list. Defaults to .")
}

class FindContentInFile {
  tool_name "find_content_in_file" @description("Reads the content of a file and returns lines containing the search query.")
  file_path string @description("The path to the file to search within.")
  search_query string @description("The string to search for (case-insensitive).")
}

class GetUserInput {
  tool_name "get_user_text_input" @description("Gets free-form text input from the user via the CLI.")
  prompt_message string @description("The message to display to the user.")
}

class ReviewAndConfirmChanges {
  tool_name "review_and_confirm_changes" @description("Displays a diff of proposed changes and asks for user confirmation to apply them.")
  file_path string @description("The path to the file to be modified.")
  new_content string @description("The proposed new content for the file.")
}

class CollectUserFeedback {
  tool_name "collect_feedback" @description("Logs feedback to the console and a file.")
  task_id string @description("The ID of the task related to the feedback.")
  feedback_type string @description("The type of feedback (e.g., 'info', 'warning', 'error').")
  message string @description("The feedback message.")
}

class RequestHumanIntervention {
  tool_name "request_human_intervention" @description("Pauses the agent and prompts the user for new instructions.")
  reason string @description("The reason for requesting intervention.")
}

class FinalAnswer {
  tool_name "final_answer" @description("Provides the final answer to the user.")
  answer string @description("The final answer to be provided to the user.")
}

class WebFetch {
  tool_name "fetch_page_content" @description("Fetches the full HTML content of a given URL using a headless browser.")
  url string @description("The URL to fetch.")
}

class APIFetch {
  tool_name "fetch_api_data" @description("Fetches data from a given API endpoint.")
  url string @description("The URL of the API endpoint.")
  method string @description("The HTTP method to use (GET, POST, PUT, DELETE, etc.). Defaults to GET.")
  headers map<string, string> @description("A dictionary of HTTP headers to send with the request.")
  data map<string, string> @description("A dictionary of data to send in the request body (for POST, PUT, etc.).")
}
