def find(padre, x):
    if padre[x] == x:
        return x
    return find(padre, padre[x])

def union(padre, rank, x, y):
    raiz_x = find(padre, x)
    raiz_y = find(padre, y)

    if raiz_x != raiz_y:
        if rank[raiz_x] < rank[raiz_y]:
            padre[raiz_x] = raiz_y
        elif rank[raiz_x] > rank[raiz_y]:
            padre[raiz_y] = raiz_x
        else:
            padre[raiz_y] = raiz_x
            rank[raiz_x] += 1


def kruskal(grafo):
    aristas = []
    for u in range(len(grafo)):
        for v in range(u + 1, len(grafo)):
            if grafo[u][v] != 0:
                aristas.append((grafo[u][v], u, v))

    aristas.sort()

    n = len(grafo)
    padre = [i for i in range(n)]
    rank = [0] * n
    mst = []

    for peso, u, v in aristas:
        if find(padre, u) != find(padre, v):
            mst.append((u, v, peso))
            union(padre, rank, u, v)

    return mst


grafo = [
    [0, 4, 0, 0],
    [4, 0, 8, 0],
    [0, 8, 0, 7],
    [0, 0, 7, 0]
]

resultado = kruskal(grafo)
print("Árbol de Expansión Mínima (MST):")
for arista in resultado:
    print(arista)
