# Chapter 2: Core Architectural Patterns

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

**Code example:**
```python
class MonolithicAgent:
    def __init__(self):
        self.memory = {}
        self.tools = self._register_tools()

    def _register_tools(self):
        return {
            "search": self._search_tool,
            "calculate": self._calculate_tool
        }

    def _search_tool(self, query):
        # Implementation of search functionality
        return f"Results for: {query}"

    def _calculate_tool(self, expression):
        # Implementation of calculation functionality
        return eval(expression)

    def process(self, user_input):
        # Process user input
        # Determine intent
        # Select and execute appropriate tool
        tool_name = self._determine_tool(user_input)
        if tool_name in self.tools:
            result = self.tools[tool_name](user_input)
            return result
        return "I don't know how to handle that request."

    def _determine_tool(self, user_input):
        # Simple intent detection logic
        if "calculate" in user_input.lower():
            return "calculate"
        return "search"
```

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

**Code example:**
```python
# Protocol definition
class ToolProtocol:
    def describe(self):
        """Return tool metadata"""
        raise NotImplementedError()

    def execute(self, parameters):
        """Execute the tool with given parameters"""
        raise NotImplementedError()

# Tool implementation
class SearchTool(ToolProtocol):
    def describe(self):
        return {
            "name": "search",
            "description": "Search for information",
            "parameters": {
                "query": "The search query string"
            }
        }

    def execute(self, parameters):
        query = parameters.get("query", "")
        # Implementation of search functionality
        return f"Results for: {query}"

# Agent implementation
class ProtocolAgent:
    def __init__(self):
        self.tools = {}
        self.memory = {}

    def register_tool(self, tool):
        metadata = tool.describe()
        self.tools[metadata["name"]] = tool

    def process(self, user_input):
        intent = self._determine_intent(user_input)
        if intent in self.tools:
            params = self._extract_parameters(user_input, intent)
            return self.tools[intent].execute(params)
        return "I don't know how to handle that request."
```

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