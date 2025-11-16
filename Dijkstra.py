import sys

def dijkstra(grafo, inicio):
    n = len(grafo)
    dist = [sys.maxsize] * n   
    visitado = [False] * n    
    dist[inicio] = 0          

    for _ in range(n):
        min_dist = sys.maxsize
        u = -1
        for i in range(n):
            if not visitado[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        visitado[u] = True

        for v in range(n):
            if grafo[u][v] != 0 and not visitado[v]:
                if dist[u] + grafo[u][v] < dist[v]:
                    dist[v] = dist[u] + grafo[u][v]

    return dist


grafo = [
    [0, 4, 0, 0],
    [4, 0, 8, 0],
    [0, 8, 0, 7],
    [0, 0, 7, 0]
]

dist = dijkstra(grafo, 0)
print("Distancias desde el nodo 0:", dist)
