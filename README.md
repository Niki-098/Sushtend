# Call Transcript Analyzer
A FastAPI-based web application that analyzes customer call transcripts using Groq's AI models to generate summaries and sentiment analysis.


## Features

**Web Interface:** Simple HTML form for transcript input<br>
**AI Analysis:** Uses Groq's Llama models for intelligent analysis<br>
**Summary Generation:** Creates concise 2-3 sentence summaries<br>
**Sentiment Analysis:** Classifies sentiment as Positive, Neutral, or Negative<br>
**Data Storage:** Saves all analyses to CSV file for record-keeping<br>
**REST API:** JSON endpoints for programmatic access<br>

## Prerequisites

Python 3.7+<br>
Groq API key (get one at console.groq.com)

## Installation

**Clone the repository** 

bash: git clone https://github.com/Niki-098/Sushtend.git<br>
 

**Create virtual environment**
bash: python -m venv venv<br>
Windows: venv\Scripts\activate<br>
Linux/Mac: source venv/bin/activate<br>

## Install dependencies

bash   pip install fastapi uvicorn groq python-dotenv requests pydantic

**Set up environment variables**

bash   # Create .env file<br>
echo "GROQ_API_KEY=your_groq_api_key_here" > .env<br>
echo "GROQ_MODEL=llama-3.1-8b-instant" >> .env

### Create templates directory and form
bash   mkdir templates<br>
Add your HTML form as templates/form.html

### Usage
Starting the Server<br>
bash: uvicorn main:app --reload<br>
The application will be available at http://localhost:8000<br>


Open your browser and go to http://localhost:8000<br>
Paste your call transcript in the text area<br>
Click "Analyze" to get summary and sentiment<br>
Results are displayed on a new page and saved to CSV<br>

