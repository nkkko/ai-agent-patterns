# AI Agent Design Patterns

A practical guide for software engineers designing intelligent systems for autonomous action.

## About This Book

AI Agent Design Patterns is a comprehensive guide for software engineers who are building agent systems. This book provides:

- **Practical Patterns**: Battle-tested architectural approaches for building robust agent systems
- **Implementation Guidance**: Concrete code examples showing how to implement each pattern
- **Design Principles**: Clear principles for making architectural decisions in agent systems
- **Visual Examples**: Diagrams and visualizations of key concepts

The book covers essential topics including:

- Building Blocks of Software Agents
- Core Architectural Patterns
- Tool Integration Patterns
- Memory and State Patterns
- Multi-Agent Patterns
- Advanced agent system design concepts

## Reading the Book

The book chapters are organized in the `chapters/` directory:

1. [Building Blocks of Software Agents](chapters/01_building_blocks_of_software_agents.md)
2. [Core Architectural Patterns](chapters/02_core_architectural_patterns.md)
3. Tool Integration Patterns (Coming soon)
4. Memory and State Patterns (Coming soon)
5. Multi-Agent Patterns (Coming soon)
6. Case Study: Building a Retrieval-Enhanced Development Assistant (Coming soon)

## Development Environment Setup

This repository contains code examples, diagrams, and supplementary materials for the book. To work with the example code and generate diagrams, follow these setup instructions:

### Prerequisites

- Python 3.10 or higher
- [Astral's uv](https://docs.astral.sh/uv/) - A fast Python package installer and resolver

### Setting Up the Development Environment

1. **Install uv** if you haven't already:

   ```bash
   curl -fsSL https://astral.sh/uv/install.sh | bash
   ```

2. **Create a virtual environment** using uv:

   ```bash
   uv venv
   ```

3. **Activate the virtual environment**:

   * On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   * On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies**:

   ```bash
   uv pip install -r requirements.txt
   ```

### Generating Diagrams

The book includes various diagrams and visual examples that are generated using Python scripts:

1. Navigate to the `images` directory:

   ```bash
   cd images
   ```

2. Run a diagram script:

   ```bash
   python agent_loop_diagram.py
   ```

Generated images will be saved to the `images/generated` directory and can be referenced in the book markdown files.

## Book Structure

- **chapters/**: Markdown files for each chapter
- **specs/**: Detailed specifications for each chapter
- **images/**: Python scripts for generating diagrams and visualizations
- **images/generated/**: Output directory for generated images

## Contributing

If you find errors or have suggestions for improvements, please open an issue or submit a pull request.

## License

See [LICENSE.md](LICENSE.md) for details on the licensing for this book and its associated code.