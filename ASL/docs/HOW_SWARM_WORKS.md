# How Swarm Makes Agents Available - Explained

## Your Question

> "How are these specialized agents available for swarm?"

Great question! Let me explain how the Swarm pattern works in Strands and how the specialized agents become available to the coordinator.

## The Answer: Explicit Agent Registration

The specialized agents are made available to the Swarm through **explicit registration** in the `Swarm` object. Here's how it works:

### Step 1: Create Individual Agents

```python
# Create the coordinator
coordinator = create_asl_coordinator_agent()

# Create all specialized agents
grammar_expert = create_grammar_expert()
vocabulary_agent = create_vocabulary_agent()
cultural_agent = create_cultural_agent()
learning_agent = create_learning_agent()
general_asl_agent = create_general_asl_agent()
```

### Step 2: Register Agents in the Swarm

```python
# Create the Swarm with ALL agents explicitly listed
asl_swarm = Swarm(
    agents=[
        coordinator,        # Entry point agent
        grammar_expert,     # These agents are now "available"
        vocabulary_agent,   # to the coordinator and each other
        cultural_agent,
        learning_agent,
        general_asl_agent,
    ],
    entry_point=coordinator,  # Start here
)
```

### Step 3: Run the Swarm

```python
# When you run the swarm, the coordinator has access to all registered agents
response = await asl_swarm.run_async(user_message, session_id=session_id)
```

## How Agent Handoffs Work

### 1. Initial Routing

```
User: "How do I sign 'thank you'?"
  ↓
Coordinator analyzes the question
  ↓
Coordinator determines: This is a vocabulary question
  ↓
Coordinator hands off to vocabulary_agent
  ↓
Vocabulary agent responds with sign description
```

### 2. Cross-Agent Handoffs

```
User: "What are the grammar rules for signing 'thank you'?"
  ↓
Coordinator → Vocabulary Agent (for the sign)
  ↓
Vocabulary Agent → Grammar Expert (for the rules)
  ↓
Grammar Expert responds with grammatical context
```

### 3. Swarm Coordination Features

The `Swarm` object provides:

- **Agent Registry**: All agents in the list are "known" to each other
- **Handoff Detection**: Prevents infinite loops (ping-pong behavior)
- **Context Preservation**: Maintains conversation state across handoffs
- **Max Iterations**: Safety limits to prevent runaway processing

## Two Ways to Use Swarm

### Method 1: Explicit Swarm (What We Use)

**Advantages:**
- Full control over which agents are available
- Clear agent relationships
- Better for production deployments
- Predictable behavior

```python
swarm = Swarm(
    agents=[agent1, agent2, agent3],
    entry_point=coordinator,
    max_handoffs=20
)
result = await swarm.run_async("question")
```

### Method 2: Swarm as a Tool (Alternative)

**Advantages:**
- More dynamic and flexible
- Agent creates specialists on-demand
- Good for exploratory tasks

```python
from strands_tools import swarm

coordinator = Agent(
    tools=[swarm],  # Agent can create specialists dynamically
    instructions="Use swarm to create specialists as needed"
)
```

In this approach, the coordinator's LLM (Claude) describes what specialists it needs, and the swarm tool creates them automatically.

## Key Configuration Parameters

### In Our Implementation

```python
asl_swarm = Swarm(
    agents=[...],                              # All available agents
    entry_point=coordinator,                   # Starting agent
    max_handoffs=20,                          # Max agent-to-agent handoffs
    max_iterations=20,                        # Max processing iterations
    repetitive_handoff_detection_window=8,    # Look back 8 handoffs
    repetitive_handoff_min_unique_agents=3,   # Need 3 unique agents
)
```

### What These Mean

- **max_handoffs**: If agents pass the question around more than 20 times, stop
- **max_iterations**: Maximum processing cycles before timeout
- **repetitive_handoff_detection_window**: Looks at last 8 handoffs to detect loops
- **repetitive_handoff_min_unique_agents**: If fewer than 3 unique agents in the window, it's a loop

## Example Flow in Our ASL Agent

### Example 1: Simple Vocabulary Question

```
Input: "How do I sign 'hello'?"

Flow:
1. asl_swarm.run_async() → starts at coordinator
2. Coordinator analyzes: "This is a vocabulary question"
3. Coordinator → vocabulary_agent
4. Vocabulary agent provides sign description
5. Response returned to user

Handoffs: 1 (coordinator → vocabulary_agent)
Agents used: 2 (coordinator, vocabulary_agent)
```

