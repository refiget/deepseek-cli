# Neovim Keymaps Configuration

This document describes the Neovim key mappings configured in `keymaps.lua`, including DeepSeek CLI integration and other useful functionalities.

## Table of Contents

1. [Basic Key Mappings](#basic-key-mappings)
2. [Advanced Navigation](#advanced-navigation)
3. [Window Management](#window-management)
4. [File Operations](#file-operations)
5. [Coding Features](#coding-features)
6. [DeepSeek CLI Integration](#deepseek-cli-integration)
7. [Telescope Configuration](#telescope-configuration)
8. [Terminal Integration](#terminal-integration)
9. [Environment Configuration](#environment-configuration)

## Basic Key Mappings

| Key | Mode | Description |
|-----|------|-------------|
| `;` | Normal | Enter command mode |
| `Q` | Normal | Quit current window |
| `Y` | Normal | Copy current line to system clipboard |
| `Y` | Visual | Copy selected text to system clipboard |
| `<leader><CR>` | Normal | Clear search highlighting |
| `sw` | Normal | Toggle line wrapping |

## Advanced Navigation

| Key | Mode | Description |
|-----|------|-------------|
| `J` | Normal | Move down 5 lines |
| `K` | Normal | Move up 5 lines |
| `gt` | Normal | Next tab (with wrapping) |
| `gT` | Normal | Previous tab (with wrapping) |

## Window Management

| Key | Mode | Description |
|-----|------|-------------|
| `<leader>l` | Normal | Move to right window |
| `<leader>k` | Normal | Move to upper window |
| `<leader>j` | Normal | Move to lower window |
| `<leader>h` | Normal | Move to left window |

## File Operations

| Key | Mode | Description |
|-----|------|-------------|
| `<leader>e` | Normal | Open file explorer (coc-explorer) |
| `<leader>mp` | Normal | Open Markdown preview in browser |
| `<leader>mP` | Normal | Stop Markdown preview |
| `<leader>f` | Normal | Format document with Coc |

## Coding Features

| Key | Mode | Description |
|-----|------|-------------|
| `r` | Normal | Run current Python file in terminal |
| `cr` | Normal | Rename variable/function with Coc |
| `<CR>` | Insert | Select confirmation in completion menu |

## DeepSeek CLI Integration

The keymaps.lua file provides seamless integration with DeepSeek CLI for code review, documentation generation, and general queries.

### Configuration

DeepSeek CLI can be configured using these environment variables:

- `DS_CLI_ROOT`: Path to DeepSeek CLI root directory
- `DEEPSEEK_API_KEY`: Your DeepSeek API key (required, only available via environment variable)

### Key Mappings

| Key | Mode | Description |
|-----|------|-------------|
| `<leader>dq` | Normal | Ask DeepSeek a question (in terminal split) |
| `<leader>dr` | Visual | Review selected code (in terminal split) |
| `<leader>dt` | Normal | Generate doctest for current buffer |

### Usage Examples

#### Asking a Question
1. Press `<leader>dq` in normal mode
2. Enter your question when prompted
3. View the response in the terminal split on the right

#### Code Review
1. Select code in visual mode
2. Press `<leader>dr`
3. View review results in the terminal split

#### Generating Doctest
1. Open a Python file
2. Press `<leader>dt` in normal mode
3. Wait for doctest generation
4. The doctest will be automatically inserted into the buffer

## Telescope Configuration

| Key | Mode | Description |
|-----|------|-------------|
| `<leader>w` | Normal | Search files in Projects + dotfiles directories |

### Features
- Search in `~/Projects` and `~/dotfiles` directories
- Includes hidden files
- Opens files in new tabs by default
- Supports split view with `<C-v>` and `<C-x>`

## Terminal Integration

| Key | Mode | Description |
|-----|------|-------------|
| `<C-N>` | Terminal | Exit terminal insert mode |

## Environment Configuration

### Default Paths
- **macOS**: DeepSeek CLI root defaults to `~/Projects/codex-projects/deepseek-cli`
- **Linux**: DeepSeek CLI root defaults to `~/projects/deepseek-cli`

### DeepSeek CLI Detection Order
1. Global `ds` command
2. Python from `DS_CLI_VENV` environment variable
3. Configuration from `~/.config/deepseek-cli/config.env`
4. Fallback to project directory Python

## Installation

1. Copy `keymaps.lua` to your Neovim configuration directory
   ```bash
   cp keymaps.lua ~/.config/nvim/
   ```

2. Source the file in your `init.lua`
   ```lua
   require("keymaps")
   ```

3. Install required plugins if not already installed:
   - `coc.nvim` for code completion and formatting
   - `markdown-preview.nvim` for Markdown preview
   - `telescope.nvim` for file searching

4. Install DeepSeek CLI as described in the main README.md

## Additional Notes

- Leader key is set to space (` `)
- Most mappings are silent (don't show command in status line)
- DeepSeek CLI integration uses a terminal split on the right side (30 columns wide)
- Doctest generation automatically inserts the result into the current buffer
- Terminal operations save files before execution

For more information about DeepSeek CLI, please refer to the main README.md file.