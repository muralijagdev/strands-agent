"""
Local Testing Script for ASL Swarm Agent

Tests the agent locally without deploying to AgentCore.
Useful for development and debugging.

Usage:
    python test_agent_local.py
    python test_agent_local.py --question "How do I sign thank you?"
"""

import argparse
import asyncio
from asl_swarm_agent import create_asl_swarm_configuration


async def test_agent_locally(question: str):
    """
    Test the ASL agent locally.

    Args:
        question: The question to ask the agent
    """

    print("=" * 80)
    print("ASL Swarm Agent - Local Testing")
    print("=" * 80)

    # Create the swarm configuration
    config = create_asl_swarm_configuration()

    print(f"\nCoordinator: {config['coordinator'].name}")
    print(f"Specialized Agents: {len(config['specialized_agents'])}")

    for agent_name, agent in config["specialized_agents"].items():
        print(f"  - {agent.name}")

    print("\n" + "-" * 80)
    print(f"Question: {question}")
    print("-" * 80)

    # Get the coordinator
    coordinator = config["coordinator"]

    try:
        # Run the coordinator with the question
        # The coordinator will use the swarm tool to delegate to specialized agents
        print("\nProcessing...")

        response = await coordinator.run_async(question)

        print("\nResponse:")
        print("-" * 80)
        print(response)
        print("-" * 80)

        return response

    except Exception as e:
        print(f"\nError during local testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def main():
    """Main function for local testing."""

    parser = argparse.ArgumentParser(description="Test ASL Agent Locally")

    parser.add_argument(
        "--question",
        type=str,
        default="How do I sign 'thank you' in ASL?",
        help="Question to ask the agent",
    )

    args = parser.parse_args()

    # Run the async test
    asyncio.run(test_agent_locally(args.question))


if __name__ == "__main__":
    # Example test questions
    example_questions = [
        "How do I sign 'thank you' in ASL?",
        "What are Wh-questions in ASL?",
        "Tell me about Deaf culture",
        "Where can I learn ASL online?",
        "What is the difference between ASL and English?",
        "How do you form yes/no questions in ASL?",
        "What are non-manual markers?",
        "What is a name sign?",
    ]

    print("\nExample questions you can test:")
    for i, q in enumerate(example_questions, 1):
        print(f"{i}. {q}")

    print("\n")

    main()