### Example 2: Complex Multi-Domain Question

```
Input: "How do I sign 'thank you' and what's the cultural significance?"

Flow:
1. asl_swarm.run_async() → starts at coordinator
2. Coordinator analyzes: "This needs vocabulary AND culture"
3. Coordinator → vocabulary_agent
4. Vocabulary agent provides sign description
5. Vocabulary agent → cultural_agent (recognizes cultural aspect)
6. Cultural agent adds cultural context
7. Combined response returned to user

Handoffs: 3 (coordinator → vocabulary → cultural)
Agents used: 3 (coordinator, vocabulary_agent, cultural_agent)
```

### Example 3: Loop Prevention

```
Input: "Tell me about ASL"

Bad scenario without loop detection:
1. Coordinator → general_asl_agent
2. General agent → grammar_expert
3. Grammar expert → general_asl_agent (thinks it needs broader context)
4. General agent → grammar_expert (thinks it needs specifics)
5. Repeat forever...

With loop detection:
1-4. Same as above
5. Swarm detects: Last 8 handoffs only use 2 agents (< 3 required)
6. Swarm stops and returns best available answer
```

## Visual Architecture

```
┌─────────────────────────────────────────┐
│         Swarm Object                    │
│  ┌───────────────────────────────────┐  │
│  │  Agent Registry                   │  │
│  │  • coordinator ✓                  │  │
│  │  • grammar_expert ✓               │  │
│  │  • vocabulary_agent ✓             │  │
│  │  • cultural_agent ✓               │  │
│  │  • learning_agent ✓               │  │
│  │  • general_asl_agent ✓            │  │
│  └───────────────────────────────────┘  │
│                                          │
│  Entry Point: coordinator                │
│  Max Handoffs: 20                        │
│  Loop Detection: Enabled                 │
└─────────────────────────────────────────┘
           ↓
    User Question
           ↓
  Coordinator analyzes
           ↓
   Routes to specialist ───→ Can hand off to another
           ↓                        ↓
     Returns response ←─────────────┘
```

## Why This Approach?

### Benefits of Explicit Agent Registration

1. **Predictable**: You know exactly which agents are available
2. **Efficient**: No overhead of dynamic agent creation
3. **Debuggable**: Clear agent relationships in logs
4. **Production-Ready**: Stable and well-defined behavior
5. **Cost-Effective**: Agents are created once, not per-request

### When to Use Dynamic Swarm Tool Instead

- Exploratory research tasks
- Unknown requirements upfront
- Highly variable specialist needs
- Prototyping and experimentation

## Code Location Reference

The complete Swarm setup is in [src/asl_swarm_agent.py](src/asl_swarm_agent.py):

- **Lines 180-187**: Create all specialist agents
- **Lines 189-205**: Register agents in Swarm with configuration
- **Lines 207-214**: Run the swarm with user input

Each specialist agent is defined in the `src/agents/` directory:
- [src/agents/grammar_expert.py](src/agents/grammar_expert.py) - Lines 10-72
- [src/agents/vocabulary_agent.py](src/agents/vocabulary_agent.py) - Lines 10-85
- [src/agents/cultural_agent.py](src/agents/cultural_agent.py) - Lines 10-102
- [src/agents/learning_agent.py](src/agents/learning_agent.py) - Lines 10-128
- [src/agents/general_asl_agent.py](src/agents/general_asl_agent.py) - Lines 10-78

## Testing Agent Availability

To verify agents are properly registered, you can:

1. **Check Swarm logs**: CloudWatch will show agent handoffs
2. **Local testing**: Use [src/test_agent_local.py](src/test_agent_local.py)
3. **Monitor handoffs**: Track which agents are invoked

## Summary

**The specialized agents become available to the Swarm by:**

1. Creating individual agent instances
2. Passing them in a list to the `Swarm()` constructor
3. The Swarm maintains an internal registry of all agents
4. The coordinator (entry point) can hand off to any registered agent
5. Any agent can hand off to any other registered agent
6. Loop detection prevents infinite handoff cycles

This creates a collaborative multi-agent system where each specialist focuses on its domain while being able to collaborate with others when needed!

## Additional Resources

- [Strands Swarm Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)
- [Multi-Agent Patterns](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/multi-agent-patterns/)
- [Strands Blog Post](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-1-0-production-ready-multi-agent-orchestration-made-simple/)
- [ARCHITECTURE.md](ARCHITECTURE.md) - Our project's architecture details
