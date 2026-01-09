import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERS
from prompts import system_prompt
from tools import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    content = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=content)])]

    if args.verbose:
        print(f"User prompt: {content}")

    client = genai.Client(api_key=api_key)
    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate content: {e}")


    print("Cannot satisfy the intended query")
    sys.exit(1)

def generate_content(client, messages, verbose):
    res = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if not res.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    prompt_token_count = res.usage_metadata.prompt_token_count
    response_token_count = res.usage_metadata.candidates_token_count
    if verbose:
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")

    if not res.candidates:
        for candidate in res.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not res.function_calls:
        return res.text

    f_res_list = []
    for function_call in res.function_calls:
        function_call_result = call_function(function_call, verbose)
        if (
            not function_call_result
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        f_res_list.append(function_call_result.parts[0])

    messages.append(types.Content(role = "user", parts = f_res_list))



if __name__ == "__main__":
    main()
