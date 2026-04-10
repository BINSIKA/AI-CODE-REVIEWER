"""
Module 1: code_parser.py
Handles syntax validation for multiple programming languages.
Uses Python's ast module for Python code, and pattern-based
checks for other languages.
"""

import ast
import re


# ─────────────────────────────────────────
#  Python parser (AST-based)
# ─────────────────────────────────────────

def _parse_python(code: str) -> dict:
    """Use Python AST to validate syntax."""
    try:
        tree = ast.parse(code)
        return {
            "status": "success",
            "tree": tree,
            "msg": "✅ Syntax is valid.",
            "errors": [],
        }
    except SyntaxError as e:
        return {
            "status": "error",
            "tree": None,
            "msg": f"❌ Syntax Error (Line {e.lineno}): {e.msg}",
            "errors": [{"line": e.lineno, "msg": str(e.msg)}],
        }
    except Exception as e:
        return {
            "status": "error",
            "tree": None,
            "msg": f"❌ Parse Error: {str(e)}",
            "errors": [{"line": 0, "msg": str(e)}],
        }


# ─────────────────────────────────────────
#  Generic brace/bracket checker
# ─────────────────────────────────────────

def _check_brackets(code: str) -> list:
    """Check for unmatched brackets, parens, braces."""
    errors = []
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    openers = set('([{')
    closers = set(')]}')
    in_string = False
    str_char = ''
    in_line_comment = False

    lines = code.split('\n')
    for line_no, line in enumerate(lines, 1):
        in_line_comment = False
        i = 0
        while i < len(line):
            ch = line[i]
            # Handle line comments for JS/TS/Java/Go/Rust/C/C++
            if not in_string and i + 1 < len(line) and line[i:i+2] == '//':
                break
            # Handle Python comments
            if not in_string and ch == '#':
                break
            # String tracking
            if ch in ('"', "'") and not in_string:
                in_string = True
                str_char = ch
            elif in_string and ch == str_char and (i == 0 or line[i-1] != '\\'):
                in_string = False
            elif not in_string:
                if ch in openers:
                    stack.append((ch, line_no))
                elif ch in closers:
                    if not stack:
                        errors.append({"line": line_no, "msg": f"Unexpected '{ch}'"})
                    elif stack[-1][0] != pairs[ch]:
                        errors.append({"line": line_no, "msg": f"Mismatched '{stack[-1][0]}' and '{ch}'"})
                        stack.pop()
                    else:
                        stack.pop()
            i += 1

    for ch, line_no in stack:
        errors.append({"line": line_no, "msg": f"Unclosed '{ch}'"})

    return errors


# ─────────────────────────────────────────
#  Language-specific lightweight parsers
# ─────────────────────────────────────────

def _parse_generic(code: str, lang: str) -> dict:
    """Generic parser for non-Python languages using bracket checks."""
    errors = _check_brackets(code)

    # Keyword-based pattern checks per language
    if lang in ("javascript", "typescript"):
        for i, line in enumerate(code.split('\n'), 1):
            t = line.strip()
            if t.startswith('//') or not t:
                continue
            # Missing semicolons heuristic (not for blocks)
            if re.search(r'\bvar\s+\w+\s*=\s*.+[^;{,]\s*$', t):
                errors.append({"line": i, "msg": "Possible missing semicolon"})

    if lang == "java":
        for i, line in enumerate(code.split('\n'), 1):
            t = line.strip()
            if not t or t.startswith('//'):
                continue
            if re.match(r'^(public|private|protected)?\s*(static\s+)?\w+\s+\w+\s*\(', t) and not t.endswith('{') and not t.endswith(';'):
                pass  # method signatures without body - ok

    if lang in ("c", "cpp"):
        for i, line in enumerate(code.split('\n'), 1):
            t = line.strip()
            if not t or t.startswith('//') or t.startswith('#'):
                continue
            # Missing semicolons after statements
            if re.match(r'^(return|int|float|double|char|long|short)\s+', t):
                if not t.endswith(';') and not t.endswith('{') and not t.endswith('}'):
                    errors.append({"line": i, "msg": "Possible missing semicolon"})

    status = "success" if not errors else "error"
    msg = "✅ Syntax appears valid." if not errors else f"❌ {len(errors)} syntax issue(s) found."
    return {"status": status, "tree": None, "msg": msg, "errors": errors}


# ─────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────

def validate_syntax(code: str, language: str = "python") -> dict:
    """
    Validate code syntax for supported languages.

    Args:
        code: Source code string.
        language: One of python | javascript | typescript |
                  java | c | cpp | go | rust

    Returns:
        dict with keys: status, tree (Python only), msg, errors
    """
    if not code or not code.strip():
        return {
            "status": "error",
            "tree": None,
            "msg": "❌ No code provided.",
            "errors": [{"line": 0, "msg": "Empty input"}],
        }

    lang = language.lower()

    if lang == "python":
        return _parse_python(code)
    else:
        return _parse_generic(code, lang)


def get_language_display_name(language: str) -> str:
    """Return human-readable language name."""
    names = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "java": "Java",
        "c": "C",
        "cpp": "C++",
        "go": "Go",
        "rust": "Rust",
    }
    return names.get(language.lower(), language.title())


SUPPORTED_LANGUAGES = list({
    "python": True,
    "javascript": True,
    "typescript": True,
    "java": True,
    "c": True,
    "cpp": True,
    "go": True,
    "rust": True,
}.keys())
