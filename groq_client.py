import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# The API key should be set as an environment variable
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  # This is the default and can be omitted
)

def analyze_transcript(transcript: str) -> dict:
    prompt_system = (
        "You are a concise assistant specialized in summarizing customer call transcripts. "
        "Return valid JSON with keys: 'summary' (2-3 sentences) and 'sentiment' "
        "(Positive, Neutral, Negative)."
    )
    
    prompt_user = f"Transcript:\n{transcript}\n\nReturn the JSON described above."
    
    try:
        # Use the official Groq client API as shown in documentation
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            model="llama3-8b-8192",  # Using the model from official documentation
            max_tokens=300,
            temperature=0.0,
        )
        
        # Extract the response content
        text = chat_completion.choices[0].message.content
        
        if text is None:
            raise ValueError("Could not parse Groq API response.")
        
        # Parse JSON safely
        try:
            parsed = json.loads(text.strip())
        except json.JSONDecodeError:
            # Try to extract JSON from the text
            start, end = text.find("{"), text.rfind("}")
            if start != -1 and end != -1:
                try:
                    parsed = json.loads(text[start:end+1])
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails completely
                    parsed = {
                        "summary": "Failed to parse summary from response",
                        "sentiment": "Neutral"
                    }
            else:
                # Fallback if no JSON braces found
                parsed = {
                    "summary": "Failed to parse summary from response",
                    "sentiment": "Neutral"
                }
        
        return {
            "summary": parsed.get("summary", "No summary available").strip(),
            "sentiment": parsed.get("sentiment", "Neutral").strip(),
        }
        
    except Exception as e:
        raise RuntimeError(f"Groq API error: {str(e)}")