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
- Neovim integration for code review and doctest generation

## Installation

### Using pipx (Only Supported Method)

We only support installation via `pipx` as it provides isolated environments for command-line tools, avoiding dependency conflicts and ensuring clean installation.

#### Step 1: Install pipx (if not already installed)

```bash
# On macOS (using Homebrew)
brew install pipx
pipx ensurepath

# On Linux (using apt)
sudo apt update
sudo apt install pipx
pipx ensurepath

# Using pip (cross-platform)
pip install --user pipx
pipx ensurepath
```

#### Step 2: Install DeepSeek CLI using pipx

```bash
# Install from PyPI (coming soon)
# pipx install ds-cli

# Install from source (current)
git clone https://github.com/yourusername/ds-cli.git
cd ds-cli
pipx install -e .
```

After installation, both `ds` and `ds-nvim` commands will be available globally.

### Managing Dependencies with pipx inject

If you need to add additional dependencies to the isolated environment created by pipx, use `pipx inject`:

```bash
# Inject a new dependency
pipx inject ds-cli <dependency-name>

# For example, to add a specific library
pipx inject ds-cli requests
```

This will install the dependency in the same isolated environment used by ds-cli, ensuring it doesn't affect other Python installations.

## Uninstallation

```bash
# If installed with pipx
pipx uninstall ds-cli

# If installed with pip
pip uninstall -y ds-cli
```

## Configuration

Set these environment variables to configure ds:

- `DEEPSEEK_API_KEY`: Your DeepSeek API key (required, **only available via environment variable**)
- `DEEPSEEK_BASE_URL`: API base URL (default: https://api.deepseek.com)
- `DEEPSEEK_MODEL`: Model name (default: deepseek-chat)
- `DEEPSEEK_LOG_FILE`: Chat history log path (default: chat_history.txt)

### Important Notes

- **API Key Security**: The DeepSeek API key can only be set via the `DEEPSEEK_API_KEY` environment variable. No command-line arguments, configuration files, or other methods are supported for setting the API key.
- **Environment Isolation**: Since we use pipx for installation, ds-cli runs in its own isolated Python environment, ensuring no conflicts with other packages.

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

# Disable streaming output
ds -ns Hello, world!

# Specify virtual environment
ds --venv /path/to/venv Hello, world!

# Show version
ds --version

# Get help
ds --help
```

## Neovim Integration

DeepSeek CLI provides `ds-nvim` command for Neovim integration with the following features:

### Code Review

```bash
# Review code from a file
ds-nvim review --file myscript.py --filetype python

# Review code directly
ds-nvim review --code "def add(a, b): return a + b" --filetype python
```

### Generate Doctest

```bash
# Generate doctest for a file
ds-nvim doctest --file myscript.py --filetype python

# Generate doctest for code directly
ds-nvim doctest --code "def add(a, b): return a + b" --filetype python
```

### Ask Questions

```bash
# Ask a question
ds-nvim ask "How to use list comprehensions in Python?"

# Ask a concise question
ds-nvim ask --concise "What is the capital of France?"
```

## Neovim Configuration with init.lua

DeepSeek CLI provides a simple `init.lua` example file that allows you to integrate all DeepSeek features into your Neovim setup with just one line.

### How to Use init.lua

1. **Locate the init.lua file**
   - The example file is located at `init.lua` in the DeepSeek CLI installation directory

2. **Add the require statement**
   - There are two ways to load the configuration:

   **Method 1: Use the provided init.lua**
   - Add this line to your Neovim configuration file (typically `~/.config/nvim/init.lua`):
     ```lua
     dofile("/path/to/deepseek-cli/init.lua")
     ```

   **Method 2: Direct require (Recommended)**
   - Simply add this line to your Neovim configuration file:
     ```lua
     -- 确保 deepseek.lua 在 Neovim 的运行路径中
     require('deepseek')
     ```

3. **Restart Neovim**
   - Close and reopen Neovim to apply the changes

### Available Key Mappings

After loading the configuration, the following key mappings will be automatically available:

| Key Mapping | Description |
|-------------|-------------|
| `<leader>dq` | Ask a question to DeepSeek |
| `<leader>dr` | Review selected code (visual mode) |
| `<leader>dt` | Generate doctest for current buffer |

### Implementation Details

- All DeepSeek-specific functionality is implemented in `deepseek.lua`
- When you `require('deepseek')`, the setup function is automatically executed
- Basic mappings (navigation, editing, splits) are still defined in `keymaps.lua`
- The `init.lua` file serves as a simple entry point for the integration

## License

MIT