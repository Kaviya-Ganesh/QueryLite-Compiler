# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT62

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import traceback

from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from ir import IRGenerator
from optimizer import Optimizer
from executor import Executor
from main import SCHEMA, DATA

class RequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/static/index.html'
        
        try:
            # Prevent path traversal
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.abspath(os.path.join(base_dir, self.path.lstrip('/')))
            if not file_path.startswith(base_dir):
                self.send_error(403)
                return
                
            with open(file_path, 'rb') as f:
                content = f.read()
                
            self.send_response(200)
            if self.path.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif self.path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif self.path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/compile':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request = json.loads(post_data.decode('utf-8'))
                query = request.get('query', '')
                
                response_data = self.run_pipeline(query)
                status_code = 200
            except Exception as e:
                response_data = {"error": f"{type(e).__name__}: {str(e)}"}
                status_code = 200 # Send 200 so fontend can display inline
                
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def run_pipeline(self, query: str):
        lexer = Lexer(query)
        tokens_list = [{"type": tok.type, "value": tok.value} for tok in lexer.tokens]
        
        # Reset lexer for parser
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
        result = executor.execute(optimized_ir)
        
        return {
            "tokens": tokens_list,
            "ast": str(ast),
            "ir": str(ir),
            "optimized_ir": str(optimized_ir),
            "result": result
        }

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"QueryLite Compiler UI → http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("\nServer stopped.")

if __name__ == '__main__':
    run_server()
