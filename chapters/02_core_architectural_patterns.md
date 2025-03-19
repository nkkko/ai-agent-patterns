---
title: "Core Architectural Patterns"
description: "Foundational architectural patterns for AI agent systems"
authors: ["Nikola Balić"]
date: 2025-03-18
last_updated: 2025-03-18
status: draft
chapter: 3
tags: ["ai", "agents", "patterns", "architecture", "design"]
---

# Chapter 3: Core Architectural Patterns

## Introduction

The foundational architecture of your agent system determines its capabilities, limitations, and future extensibility. This chapter presents battle-tested patterns for structuring your agent's core components, with clear guidance on which pattern best suits different requirements.

## Key Concepts

### Architectural Considerations
*When designing agent architectures, engineers must balance complexity, extensibility, and performance. The patterns in this chapter address these concerns with different trade-offs.*

#### Pattern: Monolithic Agent Pattern
*A simple, cohesive architecture where all agent functionality exists within a single codebase and execution context.*

**Structure and Implementation:**
- Single codebase containing all agent logic
- Direct function calls between components
- Shared memory and state management
- Unified error handling and logging

**When to use:**
- For simple agents with focused capabilities
- When rapid development is prioritized
- For agents with minimal external dependencies
- When deployment simplicity is critical

**Diagram:**
[MonolithicAgent Class Diagram - Shows the structure of a simple agent with internal memory and tool handling]

### Protocol-Based Architecture
*Separating components using well-defined protocols for communication enables flexibility and component interchangeability.*

#### Pattern: Protocol-Based Agent Pattern
*An architecture that uses standardized protocols to connect agent components and external tools.*

**Structure and Implementation:**
- Components communicate via defined protocols
- Clear interfaces between subsystems
- Tool discovery and registration mechanisms
- Protocol versioning for backward compatibility

**When to use:**
- For extensible agents with diverse tool needs
- When components may evolve independently
- For multi-team development environments
- When integration with third-party tools is required

**Diagram:**
[Protocol-Based Agent Architecture - Illustrates the relationship between the Agent, ToolProtocol interface, and concrete tool implementations like SearchTool and CalculatorTool]

## The Agent Loop Pattern

The Agent Loop is the fundamental pattern underlying all AI agent architectures. It establishes the cyclical process of observation, reasoning, and action that enables agents to interact with their environment.

### Pattern Structure

In its simplest form, the Agent Loop consists of three main phases:

1. **Observation**: The agent receives input from its environment (user queries, system data, etc.)
2. **Reasoning**: The agent processes the input to determine appropriate actions
3. **Action**: The agent executes the selected actions and observes the results

**Narrative Example:**
Consider a virtual assistant helping a user book a flight. The agent loop would operate as follows:

- In the observation phase, the agent receives the user's query "Book me a flight from New York to London next Friday."
- During reasoning, the agent interprets the intent (flight booking), identifies key parameters (origin: New York, destination: London, date: next Friday), and determines it needs to check flight availability using a travel API.
- In the action phase, the agent calls the travel API, processes the results, and responds to the user with available options.
- The loop continues when the user selects a flight option, triggering a new observation phase.

**Diagram:**
[Agent Loop Flowchart - Illustrates the cyclical process of observation, reasoning, action, and evaluation that forms the core of agent behavior]

### Key Variations

#### 1. Reactive Agent Loop

**Structure:**
- Simplified reasoning phase using predefined rules or patterns
- Quick response to environmental inputs
- Limited or no memory of past interactions

**Narrative Example:**
A smart thermostat agent operates with a reactive loop pattern. It continuously observes the current temperature, compares it against the target temperature using simple rules, and then takes appropriate action (turn heating on/off). The agent doesn't need complex reasoning or extensive memory of past states to function effectively.

**Diagram:**
[Reactive Agent Loop - Shows a simple thermostat control loop with temperature observation and heating activation/deactivation based on a target threshold]

#### 2. Deliberative Agent Loop

**Structure:**
- Enhanced reasoning phase including planning and knowledge integration
- Incorporation of memory and context from past interactions
- Goal-directed behavior rather than simple reactivity

**Narrative Example:**
A personal assistant agent helping with project management uses a deliberative loop. When asked to "schedule a team meeting," it considers multiple factors: team members' calendar availability, previous meeting patterns, project deadlines, and meeting room availability. It develops a plan with multiple steps (checking calendars, finding optimal times, sending invitations) rather than just reacting to the immediate request.

**Diagram:**
[Deliberative Agent Loop - Shows the sequence flow through Environment, Observation Module, Reasoning Engine, Planner, and Action Executor components]

### Best Practices

When implementing the Agent Loop pattern:

1. **Define clear boundaries** between observation, reasoning, and action phases
2. **Implement appropriate error handling** at each phase of the loop
3. **Consider loop frequency** - how often the agent should cycle through the loop
4. **Balance reactivity and deliberation** based on use case requirements
5. **Monitor loop performance** to identify bottlenecks or failure points

## Practical Applications

The choice of architectural pattern significantly impacts how your agent system evolves:

1. **Single-purpose agents** often benefit from the Monolithic pattern's simplicity and cohesion.

2. **General-purpose assistants** typically require the flexibility of Protocol-based approaches to incorporate diverse tools.

3. **Enterprise systems** may combine patterns, using Monolithic for core reasoning and Protocol-based for tool integration.

## Summary

Selecting the appropriate architectural pattern for your agent system should be based on specific requirements, expected growth, and team structure. The Monolithic pattern provides simplicity and rapid development for focused agents, while Protocol-based architectures offer extensibility and component independence for more complex systems.

## References

- Design Patterns: Elements of Reusable Object-Oriented Software
- Large Language Model Agent Architecture Patterns
- Protocol-Oriented Programming in Swift