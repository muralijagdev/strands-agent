# ASL Q&A Agent - Quick Start Guide

Get up and running with the ASL Q&A Agent in minutes.

## Prerequisites

- Python 3.9+
- AWS Account with Bedrock AgentCore access
- Docker Desktop (for deployment)
- AWS CLI configured

## 5-Minute Setup

### 1. Install Dependencies

```bash
cd C:\GitHub\ASL

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure AWS

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your details:
# - AWS_ACCOUNT_ID
# - AWS_REGION
# - AWS_EXECUTION_ROLE_ARN
```

### 3. Update Configuration

Edit [.bedrock_agentcore.yaml](.bedrock_agentcore.yaml):

```yaml
# Line 23: Your AWS Account ID
account: '123456789012'

# Line 24: Your preferred region
region: us-east-1

# Line 17: Your IAM execution role
execution_role: arn:aws:iam::123456789012:role/YourRole

# Line 28: Your ECR repository (or set ecr_auto_create: true)
ecr_repository: 123456789012.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-asl-qa-agent
```

### 4. Deploy to AgentCore

```bash
# Configure AgentCore CLI
bedrock-agentcore configure --region us-east-1

# Launch the agent
bedrock-agentcore launch

# This will take 5-10 minutes
```

### 5. Test the Agent

```bash
# After deployment completes, get the runtime ARN
bedrock-agentcore status

# Update .env with AGENT_RUNTIME_ARN from output

# Test with IAM authentication
python src/invoke_agent_iam.py --input "How do I sign hello in ASL?"
```

## Example Usage

### Ask About Signs

```bash
python src/invoke_agent_iam.py --input "How do I sign 'thank you' in ASL?"
```

### Ask About Grammar

```bash
python src/invoke_agent_iam.py --input "What are Wh-questions in ASL?"
```

### Ask About Culture

```bash
python src/invoke_agent_iam.py --input "Tell me about Deaf culture"
```

### Ask About Learning Resources

```bash
python src/invoke_agent_iam.py --input "Where can I learn ASL online?"
```

## Local Testing (No Deployment)

```bash
# Test agents locally without deploying
python src/test_agent_local.py --question "How do I sign hello?"
```

## Project Structure

```
ASL/
├── agents/                    # Specialized agent modules
│   ├── grammar_expert.py     # ASL grammar specialist
│   ├── vocabulary_agent.py   # Signs and vocabulary
│   ├── cultural_agent.py     # Deaf culture expert
│   ├── learning_agent.py     # Learning resources
│   └── general_asl_agent.py  # General knowledge
│
├── asl_swarm_agent.py        # Main Swarm coordinator
├── .bedrock_agentcore.yaml   # AgentCore config
├── requirements.txt          # Dependencies
│
├── invoke_agent.py           # OAuth invocation
├── invoke_agent_iam.py       # IAM invocation
├── test_agent_local.py       # Local testing
│
├── README.md                 # Overview
├── ARCHITECTURE.md           # Architecture details
├── DEPLOYMENT_GUIDE.md       # Full deployment guide
└── QUICKSTART.md             # This file
```

## How It Works

1. **User asks a question** about ASL
2. **Coordinator analyzes** the question
3. **Swarm routes** to the right specialist:
   - Grammar questions → Grammar Expert
   - Sign questions → Vocabulary Agent
   - Culture questions → Cultural Agent
   - Learning questions → Learning Agent
   - General questions → General Agent
4. **Specialist responds** with expert knowledge
5. **Response returned** to user

## Common Commands

### Deployment

```bash
# Deploy/update agent
bedrock-agentcore launch

# Check status
bedrock-agentcore status

# View logs
bedrock-agentcore logs

# Delete agent
bedrock-agentcore delete
```

### Testing

```bash
# Test with IAM
python src/invoke_agent_iam.py --input "YOUR_QUESTION"

# Test with OAuth
python src/invoke_agent.py --token JWT_TOKEN --input "YOUR_QUESTION"

# Test locally
python src/test_agent_local.py --question "YOUR_QUESTION"
```

## Example Questions

Try these questions to test different agents:

**Grammar:**
- "How do I form yes/no questions in ASL?"
- "What are non-manual markers?"
- "Explain topic-comment structure"

**Vocabulary:**
- "How do I sign 'hello'?"
- "What are the ASL numbers?"
- "How do you fingerspell?"

**Culture:**
- "What is Deaf culture?"
- "Tell me about name signs"
- "What is Deaf etiquette?"

**Learning:**
- "Where can I learn ASL?"
- "What are good ASL apps?"
- "How do I practice ASL?"

**General:**
- "What is ASL?"
- "How is ASL different from English?"
- "Is ASL universal?"

## Troubleshooting

### "AccessDeniedException"
**Fix:** Check IAM permissions in your execution role

### "Repository not found"
**Fix:** Set `ecr_auto_create: true` in `.bedrock_agentcore.yaml`

### "RuntimeClientError"
**Fix:** Check CloudWatch logs: `bedrock-agentcore logs`

### Agent not responding
**Fix:** Verify deployment: `bedrock-agentcore status`

## Next Steps

1. **Read the Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Full Deployment Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. **Customize Agents:** Edit files in `agents/` directory
4. **Add Guardrails:** Update model config in `asl_swarm_agent.py`
5. **Enable OAuth:** Configure in `.bedrock_agentcore.yaml`

## Resources

- [Strands Swarm Docs](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)
- [AWS AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html)
- [ASL Learning Resources](https://www.lifeprint.com/)

## Support

Having issues? Check:
1. CloudWatch logs (`bedrock-agentcore logs`)
2. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) troubleshooting section
3. [AgentCore Implementation Guide](C:\GitHub\jenny-strands\docs\agentcore\agentcore-implementation-guide.md)

---

**Ready to go!** Deploy with `bedrock-agentcore launch` and start asking ASL questions! 🤟
