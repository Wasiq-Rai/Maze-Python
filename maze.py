import matplotlib.pyplot as plt
import numpy as np

# Define Node class
class Node:
    def __init__(self, x, y, is_wall):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)


class Maze:
    def __init__(self, maze_layout, start_node, end_node, obstacles):
        self.maze_layout = maze_layout
        self.start_node = start_node
        self.end_node = end_node
        self.obstacles = obstacles
        self.nodes = []
        self.create_maze()

    def create_maze(self):
        rows = len(self.maze_layout)
        cols = len(self.maze_layout[0])

        for i in range(rows):
            row = []
            for j in range(cols):
                node = Node(i, j, self.maze_layout[i][j])
                row.append(node)
            self.nodes.append(row)

        for i in range(rows):
            for j in range(cols):
                if not self.nodes[i][j].is_wall:
                    # Connect neighboring nodes (considering diagonal movement)
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            new_x, new_y = i + dx, j + dy
                            if 0 <= new_x < rows and 0 <= new_y < cols and not self.nodes[new_x][new_y].is_wall:
                                self.nodes[i][j].add_neighbor(self.nodes[new_x][new_y])

    def visualize(self, current_path=[]):
        plt.figure(figsize=(len(self.maze_layout[0]), len(self.maze_layout)))

        for i in range(len(self.maze_layout)):
            for j in range(len(self.maze_layout[0])):
                if (i, j) in self.obstacles:  # Obstacle
                    plt.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'red', edgecolor='black', linewidth=1)
                elif (i, j) == self.start_node:  # Start Node
                    plt.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'blue', edgecolor='black', linewidth=1)
                elif (i, j) == self.end_node:  # End Node
                    plt.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'blue', edgecolor='black', linewidth=1)
                elif (i, j) in current_path:  # Current Path
                    plt.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'green', edgecolor='black', linewidth=1)
                else:  # Non-visitable Node
                    plt.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'skyblue', edgecolor='black', linewidth=1)

        # Adding labels
        for i in range(len(self.maze_layout)):
            for j in range(len(self.maze_layout[0])):
                plt.text(j+0.5, len(self.maze_layout)-i-0.5, f'{i},{j}', ha='center', va='center', fontsize=8, fontweight='bold')

        plt.xlim(0, len(self.maze_layout[0]))
        plt.ylim(0, len(self.maze_layout))
        plt.xticks(visible=False)
        plt.yticks(visible=False)

        plt.show()

# Example Usage
maze_layout = [
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0]
]

start_node = (0, 0)
end_node = (4, 5)
obstacles = [(0, 1),(2,1),(3,1), (2, 3), (3, 4), (4,4)]

maze = Maze(maze_layout, start_node, end_node, obstacles)
maze.visualize()
