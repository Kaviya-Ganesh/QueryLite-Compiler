# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

from ast_nodes import PullNode, FilterNode, ArrangeNode, TableNode, ColumnNode, ConditionNode
from lexer import Lexer, LexerError

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def parse(self) -> PullNode:
        return self.parse_pull()

    def parse_pull(self) -> PullNode:
        self.lexer.consume('KEYWORD', 'PULL')
        
        # Parse columns
        columns = []
        if self.lexer.peek().type == 'PUNCTUATION' and self.lexer.peek().value == '*':
            self.lexer.consume('PUNCTUATION', '*')
            columns.append(ColumnNode('*'))
        else:
            while True:
                tok = self.lexer.consume('IDENTIFIER')
                columns.append(ColumnNode(tok.value))
                if self.lexer.peek().type == 'PUNCTUATION' and self.lexer.peek().value == ',':
                    self.lexer.consume('PUNCTUATION', ',')
                else:
                    break
        
        self.lexer.consume('KEYWORD', 'FROM')
        table_tok = self.lexer.consume('IDENTIFIER')
        table = TableNode(table_tok.value)
        
        filter_node = None
        if self.lexer.peek().type == 'KEYWORD' and self.lexer.peek().value == 'FILTER':
            self.lexer.consume('KEYWORD', 'FILTER')
            left_tok = self.lexer.consume('IDENTIFIER')
            op_tok = self.lexer.consume('OPERATOR')
            
            val_tok = self.lexer.peek()
            if val_tok.type in ('LITERAL_NUMBER', 'LITERAL_STRING'):
                self.lexer.consume()
                right_val = val_tok.value
            else:
                raise ParserError(f"Expected literal in condition, got {val_tok.type}")
                
            condition = ConditionNode(ColumnNode(left_tok.value), op_tok.value, right_val)
            filter_node = FilterNode(condition)
            
        arrange_node = None
        if self.lexer.peek().type == 'KEYWORD' and self.lexer.peek().value == 'ARRANGE':
            self.lexer.consume('KEYWORD', 'ARRANGE')
            self.lexer.consume('KEYWORD', 'BY')
            col_tok = self.lexer.consume('IDENTIFIER')
            
            order = 'ASC'
            if self.lexer.peek().type == 'KEYWORD' and self.lexer.peek().value in ('ASC', 'DESC'):
                order = self.lexer.consume('KEYWORD').value
                
            arrange_node = ArrangeNode(ColumnNode(col_tok.value), order)
            
        self.lexer.consume('PUNCTUATION', ';')
        self.lexer.consume('EOF')
        
        return PullNode(columns, table, filter_node, arrange_node)
