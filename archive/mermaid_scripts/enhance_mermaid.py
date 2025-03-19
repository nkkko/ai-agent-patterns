#!/usr/bin/env python3

import os
import glob
import re

def enhance_class_diagram(file_path):
    """Enhance class diagram with proper attributes and relationships."""
    chapter_num = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
    diagram_name = os.path.basename(file_path).replace('.mmd', '')
    
    # Get basic skeleton
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract class names
    class_pattern = r'class\s+(\w+)'
    class_names = re.findall(class_pattern, content)
    
    if not class_names:
        class_names = ["ExampleClass"]
    
    enhanced_content = "classDiagram\n"
    
    # Create enhanced class definitions based on chapter and diagram
    if chapter_num == "04":  # Memory and State Patterns
        if "WorkingMemory" in class_names:
            enhanced_content += """    class WorkingMemory {
        -current_goal: string
        -subgoals: array
        -completionStatus: object
        -intermediateResults: object
        -attentionFocus: string
        +setGoal(goal: string): void
        +addSubgoal(subgoal: string): void
        +completeSubgoal(subgoal: string): void
        +storeResult(key: string, value: any): void
        +setAttention(focus: string): void
    }
"""
        elif "ConversationMemory" in class_names:
            enhanced_content += """    class ConversationMemory {
        -messages: array
        -summarizer: Summarizer
        -tokenCounter: TokenCounter
        +addMessage(role: string, content: string): void
        +getMessages(limit: number): array
        +summarizeHistory(): string
    }
"""
        else:
            for class_name in class_names:
                enhanced_content += f"""    class {class_name} {{
        -attribute1: string
        -attribute2: number
        +operation1(): void
        +operation2(param: string): string
    }}
"""
    
    elif chapter_num == "05":  # Multi-Agent Patterns
        if "OrchestratorAgent" in class_names:
            enhanced_content += """    class OrchestratorAgent {
        -specializedAgents: Agent[]
        +processRequest(userRequest: string): Response
        -decomposeTask(request: string): Task[]
        -assignSubtasks(tasks: Task[]): Assignment[]
        -aggregateResults(responses: Response[]): Result
    }
    
    class SpecialistAgent {
        -capabilities: Capability[]
        +executeTask(task: Task): Result
    }
    
    OrchestratorAgent o-- SpecialistAgent : coordinates
"""
        else:
            for i, class_name in enumerate(class_names):
                enhanced_content += f"""    class {class_name} {{
        -attribute{i+1}: string
        +execute{class_name}Task(): Result
    }}
"""
            
            if len(class_names) >= 2:
                enhanced_content += f"\n    {class_names[0]} --> {class_names[1]} : delegates to\n"
    
    elif chapter_num == "06":  # Case Study
        if "CoreAgent" in class_names:
            enhanced_content += """    class CoreAgent {
        -conversationMemory: ConversationMemory
        -longTermMemory: LongTermMemory
        -toolController: ToolController
        +processUserInput(message: string): Response
        -planResponse(context: Context): Plan
        -executeActions(plan: Plan): Result
    }
    
    class ToolController {
        -tools: Tool[]
        +executeTool(name: string, params: object): Result
    }
    
    CoreAgent --> ToolController : uses
"""
        else:
            for i, class_name in enumerate(class_names):
                enhanced_content += f"""    class {class_name} {{
        -component{i+1}: string
        +process(input: string): Output
    }}
"""
    
    # Add notes for clarity
    enhanced_content += f"\n    note for {class_names[0]} \"This is an example diagram for Chapter {chapter_num}\"\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)
    
    return True

