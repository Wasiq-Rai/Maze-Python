class Node:
    def __init__(self, x, y, is_wall):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)