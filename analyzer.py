import ast
import autopep8

def syntax_check(code, language):
    if language.lower() == "python":
        try:
            ast.parse(code)
            return "✅ Python syntax valid"
        except Exception as e:
            return f"❌ {e}"
    return "⚠️ Syntax check limited for this language"

def format_code(code, language):
    if language.lower() == "python":
        return autopep8.fix_code(code)
    return code

def calculate_score(code, issues_text):
    score = 100
    if "error" in issues_text.lower():
        score -= 40
    if "warning" in issues_text.lower():
        score -= 20
    score -= min(len(code)//200, 20)
    return max(score, 10)
