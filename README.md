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

You need Python 3.10+. No external packages are strictly required to run the project, except `pytest` for running tests.

### Starting the Compiler
Run the entry point script:
```bash
python main.py
```
You will be prompted to choose a mode:
- **[1] Terminal mode**: Runs predefined sample queries and outputs the compilation stages in the standard terminal.
- **[2] Web UI mode**: Starts a local HTTP backend server and launches a beautiful, interactive web interface. Open `http://localhost:8080` in your browser.

### Features of the Web UI:
- **Interactive Editor**: Features syntax highlighting for QueryLite keywords, strings, numbers, and operators.
- **Live Pipeline Visualization**: Displays the results of each compiler stage (Result, Tokens, AST, IR, Optimized IR) in separate tabs.
- **Execution Table**: Displays the output of the query successfully executed by the backend executor as a styled data table.
- **Progress Badges**: Real-time animated progress indicators showing the sequential completion of the Lexer, Parser, Semantic Analyzer, and Optimizer modules.
- **No External Dependencies**: Pure vanilla JavaScript, CSS, and Python standard library logic structure.

### Command Line Overrides
**Run an interactive query via CLI:**
```bash
python main.py "PULL name, age FROM users FILTER age > 21 ARRANGE BY age;"
```

**Run the tests:**
```bash
pytest tests/test_compiler.py -v
```
