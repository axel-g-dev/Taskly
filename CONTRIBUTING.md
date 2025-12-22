# Contributing to Taskly

First off, thank you for considering contributing to Taskly! It's people like you that make Taskly such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Include your environment details** (OS, Python version, Flet version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other applications**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests if applicable
3. Ensure your code follows the existing style
4. Update the documentation if needed
5. Write a clear commit message

## Development Setup

```bash
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests when relevant

Example:
```
Add temperature monitoring feature

- Created TemperatureCard component
- Enhanced data_manager with temperature collection
- Added color-coded temperature display
- Closes #123
```

## Project Structure

```
Taskly/
├── main.py              # Entry point
├── dashboard.py         # Main UI
├── data_manager.py      # Data collection
├── data_exporter.py     # Export functionality
├── config.py            # Configuration
├── utils.py             # Utilities
└── components/          # UI components
    ├── metric_card.py
    ├── temperature_card.py
    ├── charts.py
    ├── process_list.py
    ├── system_info.py
    └── alert_manager.py
```

## Testing

Before submitting a pull request:

1. Test your changes thoroughly
2. Ensure the application runs without errors
3. Test on different platforms if possible (macOS, Linux, Windows)
4. Verify that existing features still work

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉
