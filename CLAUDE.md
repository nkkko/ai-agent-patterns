# AI Agent Patterns Project Guidelines

## Build Commands
- `make pdf` - Generate PDF book
- `make epub` - Generate EPUB book
- `make html` - Generate HTML book
- `make all` - Generate all formats
- `make clean` - Remove generated files

## Python Setup
- Python 3.7+ required
- Install dependencies: `pip install -r requirements.txt`
- Run Python scripts: `python images/agent_loop_diagram.py`

## Code Style Guidelines
### Python
- PEP 8 style conventions
- Imports order: stdlib → third-party → local
- Docstrings for all functions and classes
- Proper error handling with try/except blocks
- Type hints encouraged for function parameters
- Descriptive variable names (snake_case)

### Markdown
- Consistent header levels (## for chapter titles, ### for sections)
- Use hyphen-prefixed lists (- item) not asterisks
- Code blocks with language identifier: ```python
- One blank line between sections

## Diagrams
- Use matplotlib for Python-generated diagrams
- Save images to images/generated/ directory
- 300 DPI for publication-quality images