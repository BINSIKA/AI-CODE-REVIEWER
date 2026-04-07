# AI Code Reviewer

AI Code Reviewer is a student project developed during the Infosys-Springboard Internship.  
It analyzes Python code and provides instant feedback using Groq’s LLaMA 3.1 model.

---

##  Features
- **Syntax Parsing**: Validates Python code using AST.
- **Static Analysis**: Detects unused variables and imports.
- **AI Suggestions**: Explains errors, gives PEP8 style tips, and performance reviews.
- **Frontend**: Dark-themed UI built with Reflex and a standalone HTML page.
- **Backend**: Flask API with `/api/review` endpoint.

---

## 🛠️Tech Stack
- **Frontend**: Reflex, HTML/CSS/JS
- **Backend**: Flask, Python
- **AI Model**: Groq LLaMA 3.1 via `langchain_groq`
- **Other Tools**: AST, dotenv, Flask-CORS

---

## Project Structure
ai_code_reviewer/
│── ai_code_reviewer.py   # Unified backend
│── code_parser.py        # Syntax validation
│── error_detector.py     # Static analysis
│── ai_suggester.py       # AI feedback
│── server.py             # Flask API
│── rxconfig.py           # Reflex config
│── main.py               # Reflex frontend
│── components/           # Navbar, Hero, Footer
│── static/index.html     # Dark-themed frontend
│── requirements.txt      # Dependencies
│── .env                  # Secrets (GROQ_API_KEY)

Code

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/binsika/ai-code-reviewer.git
   cd ai-code-reviewer
Create a virtual environment:

bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
Install dependencies:

bash
pip install -r requirements.txt
Add your Groq API key to .env:

Code
GROQ_API_KEY=your_api_key_here
▶️ Running the Project
Backend (Flask)
bash
python ai_code_reviewer.py
Runs on: http://0.0.0.0:5000

Frontend (HTML)
Open static/index.html in your browser.
It connects to the backend via http://localhost:5000/api/review.

Reflex Frontend
bash
reflex run
**** Usage****
Paste Python code in the editor.

Click Review My Code.

**Get results in 3 steps:**

Syntax Parsing

Static Analysis

AI Teacher Report
