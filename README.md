# Anthropic API Example - CLI Chat

This repository demonstrates a simple command-line chat implementation using the Anthropic API for access to the Claude family of models. It serves as a foundational building block for developers looking to integrate advanced AI capabilities into their Python applications.

## Overview

This API provides access to Anthropic's powerful Claude models, enabling developers to build applications with state-of-the-art generative AI capabilities. This repository implements a simple command-line chat interface that maintains conversation history and shows the basic patterns that can be extended for more complex use cases.

## Features

- Simple CLI-based chat interface
- Conversation history management with proper message formatting
- Environment variable configuration
- Error handling and graceful degradation

## Getting Started

### Prerequisites

- Anthropic API key (available from [Anthropic's Console](https://console.anthropic.com/))
- Python 3.7 or later
- Required packages: `anthropic`, `python-dotenv`

### Installation

1. Clone this repository
2. Install dependencies: 
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   MODEL=claude-3-7-sonnet-20250219  # Optional, will use default if not specified
   ```
4. Run the example: 
   ```
   python main.py
   ```

## Building More Advanced Applications

This simple example can be extended in numerous ways:

### 1. Enhanced Context Management

The current implementation already handles basic conversation history, but you can extend it to include:

```python
# Example of more sophisticated context management
def manage_context(conversation, max_tokens=100000):
    """Manage conversation context to prevent exceeding token limits"""
    # Estimate token count (rough approximation)
    total_tokens = sum(len(msg["content"].split()) * 1.3 for msg in conversation)
    
    # If approaching limit, remove oldest exchanges while preserving most recent context
    while total_tokens > max_tokens and len(conversation) > 2:
        # Remove oldest exchange (user message and assistant response)
        conversation.pop(0)
        if conversation:
            conversation.pop(0)
        # Recalculate token estimate
        total_tokens = sum(len(msg["content"].split()) * 1.3 for msg in conversation)
    
    return conversation
```

### 2. System Prompts and Instructions

Leverage Claude's system prompts for consistent behavior:

```python
# Example of using system prompts
def chat_with_system_prompt(system_prompt):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    model = os.getenv("MODEL", DEFAULT_MODEL)
    
    # Initialize conversation with system prompt
    conversation = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Continue with the rest of the chat logic...
    # When sending to API:
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,  # Using the dedicated system parameter
        messages=[msg for msg in conversation if msg["role"] != "system"]
    )
```

### 3. Multimodal Capabilities

Extend beyond text to leverage Claude's multimodal abilities:

```python
# Example of handling image inputs with Claude
from PIL import Image
import base64
import io

def analyze_image(image_path, prompt):
    """Analyze an image with Claude"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Load and encode the image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    # Create the message with text and image
    response = client.messages.create(
        model="claude-3-opus-20240229",  # Use a model with vision capabilities
        max_tokens=1024,
        messages=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image", 
                        "source": {
                            "type": "base64", 
                            "media_type": "image/jpeg", 
                            "data": image_data
                        }
                    }
                ]
            }
        ]
    )
    
    return response.content[0].text
```

### 4. Tool Use with Function Calling

Implement function calling to allow Claude to use tools:

```python
import json
from anthropic.types import ContentBlockParam, FunctionConfig, ToolChoice, ToolParam, ToolUseBlock

def weather_tool(location):
    """Example function that would provide weather data"""
    # In a real application, this would call a weather API
    return {"temperature": 72, "condition": "Sunny", "location": location}

def chat_with_tools():
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Define the tools Claude can use
    tools = [
        ToolParam(
            name="get_weather",
            description="Get the current weather for a location",
            function_config=FunctionConfig(
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        }
                    },
                    "required": ["location"]
                }
            )
        )
    ]
    
    # User asks about weather
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
        tools=tools,
        tool_choice=ToolChoice.auto
    )
    
    # Check if Claude wants to use a tool
    for content_block in response.content:
        if isinstance(content_block, ToolUseBlock):
            tool_name = content_block.name
            tool_args = json.loads(content_block.input)
            
            if tool_name == "get_weather":
                # Call the actual function
                result = weather_tool(tool_args["location"])
                
                # Send the tool result back to Claude
                final_response = client.messages.create(
                    model="claude-3-7-sonnet-20250219",
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": "What's the weather like in San Francisco?"},
                        {
                            "role": "assistant",
                            "content": [content_block]
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": content_block.id,
                                    "result": json.dumps(result)
                                }
                            ]
                        }
                    ]
                )
                
                return final_response.content[0].text
```

### 5. Integration with Other Services

Combine with other APIs and services for end-to-end solutions:

- Database integration (SQLAlchemy, MongoDB) for persistent storage
- Web frameworks (Flask, FastAPI) for creating API endpoints
- Vector databases (Pinecone, Chroma) for retrieval-augmented generation (RAG)
- Speech-to-text and text-to-speech for voice interfaces

### 6. Deployment Options

Scale your application with different deployment strategies:

- Containerization with Docker
- Cloud Functions or AWS Lambda for serverless deployment
- Traditional web hosting with Gunicorn/WSGI
- Schedule batch processing with tools like Airflow

## Best Practices

When extending this example, consider these best practices:

- Implement proper error handling and retry mechanisms
- Use streaming for better user experience with long responses
- Add rate limiting to manage API usage and costs
- Implement content moderation for user inputs
- Consider ethical implications of AI-generated content
- Store sensitive credentials securely (not in code)
- Implement proper token counting and context management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Anthropic team for providing the Claude API
- Open source community for supporting AI development