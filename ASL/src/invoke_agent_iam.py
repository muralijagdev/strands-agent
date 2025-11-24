"""
IAM (SigV4) Invocation Script for ASL Agent

This script invokes the ASL Q&A Agent using AWS IAM authentication.
Use this for background jobs and service-to-service communication.

Usage:
    python invoke_agent_iam.py --input "How do I sign hello?"
    python invoke_agent_iam.py --input "What are Wh-questions?" --session SESSION_ID
    python invoke_agent_iam.py --input "Tell me about Deaf culture" --region us-east-1
"""

import argparse
import json
import uuid
import sys
from typing import Optional
import boto3
from botocore.exceptions import ClientError


def invoke_agent_with_iam(
    agent_runtime_arn: str,
    user_input: str,
    session_id: Optional[str] = None,
    region_name: str = "us-east-1",
) -> dict:
    """
    Invoke the ASL Agent using AWS IAM (SigV4) authentication.

    Args:
        agent_runtime_arn: The AgentCore runtime ARN
        user_input: The user's question or input
        session_id: Optional session ID for conversation continuity
        region_name: AWS region (default: us-east-1)

    Returns:
        Dictionary containing the agent's response
    """

    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    print(f"Session ID: {session_id}")
    print(f"Question: {user_input}")
    print(f"Region: {region_name}")
    print("-" * 60)

    try:
        # Create Bedrock AgentCore client
        client = boto3.client("bedrock-agentcore", region_name=region_name)

        # Prepare the payload
        payload = {
            "input": user_input,
            "session_id": session_id,
        }

        # Invoke the agent
        response = client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            qualifier="DEFAULT",
            body=json.dumps(payload),
            contentType="application/json",
        )

        # Process the response
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            # Read the streaming response
            print("Response: ", end="", flush=True)

            full_response = ""
            if "body" in response:
                body = response["body"]

                # Read streaming body
                for chunk in body:
                    if "chunk" in chunk:
                        chunk_data = chunk["chunk"].get("bytes", b"")
                        chunk_text = chunk_data.decode("utf-8")
                        print(chunk_text, end="", flush=True)
                        full_response += chunk_text

            print("\n" + "-" * 60)

            return {
                "session_id": session_id,
                "response": full_response,
                "status": "success",
            }
        else:
            error_msg = f"Unexpected status code: {response['ResponseMetadata']['HTTPStatusCode']}"
            print(f"\nError: {error_msg}", file=sys.stderr)
            return {"status": "error", "error": error_msg}

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        error_msg = f"AWS Error ({error_code}): {error_message}"
        print(f"\nError: {error_msg}", file=sys.stderr)

        # Provide helpful error messages
        if error_code == "AccessDeniedException":
            print(
                "\nTip: Ensure your IAM role has the following permissions:",
                file=sys.stderr,
            )
            print("  - bedrock-agentcore:InvokeAgentRuntime", file=sys.stderr)
            print("  - bedrock:InvokeModel", file=sys.stderr)
            print(
                "  - bedrock:InvokeModelWithResponseStream", file=sys.stderr
            )

        return {"status": "error", "error": error_msg}

    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        print(f"\nError: {error_msg}", file=sys.stderr)
        return {"status": "error", "error": error_msg}


def main():
    """Main function to handle command-line invocation."""

    parser = argparse.ArgumentParser(
        description="Invoke ASL Agent with IAM (SigV4) Authentication"
    )

    parser.add_argument(
        "--arn",
        type=str,
        help="AgentCore runtime ARN",
        default=None,
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

    parser.add_argument(
        "--region",
        type=str,
        default="us-east-1",
        help="AWS region (default: us-east-1)",
    )

    args = parser.parse_args()

    # Get ARN from args or environment
    runtime_arn = args.arn
    if not runtime_arn:
        import os
        from dotenv import load_dotenv

        load_dotenv()
        runtime_arn = os.getenv("AGENT_RUNTIME_ARN")

    if not runtime_arn:
        print(
            "Error: Agent runtime ARN not provided. Use --arn or set AGENT_RUNTIME_ARN in .env",
            file=sys.stderr,
        )
        sys.exit(1)

    # Invoke the agent
    result = invoke_agent_with_iam(
        agent_runtime_arn=runtime_arn,
        user_input=args.input,
        session_id=args.session,
        region_name=args.region,
    )

    # Exit with appropriate code
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
