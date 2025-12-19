# DeepSeek CLI (ds)

A command-line interface for DeepSeek API, providing a convenient way to interact with DeepSeek chat models from your terminal.

## Features

- Multiple modes: Normal chat, spell correction, and translation
- Streaming responses from DeepSeek API
- Syntax highlighting for Python code blocks
- Configurable via environment variables
- Automatic chat history logging
- Color output (disabled when not in a terminal)
- Virtual environment support

## Installation

### From Source

```bash
git clone https://github.com/yourusername/ds-cli.git
cd ds-cli

# Install using script (recommended)
./install.sh

# Or install manually
pip install -e .
```

## Uninstallation

```bash
pip uninstall -y ds-cli
```

## Configuration

Set these environment variables to configure ds:

- `DEEPSEEK_API_KEY`: Your DeepSeek API key (required)
- `DEEPSEEK_BASE_URL`: API base URL (default: https://api.deepseek.com)
- `DEEPSEEK_MODEL`: Model name (default: deepseek-chat)
- `DEEPSEEK_LOG_FILE`: Chat history log path (default: chat_history.txt)
- `DEEPSEEK_VENV_PATH`: Custom Python virtual environment path

Example:
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

## Usage

### Basic Chat
```bash
ds Hello, how are you?
```

### Spell Correction
```bash
ds -s I hav a speling error
```

### Translation
```bash
ds -t Chinese Hello, world!
```

### Additional Options
```bash
# Disable color output
ds -nc Hello, world!

# Specify virtual environment
ds --venv /path/to/venv Hello, world!

# Show version
ds --version

# Get help
ds --help
```

## License

MIT
