**Milestone 1 – Syntax Validation & Parsing**

This project is a Python utility that validates Python source code using Python’s built-in AST (Abstract Syntax Tree) module. It checks whether the code is syntactically valid and, if so, returns a cleaned and standardized version of the code.

**Features**

  Validates Python syntax safely using ast.parse

  Identifies and reports syntax errors with line and offset information

  Automatically reformats valid code using ast.unparse

  Does not rely on any external libraries (pure Python standard library)

**How It Work**

  Takes Python source code as a string input

  Parses the source code into an Abstract Syntax Tree

  If parsing is successful:

          Returns a cleaned version of the source code

If parsing fails:

          Returns a clear syntax error message with location information

**Milestone 2 – Error & Bug Detection**

**Code Parser (code_parser.py):** Acts as a scanner to convert code strings into an Abstract Syntax Tree (AST). It validates syntax and prepares the code  for analysis.

**Error Detector (error_detector.py):** Uses an ast.NodeVisitor to "walk" through the tree and identify logical errors. It tracks ast.Store  and ast.Load 
to find unused variables or imports.

**AI Suggester (ai_suggester.py):** Uses the GPT API to provide intelligent explanations for errors. It suggests optimizations for time and space complexity and encourages better coding style.

**Key Outcomes**
  Identify syntax and logical errors automatically.
  Detect unused variables by comparing definitions against usages.
  Provide instant, human-like feedback on code performance and style.

