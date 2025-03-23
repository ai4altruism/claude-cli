import anthropic
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set default model in case it's not specified in .env file
DEFAULT_MODEL = "claude-3-7-sonnet-20250219"

def chat_with_claude():
    # Set up the Anthropic API client
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    
    # Keep track of conversation history
    conversation = []
    
    # Get model from environment variable or use default
    model = os.getenv("MODEL", DEFAULT_MODEL)
    
    print("Welcome to Claude Chat CLI!")
    print(f"Using model: {model}")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("\nThank you for chatting with Claude. Goodbye!")
            break
        
        # Add user message to conversation history
        conversation.append({"role": "user", "content": user_input})
        
        try:
            # Get model from environment variable or use default
            model = os.getenv("MODEL", DEFAULT_MODEL)
            
            # Send the entire conversation to Claude
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=conversation
            )
            
            # Extract and print Claude's response
            assistant_message = response.content[0].text
            print(f"\nClaude: {assistant_message}")
            
            # Add Claude's response to conversation history
            conversation.append({"role": "assistant", "content": assistant_message})
            
        except Exception as e:
            print(f"\nError: {e}")
            # Optionally remove the last user message if there was an error
            if conversation:
                conversation.pop()

if __name__ == "__main__":
    chat_with_claude()