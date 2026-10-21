import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from crewai import BaseLLM

load_dotenv()


class HuggingFaceCrewLLM(BaseLLM):
    """
    CrewAI LLM adapter for Hugging Face's OpenAI-compatible router.
    Removes CrewAI's cache_breakpoint metadata before sending messages.
    """

    def __init__(
        self,
        temperature: float = 0.2,
        max_tokens: int = 1200,
    ):
        super().__init__(
            model="openai/gpt-oss-120b",
            temperature=temperature,
        )

        self.temperature = temperature
        self.max_tokens = max_tokens

        self.api_key = os.getenv("HF_TOKEN")

        if not self.api_key:
            raise ValueError(
                "HF_TOKEN is missing from the .env file."
            )

        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=self.api_key,
        )

    def _clean_messages(self, messages):
        """Remove CrewAI-only fields unsupported by Hugging Face."""

        cleaned = []

        for message in messages:
            if isinstance(message, dict):
                new_message = dict(message)

                # Remove CrewAI cache metadata
                new_message.pop("cache_breakpoint", None)

                cleaned.append(new_message)

            else:
                cleaned.append(message)

        return cleaned

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        **kwargs: Any,
    ) -> str:

        # Convert string prompt to OpenAI message format
        if isinstance(messages, str):
            messages = [
                {
                    "role": "user",
                    "content": messages,
                }
            ]

        # Remove unsupported CrewAI metadata
        messages = self._clean_messages(messages)

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b:fastest",
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response.choices[0].message.content or ""

    def supports_function_calling(self) -> bool:
        return False

    def get_context_window_size(self) -> int:
        return 131072


def get_llm(
    temperature: float = 0.2,
    max_tokens: int = 1200,
):
    return HuggingFaceCrewLLM(
        temperature=temperature,
        max_tokens=max_tokens,
    )