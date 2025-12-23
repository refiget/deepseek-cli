import json
import sys
import time
import threading
from pathlib import Path
from typing import List, Dict, Any
import openai
from .config import API_KEY, BASE_URL, MODEL, LOG_FILE, ENABLE_COLOR, SPINNER, STREAM, COLOR_SCHEME, NON_CODE_STYLE
from .utils import format_error_message, format_info_message
from .highlighter import render_content, render_incremental, strip_ansi


class DeepSeekChat:
    """
    A class to handle DeepSeek API communication with streaming support.
    """
    
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None, log_file: Path = None):
        """
        Initialize the DeepSeekChat instance.
        
        Args:
            api_key: DeepSeek API key.
            base_url: DeepSeek API base URL.
            model: DeepSeek model name.
            log_file: Path to log file for chat history.
        """
        self.api_key = api_key or API_KEY
        self.base_url = base_url or BASE_URL
        self.model = model or MODEL
        self.log_file = log_file or LOG_FILE
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def build_system_prompt(self, mode: str, language: str) -> str:
        """
        Build the system prompt based on the selected mode and language.
        
        Args:
            mode: Operation mode ("normal", "spell", "trans").
            language: Target language for translation.
            
        Returns:
            System prompt string.
        """
        prompts = {
            "normal": f"You are a concise CLI assistant for DeepSeek API. Your task is to provide direct, concise answers:\n1. If the user asks for code, return ONLY the code without any explanations, comments, or context.\n2. If the user asks a non-code question, return a brief, direct answer.\n3. Never return empty responses.\n4. Always provide the answer in the requested language.\n\nLanguage: {language}",
            "spell": f"You are a CLI spell correction assistant. Correct spelling errors and return only the fixed text.\nLanguage: {language}",
            "trans": f"You are a CLI translation assistant. Translate the text between English and Chinese only.\nReturn only the translated text, no additional explanations. Target language: {language}"  
        }
        return prompts.get(mode, prompts["normal"])
    
    def log_chat(self, messages: List[Dict[str, str]], response: str):
        """
        Log chat history to the specified log file.
        
        Args:
            messages: List of chat messages.
            response: Assistant response.
        """
        try:
            chat_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "messages": messages,
                "response": strip_ansi(response),
                "model": self.model
            }

            # Ensure log directory exists and append as NDJSON for safety
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(chat_entry, ensure_ascii=False))
                f.write("\n")

        except Exception as e:
            error_msg = format_error_message("Logging Error", f"Failed to log chat history: {e}", ENABLE_COLOR)
            print(error_msg, file=sys.stderr)
    
    def chat(self, query: str, mode: str = "normal", language: str = "English", stream: bool = None):
        """
        Send a query to the DeepSeek API and return the response.
        
        Args:
            query: User query.
            mode: Operation mode ("normal", "spell", "trans").
            language: Target language for translation.
            stream: Whether to stream the response.
            
        Returns:
            Assistant response string.
        """
        # Use global config if stream is not specified
        if stream is None:
            stream = STREAM
        # Validate API key presence (format may vary by provider/proxy)
        if not self.api_key:
            raise ValueError("API key is missing. Please set the DEEPSEEK_API_KEY environment variable.")
        
        # Build messages for API call
        system_prompt = self.build_system_prompt(mode, language)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        try:
            response_text = ""

            # Function to display loading animation
            def loading_animation():
                animation_chars = ["|", "/", "-", "\\"]
                idx = 0
                while loading:
                    print(f"\r{animation_chars[idx]} Thinking...", end="", flush=True)
                    idx = (idx + 1) % len(animation_chars)
                    time.sleep(0.1)

            loading = False
            animation_thread = None

            def stop_loading():
                nonlocal loading
                if loading and animation_thread is not None:
                    loading = False
                    animation_thread.join()
                    print("\r" + " " * 50, end="\r", flush=True)

            if SPINNER:
                loading = True
                animation_thread = threading.Thread(target=loading_animation)
                animation_thread.start()

            # Make API call with appropriate streaming setting
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream
            )

            # Process and print the response
            if stream:
                buffer = ""
                first_chunk = True
                for chunk in response:
                    if hasattr(chunk, 'choices') and chunk.choices:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content:
                            if first_chunk:
                                stop_loading()
                                first_chunk = False
                            content_chunk = delta.content
                            response_text += content_chunk
                # Ensure loading indicator stops even if no content is streamed
                stop_loading()
                
                # Render the response with syntax highlighting
                from .utils import render_content
                rendered_response = render_content(response_text, enable_color=ENABLE_COLOR, theme_name=COLOR_SCHEME, non_code_style=NON_CODE_STYLE)
                return rendered_response
            else:
                # Get content from non-streaming response
                if hasattr(response, 'choices') and response.choices:
                    response_text = response.choices[0].message.content or ""
                    
                    # Stop loading once we have the full response
                    stop_loading()
                    
                    # Just return the response text, don't print it here
                    # The caller will handle printing
                else:
                    stop_loading()

            # Render the response with syntax highlighting
            from .utils import render_content
            rendered_response = render_content(response_text, enable_color=ENABLE_COLOR, theme_name=COLOR_SCHEME, non_code_style=NON_CODE_STYLE)
            
            # Log chat history
            self.log_chat(messages, rendered_response)
            
            return rendered_response
        
        except openai.APIError as e:
            raise RuntimeError(f"DeepSeek API error occurred: {e}") from e
        
        except openai.APIConnectionError as e:
            raise RuntimeError(f"Failed to connect to DeepSeek API: {e}") from e
        
        except openai.RateLimitError as e:
            raise RuntimeError(f"DeepSeek API rate limit exceeded: {e}") from e
        
        except openai.AuthenticationError as e:
            raise RuntimeError(f"DeepSeek API authentication failed: {e}") from e
        
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}") from e
        
        finally:
            # Ensure spinner is stopped on any early exit
            try:
                stop_loading()
            except Exception:
                pass


def chat(query: str, mode: str = "normal", language: str = "English", stream: bool = None):
    """
    A convenience function to create a DeepSeekChat instance and send a query.
    
    Args:
        query: User query.
        mode: Operation mode ("normal", "spell", "trans").
        language: Target language for translation.
        stream: Whether to stream the response.
        
    Returns:
        Assistant response string.
    """
    chat_instance = DeepSeekChat()
    return chat_instance.chat(query, mode, language, stream)
