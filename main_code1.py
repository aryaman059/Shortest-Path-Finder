import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import heapq
import networkx as nx

class Graph:
    def __init__(self):
        self.graph = {}
        self.edges = []

    def add_edge(self, u, v, weight):
        if any((u == a and v == b) or (u == b and v == a) for a, b, w in self.edges):
            return
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
        self.edges.append((u, v, weight))

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.graph}
        previous = {node: None for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return distances, previous

    def shortest_path(self, start, end):
        distances, previous = self.dijkstra(start)
        if distances[end] == float('inf'):
            return [], float('inf')
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        return path, distances[end]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Shortest Path Finder (Dijkstra)")

        self.graph = Graph()

        tk.Label(root, text="Start Point:").grid(row=0, column=0)
        self.start_entry = tk.Entry(root)
        self.start_entry.grid(row=0, column=1)

        tk.Label(root, text="End Point:").grid(row=1, column=0)
        self.end_entry = tk.Entry(root)
        self.end_entry.grid(row=1, column=1)

        tk.Button(root, text="Find Shortest Path", command=self.find_path).grid(row=2, column=0, columnspan=2, pady=5)

        self.output_text = tk.Text(root, height=4, width=45)
        self.output_text.grid(row=3, column=0, columnspan=2)

        tk.Label(root, text="New Edge:").grid(row=4, column=0, pady=(15, 0))
        self.node_u = tk.Entry(root, width=5)
        self.node_u.grid(row=5, column=0, sticky='w', padx=(10, 0))

        self.node_v = tk.Entry(root, width=5)
        self.node_v.grid(row=5, column=0)

        self.weight_entry = tk.Entry(root, width=5)
        self.weight_entry.grid(row=5, column=1, sticky='w', padx=(0, 30))

        tk.Button(root, text="Add Edge", command=self.add_edge).grid(row=5, column=1, sticky='e')
        tk.Button(root, text="Save Graph as Image", command=self.save_graph).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Reset Graph", command=self.reset_graph).grid(row=7, column=0, columnspan=2, pady=5)

        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=10, padx=10, pady=10)

        self.draw_graph()

    def find_path(self):
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        if start not in self.graph.graph or end not in self.graph.graph:
            messagebox.showerror("Error", "Invalid start or end point.")
            return

        path, distance = self.graph.shortest_path(start, end)
        self.output_text.delete(1.0, tk.END)

        if not path or distance == float('inf'):
            self.output_text.insert(tk.END, "No path exists between the selected nodes.")
        else:
            self.output_text.insert(tk.END, f"Path: {' -> '.join(path)}\n")
            self.output_text.insert(tk.END, f"Distance: {distance}")
            self.draw_graph(path)

    def add_edge(self):
        u = self.node_u.get().strip()
        v = self.node_v.get().strip()
        try:
            weight = int(self.weight_entry.get())
            if u and v and u != v:
                self.graph.add_edge(u, v, weight)
                self.draw_graph()
                messagebox.showinfo("Edge Added", f"Edge {u} - {v} ({weight}) added.")
            else:
                messagebox.showerror("Error", "Invalid nodes.")
        except ValueError:
            messagebox.showerror("Error", "Weight must be an integer.")

    def draw_graph(self, path=None):
        self.ax.clear()
        G = nx.Graph()
        for u, v, w in self.graph.edges:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color='lightblue', node_size=800,
         font_size=10)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)

        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, 
        ax=self.ax)

        self.canvas.draw()

    def save_graph(self):
        self.figure.savefig("shortest_path_graph.png")
        messagebox.showinfo("Saved", "Graph saved as 'shortest_path_graph.png'")

    def reset_graph(self):
        self.graph = Graph()
        self.output_text.delete(1.0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.node_u.delete(0, tk.END)
        self.node_v.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.draw_graph()
        messagebox.showinfo("Graph Reset", "Graph has been reset.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
