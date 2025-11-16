def warshall(grafo):
    n = len(grafo)
    alcance = [[grafo[i][j] for j in range(n)] for i in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if alcance[i][k] == 1 and alcance[k][j] == 1:
                    alcance[i][j] = 1

    return alcance


grafo = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

resultado = warshall(grafo)

print("Matriz de alcanzabilidad:")
for fila in resultado:
    print(fila)
