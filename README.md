# QueryLite Compiler

A fully functional compiler for the custom QueryLite language.

Authors: Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

## Architecture
- **Lexer**: Tokenizes raw query strings using regex.
- **Parser**: A recursive descent parser that validates syntax and builds an Abstract Syntax Tree (AST).
- **Semantic Analyzer**: Validates table names, column names, and types against an in-memory schema.
- **IR Generator**: Maps the AST to a Relational Algebra tree.
- **Optimizer**: Applies basic optimizations.
- **Executor**: Runs the optimized IR against in-memory data and renders a formatted ASCII table.

## Usage

You need Python 3.10+. No external packages are strictly required to run the CLI, except `pytest` for running tests.

**Run predefined examples:**
```bash
python main.py
```

**Run an interactive query:**
```bash
python main.py "PULL name, age FROM users FILTER age > 21 ARRANGE BY age;"
```

**Run the tests:**
```bash
pytest tests/test_compiler.py -v
```
