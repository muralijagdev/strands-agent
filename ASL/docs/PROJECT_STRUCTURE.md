# ASL Q&A Agent - Project Structure

## Directory Layout

```
ASL/
├── src/                              # Source code directory
│   ├── __init__.py                   # Package initialization
│   │
│   ├── agents/                       # Specialized agent modules
│   │   ├── __init__.py              # Agents package init
│   │   ├── grammar_expert.py        # ASL grammar and linguistics specialist
│   │   ├── vocabulary_agent.py      # Signs, vocabulary, and fingerspelling
│   │   ├── cultural_agent.py        # Deaf culture and community expert
│   │   ├── learning_agent.py        # Learning resources and strategies
│   │   └── general_asl_agent.py     # General ASL knowledge coordinator
│   │
│   ├── asl_swarm_agent.py           # Main Swarm coordinator (AgentCore entrypoint)
│   ├── invoke_agent.py              # OAuth/JWT bearer token invocation script
│   ├── invoke_agent_iam.py          # IAM SigV4 authentication invocation script
│   └── test_agent_local.py          # Local testing utility (no deployment needed)
│
├── .bedrock_agentcore.yaml          # AWS AgentCore deployment configuration
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
│
└── Documentation/
    ├── README.md                     # Project overview and introduction
    ├── QUICKSTART.md                 # 5-minute setup guide
    ├── DEPLOYMENT_GUIDE.md           # Complete deployment walkthrough
    ├── ARCHITECTURE.md               # Technical architecture and design
    ├── HOW_SWARM_WORKS.md            # Swarm pattern explanation
    └── PROJECT_STRUCTURE.md          # This file
```

## File Descriptions

### Source Code (`src/`)

#### Main Application

**[src/asl_swarm_agent.py](src/asl_swarm_agent.py)**
- Main coordinator agent using Strands Swarm pattern
- AgentCore entrypoint decorated with `@app.entrypoint`
- Creates and orchestrates specialized agents
- Handles routing logic and agent handoffs
- ~245 lines

#### Specialized Agents (`src/agents/`)

**[src/agents/grammar_expert.py](src/agents/grammar_expert.py)**
- ASL grammar rules and syntax
- Question formation (Wh-questions, yes/no)
- Non-manual markers (NMM)
- Sentence structure patterns
- ~72 lines

**[src/agents/vocabulary_agent.py](src/agents/vocabulary_agent.py)**
- Sign descriptions (handshape, movement, location)
- Fingerspelling and manual alphabet
- Regional variations
- Common and specialized vocabulary
- ~85 lines

**[src/agents/cultural_agent.py](src/agents/cultural_agent.py)**
- Deaf culture and identity
- Community organizations
- History and heritage
- Social etiquette and norms
- ~102 lines

**[src/agents/learning_agent.py](src/agents/learning_agent.py)**
- Online platforms and courses
- Learning strategies and practice tips
- Mobile apps and resources
- Skill assessment guidance
- ~128 lines

**[src/agents/general_asl_agent.py](src/agents/general_asl_agent.py)**
- Broad ASL knowledge
- Cross-domain questions
- General misconceptions
- Getting started guidance
- ~78 lines

#### Testing and Invocation Scripts

**[src/invoke_agent.py](src/invoke_agent.py)**
- OAuth/JWT bearer token authentication
- For interactive user sessions
- Streaming response support
- Command-line interface
- ~120 lines

**[src/invoke_agent_iam.py](src/invoke_agent_iam.py)**
- AWS IAM SigV4 authentication
- For background jobs and service-to-service
- boto3 client integration
- Error handling with helpful messages
- ~140 lines

**[src/test_agent_local.py](src/test_agent_local.py)**
- Local testing without deployment
- Validates Swarm configuration
- Tests agent coordination
- No AWS deployment required
- ~80 lines

### Configuration Files

