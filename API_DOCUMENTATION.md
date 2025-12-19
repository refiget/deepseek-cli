# DeepSeek CLI API Documentation

DeepSeek CLI (ds) provides a set of built-in APIs that can be used to integrate with other tools, including neovim (nvim). This document describes these APIs and how to use them with nvim keybindings.

## Available APIs

All APIs are exported from the `ds` package and can be imported directly.

### 1. Chat API

The main API for interacting with the DeepSeek service.

```python
from ds import chat

response = chat(query, mode="normal", language="English", stream=True)
```

**Parameters:**
- `query`: str - The user query to send to DeepSeek API
- `mode`: str - Operation mode ("normal", "spell", "trans")
- `language`: str - Target language for translation or response
- `stream`: bool - Whether to stream the response (default: True)

**Returns:**
- str - The full response from DeepSeek API

### 2. Rendering APIs

#### render_content
```python
from ds import render_content

rendered = render_content(content, enable_color=True)
```

**Parameters:**
- `content`: str - Content string that may contain Python code blocks
- `enable_color`: bool - Whether to enable ANSI color codes

**Returns:**
- str - Rendered content with syntax highlighted code blocks

#### strip_ansi
```python
from ds import strip_ansi

clean_text = strip_ansi(text_with_colors)
```

**Parameters:**
- `text`: str - Text containing ANSI escape sequences

**Returns:**
- str - Cleaned text without ANSI escape sequences

### 3. Configuration API

#### load_config
```python
from ds import load_config

config = load_config()
```

**Returns:**
- dict - Loaded configuration

### 4. Low-level API (DeepSeekChat class)

For more control, you can use the `DeepSeekChat` class directly:

```python
from ds.chat import DeepSeekChat

# Initialize with custom settings
chat_instance = DeepSeekChat(
    api_key="your_api_key",
    base_url="https://api.deepseek.com",
    model="deepseek-coder-v1.5",
    log_file=Path("/path/to/log/file.txt")
)

# Send a query
response = chat_instance.chat(query, mode="normal", language="English", stream=True)
```

## Neovim Integration

Here's how to integrate DeepSeek CLI API with nvim keybindings.

### Option 1: Using Python in Neovim

Create a Python script that uses DeepSeek CLI API and configure nvim to call it.

#### Step 1: Create nvim_deepseek.py

```python
#!/usr/bin/env python3
import sys
import os

# Add the deepseek-cli directory to Python path
sys.path.append('/Users/mac/Projects/Trae-projects/deepseek-cli')

from ds import chat, render_content, strip_ansi


def query_deepseek(query, mode="normal", language="English", stream=False):
    """Query DeepSeek API and return the response."""
    try:
        response = chat(query, mode=mode, language=language, stream=stream)
        return response
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nvim_deepseek.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    response = query_deepseek(query)
    print(response)
```

#### Step 2: Configure nvim Keybindings

Add the following to your `~/.config/nvim/init.vim` or `~/.config/nvim/init.lua`:

**Vimscript (init.vim):**

```vim
" DeepSeek CLI Integration
function! DeepSeekQuery(query)
    let l:cmd = 'python3 /Users/mac/Projects/Trae-projects/deepseek-cli/nvim_deepseek.py ' . shellescape(a:query)
    let l:response = system(l:cmd)
    return l:response
endfunction

" Query DeepSeek for the current word
nnoremap <Leader>d :let @"=DeepSeekQuery(expand('<cword>'))<CR>""P

" Query DeepSeek for the selected text (visual mode)
vmap <Leader>d y:let @"=DeepSeekQuery(getreg('"'))<CR>""P

" Query DeepSeek with custom input
nnoremap <Leader>D :call inputsave()<CR>:let l:query=input("DeepSeek Query: ")<CR>:call inputrestore()<CR>:let @"=DeepSeekQuery(l:query)<CR>""P
```

**Lua (init.lua):**

```lua
-- DeepSeek CLI Integration
function DeepSeekQuery(query)
    local cmd = 'python3 /Users/mac/Projects/Trae-projects/deepseek-cli/nvim_deepseek.py ' .. vim.fn.shellescape(query)
    local response = vim.fn.system(cmd)
    return response
end

-- Query DeepSeek for the current word
vim.keymap.set('n', '<Leader>d', function()
    local word = vim.fn.expand('<cword>')
    local response = DeepSeekQuery(word)
    vim.api.nvim_paste(response, true, -1)
end)

-- Query DeepSeek for the selected text (visual mode)
vim.keymap.set('v', '<Leader>d', function()
    vim.cmd('normal! "xy')
    local selected_text = vim.fn.getreg('x')
    local response = DeepSeekQuery(selected_text)
    vim.api.nvim_paste(response, true, -1)
end)

-- Query DeepSeek with custom input
vim.keymap.set('n', '<Leader>D', function()
    local query = vim.fn.input('DeepSeek Query: ')
    if query ~= '' then
        local response = DeepSeekQuery(query)
        vim.api.nvim_paste(response, true, -1)
    end
end)
```

