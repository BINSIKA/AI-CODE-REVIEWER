import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_review(code, language):
    prompt = f"""
You are an expert code reviewer.

Language: {language}

Give:
1. Bugs
2. Improvements
3. Performance tips
4. Security warnings
5. Final rating out of 100

Code:
{code}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
