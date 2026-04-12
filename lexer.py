# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

import re
from typing import NamedTuple, List

class Token(NamedTuple):
    type: str
    value: str

class LexerError(Exception):
    pass

class Lexer:
    TOKENS = [
        ('KEYWORD', r'(?i:\b(?:PULL|FROM|FILTER|ARRANGE|BY|ASC|DESC)\b)'),
        ('OPERATOR', r'==|!=|>=|<=|>|<'),
        ('PUNCTUATION', r'[,;*]'),
        ('LITERAL_STRING', r'"[^"]*"|\'[^\']*\''),
        ('LITERAL_NUMBER', r'\d+(?:\.\d+)?'),
        ('IDENTIFIER', r'[a-zA-Z_]\w*'),
        ('WHITESPACE', r'\s+'),
    ]
    
    def __init__(self, text: str):
        self.text = text
        self.tokens = self._tokenize()
        self.pos = 0

    def _tokenize(self) -> List[Token]:
        tokens = []
        pos = 0
        text = self.text
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKENS)
        get_token = re.compile(tok_regex).match
        
        while pos < len(text):
            match = get_token(text, pos)
            if not match:
                raise LexerError(f'Unexpected character at index {pos}: {text[pos]}')
            type = match.lastgroup
            value = match.group(type)
            if type != 'WHITESPACE':
                if type == 'LITERAL_STRING':
                    value = value[1:-1] # Strip quotes
                elif type == 'KEYWORD':
                    value = value.upper()
                elif type == 'LITERAL_NUMBER':
                    value = float(value) if '.' in value else int(value)
                tokens.append(Token(type, value))
            pos = match.end()
        
        tokens.append(Token('EOF', ''))
        return tokens

    def peek(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def consume(self, expected_type: str = None, expected_value: str = None) -> Token:
        token = self.peek()
        if expected_type and token.type != expected_type:
            raise LexerError(f"Expected type {expected_type}, got {token.type} ({token.value})")
        if expected_value and token.value != expected_value:
            raise LexerError(f"Expected '{expected_value}', got '{token.value}'")
        self.pos += 1
        return token
