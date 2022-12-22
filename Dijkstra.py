import math


def BuildPath(Parent, s, e):
    path = [e]
    if (e not in Parent):
        return ('пути нет')
    for i in range(len(Parent)):
        if path[i] == s:
            break
        else:
            path.append(Parent[path[i]])
    path.reverse()
    return path


def Dijkstra(G, start, end):
    if len(G) == 0:
        return G
    Distance = {i: math.inf for i in range(len(G))}
    Distance[start] = 0
    Parent = {}
    Q = [i for i in range(len(G))]
    while len(Q) > 0:
        min = math.inf
        minIndex = math.inf
        for i in Q:
            if Distance[i] < min:
                min = Distance[i]
                minIndex = i
        if minIndex == math.inf:
            return []
        u = Q.pop(Q.index(minIndex))
        if u == end:
            return BuildPath(Parent, start, end)
        for v in range(len(G)):
            if G[u][v] == 0:
                continue
            if Distance[v] > Distance[u] + G[u][v]:
                Distance[v] = Distance[u] + G[u][v]
                Parent[v] = u
