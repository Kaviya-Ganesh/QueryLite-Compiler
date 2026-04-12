# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

from ast_nodes import PullNode

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self, schema: dict):
        self.schema = schema
        
    def analyze(self, ast: PullNode):
        table_name = ast.table.name
        if table_name not in self.schema:
            raise SemanticError(f"Table '{table_name}' does not exist.")
            
        table_chars = self.schema[table_name]
        
        for col in ast.columns:
            if col.name != '*' and col.name not in table_chars:
                raise SemanticError(f"Column '{col.name}' does not exist in table '{table_name}'.")
                
        if ast.filter_node:
            cond = ast.filter_node.condition
            left_col = cond.left.name
            if left_col not in table_chars:
                raise SemanticError(f"Column '{left_col}' in FILTER does not exist in table '{table_name}'.")
                
            expected_type = table_chars[left_col]
            if not isinstance(cond.right, expected_type):
                # Handle numeric coercions
                try:
                    cond.right = expected_type(cond.right)
                except ValueError:
                    raise SemanticError(f"Type mismatch in FILTER: '{left_col}' expected {expected_type.__name__}, got {type(cond.right).__name__}.")
                    
        if ast.arrange_node:
            arr_col = ast.arrange_node.column.name
            if arr_col not in table_chars:
                 raise SemanticError(f"Column '{arr_col}' in ARRANGE BY does not exist in table '{table_name}'.")
