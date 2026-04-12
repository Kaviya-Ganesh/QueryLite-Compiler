# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

import sys
from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from ir import IRGenerator
from optimizer import Optimizer
from executor import Executor

SCHEMA = {
    "users": {
        "name": str,
        "age": int
    },
    "products": {
        "name": str,
        "price": int
    }
}

DATA = {
    "users": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 19}, {"name": "Kaviya", "age": 22}],
    "products": [{"name": "Phone", "price": 300}, {"name": "Laptop", "price": 1200}, {"name": "Tablet", "price": 450}]
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
        print(f"\n[4] IR Tree:\n  {ir}")
        
        optimizer = Optimizer()
        optimized_ir = optimizer.optimize(ir)
        print(f"\n[5] Optimized IR Tree:\n  {optimized_ir}")
        
        executor = Executor(DATA)
        result = executor.execute(optimized_ir)
        print("\n[6] Final Result:")
        print(executor.format_table(result))
        
    except (LexerError, ParserError, SemanticError, Exception) as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")

if __name__ == "__main__":
    queries = [
        "PULL name, age FROM users FILTER age > 21 ARRANGE BY age;",
        "PULL * FROM products FILTER price < 500;",
        "PULL name FROM users FILTER age == 22;"
    ]
    
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        run_query(user_query)
    else:
        for q in queries:
            run_query(q)
            print("-" * 50)
