# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

from typing import Any, List

class IRNode:
    pass

class TableScan(IRNode):
    def __init__(self, table_name: str):
        self.table_name = table_name

    def __repr__(self):
        return f"TableScan({self.table_name})"

class FilterOp(IRNode):
    def __init__(self, child: IRNode, column: str, operator: str, value: Any):
        self.child = child
        self.column = column
        self.operator = operator
        self.value = value

    def __repr__(self):
        if isinstance(self.value, str):
            val_repr = f"'{self.value}'"
        else:
            val_repr = str(self.value)
        return f"FilterOp({self.column} {self.operator} {val_repr}) -> {self.child}"

class ProjectOp(IRNode):
    def __init__(self, child: IRNode, columns: List[str]):
        self.child = child
        self.columns = columns

    def __repr__(self):
        return f"ProjectOp({', '.join(self.columns)}) -> {self.child}"

class SortOp(IRNode):
    def __init__(self, child: IRNode, column: str, order: str):
        self.child = child
        self.column = column
        self.order = order

    def __repr__(self):
        return f"SortOp({self.column} {self.order}) -> {self.child}"

class IRGenerator:
    def __init__(self, ast):
        self.ast = ast

    def generate(self) -> IRNode:
        node = TableScan(self.ast.table.name)
        
        if self.ast.filter_node:
            cond = self.ast.filter_node.condition
            node = FilterOp(node, cond.left.name, cond.operator, cond.right)
            
        if self.ast.arrange_node:
            node = SortOp(node, self.ast.arrange_node.column.name, self.ast.arrange_node.order)
            
        cols = [c.name for c in self.ast.columns]
        node = ProjectOp(node, cols)
        
        return node
