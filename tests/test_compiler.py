# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

import pytest
import sys
import os

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import SCHEMA, DATA
from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from ir import IRGenerator
from optimizer import Optimizer
from executor import Executor

def execute_query(query: str):
    lexer = Lexer(query)
    parser = Parser(lexer)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(SCHEMA)
    analyzer.analyze(ast)
    ir_gen = IRGenerator(ast)
    ir = ir_gen.generate()
    optimizer = Optimizer()
    optimized_ir = optimizer.optimize(ir)
    executor = Executor(DATA)
    return executor.execute(optimized_ir)

def test_query_all_columns():
    query = "PULL * FROM products;"
    result = execute_query(query)
    assert len(result) == 3
    assert result[0] == {"name": "Phone", "price": 300}

def test_query_projection_and_filter():
    query = "PULL name FROM users FILTER age > 21;"
    result = execute_query(query)
    assert len(result) == 2
    names = [r["name"] for r in result]
    assert "Alice" in names
    assert "Kaviya" in names

def test_query_sort():
    query = "PULL name, price FROM products ARRANGE BY price DESC;"
    result = execute_query(query)
    assert len(result) == 3
    assert result[0]["price"] == 1200
    assert result[1]["price"] == 450
    assert result[2]["price"] == 300
    
def test_query_filter_and_sort():
    query = "PULL name, age FROM users FILTER age >= 20 ARRANGE BY age ASC;"
    result = execute_query(query)
    assert len(result) == 2
    assert result[0]["name"] == "Kaviya"
    assert result[1]["name"] == "Alice"

def test_syntax_error():
    query = "PULL name users;" # missing FROM
    with pytest.raises(Exception):
        execute_query(query)

def test_syntax_error_parser():
    query = "PULL name FROM users FILTER;" # missing condition
    with pytest.raises(Exception):
         execute_query(query)

def test_semantic_error_bad_table():
    query = "PULL * FROM nonexistent;"
    with pytest.raises(SemanticError):
        execute_query(query)

def test_semantic_error_bad_column():
    query = "PULL nonexistent_col FROM users;"
    with pytest.raises(SemanticError):
        execute_query(query)

def test_semantic_error_type_mismatch():
    query = 'PULL name FROM users FILTER age == "twenty";'
    with pytest.raises(SemanticError):
        execute_query(query)
