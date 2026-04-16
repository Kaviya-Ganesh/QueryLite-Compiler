# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT62

from ir import IRNode, TableScan, FilterOp, ProjectOp, SortOp

class Executor:
    def __init__(self, data: dict):
        self.data = data

    def execute(self, plan: IRNode):
        return self._eval(plan)

    def _eval(self, node: IRNode):
        if isinstance(node, TableScan):
            return [dict(row) for row in self.data[node.table_name]]
            
        elif isinstance(node, FilterOp):
            child_data = self._eval(node.child)
            return [row for row in child_data if self._matches(row[node.column], node.operator, node.value)]
            
        elif isinstance(node, SortOp):
            child_data = self._eval(node.child)
            reverse = node.order == 'DESC'
            return sorted(child_data, key=lambda x: x[node.column], reverse=reverse)
            
        elif isinstance(node, ProjectOp):
            child_data = self._eval(node.child)
            if '*' in node.columns:
                return child_data
            
            result = []
            for row in child_data:
                result.append({k: row[k] for k in node.columns})
            return result
            
        raise Exception(f"Unknown IRNode {type(node)}")

    def _matches(self, left, op, right):
        if op == '>': return left > right
        elif op == '<': return left < right
        elif op == '==': return left == right
        elif op == '!=': return left != right
        elif op == '>=': return left >= right
        elif op == '<=': return left <= right
        return False

    def format_table(self, rows):
        if not rows:
            return "Empty result set."
            
        keys = list(rows[0].keys())
        widths = {k: len(str(k)) for k in keys}
        for row in rows:
            for k in keys:
                widths[k] = max(widths[k], len(str(row.get(k, ''))))
                
        header = " | ".join(f"{str(k):<{widths[k]}}" for k in keys)
        separator = "-+-".join("-" * widths[k] for k in keys)
        lines = [header, separator]
        for row in rows:
            lines.append(" | ".join(f"{str(row.get(k, '')):<{widths[k]}}" for k in keys))
            
        return "\n".join(lines)
