function Orchestrate(query: string, history: string[]) -> ReadFile | WriteFile | ListDirectoryContents | FindContentInFile | GetUserInput | ReviewAndConfirmChanges | CollectUserFeedback | RequestHumanIntervention | FinalAnswer | WebFetch | APIFetch {
  client OpenRouter
  prompt #"
    You are a helpful assistant. Your job is to help the user with their request.
    You have the following tools at your disposal, defined as classes:
    {{ ctx.output_format }}

    Based on the user's query and the conversation history, which tool should you use? You must use a tool.

    Query: {{ query }}
    {% if history is defined and history|length > 0 %}
    History:
    {{ history | join("\n") }}
    {% endif %}

    Choose the best tool for the query and fill in the parameters.
  "#
}

function SummarizeText(text: string) -> string {
  client OpenRouter
  prompt #"
    Summarize the following text, keeping the summary concise and under 200 words:

    {{ text }}
  "#
}
