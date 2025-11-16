import sys

def floyd(grafo):
    n = len(grafo)
    dist = [[grafo[i][j] for j in range(n)] for i in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


INF = sys.maxsize
grafo = [
    [0,   4,   INF, INF],
    [4,   0,   8,   INF],
    [INF, 8,   0,   7],
    [INF, INF, 7,   0]
]

resultado = floyd(grafo)

print("Matriz de distancias más cortas entre todos los nodos:")
for fila in resultado:
    print(fila)
