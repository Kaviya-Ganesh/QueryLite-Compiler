# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

from ir import IRNode, TableScan, FilterOp, ProjectOp, SortOp

class Optimizer:
    def optimize(self, root: IRNode) -> IRNode:
        root = self._remove_duplicate_projections(root)
        root = self._ensure_filter_before_sort(root)
        return root

    def _remove_duplicate_projections(self, node: IRNode) -> IRNode:
        if isinstance(node, ProjectOp):
            unique_cols = []
            for col in node.columns:
                if col not in unique_cols:
                    unique_cols.append(col)
            node.columns = unique_cols
            node.child = self._remove_duplicate_projections(node.child)
        elif hasattr(node, 'child'):
            node.child = self._remove_duplicate_projections(node.child)
        return node

    def _ensure_filter_before_sort(self, node: IRNode) -> IRNode:
         if isinstance(node, SortOp) and isinstance(node.child, FilterOp):
             filter_node = node.child
             table_scan_node = filter_node.child
             
             # Swap: Filter becomes parent of Sort
             node.child = table_scan_node
             filter_node.child = node
             
             return self._ensure_filter_before_sort(filter_node)
             
         if hasattr(node, 'child'):
             node.child = self._ensure_filter_before_sort(node.child)
             
         return node