def enhance_sequence_diagram(file_path):
    """Enhance sequence diagram with meaningful sequences."""
    chapter_num = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
    
    # Create a more detailed sequence diagram
    enhanced_content = "sequenceDiagram\n"
    
    if chapter_num == "04":  # Memory and State Patterns
        enhanced_content += """    participant User
    participant Agent
    participant Memory
    
    User->>Agent: Send request
    Agent->>Memory: Store request
    Agent->>Memory: Retrieve context
    Memory->>Agent: Return relevant history
    Agent->>User: Respond with context
    
    Note over Memory: Maintains conversation state
"""
    elif chapter_num == "05":  # Multi-Agent Patterns
        enhanced_content += """    participant User
    participant Orchestrator
    participant Agent1
    participant Agent2
    
    User->>Orchestrator: Submit task
    Orchestrator->>Agent1: Assign subtask 1
    Orchestrator->>Agent2: Assign subtask 2
    Agent1-->>Orchestrator: Return result 1
    Agent2-->>Orchestrator: Return result 2
    Orchestrator->>User: Deliver combined results
    
    Note over Orchestrator: Coordinates multi-agent workflow
"""
    elif chapter_num == "06":  # Case Study
        enhanced_content += """    participant User
    participant DevAssistant
    participant CodeRetriever
    participant DocRetriever
    
    User->>DevAssistant: Ask coding question
    DevAssistant->>CodeRetriever: Search for code examples
    DevAssistant->>DocRetriever: Fetch documentation
    CodeRetriever-->>DevAssistant: Return code snippets
    DocRetriever-->>DevAssistant: Return documentation
    DevAssistant->>User: Provide comprehensive answer
    
    Note over DevAssistant: Enhances responses with context
"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)
    
    return True

def enhance_flowchart_diagram(file_path):
    """Create a more detailed flowchart diagram."""
    chapter_num = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
    
    # Create a detailed flowchart based on chapter
    if chapter_num == "04":  # Memory and State Patterns
        enhanced_content = """flowchart TD
    A[User Input] --> B{Parse Request}
    B --> C[Retrieve from Memory]
    B --> D[Store in Memory]
    C --> E[Generate Response]
    D --> E
    E --> F[Return to User]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
"""
    elif chapter_num == "05":  # Multi-Agent Patterns
        enhanced_content = """flowchart TD
    A[User Request] --> B{Route Request}
    B --> C[Agent 1 Processing]
    B --> D[Agent 2 Processing]
    B --> E[Agent 3 Processing]
    C --> F[Aggregate Results]
    D --> F
    E --> F
    F --> G[Format Response]
    G --> H[Return to User]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
"""
    elif chapter_num == "06":  # Case Study
        enhanced_content = """flowchart TD
    A[Developer Query] --> B{Analyze Intent}
    B --> C[Search Codebase]
    B --> D[Search Documentation]
    B --> E[Generate New Code]
    C --> F[Combine Results]
    D --> F
    E --> F
    F --> G[Present to Developer]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
"""
    else:
        enhanced_content = """flowchart TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[Action 1]
    C -->|No| E[Action 2]
    D --> F[End]
    E --> F
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)
    
    return True

def enhance_mermaid_file(file_path):
    """Enhance a mermaid file with proper content based on its type."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if content.startswith('classDiagram'):
        print(f"Enhancing class diagram: {file_path}")
        return enhance_class_diagram(file_path)
    elif content.startswith('sequenceDiagram'):
        print(f"Enhancing sequence diagram: {file_path}")
        return enhance_sequence_diagram(file_path)
    elif content.startswith('flowchart') or content.startswith('graph'):
        print(f"Enhancing flowchart diagram: {file_path}")
        return enhance_flowchart_diagram(file_path)
    else:
        print(f"Unknown diagram type in {file_path}, using default flowchart")
        return enhance_flowchart_diagram(file_path)

def main():
    mermaid_files = glob.glob("chapters/*/mermaid/*.mmd")
    
    if not mermaid_files:
        print("No mermaid diagram files found.")
        return
    
    enhanced_count = 0
    
    for file_path in mermaid_files:
        if enhance_mermaid_file(file_path):
            enhanced_count += 1
    
    print(f"\nEnhanced {enhanced_count} out of {len(mermaid_files)} diagram files")

if __name__ == "__main__":
    main()