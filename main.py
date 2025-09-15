import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

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

    result = generate_content(client, messages, verbose=verbose)
    if result:
        print(result)


def generate_content(client, messages, verbose=False, call_trace=None):
    if call_trace is None:
        call_trace = []

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

    # Add each candidate's content to messages
    if hasattr(response, "candidates") and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, "content") and candidate.content:
                messages.append(candidate.content)

    # Optionally, handle the first candidate's text for return
    first_text = None
    if response.candidates and hasattr(response.candidates[0], "content"):
        parts = getattr(response.candidates[0].content, "parts", [])
        if parts and hasattr(parts[0], "text"):
            first_text = parts[0].text

    if not response.function_calls:
        # Print the call trace before the final response
        for trace in call_trace:
            print(trace)
        print("Final response:")
        return first_text

    function_responses = []
    for function_call_part in response.function_calls:
        # Print function call trace
        func_name = getattr(function_call_part, "name", "unknown_function")
        trace_msg = f"- Calling function: {func_name}"
        call_trace.append(trace_msg)

        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        # Add function response to messages
        messages.append(
            types.Content(role="function", parts=[function_call_result.parts[0]])
        )
        function_responses.append(function_call_result.parts[0])
        # After each function call, also append as a user message
        messages.append(
            types.Content(role="user", parts=[function_call_result.parts[0]])
        )

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    # Recursively call generate_content with updated messages
    return generate_content(client, messages, verbose, call_trace)


def run_agent_loop(client, messages, verbose=False, max_iterations=20):
    for i in range(max_iterations):
        try:
            result = generate_content(client, messages, verbose)
            if result:
                print(result)
                break
        except Exception as e:
            print(f"Error during agent loop (iteration {i+1}): {e}")
            break
    else:
        print("Reached maximum iterations without a final response.")


if __name__ == "__main__":
    main()
