import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
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
    verbose = args.verbose

    messages = [types.Content(role="user", parts=[types.Part(text=content)])]

    if verbose:
        print(f"User prompt: {content}")

    client = genai.Client(api_key=api_key)
    res = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    if not res.usage_metadata:
        raise RuntimeError("a problem occurred in the response")

    prompt_token_count = res.usage_metadata.prompt_token_count
    response_token_count = res.usage_metadata.candidates_token_count

    if verbose:
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")
    
    f_res_list = []
    if res.function_calls:
        print("Function Calls :")
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

    print("Response :")
    print(res.text)


if __name__ == "__main__":
    main()
