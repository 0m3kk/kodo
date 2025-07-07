client OpenRouter {
  provider "openai-generic"
  options {
    api_key env.OPENROUTER_API_KEY
    base_url "https://openrouter.ai/api/v1"
    model "deepseek/deepseek-chat:free"
  }
}
