# ASL Q&A Agent - Strands Swarm Implementation

An intelligent American Sign Language (ASL) question-answering system built with Strands Swarm agentic framework, deployable to AWS AgentCore.

## Overview

This project implements a multi-agent system specialized in answering questions about American Sign Language (ASL). The agent uses the Swarm pattern to coordinate between specialized sub-agents, each focusing on different aspects of ASL knowledge.

## Architecture

### Specialized Agents

1. **Grammar Expert Agent** - Handles ASL grammar, syntax, and linguistic structure
2. **Vocabulary Agent** - Answers questions about signs, meanings, and translations
3. **Cultural Agent** - Provides information about Deaf culture and community
4. **Learning Resources Agent** - Recommends tutorials, courses, and practice materials
5. **General ASL Agent** - Handles general queries and coordinates responses

### Swarm Coordination

The main coordinator uses Strands Swarm to dynamically route questions to the most appropriate specialized agent, enabling efficient and accurate responses.

## Project Structure

```
ASL/
├── agents/
│   ├── __init__.py
│   ├── grammar_expert.py      # ASL grammar and syntax agent
│   ├── vocabulary_agent.py    # Signs and vocabulary agent
│   ├── cultural_agent.py      # Deaf culture expert
│   ├── learning_agent.py      # Learning resources agent
│   └── general_asl_agent.py   # General ASL knowledge
├── asl_swarm_agent.py         # Main Swarm coordinator
├── .bedrock_agentcore.yaml    # AgentCore deployment config
├── requirements.txt           # Python dependencies
├── invoke_agent.py            # OAuth invocation script
├── invoke_agent_iam.py        # IAM invocation script
└── README.md                  # This file
```

## Setup

### Prerequisites

- Python 3.9+
- AWS Account with Bedrock AgentCore access
- Docker Desktop (for deployment)
- AWS CLI configured

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Deployment to AWS AgentCore

### Step 1: Configure AgentCore

```bash
# Configure for your target region
bedrock-agentcore configure --region us-east-1
```

### Step 2: Deploy the Agent

```bash
# Launch the agent runtime
bedrock-agentcore launch
```

### Step 3: Check Status

```bash
# Monitor deployment
bedrock-agentcore status
```

## Usage

### Local Testing

```python
from src.asl_swarm_agent import create_asl_swarm_agent

# Create the agent
agent = create_asl_swarm_agent()

# Ask a question
response = agent.run("How do I sign 'thank you' in ASL?")
print(response)
```

### OAuth Invocation (User Sessions)

```bash
python src/invoke_agent.py --token YOUR_JWT_TOKEN --input "What are Wh-questions in ASL?"
```

### IAM Invocation (Background Jobs)

```bash
python src/invoke_agent_iam.py --input "Explain ASL facial expressions"
```

## Example Questions

- "How do I sign 'hello' in ASL?"
- "What are the grammar rules for ASL questions?"
- "Tell me about Deaf culture"
- "Where can I learn ASL online?"
- "How are yes/no questions different in ASL?"
- "What are non-manual markers in ASL?"

## AgentCore Configuration

The [.bedrock_agentcore.yaml](.bedrock_agentcore.yaml) file contains:

- Agent runtime configuration
- Model selection (Claude 3.5 Sonnet)
- IAM roles and permissions
- Network and observability settings
- Authentication configuration (OAuth/IAM)

## Authentication Options

### OAuth (User Sessions)
- For interactive user queries
- Requires JWT bearer token
- Configured via `customJWTAuthorizer`

### IAM (Background Jobs)
- For automated processes
- Uses AWS SigV4 authentication
- Configured via separate endpoint

## Monitoring

- CloudWatch logs for agent interactions
- Observability enabled in AgentCore configuration
- Session tracking and telemetry

## Resources

### ASL Learning Resources
- [Lifeprint ASL](https://www.lifeprint.com/)
- [HandSpeak ASL Dictionary](https://www.handspeak.com/)
- [Start ASL](https://www.startasl.com/)
- [Able Lingo ASL](https://learn.ablelingo.com/)

### Strands Framework
- [Strands Agents Documentation](https://strandsagents.com/latest/)
- [Swarm Pattern Guide](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)

### AWS Documentation
- [Bedrock AgentCore Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html)
- [Strands Agents on AWS](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/)

## License

MIT License

## Support

For issues or questions, please refer to:
- Strands Agents documentation
- AWS Bedrock AgentCore support
- ASL learning community resources
