*   **Single-Agent Architecture**: This architecture consists of a single agent, typically a Large Language Model (LLM), equipped with access to various tools. The LLM acts as the brain, deciding whether and how to use these tools to solve a query or task. This approach is often suitable for relatively straightforward tasks.

*   **Multi-Agent Architecture**: This architecture involves multiple AI agents working collaboratively to resolve complex tasks. Each agent can be responsible for a specific group of tasks or have a specialised role. Multi-agent systems can handle complex and dynamic problems and allow for parallel processing, potentially using smaller models specialised for distinct tasks. They require robust mechanisms to manage interactions and can be more challenging to debug.

*   **Network of Agents (Horizontal Architecture)**: In this pattern, multiple agents, each with their own individual tools, communicate with each other by deciding which agent should act next. This can also manifest as a sequence of agents where the output of one agent becomes the input for the following agent. While offering flexibility, this architecture can sometimes be unreliable due to its loose communication patterns, potentially leading to increased time and cost.

*   **Supervisor Agent Approach (Hierarchical Architecture)**: This architecture features a single, central 'supervisor' agent whose primary job is to route tasks to other, more specialised 'sub-agents'. The sub-agents can then focus on their specific tasks without needing to decide who to communicate with next; that responsibility lies with the supervisor. This structure can be layered, with supervisor agents managing other supervisor agents.

*   **Supervisor with Tools Architecture**: A variation of the supervisor pattern where the sub-agents are treated as tools accessible to the central LLM (the supervisor). Communication between the supervisor and sub-agents occurs through the parameters of the tool calls. This can be a simpler approach, but communication is limited to the tool call parameters rather than shared state.

*   **Custom Cognitive Architecture**: This refers to building a multi-agent system with a design that is highly specific to the domain of the application. Rather than relying on off-the-shelf supervisor or hierarchical structures, it borrows aspects from various patterns to create a bespoke solution. This level of customisation is often necessary to achieve production-ready systems.

*   **Iterative Cycles (Loop)**: In this pattern, agents operate in iterative cycles, continuously refining their outputs based on feedback received from other agents. This is useful in evaluation scenarios like code writing and testing.

*   **Parallel**: This design involves multiple agents working simultaneously on different parts of a larger task, aiming for efficiency through parallel processing. A challenge can be managing communication and avoiding duplicated efforts.

*   **Sequential**: This pattern arranges agents in a chain where the output of one agent serves as the input for the next, creating a pipeline for task completion.

*   **Shared Database with Different Tools**: In this architecture, multiple agents interact with a common database but utilise different tools to perform their specific tasks.

*   **Agent Supervisor**: This is a specialised agent designed to coordinate and manage other agents. A common way to implement this is by wrapping the other agents as tools that the supervisor can then call.

*   **Handoffs**: Within the context of the OpenAI Agents SDK, a 'handoff' is a primitive that allows one agent to explicitly delegate a specific task to another agent.

*   **Reflection Pattern**: This pattern involves an agent that iteratively generates an output and then reflects on it, using the critique to refine the subsequent output. This creates a loop of generation and self-correction, potentially improving the quality of the final result. The loop can be stopped after a fixed number of iterations or based on predefined stop criteria.

*   **Tool Use Pattern**: In this architecture, agents are designed to interact with and utilise external tools to perform specific tasks or gather necessary information. The agent decides when and how to use these tools based on the user's request and the current context. Frameworks and libraries often provide mechanisms to easily integrate and manage these tools.

*   **Planning Pattern (ReAct)**: This pattern, exemplified by the ReAct (Reason and Act) technique, involves agents that interleave reasoning steps with action steps. The agent first reasons about the user's request and the necessary steps, then takes an action (like using a tool), observes the outcome, and reasons about the next steps. This iterative process of reasoning and acting continues until the agent can provide a final response.

*   **Multi-Agent Pattern**: As previously mentioned, this involves multiple agents working together. Source explicitly lists it as one of the fundamental agentic patterns. These agents can have different roles and capabilities, and their interactions need to be carefully managed to achieve a common goal.

*   **Interface Agents**: These are agents designed to learn a user's preferences over time through examples and feedback. They aim to act as an extension of the human's wishes, assisting in tasks like filtering information or making suggestions based on learned behaviour. This aligns with the idea of agents maintaining context and having specific roles.
