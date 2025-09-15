import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY or not API_KEY.startswith("sk-or-"):
    raise RuntimeError("Missing or wrong OPENROUTER_API_KEY (should start with 'sk-or-').")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

DEFAULT_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"  

def complete_text(prompt: str, model: str = DEFAULT_MODEL) -> str:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800,
            extra_headers={
                
                "HTTP-Referer": "http://localhost",
                "X-Title": "Proof Generator",
            },
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:

        raise RuntimeError(f"LLM call failed: {e}") from e