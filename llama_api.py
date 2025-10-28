# import ollama

# # Synchronous ask (kept for caching or non-stream calls)
# def ask_ollama(prompt: str, model_name: str = "llama3"):
#     response = ollama.chat(
#         model=model_name,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant for college queries."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.get("message", {}).get("content", "")

# # Streaming generator: yields incremental text chunks
# def ask_ollama_stream(prompt: str, model_name: str = "llama3"):
#     stream = ollama.chat(
#         model=model_name,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant for college queries."},
#             {"role": "user", "content": prompt}
#         ],
#         stream=True
#     )
#     buffer = ""
#     for chunk in stream:
#         # chunk may contain partial content; combine
#         text = chunk.get("message", {}).get("content", "")
#         if text:
#             # yield incremental text (could be full or partial)
#             yield text

from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_KEY:
    raise ValueError("❌ Missing OPENROUTER_API_KEY in .env")

print("Loaded key prefix:", OPENROUTER_KEY[:15])

# Initialize OpenRouter API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)


# 🧠 Non-streaming function
def ask_ollama(prompt: str, model_name: str = "openai/gpt-oss-20b:free"):
    """
    Sends a prompt to OpenRouter and returns the full response text.
    """
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://ifheindia.org",  # optional (for OpenRouter analytics)
            "X-Title": "IFHE Chatbot",               # project title
        },
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant for IFHE University."},
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content.strip()


def ask_ollama_stream(prompt: str, model_name: str = "openai/gpt-oss-20b:free"):
    """
    Streams response token-by-token for real-time output.
    Includes detailed logging for debugging.
    """
    try:
        print(f"🚀 Connecting to OpenRouter model: {model_name}")
        stream = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://ifheindia.org",
                "X-Title": "IFHE Chatbot",
            },
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful academic assistant for IFHE University."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        for chunk in stream:
            # Log structure of each chunk
            print(f"📦 Chunk received: {chunk}")
            if hasattr(chunk.choices[0].delta, "content"):
                text = chunk.choices[0].delta.content
                if text:
                    print(f"🧩 Token: {text!r}")
                    yield text

        print("✅ Streaming complete.")

    except Exception as e:
        print("⚠️ Streaming error (inside llama_api):", e)
        yield f"⚠️ Error while streaming: {str(e)}"

