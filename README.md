# Claude CLI Chat

A simple command-line interface for chatting with Anthropic's Claude AI assistant.

## Features

- Interactive command-line chat with Claude
- Maintains conversation context for natural interactions
- Configurable model selection via environment variables
- Simple exit commands ("exit" or "quit")

## Prerequisites

- Python 3.8+
- Anthropic API key

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/claude-cli-chat.git
   cd claude-cli-chat
   ```

2. Install required packages:
   ```bash
   pip install anthropic python-dotenv
   ```

3. Create a `.env` file in the project directory:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   MODEL=claude-3-7-sonnet-20250219
   ```

## Usage

Run the application:
```bash
python claude_chat.py
```

Type your messages at the prompt and press Enter. Claude will respond in the terminal.

To end the conversation, type `exit` or `quit` at the prompt.

## Available Models

You can change the model by updating the MODEL variable in your `.env` file:

- `claude-3-opus-20240229` - Most powerful model, great for complex tasks
- `claude-3-sonnet-20240229` - Balanced performance and efficiency
- `claude-3-5-sonnet-20240620` - Enhanced model with improved reasoning
- `claude-3-7-sonnet-20250219` - Latest model (default)
- `claude-3-haiku-20240307` - Fastest model for simple tasks

## License

N/A

## Contributing

N/A