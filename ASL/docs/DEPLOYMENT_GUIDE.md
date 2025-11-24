# ASL Agent Deployment Guide

Step-by-step guide to deploy the ASL Q&A Agent to AWS Bedrock AgentCore.

## Prerequisites

### 1. AWS Account Setup

- AWS Account with access to Bedrock AgentCore
- IAM user with appropriate permissions
- AWS CLI installed and configured

### 2. Local Development Environment

- Python 3.9 or higher
- Docker Desktop installed and running
- Git for version control

### 3. Required AWS Permissions

Your IAM user/role needs:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock-agentcore:*",
        "ecr:*",
        "codebuild:*",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

## Step 1: Initial Setup

### Clone and Setup Project

```bash
# Navigate to project directory
cd C:\GitHub\ASL

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your AWS details
# Update:
# - AWS_ACCOUNT_ID
# - AWS_REGION
# - AWS_EXECUTION_ROLE_ARN
```

## Step 2: Configure AgentCore

### Update .bedrock_agentcore.yaml

Edit [.bedrock_agentcore.yaml](.bedrock_agentcore.yaml) and update:

1. **Account ID** (line 23):
   ```yaml
   account: 'YOUR_ACCOUNT_ID'
   ```

2. **Region** (line 24):
   ```yaml
   region: us-east-1  # Change to your preferred region
   ```

3. **Execution Role** (line 17):
   ```yaml
   execution_role: arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_AGENTCORE_ROLE
   ```

4. **ECR Repository** (line 28):
   ```yaml
   ecr_repository: YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-asl-qa-agent
   ```

   Or set `ecr_auto_create: true` to automatically create the repository.

### Configure AgentCore CLI

```bash
# Configure for your target region
bedrock-agentcore configure --region us-east-1
```

## Step 3: Create IAM Execution Role

### Option A: Manual Creation

1. Go to AWS Console > IAM > Roles
2. Create new role with these policies:

**Trust Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock-agentcore.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Permissions Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:/aws/bedrock-agentcore/*"
    }
  ]
}
```

### Option B: Auto-Creation

Set in [.bedrock_agentcore.yaml](.bedrock_agentcore.yaml):
```yaml
execution_role_auto_create: true
```

## Step 4: Create ECR Repository (Optional)

If not using `ecr_auto_create: true`:

```bash
# Create ECR repository
aws ecr create-repository \
  --repository-name bedrock-agentcore-asl-qa-agent \
  --region us-east-1

# Note the repository URI from the output
```

## Step 5: Deploy to AgentCore

### Launch the Agent

```bash
# From the project directory
bedrock-agentcore launch

# This will:
# 1. Build Docker container
# 2. Push to ECR
# 3. Create AgentCore runtime
# 4. Deploy the agent
```

### Monitor Deployment

```bash
# Check deployment status
bedrock-agentcore status

# View logs
bedrock-agentcore logs

# Get agent details
bedrock-agentcore describe
```

## Step 6: Configure Authentication

### Option A: IAM Authentication (Default)

No additional configuration needed. Use [invoke_agent_iam.py](invoke_agent_iam.py) for invocation.

### Option B: OAuth/JWT Authentication

1. Update [.bedrock_agentcore.yaml](.bedrock_agentcore.yaml):

```yaml
auth:
  customJWTAuthorizer:
    discoveryUrl: "https://your-idp.com/.well-known/openid-configuration"
    allowedAudiences:
      - "your-audience"
    allowedClients:
      - "your-client-id"
```

2. Redeploy:
```bash
bedrock-agentcore launch
```

3. Use [invoke_agent.py](invoke_agent.py) with JWT token for invocation.

## Step 7: Test the Deployment

### Get Agent Details

After deployment, note the values from:

```bash
bedrock-agentcore status
```

Update your `.env` file with:
- `AGENT_RUNTIME_ARN`
- `AGENT_ENDPOINT_ARN`
- `AGENT_ID`

### Test with IAM Authentication

```bash
python src/invoke_agent_iam.py --input "How do I sign hello in ASL?"
```

### Test with OAuth Authentication

```bash
python src/invoke_agent.py --token YOUR_JWT_TOKEN --input "What are Wh-questions in ASL?"
```

## Step 8: Monitor and Debug

### View CloudWatch Logs

1. Go to AWS Console > CloudWatch > Log Groups
2. Find `/aws/bedrock-agentcore/asl-qa-agent`
3. View recent log streams

### Check Agent Status

```bash
# Detailed status
bedrock-agentcore status --verbose

# View logs in real-time
bedrock-agentcore logs --follow
```

### Common Issues

**Issue: "AccessDeniedException"**
- Check IAM role permissions
- Ensure Bedrock model access is granted
- Verify role trust relationship

**Issue: "RuntimeClientError"**
- Check CloudWatch logs for details
- Verify Docker container built successfully
- Check agent entrypoint file exists

**Issue: "Repository not found"**
- Create ECR repository manually
- Or set `ecr_auto_create: true`

## Step 9: Update and Redeploy

### Update Agent Code

```bash
# Make changes to agents or main file
# Then redeploy
bedrock-agentcore launch

# This creates a new version
```

### Rollback to Previous Version

```bash
bedrock-agentcore rollback --version PREVIOUS_VERSION
```

## Step 10: Production Considerations

### Enable Guardrails

Update [asl_swarm_agent.py](asl_swarm_agent.py):

```python
model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    guardrail_id="your-guardrail-id",
    guardrail_version="1",
    guardrail_trace="enabled",
)
```

### Configure VPC (Private Network)

Update [.bedrock_agentcore.yaml](.bedrock_agentcore.yaml):

```yaml
network_configuration:
  network_mode: PRIVATE
  vpc_config:
    subnet_ids:
      - subnet-xxxxx
      - subnet-yyyyy
    security_group_ids:
      - sg-xxxxx
```

### Set Up Alarms

Create CloudWatch alarms for:
- Error rates
- Response latency
- Invocation count
- Model throttling

### Enable Session Storage

For production, consider S3 session storage:

```python
from strands.session.s3_session_manager import S3SessionManager

session_manager = S3SessionManager(
    session_id=session_id,
    bucket="your-session-bucket",
    prefix="sessions/",
    region_name=region_name
)
```

## Cleanup

### Delete Agent Runtime

```bash
bedrock-agentcore delete

# Confirm deletion when prompted
```

### Delete ECR Repository

```bash
aws ecr delete-repository \
  --repository-name bedrock-agentcore-asl-qa-agent \
  --region us-east-1 \
  --force
```

## Additional Resources

- [AgentCore Implementation Guide](C:\GitHub\jenny-strands\docs\agentcore\agentcore-implementation-guide.md)
- [Strands Swarm Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)

## Support

For issues:
1. Check CloudWatch logs
2. Review [README.md](README.md) for architecture details
3. Consult AWS Bedrock AgentCore documentation
4. Review jenny-strands implementation guide for troubleshooting tips
