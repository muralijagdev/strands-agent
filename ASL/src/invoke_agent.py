"""
OAuth Bearer Token Invocation Script for ASL Agent

This script invokes the ASL Q&A Agent using OAuth bearer token authentication.
Use this for interactive user sessions where you have a JWT token.

Usage:
    python invoke_agent.py --token YOUR_JWT_TOKEN --input "How do I sign hello?"
    python invoke_agent.py --token YOUR_JWT_TOKEN --input "What are Wh-questions?" --session SESSION_ID
"""

import argparse
import json
import uuid
import requests
import sys
from typing import Optional


def invoke_agent_with_oauth(
    agent_endpoint: str,
    auth_token: str,
    user_input: str,
    session_id: Optional[str] = None,
) -> dict:
    """
    Invoke the ASL Agent using OAuth bearer token authentication.

    Args:
        agent_endpoint: The AgentCore runtime endpoint URL
        auth_token: JWT bearer token for authentication
        user_input: The user's question or input
        session_id: Optional session ID for conversation continuity

    Returns:
        Dictionary containing the agent's response
    """

    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    # Prepare the request
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": session_id,
    }

    payload = {
        "input": user_input,
        "session_id": session_id,
    }

    print(f"Session ID: {session_id}")
    print(f"Question: {user_input}")
    print("-" * 60)

    try:
        # Make the request with streaming
        response = requests.post(
            agent_endpoint,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60,
        )

        response.raise_for_status()

        # Process streaming response
        full_response = ""
        print("Response: ", end="", flush=True)

        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                print(chunk, end="", flush=True)
                full_response += chunk

        print("\n" + "-" * 60)

        return {
            "session_id": session_id,
            "response": full_response,
            "status": "success",
        }

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {e.response.status_code} - {e.response.text}"
        print(f"\nError: {error_msg}", file=sys.stderr)
        return {"status": "error", "error": error_msg}

    except requests.exceptions.RequestException as e:
        error_msg = f"Request Error: {str(e)}"
        print(f"\nError: {error_msg}", file=sys.stderr)
        return {"status": "error", "error": error_msg}

    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        print(f"\nError: {error_msg}", file=sys.stderr)
        return {"status": "error", "error": error_msg}


def main():
    """Main function to handle command-line invocation."""

    parser = argparse.ArgumentParser(
        description="Invoke ASL Agent with OAuth Bearer Token"
    )

    parser.add_argument(
        "--endpoint",
        type=str,
        help="AgentCore runtime endpoint URL",
        default=None,
    )

    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="JWT bearer token for authentication",
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Question or input for the agent",
    )

    parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="Session ID for conversation continuity (optional)",
    )

    args = parser.parse_args()

    # Get endpoint from args or environment
    endpoint = args.endpoint
    if not endpoint:
        import os
        from dotenv import load_dotenv

        load_dotenv()
        endpoint = os.getenv("AGENT_ENDPOINT_ARN")

    if not endpoint:
        print(
            "Error: Agent endpoint not provided. Use --endpoint or set AGENT_ENDPOINT_ARN in .env",
            file=sys.stderr,
        )
        sys.exit(1)

    # Invoke the agent
    result = invoke_agent_with_oauth(
        agent_endpoint=endpoint,
        auth_token=args.token,
        user_input=args.input,
        session_id=args.session,
    )

    # Exit with appropriate code
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
