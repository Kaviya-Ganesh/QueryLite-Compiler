# Kaviya SG (23PT18) & Sangamithra SG (23PT30) — Compiler Design Lab, Course 23XT67

from dataclasses import dataclass
from typing import Any, Optional, List

@dataclass
class ColumnNode:
    name: str

@dataclass
class TableNode:
    name: str

@dataclass
class ConditionNode:
    left: ColumnNode
    operator: str
    right: Any

@dataclass
class FilterNode:
    condition: ConditionNode

@dataclass
class ArrangeNode:
    column: ColumnNode
    order: str  # 'ASC' or 'DESC'

@dataclass
class PullNode:
    columns: List[ColumnNode]
    table: TableNode
    filter_node: Optional[FilterNode] = None
    arrange_node: Optional[ArrangeNode] = None
