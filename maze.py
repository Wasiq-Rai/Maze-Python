import matplotlib.pyplot as plt
import heapq

class Node:
    def __init__(self, x, y, is_wall):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.neighbors = []
        self.parent = None
        self.g = float('inf')  # Cost from start node to current node
        self.h = float('inf')  # Heuristic estimate to goal node

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __lt__(self, other):
        # Compare nodes based on their f value (f = g + h)
        return (self.g + self.h) < (other.g + other.h)

class Maze:
    def __init__(self, maze_layout, start_node, end_node, obstacles):
        self.maze_layout = maze_layout
        self.start_node = start_node
        self.end_node = end_node
        self.obstacles = obstacles
        self.nodes = []
        self.visited = set()  # Keep track of visited nodes
        self.open_set = []  # Nodes to be explored
        self.closed_set = set()  # Nodes already explored
        self.create_maze()

    def create_maze(self):
        rows = len(self.maze_layout)
        cols = len(self.maze_layout[0])

        for i in range(rows):
            row = []
            for j in range(cols):
                is_wall = (i, j) in self.obstacles
                node = Node(i, j, is_wall)
                row.append(node)
            self.nodes.append(row)

        for i in range(rows):
            for j in range(cols):
                if not self.nodes[i][j].is_wall:
                    # Connect neighboring nodes (considering only right, left, up, and down movements)
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_x, new_y = i + dx, j + dy
                        if 0 <= new_x < rows and 0 <= new_y < cols and not self.nodes[new_x][new_y].is_wall:
                            self.nodes[i][j].add_neighbor(self.nodes[new_x][new_y])

    def heuristic(self, node):
        # Define heuristic function (Manhattan distance)
        return abs(node.x - self.end_node[0]) + abs(node.y - self.end_node[1])

    def A_star_algorithm(self):
        start_node = self.nodes[self.start_node[0]][self.start_node[1]]
        end_node = self.nodes[self.end_node[0]][self.end_node[1]]
        start_node.g = 0
        start_node.h = self.heuristic(start_node)
        heapq.heappush(self.open_set, start_node)

        while self.open_set:
            current_node = heapq.heappop(self.open_set)

            if current_node == end_node:
                print("Success! Shortest path found.")
                return self.reconstruct_path(current_node)

            self.closed_set.add(current_node)

            for neighbor in current_node.neighbors:
                if neighbor in self.closed_set or neighbor.is_wall:
                    continue

                tentative_g = current_node.g + 1  # Cost from start to neighbor is always 1 in this case

                if tentative_g < neighbor.g:
                    neighbor.parent = current_node
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(neighbor)
                    heapq.heappush(self.open_set, neighbor)

        print("Failed to find a path.")
        return []

    def reconstruct_path(self, current_node):
        path = []
        while current_node:
            path.insert(0, (current_node.x, current_node.y))  # Insert at the beginning to maintain order
            current_node = current_node.parent
        return path

    def visualize(self, current_path, ax):
        ax.clear()

        for i in range(len(self.maze_layout)):
            for j in range(len(self.maze_layout[0])):
                if (i, j) in self.obstacles:  # Obstacle
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'red', edgecolor='black', linewidth=1)
                elif (i, j) == self.start_node:  # Start Node
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'blue', edgecolor='black', linewidth=1)
                elif (i, j) == self.end_node:  # End Node
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'blue', edgecolor='black', linewidth=1)
                elif (i, j) in current_path:  # Current Path
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'green', edgecolor='black', linewidth=1)
                else:  # Non-visitable Node
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'skyblue', edgecolor='black', linewidth=1)

        
        # Adding labels
        for i in range(len(self.maze_layout)):
            for j in range(len(self.maze_layout[0])):
                ax.text(j+0.5, len(self.maze_layout)-i-0.5, f'{i},{j}', ha='center', va='center', fontsize=8, fontweight='bold')

        ax.set_xlim(0, len(self.maze_layout[0]))
        ax.set_ylim(0, len(self.maze_layout))
        ax.set_xticks([])
        ax.set_yticks([])
        plt.draw()  # Update the plot without closing the window
        plt.pause(0.1)  # Pause to display the plot

class MazeSolver:
    def __init__(self, maze_layout, start_node, end_node, obstacles):
        self.maze = Maze(maze_layout, start_node, end_node, obstacles)
        self.fig, self.ax = plt.subplots()

    def solve(self):
        shortest_path = self.maze.A_star_algorithm()
        if shortest_path:
            print("Shortest Path:", shortest_path)
        self.maze.visualize(shortest_path, self.ax)
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
obstacles = [(0, 1),(1,3),(2, 1), (3, 1), (2, 3), (3, 4) ]

solver = MazeSolver(maze_layout, start_node, end_node, obstacles)
solver.solve()