**[.bedrock_agentcore.yaml](.bedrock_agentcore.yaml)**
- AgentCore runtime configuration
- AWS account and region settings
- IAM execution role ARN
- ECR repository configuration
- Network and observability settings
- Authentication configuration (OAuth/IAM)

**[.env.example](.env.example)**
- Template for environment variables
- AWS credentials and configuration
- Agent runtime ARNs
- OAuth settings (if used)

**[requirements.txt](requirements.txt)**
- Python package dependencies
- Strands agents framework
- AWS Bedrock AgentCore SDK
- boto3 and supporting libraries

**[.gitignore](.gitignore)**
- Python bytecode and cache
- Virtual environments
- Environment variables (.env)
- Session storage
- IDE files

### Documentation

**[README.md](README.md)**
- Project overview
- Architecture diagram
- Quick usage examples
- Resource links

**[QUICKSTART.md](QUICKSTART.md)**
- 5-minute setup guide
- Essential commands
- Quick examples
- Common troubleshooting

**[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**
- Step-by-step deployment
- Prerequisites and setup
- IAM configuration
- Authentication options
- Monitoring and debugging
- Production considerations

**[ARCHITECTURE.md](ARCHITECTURE.md)**
- Detailed system architecture
- Component descriptions
- Swarm pattern implementation
- AWS integration details
- Scalability and security

**[HOW_SWARM_WORKS.md](HOW_SWARM_WORKS.md)**
- Swarm pattern explanation
- Agent availability mechanism
- Handoff flow examples
- Configuration parameters
- Visual diagrams

**[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**
- This file
- Directory layout
- File descriptions
- Line counts and purposes

## Import Structure

### Agent Imports
```python
# In src/asl_swarm_agent.py
from src.agents import (
    create_grammar_expert,
    create_vocabulary_agent,
    create_cultural_agent,
    create_learning_agent,
    create_general_asl_agent,
)
```

### Framework Imports
```python
# Strands framework
from strands import Agent
from strands.multiagent import Swarm

# AWS AgentCore
from bedrock_agentcore.runtime import BedrockAgentCoreApp, RequestContext
from bedrock_agentcore.models import BedrockModel
```

## Entry Points

### AgentCore Deployment
- **Entrypoint**: `src/asl_swarm_agent.py`
- **Function**: `agent_invocation(request: RequestContext)`
- **Decorator**: `@app.entrypoint`

### Local Testing
```bash
python src/test_agent_local.py --question "YOUR_QUESTION"
```

### OAuth Invocation
```bash
python src/invoke_agent.py --token JWT_TOKEN --input "YOUR_QUESTION"
```

### IAM Invocation
```bash
python src/invoke_agent_iam.py --input "YOUR_QUESTION"
```

## Dependencies

### Core Framework
- `strands>=1.0.0` - Agent framework and Swarm
- `bedrock-agentcore>=1.0.0` - AWS AgentCore SDK

### AWS Integration
- `boto3>=1.34.0` - AWS SDK
- `botocore>=1.34.0` - AWS core library

### Utilities
- `requests>=2.31.0` - HTTP client
- `pydantic>=2.5.0` - Data validation
- `python-dotenv>=1.0.0` - Environment management

## File Sizes

- **Total Source Code**: ~900 lines
- **Documentation**: ~2,500 lines
- **Configuration**: ~150 lines

## Development Workflow

1. **Edit agents**: Modify files in `src/agents/`
2. **Test locally**: Run `src/test_agent_local.py`
3. **Update coordinator**: Modify `src/asl_swarm_agent.py`
4. **Deploy**: Run `bedrock-agentcore launch`
5. **Test deployment**: Use invoke scripts

## Production Deployment

1. Source code in `src/` is containerized
2. Docker image built via AWS CodeBuild
3. Image pushed to ECR
4. AgentCore runtime pulls and runs image
5. Entrypoint: `src/asl_swarm_agent.py:agent_invocation`

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for setup
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for design
- Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) to deploy
- Understand [HOW_SWARM_WORKS.md](HOW_SWARM_WORKS.md) for patterns
