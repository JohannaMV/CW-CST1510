from typing import List, Dict
from google import genai

class AIAssistant:
    """Simple wrapper around an AI/chat model."""
    def __init__(self, api_key: str, system_prompt: str = "You are a helpful assistant."):
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []

        self._client = genai.Client(api_key=api_key)

    def set_system_prompt(self, prompt: str) -> None:
        self._system_prompt = prompt

    def send_message(self, user_message: str) -> str:
        self._history.append({"role": "user", "content": user_message})

        response = self._client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_message},
            ],
        )

        ai_reply = response.text
        self._history.append({"role": "assistant", "content": ai_reply})

        return ai_reply

    def clear_history(self) -> None:
        self._history.clear()

