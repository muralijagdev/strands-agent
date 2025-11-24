# ASL Q&A Agent - Architecture Overview

## System Architecture

The ASL Q&A Agent is built using the **Strands Swarm** agentic framework pattern, deployable to AWS Bedrock AgentCore Runtime.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     User / Application                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ OAuth JWT or IAM SigV4
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              AWS Bedrock AgentCore Runtime                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           ASL Q&A Coordinator Agent                   │  │
│  │         (asl_swarm_agent.py)                          │  │
│  │                                                         │  │
│  │  - Analyzes incoming questions                        │  │
│  │  - Routes to specialized agents via Swarm             │  │
│  │  - Coordinates responses                              │  │
│  └───────────────┬───────────────────────────────────────┘  │
│                  │                                           │
│                  │ Swarm Tool                                │
│                  ▼                                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Specialized Agent Swarm                     │  │
│  │                                                         │  │
│  │  ┌─────────────────┐  ┌─────────────────┐            │  │
│  │  │ Grammar Expert  │  │ Vocabulary Agent│            │  │
│  │  │                 │  │                 │            │  │
│  │  │ - ASL grammar   │  │ - Signs         │            │  │
│  │  │ - Syntax rules  │  │ - Fingerspelling│            │  │
│  │  │ - Questions     │  │ - Descriptions  │            │  │
│  │  │ - NMM           │  │ - Variations    │            │  │
│  │  └─────────────────┘  └─────────────────┘            │  │
│  │                                                         │  │
│  │  ┌─────────────────┐  ┌─────────────────┐            │  │
│  │  │ Cultural Agent  │  │ Learning Agent  │            │  │
│  │  │                 │  │                 │            │  │
│  │  │ - Deaf culture  │  │ - Courses       │            │  │
│  │  │ - Community     │  │ - Tutorials     │            │  │
│  │  │ - History       │  │ - Resources     │            │  │
│  │  │ - Etiquette     │  │ - Practice tips │            │  │
│  │  └─────────────────┘  └─────────────────┘            │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────┐              │  │
│  │  │      General ASL Agent              │              │  │
│  │  │                                     │              │  │
│  │  │  - Broad ASL knowledge              │              │  │
│  │  │  - Cross-domain questions           │              │  │
│  │  │  - Context bridging                 │              │  │
│  │  └─────────────────────────────────────┘              │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│                          ▼                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     Claude 3.5 Sonnet Model (Bedrock)                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              AWS Services Integration                        │
│                                                               │
│  CloudWatch Logs  │  ECR Container Registry  │  CodeBuild   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Coordinator Agent (`asl_swarm_agent.py`)

The main orchestrator that:
- Receives user questions
- Analyzes question intent and domain
- Uses the Swarm tool to route to specialized agents
- Aggregates and returns responses
- Manages session state

**Key Features:**
- Dynamic agent selection
- Context-aware routing
- Session management
- Error handling

### 2. Specialized Agents

#### Grammar Expert Agent (`agents/grammar_expert.py`)
**Domain:** ASL grammar and linguistic structure

**Expertise:**
- ASL grammar rules (topic-comment, time-topic-comment)
- Question formation (Wh-questions, yes/no questions)
- Non-manual markers (facial expressions, head movements)
- Sentence structure and word order
- Directional verbs and classifiers
- Linguistic features (phonology, morphology, syntax)

**Example Questions:**
- "How do I form Wh-questions in ASL?"
- "What are non-manual markers?"
- "Explain ASL sentence structure"

#### Vocabulary Agent (`agents/vocabulary_agent.py`)
**Domain:** ASL signs and vocabulary

**Expertise:**
- Sign descriptions (handshape, movement, location)
- Common vocabulary (greetings, numbers, colors)
- Specialized vocabulary (medical, educational)
- Regional variations
- Fingerspelling and manual alphabet
- Sign families and relationships

**Example Questions:**
- "How do I sign 'thank you'?"
- "What are the numbers in ASL?"
- "How do you fingerspell names?"

#### Cultural Agent (`agents/cultural_agent.py`)
**Domain:** Deaf culture and community

**Expertise:**
- Deaf identity and cultural values
- Community organizations and institutions
- Deaf history and heritage
- Social etiquette and norms
- Communication access rights
- Arts and expression
- Intersectional perspectives

**Example Questions:**
- "Tell me about Deaf culture"
- "What is a name sign?"
- "How do I respectfully get a Deaf person's attention?"

#### Learning Resources Agent (`agents/learning_agent.py`)
**Domain:** ASL education and learning strategies

**Expertise:**
- Online platforms and courses
- Mobile apps and tools
- Books and materials
- Practice strategies
- In-person learning opportunities
- Skill assessment
- Common learning challenges

**Example Questions:**
- "Where can I learn ASL online?"
- "What are the best ASL apps?"
- "How do I practice receptive skills?"

#### General ASL Agent (`agents/general_asl_agent.py`)
**Domain:** Broad ASL knowledge

**Expertise:**
- General ASL information
- Cross-domain topics
- ASL vs English differences
- Common misconceptions
- Getting started guidance
- Contextual bridging

**Example Questions:**
- "What is ASL?"
- "Is ASL the same as signed English?"
- "How is ASL different from other sign languages?"

## Swarm Pattern

### How Swarm Works

1. **Question Reception:** User question arrives at coordinator
2. **Analysis:** Coordinator analyzes question domain and intent
3. **Agent Selection:** Coordinator uses Swarm tool to select appropriate specialist
4. **Delegation:** Question is routed to specialized agent
5. **Processing:** Specialist agent processes and responds
6. **Handoff (if needed):** Agent can hand off to another specialist
7. **Response:** Answer is returned through coordinator to user

