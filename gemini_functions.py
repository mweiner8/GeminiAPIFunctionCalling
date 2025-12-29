"""
Shared Gemini function calling logic for Speed Camera API
This module contains all the shared functionality used by both CLI and GUI versions
"""

import os
import json
import requests
from typing import Any, Dict
from google import genai
from google.genai import types, errors
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SPEED_CAMERA_API_BASE_URL = "https://speedcameraapi.onrender.com"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in .env file")

# Configure Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# API Function implementations
def get_cameras_by_zipcode(zipcode: str) -> Dict[str, Any]:
    """
    Call the Speed Camera API to get all cameras in a specific zipcode.

    Args:
        zipcode: 5-digit US zipcode

    Returns:
        Dictionary with cameras list and metadata
    """
    try:
        url = f"{SPEED_CAMERA_API_BASE_URL}/cameras/zipcode/{zipcode}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        cameras = response.json()
        return {
            "success": True,
            "zipcode": zipcode,
            "count": len(cameras),
            "cameras": cameras
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "zipcode": zipcode
        }


def search_cameras_by_street(street: str, zipcode: str) -> Dict[str, Any]:
    """
    Search for cameras by street name within a zipcode.

    Args:
        street: Street name to search for
        zipcode: 5-digit US zipcode

    Returns:
        Dictionary with matching cameras and metadata
    """
    try:
        url = f"{SPEED_CAMERA_API_BASE_URL}/cameras/search"
        params = {"street": street, "zipcode": zipcode}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        cameras = response.json()
        return {
            "success": True,
            "street": street,
            "zipcode": zipcode,
            "count": len(cameras),
            "cameras": cameras
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "street": street,
            "zipcode": zipcode
        }


# Gemini function declarations
get_cameras_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_cameras_by_zipcode",
            description="Get all speed cameras in a specific zipcode. Use this when the user asks about cameras in a particular area or zipcode.",
            parameters={
                "type": "OBJECT",
                "properties": {
                    "zipcode": {
                        "type": "STRING",
                        "description": "5-digit US zipcode (e.g., '10036', '90212')"
                    }
                },
                "required": ["zipcode"]
            }
        ),
        types.FunctionDeclaration(
            name="search_cameras_by_street",
            description="Search for speed cameras by street name within a specific zipcode. Use this when the user asks about cameras on a particular street. IMPORTANT: Always use standard street abbreviations: Ave (not Avenue), St (not Street), Blvd (not Boulevard), Dr (not Drive), Rd (not Road), Ln (not Lane), Ct (not Court), Pl (not Place).",
            parameters={
                "type": "OBJECT",
                "properties": {
                    "street": {
                        "type": "STRING",
                        "description": "Street name to search for using standard abbreviations (e.g., '5th Ave' not '5th Avenue', 'Broadway', 'Market St' not 'Market Street', 'Wilshire Blvd' not 'Wilshire Boulevard')"
                    },
                    "zipcode": {
                        "type": "STRING",
                        "description": "5-digit US zipcode where to search"
                    }
                },
                "required": ["street", "zipcode"]
            }
        )
    ]
)

# Map function names to actual Python functions
available_functions = {
    "get_cameras_by_zipcode": get_cameras_by_zipcode,
    "search_cameras_by_street": search_cameras_by_street
}


def execute_function_call(function_call, verbose: bool = True) -> Dict[str, Any]:
    """
    Execute the function call returned by Gemini.

    Args:
        function_call: The function call object from Gemini
        verbose: If True, print detailed logs (for CLI). If False, silent (for GUI)

    Returns:
        Dictionary with function results
    """
    function_name = function_call.name
    function_args = function_call.args

    if verbose:
        print(f"\n{'='*60}")
        print(f"🔧 FUNCTION CALL DETECTED")
        print(f"{'='*60}")
        print(f"Function: {function_name}")
        print(f"Arguments: {json.dumps(function_args, indent=2)}")
        print(f"{'='*60}\n")

    # Get the actual function
    function_to_call = available_functions.get(function_name)

    if not function_to_call:
        return {"error": f"Function {function_name} not found"}

    # Call the function with the provided arguments
    result = function_to_call(**function_args)

    if verbose:
        print(f"📊 API RESPONSE:")
        print(json.dumps(result, indent=2))
        print(f"\n{'='*60}\n")

    return result


def chat_with_gemini(user_message: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Send a message to Gemini and handle function calling.

    Args:
        user_message: The user's question
        verbose: If True, print detailed logs (for CLI). If False, silent (for GUI)

    Returns:
        Dictionary with:
            - response: The final text response from Gemini
            - function_calls: List of function calls made (with name and args)
            - error: Error message if something went wrong (optional)
    """
    if verbose:
        print(f"💬 USER: {user_message}\n")

    # Track function calls
    function_calls_made = []

    # Start with the user's message
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
    ]

    # Continue the conversation until we get a text response
    try:
        while True:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[get_cameras_tool],
                    temperature=0.7
                )
            )

            # Check if there's a function call in the response
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call

                # Track this function call
                function_calls_made.append({
                    "name": function_call.name,
                    "args": dict(function_call.args)
                })

                # Execute the function
                function_result = execute_function_call(function_call, verbose=verbose)

                # Add the model's response (with function call) to messages
                messages.append(response.candidates[0].content)

                # Add the function response
                messages.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                function_response=types.FunctionResponse(
                                    name=function_call.name,
                                    response=function_result
                                )
                            )
                        ]
                    )
                )
            else:
                # No function call, we have the final text response
                final_response = response.text

                if verbose:
                    print(f"🤖 GEMINI: {final_response}\n")

                return {
                    "response": final_response,
                    "function_calls": function_calls_made
                }

    except errors.ClientError as e:
        error_msg = str(e)

        # Check if it's a rate limit error
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            user_friendly_msg = (
                "⚠️ Rate limit exceeded! You've hit the Gemini API quota. "
                "The free tier allows 20 requests per day for gemini-2.5-flash. "
                "Please wait a few minutes and try again, or check your usage at: "
                "https://ai.dev/usage?tab=rate-limit"
            )

            if verbose:
                print(f"\n❌ {user_friendly_msg}\n")
                print(f"Technical details: {error_msg}\n")

            return {
                "error": user_friendly_msg,
                "error_details": error_msg,
                "function_calls": function_calls_made
            }
        else:
            # Other API errors
            if verbose:
                print(f"\n❌ Gemini API Error: {error_msg}\n")

            return {
                "error": f"Gemini API Error: {error_msg}",
                "function_calls": function_calls_made
            }

    except Exception as e:
        # Catch-all for unexpected errors
        error_msg = str(e)

        if verbose:
            print(f"\n❌ Unexpected Error: {error_msg}\n")

        return {
            "error": f"Unexpected error: {error_msg}",
            "function_calls": function_calls_made
        }