import os
import openai
from prompt_input import prompt

openai.api_key = "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"


def process_gpt4(text):
    """This function prompts the gpt-4 model and returns the output"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {"role": "user", "content": prompt + text},
        ],
    )

    result = response["choices"][0]["message"]["content"]

    return result
