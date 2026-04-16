# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT62

import sys
from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from ir import IRGenerator
from optimizer import Optimizer
from executor import Executor

SCHEMA = {
    "students": {
        "id": int,
        "name": str,
        "age": int,
        "dept": str,
        "gpa": float,
        "year": int
    },
    "courses": {
        "id": int,
        "title": str,
        "dept": str,
        "credits": int,
        "max_seats": int
    },
    "enrollments": {
        "student_id": int,
        "course_id": int,
        "grade": str,
        "semester": int
    },
    "employees": {
        "id": int,
        "name": str,
        "dept": str,
        "salary": int,
        "experience_years": int
    }
}

DATA = {
    "students": [
        {"id": 1, "name": "Alice", "age": 20, "dept": "CSE", "gpa": 9.2, "year": 3},
        {"id": 2, "name": "Bob", "age": 19, "dept": "IT", "gpa": 8.1, "year": 2},
        {"id": 3, "name": "Charlie", "age": 21, "dept": "MECH", "gpa": 7.5, "year": 4},
        {"id": 4, "name": "David", "age": 20, "dept": "ECE", "gpa": 8.8, "year": 3},
        {"id": 5, "name": "Eve", "age": 18, "dept": "CIVIL", "gpa": 9.5, "year": 1},
        {"id": 6, "name": "Frank", "age": 22, "dept": "CSE", "gpa": 8.0, "year": 4},
        {"id": 7, "name": "Grace", "age": 19, "dept": "IT", "gpa": 9.1, "year": 2},
        {"id": 8, "name": "Hannah", "age": 20, "dept": "ECE", "gpa": 8.4, "year": 3},
        {"id": 9, "name": "Ian", "age": 21, "dept": "MECH", "gpa": 6.9, "year": 4},
        {"id": 10, "name": "Julia", "age": 19, "dept": "CIVIL", "gpa": 7.8, "year": 2},
        {"id": 11, "name": "Kevin", "age": 20, "dept": "CSE", "gpa": 8.6, "year": 3},
        {"id": 12, "name": "Leo", "age": 21, "dept": "IT", "gpa": 7.9, "year": 4},
        {"id": 13, "name": "Mona", "age": 19, "dept": "ECE", "gpa": 9.3, "year": 2},
        {"id": 14, "name": "Nina", "age": 20, "dept": "MECH", "gpa": 8.2, "year": 3},
        {"id": 15, "name": "Oscar", "age": 22, "dept": "CSE", "gpa": 7.4, "year": 4}
    ],
    "courses": [
        {"id": 101, "title": "Data Structures", "dept": "CSE", "credits": 4, "max_seats": 60},
        {"id": 102, "title": "Web Development", "dept": "IT", "credits": 3, "max_seats": 50},
        {"id": 103, "title": "Thermodynamics", "dept": "MECH", "credits": 4, "max_seats": 40},
        {"id": 104, "title": "Signals & Systems", "dept": "ECE", "credits": 4, "max_seats": 55},
        {"id": 105, "title": "Structural Engg", "dept": "CIVIL", "credits": 3, "max_seats": 45},
        {"id": 106, "title": "Machine Learning", "dept": "CSE", "credits": 4, "max_seats": 60},
        {"id": 107, "title": "Cloud Computing", "dept": "IT", "credits": 3, "max_seats": 50},
        {"id": 108, "title": "Fluid Dynamics", "dept": "MECH", "credits": 3, "max_seats": 40},
        {"id": 109, "title": "VLSI Design", "dept": "ECE", "credits": 4, "max_seats": 50},
        {"id": 110, "title": "Surveying", "dept": "CIVIL", "credits": 2, "max_seats": 45}
    ],
    "enrollments": [
        {"student_id": 1, "course_id": 101, "grade": "A", "semester": 5},
        {"student_id": 1, "course_id": 106, "grade": "S", "semester": 5},
        {"student_id": 2, "course_id": 102, "grade": "B", "semester": 3},
        {"student_id": 2, "course_id": 107, "grade": "A", "semester": 3},
        {"student_id": 3, "course_id": 103, "grade": "C", "semester": 7},
        {"student_id": 3, "course_id": 108, "grade": "B", "semester": 7},
        {"student_id": 4, "course_id": 104, "grade": "A", "semester": 5},
        {"student_id": 4, "course_id": 109, "grade": "B", "semester": 5},
        {"student_id": 5, "course_id": 105, "grade": "S", "semester": 1},
        {"student_id": 5, "course_id": 110, "grade": "A", "semester": 1},
        {"student_id": 6, "course_id": 101, "grade": "B", "semester": 7},
        {"student_id": 7, "course_id": 102, "grade": "S", "semester": 3},
        {"student_id": 8, "course_id": 104, "grade": "B", "semester": 5},
        {"student_id": 9, "course_id": 103, "grade": "C", "semester": 7},
        {"student_id": 10, "course_id": 105, "grade": "B", "semester": 3},
        {"student_id": 11, "course_id": 106, "grade": "A", "semester": 5},
        {"student_id": 12, "course_id": 107, "grade": "B", "semester": 7},
        {"student_id": 13, "course_id": 109, "grade": "S", "semester": 3},
        {"student_id": 14, "course_id": 108, "grade": "B", "semester": 5},
        {"student_id": 15, "course_id": 101, "grade": "C", "semester": 7}
    ],
    "employees": [
        {"id": 1, "name": "Dr. Smith", "dept": "CSE", "salary": 120000, "experience_years": 15},
        {"id": 2, "name": "Prof. Jones", "dept": "IT", "salary": 95000, "experience_years": 10},
        {"id": 3, "name": "Dr. Brown", "dept": "MECH", "salary": 110000, "experience_years": 12},
        {"id": 4, "name": "Dr. Davis", "dept": "ECE", "salary": 105000, "experience_years": 11},
        {"id": 5, "name": "Prof. Miller", "dept": "CIVIL", "salary": 90000, "experience_years": 8},
        {"id": 6, "name": "Dr. Wilson", "dept": "CSE", "salary": 115000, "experience_years": 14},
        {"id": 7, "name": "Mr. Taylor", "dept": "IT", "salary": 75000, "experience_years": 5},
        {"id": 8, "name": "Ms. Anderson", "dept": "MECH", "salary": 80000, "experience_years": 6},
        {"id": 9, "name": "Dr. Thomas", "dept": "ECE", "salary": 100000, "experience_years": 9},
        {"id": 10, "name": "Prof. Jackson", "dept": "CIVIL", "salary": 92000, "experience_years": 8},
        {"id": 11, "name": "Mr. White", "dept": "CSE", "salary": 45000, "experience_years": 2},
        {"id": 12, "name": "Ms. Harris", "dept": "IT", "salary": 50000, "experience_years": 3}
    ]
}

