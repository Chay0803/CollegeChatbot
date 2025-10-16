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

from openai import OpenAI
import os

# Load OpenRouter API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", "<OPENROUTER_API_KEY>"),  # Replace if not using env vars
)

def ask_ollama(prompt: str, model_name: str = "openai/gpt-oss-20b:free"):
    """
    Sends a prompt to the OpenRouter API and returns the generated text response.
    (Maintains backward compatibility with previous function name.)
    """
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://ifheindia.org",  # Optional, for OpenRouter rankings
            "X-Title": "IFHE College Chatbot",       # Optional, project name
        },
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant for IFHE University."},
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content.strip()


# Optional: Streaming support (if you want real-time typing effect later)
def ask_ollama_stream(prompt: str, model_name: str = "openai/gpt-oss-20b:free"):
    """
    Streams response from OpenRouter model.
    """
    stream = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant for IFHE University."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.get("content", "")
        if content:
            yield content
