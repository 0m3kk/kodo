class ToolCall {
  name Tool
  args map<string, string>
}

function Orchestrate(query: string, history: string[]) -> ToolCall {
  client OpenRouter
  prompt #"
    You are a helpful assistant. Your job is to help the user with their request.
    You have the following tools at your disposal:
    - ReadFile(filePath: string) -> string
    - WriteFile(filePath: string, content: string) -> bool
    - ListDirectoryContents(directoryPath: string) -> list<string>
    - FindContentInFile(filePath: string, searchQuery: string) -> list<string>
    - GetUserInput(prompt: string) -> string
    - ReviewAndConfirmChanges(filePath: string, newContent: string) -> bool
    - CollectUserFeedback(taskId: string, feedbackType: string, feedbackMessage: string) -> void
    - RequestHumanIntervention(reason: string) -> string
    - FinalAnswer(answer: string) -> string
    - WebFetch(url: string) -> string
    - APIFetch(url: string, method: string, headers: string, data: string) -> string

    Based on the user's query and the conversation history, which tool should you use? You must use a tool.

    Query: {{ query }}
    {% if history is defined and history|length > 0 %}
     History:
    {{ history | join("\n") }}
    {% endif %}

    {{ ctx.output_format }}
  "#
}
