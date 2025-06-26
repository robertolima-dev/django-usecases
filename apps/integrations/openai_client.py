import logging
import random

import openai
from django.conf import settings
from tenacity import (  # noqa: E501
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self, simulate_failure=False):
        openai.api_key = settings.OPENAI_API_KEY
        self.simulate_failure = simulate_failure

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(Exception)
    )
    def call_chat_completion(self, messages, model="gpt-4", temperature=0.7):
        if self.simulate_failure and random.random() < 0.7:
            logger.warning("Simulando falha na chamada à OpenAI")
            raise Exception("Simulated failure")

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error("Erro ao chamar OpenAI: %s", str(e), exc_info=True)
            raise
