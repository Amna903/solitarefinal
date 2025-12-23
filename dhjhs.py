import networkx as nx
import matplotlib.pyplot as plt
import random

class MazeGraph:
    def __init__(self, rows, cols):
        self.graph = nx.Graph()
        self.rows = rows
        self.cols = cols
        self.create_nodes()
        self.generate_maze()

    def create_nodes(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.graph.add_node((row, col))

    def generate_maze(self):
        # Create a list of all edges in the grid
        edges = []
        for row in range(self.rows):
            for col in range(self.cols):
                if row < self.rows - 1:  # Vertical edge
                    edges.append(((row, col), (row + 1, col)))
                if col < self.cols - 1:  # Horizontal edge
                    edges.append(((row, col), (row, col + 1)))
        
        # Randomize edges to create maze paths
        random.shuffle(edges)

        # Use a disjoint-set data structure to ensure no cycles (Kruskal's algorithm)
        parent = {}
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)
            if root1 != root2:
                parent[root2] = root1

        for node in self.graph.nodes:
            parent[node] = node

        for edge in edges:
            node1, node2 = edge
            if find(node1) != find(node2):  # No cycle
                self.graph.add_edge(node1, node2)
                union(node1, node2)

    def draw_maze(self):
        pos = {(row, col): (col, -row) for row, col in self.graph.nodes}
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_color='black')
        plt.show()

# Usage
rows, cols = 4, 4  # Adjust the grid size here
maze = MazeGraph(rows, cols)
maze.draw_maze()
