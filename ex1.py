# ex1.py
# Uninformed Search Algorithm - BFS

from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

visited = []
queue = deque()

start = 'A'

visited.append(start)
queue.append(start)

print("BFS Traversal:")

while queue:
    node = queue.popleft()
    print(node, end=" ")

    for neighbour in graph[node]:
        if neighbour not in visited:
            visited.append(neighbour)
            queue.append(neighbour)