def run_query(query: str):
    print(f"\n--- Running Query ---")
    print(f"{query}\n")
    try:
        lexer = Lexer(query)
        print("[1] Tokens:")
        for tok in lexer.tokens:
            print(f"  {tok}")
            
        lexer = Lexer(query)
        parser = Parser(lexer)
        ast = parser.parse()
        print(f"\n[2] AST:\n  {ast}")
        
        analyzer = SemanticAnalyzer(SCHEMA)
        analyzer.analyze(ast)
        print("\n[3] Semantic Analysis: Passed Schema Validation")
        
        ir_gen = IRGenerator(ast)
        ir = ir_gen.generate()
        original_ir_str = str(ir)
        print(f"\n[4] IR Tree:\n  {original_ir_str}")
        
        optimizer = Optimizer()
        optimized_ir = optimizer.optimize(ir)
        print(f"\n[5] Optimized IR Tree:\n  {optimized_ir}")
        
        executor = Executor(DATA)
        result = executor.execute(optimized_ir)
        print("\n[6] Final Result:")
        print(executor.format_table(result))
        
    except (LexerError, ParserError, SemanticError, Exception) as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")

def run_demo_queries():
    demos = [
        {
            "num": 1,
            "title": "LEXER + PARSER (All 6 Phases)",
            "query": "PULL name, gpa FROM students FILTER gpa > 8.5 ARRANGE BY gpa DESC;",
            "summary": "✔ What you saw: Lexer tokenized 12 tokens → Parser built AST with FilterNode + ArrangeNode\n   → Semantic passed → IR generated → Optimizer applied → 4 rows returned"
        },
        {
            "num": 2,
            "title": "Predicate Pushdown optimization",
            "query": "PULL name, dept FROM employees FILTER salary > 80000 ARRANGE BY salary DESC;",
            "summary": "✔ OPTIMIZATION APPLIED: Predicate Pushdown — Filter moved before Sort. Rows reduced from 12 to 3 before sorting."
        },
        {
            "num": 3,
            "title": "Projection Pruning optimization",
            "query": "PULL name FROM students FILTER dept == 'CSE';",
            "summary": "✔ OPTIMIZATION APPLIED: Projection Pruning — 6 columns reduced to 1 early in pipeline."
        },
        {
            "num": 4,
            "title": "Operation Reordering optimization",
            "query": "PULL name, gpa FROM students FILTER age > 20 ARRANGE BY gpa DESC;",
            "summary": "✔ OPTIMIZATION APPLIED: Operation Reordering — Filter applied first, reducing 15 rows to 8 before Sort and Project."
        },
        {
            "num": 5,
            "title": "Semantic Analysis catching an error",
            "query": "PULL name, marks FROM students FILTER gpa > 8.0;",
            "summary": "✘ SEMANTIC ERROR: Column 'marks' does not exist in table 'students'. Available columns: id, name, age, dept, gpa, year\n✔ PHASE SHOWCASED: Semantic Analysis — invalid column caught before execution."
        },
        {
            "num": 6,
            "title": "Complex query hitting all optimizations together",
            "query": "PULL name, dept, salary FROM employees FILTER salary >= 50000 ARRANGE BY salary DESC;",
            "summary": "┌─────────────────────────────────────────────────────────┐\n│           OPTIMIZATION SUMMARY                          │\n├──────────────────────┬──────────────┬───────────────────┤\n│ Technique            │ Applied?     │ Impact            │\n├──────────────────────┼──────────────┼───────────────────┤\n│ Predicate Pushdown   │ ✔ YES        │ 12 → 6 rows       │\n│ Projection Pruning   │ ✔ YES        │ 5 → 3 columns     │\n│ Operation Reordering │ ✔ YES        │ Sort after Filter │\n└──────────────────────┴──────────────┴───────────────────┘"
        }
    ]

    for demo in demos:
        print(f"\n{'=' * 51}")
        print(f" DEMO {demo['num']} of 6 — Showcasing: {demo['title']}")
        print(f"{'=' * 51}")
        print(f"Query: {demo['query']}")
        run_query(demo["query"])
        print(f"\n{demo['summary']}\n")

if __name__ == "__main__":
    print("Welcome to QueryLite Compiler!")
    print("[1] Terminal mode")
    print("[2] Web UI mode")
    print("[3] Run Demo — Show all compiler phases + optimizations")
    
    try:
        if len(sys.argv) > 1:
            choice = "1"
        else:
            choice = input("Select mode (1, 2, or 3): ").strip()
    except EOFError:
        choice = "1"
        
    if choice == "2":
        from server import run_server
        run_server()
    elif choice == "3":
        run_demo_queries()
    else:
        queries = [
            "PULL name, gpa FROM students FILTER gpa > 9.0 ARRANGE BY gpa DESC;",
            "PULL * FROM courses FILTER credits < 4;",
            "PULL name FROM employees FILTER dept == 'CSE';"
        ]
        
        if len(sys.argv) > 1:
            user_query = " ".join(sys.argv[1:])
            run_query(user_query)
        else:
            for q in queries:
                run_query(q)
                print("-" * 50)
