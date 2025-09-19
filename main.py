
# --- FastAPI app ---
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from models import TranscriptIn
from csv_utils import save_to_csv

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_BASE = "https://api.groq.com/openai/v1/chat/completions"

def analyze_transcript(transcript: str) -> dict:
    prompt_system = (
        "You are a concise assistant specialized in summarizing customer call transcripts. "
        "Return valid JSON with keys: 'summary' (2-3 sentences) and 'sentiment' "
        "(Positive, Neutral, Negative)."
    )
    prompt_user = f"Transcript:\n{transcript}\n\nReturn the JSON described above."
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user},
        ],
        "max_tokens": 300,
        "temperature": 0.0,
    }
    resp = requests.post(GROQ_BASE, headers=headers, json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    text = None
    if "choices" in data and len(data["choices"]) > 0:
        choice = data["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            text = choice["message"]["content"]
    if text is None:
        raise ValueError("Could not parse Groq API response.")
    try:
        parsed = json.loads(text.strip())
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1:
            try:
                parsed = json.loads(text[start:end+1])
            except json.JSONDecodeError:
                parsed = {"summary": text[:200] + "..." if len(text) > 200 else text, "sentiment": "Neutral"}
        else:
            parsed = {"summary": text[:200] + "..." if len(text) > 200 else text, "sentiment": "Neutral"}
    return {
        "summary": parsed.get("summary", "No summary available").strip(),
        "sentiment": parsed.get("sentiment", "Neutral").strip(),
    }

CSV_FILENAME = "call_analysis.csv"
app = FastAPI(title="Call Transcript Analyzer (Groq)")
with open("templates/form.html", "r", encoding="utf-8") as f:
    HTML_FORM = f.read()

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_FORM

@app.post("/analyze")
async def analyze_api(item: TranscriptIn):
    transcript = item.transcript.strip()
    if not transcript:
        return JSONResponse(status_code=400, content={"error": "Empty transcript."})
    try:
        result = analyze_transcript(transcript)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    summary = result["summary"]
    sentiment = result["sentiment"]
    print("=== TRANSCRIPT ===")
    print(transcript)
    print("=== SUMMARY ===")
    print(summary)
    print("=== SENTIMENT ===")
    print(sentiment)
    save_to_csv(CSV_FILENAME, transcript, summary, sentiment)
    return {"transcript": transcript, "summary": summary, "sentiment": sentiment}

@app.post("/analyze-form", response_class=HTMLResponse)
async def analyze_form(transcript: str = Form(...)):
    result = await analyze_api(TranscriptIn(transcript=transcript))
    if isinstance(result, JSONResponse):
        return HTMLResponse(f"<pre>Error: {result.body.decode()}</pre>", status_code=result.status_code)

    html = f"""
    <html>
    <head>
        <title>Call Analysis Result</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #f4f6fa;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: #fff;
                border-radius: 12px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                padding: 32px 28px 24px 28px;
            }}
            h2 {{
                color: #2d3a4a;
                margin-top: 0;
            }}
            h3 {{
                color: #4a5a6a;
                margin-bottom: 6px;
            }}
            pre {{
                background: #f0f3f7;
                border-radius: 6px;
                padding: 12px;
                font-size: 1em;
                overflow-x: auto;
            }}
            .sentiment {{
                font-weight: bold;
                color: #0078d4;
            }}
            .footer {{
                margin-top: 18px;
                font-size: 0.98em;
                color: #888;
            }}
            .button {{
                display: inline-block;
                margin-top: 18px;
                padding: 8px 18px;
                background: #0078d4;
                color: #fff;
                border-radius: 5px;
                text-decoration: none;
                font-weight: 500;
                transition: background 0.2s;
            }}
            .button:hover {{
                background: #005fa3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Call Analysis Result</h2>
            <h3>Transcript</h3><pre>{result['transcript']}</pre>
            <h3>Summary</h3><pre>{result['summary']}</pre>
            <h3>Sentiment</h3><pre class="sentiment">{result['sentiment']}</pre>
            <div class="footer">Saved to <b>{CSV_FILENAME}</b></div>
            <a class="button" href="/">Analyze another</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html)