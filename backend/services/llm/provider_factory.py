from core.settings import settings


class ProviderFactory:
    @staticmethod
    def create():
        provider = settings.LLM_PROVIDER.lower()

        if provider == "deepseek":
            from services.llm.deepseek_service import DeepSeekService
            return DeepSeekService()
        elif provider == "openai":
            from services.llm.openai_provider import OpenAIProvider
            return OpenAIProvider()

        raise ValueError(
            f"Unsupported LLM Provider: {provider}"
        )