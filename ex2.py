# ex2.py
# Informed Search Algorithm - A*

graph = {
    'A': {'B': 1, 'C': 3},
    'B': {'D': 1, 'E': 5},
    'C': {'F': 2},
    'D': {},
    'E': {},
    'F': {}
}

heuristic = {
    'A': 6,
    'B': 4,
    'C': 2,
    'D': 0,
    'E': 0,
    'F': 0
}

open_list = ['A']
closed_list = []
g = {'A': 0}
parent = {'A': 'A'}

goal = 'F'

while open_list:
    n = open_list[0]

    for v in open_list:
        if g[v] + heuristic[v] < g[n] + heuristic[n]:
            n = v

    if n == goal:
        path = []
        while parent[n] != n:
            path.append(n)
            n = parent[n]
        path.append('A')
        path.reverse()
        print("Path found:", path)
        break

    for m in graph[n]:
        cost = graph[n][m]

        if m not in open_list and m not in closed_list:
            open_list.append(m)
            parent[m] = n
            g[m] = g[n] + cost

    open_list.remove(n)
    closed_list.append(n)
