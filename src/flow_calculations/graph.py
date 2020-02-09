import typing
from typing  import List, Dict
import math
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
except ImportError:
    from node import Node, NodeType
    from point import Point
    
# Assumptions:
# There is only one source node
# The source node has the cumulative weight of all other nodes
# The bifurcation node has the cumulative weight of the sources leading to it
# All edges start at source nodes

class Graph:

    def __init__(self) -> None:
        self.edge_map: Dict[Node, Dict[Node, int]] = {}

    def __repr__(self) -> str:
        return str(self.edge_map)
    
    def add_node(self, node: Node) -> None:
        self.edge_map[node] = {}

    def add_edge(self, start: Node, end: Node) -> None:
        self.edge_map[start][end] = start.weight
        if end.node_type == NodeType.BIFURCATION:
            end.weight += start.weight

    def delete_edge(self, start: Node, end: Node) -> None:
        if start in self.edge_map:
            if end in self.edge_map[start]:
                del self.edge_map[start][end]

    def remove_node(self, node: Node) -> None:
        for key in self.edge_map.copy():
            if key == node:
              del self.edge_map[node]
            elif node in self.edge_map[key]:
               del self.edge_map[key][node]

    def get_sink(self):
        for node in self.edge_map:
            if node.node_type == NodeType.SINK:
                return node

    def get_sources(self) -> List[Node]:
        sources: List[Node] = []
        for node in self.edge_map:
            if node.node_type == NodeType.SOURCE:
                sources.append(node)
        return sources

    def get_bifurcations(self) -> List[Node]:
        bifurcations: List[Node] = []
        for node in self.edge_map:
            if node.node_type == NodeType.BIFURCATION:
                bifurcations.append(node)
        return bifurcations

    def get_source_weights(self) -> List[float]:
        sources: List[Node] = self.get_sources()
        return [node.weight for node in sources]

    def get_sink_point(self) -> List[Point]:
        return self.get_sink().point

    def get_source_points(self) -> List[Point]:
        sources: List[Node] = self.get_sources()
        return [node.point for node in sources]
        
    def get_bifurcation_points(self) -> List[Point]:
        bifurcations: List[Node] = self.get_bifurcations()
        return [node.point for node in bifurcations]
