import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    args = sys.argv[1:]
    verbose = False

    if not args:
        print("No prompt provided")
        sys.exit(1)
    if "--verbose" in args:
        args.remove("--verbose")
        verbose = True

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose=verbose)


def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if verbose:
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print("Response: ")
    print(response.text)


if __name__ == "__main__":
    main()