### Swarm Benefits

- **Expertise Specialization:** Each agent focuses on its domain
- **Dynamic Routing:** Intelligent question routing
- **Scalability:** Easy to add new specialized agents
- **Context Preservation:** Session state maintained across handoffs
- **Collaborative Problem-Solving:** Agents can work together on complex questions

### Repetitive Handoff Detection

The Swarm automatically detects "ping-pong" behavior between agents and prevents infinite loops.

## AWS AgentCore Integration

### Deployment Architecture

```
Developer → Docker Build → ECR → CodeBuild → AgentCore Runtime
                                                    ↓
                                          CloudWatch Logging
                                          Session Management
                                          IAM/OAuth Auth
```

### AgentCore Features Used

1. **Container Runtime:** Docker-based agent deployment
2. **Model Integration:** Direct access to Claude 3.5 Sonnet
3. **Authentication:** Support for IAM and OAuth
4. **Observability:** CloudWatch integration
5. **Session Management:** Built-in session persistence
6. **Streaming:** Real-time response streaming

### Network Configuration

**Public Mode:**
- Agent accessible via public endpoint
- Suitable for development and testing
- OAuth/IAM authentication required

**Private Mode (VPC):**
- Agent in private subnet
- Enhanced security
- VPC endpoint access only

## Authentication Patterns

### Option 1: IAM Authentication (Default)

**Use Case:** Background jobs, service-to-service communication

**How it Works:**
- AWS SigV4 request signing
- IAM role-based access
- No user tokens needed
- Automatic credential rotation

**Implementation:** [invoke_agent_iam.py](invoke_agent_iam.py)

### Option 2: OAuth/JWT Authentication

**Use Case:** Interactive user sessions

**How it Works:**
- JWT bearer token authentication
- OAuth 2.0 discovery
- User identity preservation
- Session continuity

**Implementation:** [invoke_agent.py](invoke_agent.py)

### Hybrid Authentication

For systems requiring both:
- Create separate endpoints for each auth type
- Or deploy separate runtimes for different use cases
- See [AgentCore Implementation Guide](C:\GitHub\jenny-strands\docs\agentcore\agentcore-implementation-guide.md) for details

## Session Management

### Session Flow

```
User Request → Session ID → Agent Context → Processing → Response
                   ↓
            Session Storage
         (File-based or S3)
```

### Session Data

- Conversation history
- User preferences
- Context state
- Agent handoff history

### Storage Options

**Development:** File-based storage
**Production:** S3-based storage for durability

## Model Configuration

### Claude 3.5 Sonnet

**Why This Model:**
- Strong reasoning capabilities
- Excellent instruction following
- Context understanding
- Nuanced response generation
- Cultural sensitivity

**Configuration:**
```python
model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    # Optional guardrails
)
```

### Guardrails (Optional)

Add content filtering and safety:
- Input validation
- Output filtering
- Topic restrictions
- PII detection

## Monitoring and Observability

### CloudWatch Integration

**Logs:**
- Agent invocations
- Swarm routing decisions
- Agent responses
- Error traces

**Metrics:**
- Invocation count
- Response latency
- Error rates
- Model usage

### Debugging

1. Check CloudWatch logs
2. Review agent routing decisions
3. Examine model responses
4. Test specialized agents individually

## Scalability Considerations

### Horizontal Scaling

- AgentCore automatically scales based on load
- Container-based deployment enables multiple instances
- Session management supports distributed architecture

### Performance Optimization

- **Model Selection:** Use appropriate Claude model for task complexity
- **Caching:** Cache common responses
- **Session Storage:** Use S3 for distributed sessions
- **Monitoring:** Track latency and optimize slow paths

## Security

### Best Practices

1. **Least Privilege IAM:** Minimal required permissions
2. **Guardrails:** Content filtering and validation
3. **Authentication:** Strong OAuth or IAM authentication
4. **Encryption:** Data encrypted in transit and at rest
5. **Audit Logging:** CloudTrail integration
6. **Network Security:** VPC isolation for production

## Future Enhancements

### Potential Additions

1. **Video Integration:** ASL video demonstration links
2. **Practice Modes:** Interactive learning exercises
3. **Regional Variants:** Expanded regional sign variations
4. **Multimodal Input:** Image-based sign recognition
5. **Community Features:** User feedback and contributions
6. **Advanced Analytics:** Learning progress tracking
7. **Personalization:** User-specific recommendations

### Additional Specialized Agents

- **Interpreter Training Agent:** Professional interpreting guidance
- **DeafBlind Communication Agent:** Tactile sign language
- **ASL Linguistics Research Agent:** Academic research support
- **Child Development Agent:** ASL for children and families

## Testing Strategy

### Local Testing
- [test_agent_local.py](test_agent_local.py) for development
- Unit tests for individual agents
- Integration tests for Swarm coordination

### Staging Testing
- Deploy to staging AgentCore environment
- Test authentication flows
- Validate session management
- Performance benchmarking

### Production Testing
- A/B testing for agent improvements
- User feedback collection
- Monitoring and alerting
- Continuous improvement

## References

### Documentation
- [README.md](README.md) - Project overview
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Step-by-step deployment
- [AgentCore Implementation Guide](C:\GitHub\jenny-strands\docs\agentcore\agentcore-implementation-guide.md) - Detailed AgentCore patterns

### External Resources
- [Strands Swarm Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html)
- [Claude 3.5 Sonnet](https://www.anthropic.com/claude)

### ASL Resources
- [Lifeprint](https://www.lifeprint.com/)
- [HandSpeak](https://www.handspeak.com/)
- [Start ASL](https://www.startasl.com/)