### Option 2: Using Neovim Python API

For more seamless integration, you can use the Neovim Python API directly.

#### Step 1: Install pynvim

```bash
pip install pynvim
```

#### Step 2: Create a Neovim Plugin

Create a file at `~/.config/nvim/rplugin/python3/deepseek.py`:

```python
import pynvim
from ds import chat, render_content


@pynvim.plugin
class DeepSeekPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
    
    @pynvim.command('DeepSeek', nargs='+', range='', bang=True)
    def deepseek_command(self, args, range, bang):
        """Call DeepSeek API with the given query."""
        query = ' '.join(args)
        
        try:
            response = chat(query, stream=False)
            
            # Insert response below current line
            self.nvim.current.buffer.append(response.split('\n'), self.nvim.current.window.cursor[0])
        except Exception as e:
            self.nvim.err_write(f"Error: {str(e)}\n")
    
    @pynvim.function('DeepSeekQuery', sync=True)
    def deepseek_query(self, args):
        """Query DeepSeek API and return the result."""
        if not args:
            return "No query provided"
        
        query = args[0]
        try:
            return chat(query, stream=False)
        except Exception as e:
            return f"Error: {str(e)}"
    
    @pynvim.function('DeepSeekExplain', sync=True)
    def deepseek_explain(self, args):
        """Explain the selected code using DeepSeek."""
        if not args:
            return "No code provided"
        
        code = args[0]
        query = f"Explain this code: {code}"
        try:
            return chat(query, stream=False)
        except Exception as e:
            return f"Error: {str(e)}"
```

#### Step 3: Configure Keybindings

Add the following to your `init.lua` or `init.vim`:

**Vimscript (init.vim):**

```vim
" Update remote plugins
:UpdateRemotePlugins

" Query DeepSeek for the current word
nnoremap <Leader>d :call DeepSeekQuery(expand('<cword>'))<CR>

" Explain the selected code
vmap <Leader>e y:call DeepSeekExplain(getreg('"'))<CR>

" Run DeepSeek command
nnoremap <Leader>D :DeepSeek<Space>
```

**Lua (init.lua):**

```lua
-- Update remote plugins
vim.cmd('UpdateRemotePlugins')

-- Query DeepSeek for the current word
vim.keymap.set('n', '<Leader>d', function()
    local word = vim.fn.expand('<cword>')
    local response = vim.fn.DeepSeekQuery(word)
    vim.api.nvim_paste(response, true, -1)
end)

-- Explain the selected code
vim.keymap.set('v', '<Leader>e', function()
    vim.cmd('normal! "xy')
    local code = vim.fn.getreg('x')
    local explanation = vim.fn.DeepSeekExplain(code)
    vim.api.nvim_paste(explanation, true, -1)
end)

-- Run DeepSeek command
vim.keymap.set('n', '<Leader>D', ':DeepSeek ')
```

## Advanced Usage

### Customizing the Response

You can customize how the response is displayed using the rendering APIs:

```python
from ds import chat, render_content, strip_ansi

# Get response
response = chat("Write a Python function to calculate factorial", stream=False)

# Render with syntax highlighting
rendered = render_content(response)

# Or get plain text (without colors)
plain_text = strip_ansi(rendered)
```

### Using Different Modes

```python
# Normal mode (default)
response = chat("What is the capital of France?")

# Spell correction mode
response = chat("Helo world", mode="spell")

# Translation mode
response = chat("Hello world", mode="trans", language="Chinese")
```

## Troubleshooting

1. **Module not found error**: Ensure that the deepseek-cli directory is in your Python path.
2. **API key issues**: Make sure your API key is properly configured in the environment variables or config file.
3. **Permission issues**: Ensure the Python scripts are executable.

## Conclusion

DeepSeek CLI provides a flexible API that can be easily integrated with nvim keybindings, allowing you to access powerful AI capabilities directly from your editor. The examples provided here can be customized to fit your specific workflow and keybinding preferences.
