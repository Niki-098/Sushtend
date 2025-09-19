import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print the API key to debug (remove this after confirming it works)
api_key = os.environ.get("GROQ_API_KEY")
print(f"API Key: {api_key}")

# Initialize the Groq client
client = Groq(api_key=api_key)

# Retrieve the list of available models
try:
    models = client.models.list()
    print(f"models object: {models}")
    # Print the model IDs
    for model in getattr(models, 'data', []):
        print(f"Model ID: {getattr(model, 'id', 'No id')}")
    # Use the first available model for a sample API call
    if hasattr(models, 'data') and models.data:
        model_id = models.data[0].id
        print(f"\nUsing model: {model_id} for a sample API call...")
        # Example: chat completion (adjust as needed for your API)
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": "Hello! What is your name?"}]
            )
            print(f"Sample response from model {model_id}: {response}")
        except Exception as api_e:
            print(f"API call failed: {api_e}")
except Exception as e:
    print(f"An error occurred: {e}")