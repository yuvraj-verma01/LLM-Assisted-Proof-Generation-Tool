import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set. Put it in a .env file or environment variable.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

def complete_text(prompt: str, model: str = "deepseek/deepseek-r1:free") -> str:
    """
    Send a prompt to the OpenRouter LLM and return the response text.
    Default model: deepseek/deepseek-r1:free
    """
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost",   
            "X-Title": "Proof Checker",           
        },
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800,
    )
    return completion.choices[0].message.content.strip()
