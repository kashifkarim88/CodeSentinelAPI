import os
from dotenv import load_dotenv

# Load the .env file explicitly
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# DEBUG: Verify the key is loaded (Delete this print after it works)
if OPENROUTER_API_KEY:
    # Prints only the first 10 chars for safety
    print(f"--- [CONFIG] OpenRouter Key Loaded: {OPENROUTER_API_KEY[:10]}... ---")
else:
    print("--- [ERROR] OPENROUTER_API_KEY NOT FOUND IN .ENV ---")

# Ensure there are no extra spaces or quotes
if OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = OPENROUTER_API_KEY.strip().replace('"', '').replace("'", "")

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")
HF_TOKEN = os.getenv("HF_TOKEN")