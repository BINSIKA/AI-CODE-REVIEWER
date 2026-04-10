"""
analyzer.py
Orchestrates the full analysis pipeline:
  1. code_parser   → syntax validation
  2. error_detector → static analysis
  3. ai_suggester  → AI review via Groq LLaMA
"""

from code_parser import validate_syntax, get_language_display_name
from error_detector import get_static_errors, calculate_quality_grade, get_linter_tools
from ai_suggester import AISuggester

# Shared AI instance (avoid re-initialising on every request)
_ai = AISuggester()


def run_full_analysis(code: str, language: str = "python") -> dict:
    """
    Run the complete 3-step code review pipeline.

    Args:
        code:     Source code string submitted by the user.
        language: Target language (default: python).

    Returns:
        dict containing all analysis results.
    """
    lang = language.lower()
    lang_display = get_language_display_name(lang)

    # ── Step 1: Syntax Parsing ───────────────────────────────────
    parse_result = validate_syntax(code, lang)
    syntax_ok = parse_result["status"] == "success"

    # ── Step 2: Static Analysis ──────────────────────────────────
    static = get_static_errors(
        tree=parse_result.get("tree"),
        code=code,
        language=lang,
    )

    # Combine syntax errors + static issues for total count
    all_issues: list[dict] = []

    # Add syntax errors first
    for err in parse_result.get("errors", []):
        all_issues.append({
            "text": err["msg"],
            "line": err.get("line", 0),
            "severity": "error",
        })

    all_issues.extend(static["issues"])

    issue_count = len(all_issues)
    grade = calculate_quality_grade(issue_count)

    # Flatten static issues as plain strings for the AI prompt
    static_strings = [
        f"Line {i['line']}: {i['text']}" for i in all_issues
    ]

    # ── Step 3: AI Analysis ──────────────────────────────────────
    ai_report = _ai.generate_report(code, lang_display, static_strings)

    # ── Build full response ──────────────────────────────────────
    return {
        # Meta
        "language": lang,
        "language_display": lang_display,

        # Syntax
        "syntax_status": parse_result["status"],
        "syntax_msg": parse_result["msg"],
        "syntax_errors": parse_result.get("errors", []),

        # Static
        "unused_imports": static["unused_imports"],
        "unused_functions": static["unused_functions"],
        "unused_variables": static["unused_variables"],
        "style_violations": static["style_violations"],
        "created_vars": static.get("created_vars", []),
        "used_vars": static.get("used_vars", []),
        "linter_tools": get_linter_tools(lang),

        # Combined issues
        "issues": all_issues,
        "issue_count": issue_count,
        "grade": grade,

        # AI
        "summary": ai_report.get("summary", ""),
        "corrected_code": ai_report.get("corrected_code", code),
        "optimizations": ai_report.get("optimizations", []),
        "detected_bugs": ai_report.get("detected_bugs", []),
    }


def run_chat(user_message: str, context: str = "", history: list = None) -> str:
    """
    Send a chat message to the AI assistant with analysis context.
    """
    return _ai.chat_message(user_message, context, history or [])
