"""One small live request, explicitly invoked from the terminal."""
import sys
from google.genai import types
from engine import client, MODEL, usage, error_message

def main():
    try:
        with client() as api:
            response = api.models.generate_content(
                model=MODEL,
                contents="Reply with the words API connection successful.",
                config=types.GenerateContentConfig(max_output_tokens=128),
            )
        print("Model:", MODEL)
        print("Response:", response.text)
        print("Usage:", usage(response))
        print("API request succeeded. Check AI Studio billing to confirm the funding source.")
        return 0
    except Exception as exc:
        print(error_message(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
