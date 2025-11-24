"""
ASL Swarm Agent - Main Coordinator

This module implements the main Swarm coordinator for the ASL Q&A system.
It uses the Strands Swarm pattern to dynamically route questions to specialized agents.

Deployable to AWS Bedrock AgentCore Runtime.
"""

import uuid
import os
from typing import Optional
from bedrock_agentcore.runtime import BedrockAgentCoreApp, RequestContext
from bedrock_agentcore.models import BedrockModel
from strands import Agent  # Strands Agent
from strands.multiagent import Swarm  # Swarm for multi-agent coordination

# Import specialized agents
from src.agents import (
    create_grammar_expert,
    create_vocabulary_agent,
    create_cultural_agent,
    create_learning_agent,
    create_general_asl_agent,
)


# Model configuration
model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    # Optional: Add guardrails if needed
    # guardrail_id="your-guardrail-id",
    # guardrail_version="1",
    # guardrail_trace="enabled",
)


def create_asl_coordinator_agent() -> Agent:
    """
    Creates the main coordinator agent that uses Swarm to route questions.

    Returns:
        Agent configured as the Swarm coordinator
    """

    system_prompt = """You are the ASL Q&A Coordinator Agent. Your role is to analyze incoming questions
about American Sign Language and route them to the most appropriate specialized agent.

You have access to a swarm of specialized agents:

1. **Grammar Expert Agent** - For questions about:
   - ASL grammar rules and syntax
   - Sentence structure (topic-comment, time-topic-comment)
   - Question formation (Wh-questions, yes/no questions)
   - Non-manual markers in grammar
   - Linguistic features and patterns
   - Directional verbs and agreement
   - Classifiers

2. **Vocabulary Agent** - For questions about:
   - How to sign specific words or phrases
   - Sign descriptions and formations
   - Fingerspelling
   - Numbers, colors, common vocabulary
   - Sign variations and regional differences
   - Handshapes, movements, locations

3. **Cultural Agent** - For questions about:
   - Deaf culture and community
   - Deaf identity and perspectives
   - Social etiquette and norms
   - Deaf history and heritage
   - Communication access and rights
   - Deaf arts and expression
   - Cultural values

4. **Learning Resources Agent** - For questions about:
   - Where to learn ASL
   - Online courses and tutorials
   - Books and apps
   - Practice strategies
   - Learning challenges and tips
   - Skill assessment
   - Educational programs

5. **General ASL Agent** - For broad questions about:
   - What is ASL
   - ASL vs other sign languages
   - ASL vs English differences
   - Getting started with ASL
   - General misconceptions
   - Overview topics

**Your Process**:

1. Analyze the user's question carefully
2. Determine which specialized agent is best suited to answer
3. Use the swarm tool to delegate to that agent
4. If the question spans multiple domains, start with the most relevant agent
5. The swarm agents can hand off to each other if needed

**Guidelines**:

- Route grammar and linguistic questions to Grammar Expert
- Route "how do I sign..." questions to Vocabulary Agent
- Route culture and etiquette questions to Cultural Agent
- Route learning and resource questions to Learning Resources Agent
- Route broad or general questions to General ASL Agent
- For complex questions, let the initial agent handle it - they can request help from others if needed

When you determine which specialist is needed, you can hand off to them by indicating their name and role.
The Swarm will automatically route the question to that specialist."""

    # Create the coordinator agent
    # Note: When used in a Swarm, the coordinator doesn't need the swarm tool
    # The Swarm itself handles agent coordination and handoffs
    coordinator = Agent(
        name="ASL Q&A Coordinator",
        description="Main coordinator that routes ASL questions to specialized agents using Swarm pattern",
        instructions=system_prompt,
        model=model.model_id,
    )

    return coordinator


def create_asl_swarm_configuration() -> dict:
    """
    Creates the configuration for the ASL Swarm including all specialized agents.

    Returns:
        Dictionary containing the swarm configuration
    """

    swarm_config = {
        "coordinator": create_asl_coordinator_agent(),
        "specialized_agents": {
            "grammar_expert": create_grammar_expert(),
            "vocabulary_agent": create_vocabulary_agent(),
            "cultural_agent": create_cultural_agent(),
            "learning_agent": create_learning_agent(),
            "general_asl_agent": create_general_asl_agent(),
        },
    }

    return swarm_config


# AgentCore Application Setup
app = BedrockAgentCoreApp()


@app.entrypoint
async def agent_invocation(request: RequestContext):
    """
    Main entrypoint for AgentCore Runtime.

    This function is called when the agent is invoked via AgentCore.
    It handles the request, creates the Swarm, and returns streaming responses.

    Args:
        request: RequestContext containing input, session_id, and other metadata

    Returns:
        Streaming response from the agent
    """

    # Extract session and user information
    session_id = request.session_id or str(uuid.uuid4())
    user_id = getattr(request, "user_id", "anonymous")

    # Parse input - handle both string and dict formats
    if isinstance(request.input, dict):
        user_message = request.input.get("input", request.input.get("prompt", ""))
    elif isinstance(request.input, str):
        user_message = request.input
    else:
        user_message = str(request.input)

    # Create the coordinator agent
    coordinator = create_asl_coordinator_agent()

    # Create all specialized agents
    grammar_expert = create_grammar_expert()
    vocabulary_agent = create_vocabulary_agent()
    cultural_agent = create_cultural_agent()
    learning_agent = create_learning_agent()
    general_asl_agent = create_general_asl_agent()

    # Create the Swarm with all agents
    # The coordinator is the entry point, and it can hand off to any specialist
    asl_swarm = Swarm(
        agents=[
            coordinator,
            grammar_expert,
            vocabulary_agent,
            cultural_agent,
            learning_agent,
            general_asl_agent,
        ],
        entry_point=coordinator,  # Start with the coordinator
        max_handoffs=20,  # Allow up to 20 agent handoffs
        max_iterations=20,  # Maximum iterations for the swarm
        repetitive_handoff_detection_window=8,  # Detect ping-pong behavior
        repetitive_handoff_min_unique_agents=3,  # Require 3 unique agents to avoid loops
    )

    try:
        # Run the swarm with the user's question
        # The coordinator will analyze and route to appropriate specialists
        # Specialists can hand off to each other if needed
        response = await asl_swarm.run_async(
            user_message,
            session_id=session_id,
        )

        # Return the response
        return response

    except Exception as e:
        error_message = f"Error processing ASL question: {str(e)}"
        print(error_message)
        return {"error": error_message}


# For local testing
if __name__ == "__main__":
    print("ASL Swarm Agent - Local Testing Mode")
    print("=" * 60)

    # Create test configuration
    config = create_asl_swarm_configuration()

    print("\nSwarm Configuration:")
    print(f"- Coordinator: {config['coordinator'].name}")
    print(f"- Specialized Agents: {len(config['specialized_agents'])}")

    for agent_name, agent in config["specialized_agents"].items():
        print(f"  - {agent_name}: {agent.name}")

    print("\n" + "=" * 60)
    print("\nExample questions to test:")
    print('- "How do I sign thank you in ASL?"')
    print('- "What are Wh-questions in ASL?"')
    print('- "Tell me about Deaf culture"')
    print('- "Where can I learn ASL online?"')
    print('- "What is the difference between ASL and English?"')
    print("\nTo test locally, integrate with Strands framework testing utilities.")
    print("To deploy to AgentCore, use: bedrock-agentcore launch")
