import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None


class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def esVacio(self):
        return self.raiz is None

    def insertar(self, dato):
        if self.raiz is None:
            self.raiz = Nodo(dato)
        else:
            self._insertar(self.raiz, dato)

    def _insertar(self, actual, dato):
        if dato < actual.dato:
            if actual.izq is None:
                actual.izq = Nodo(dato)
            else:
                self._insertar(actual.izq, dato)
        elif dato > actual.dato:
            if actual.der is None:
                actual.der = Nodo(dato)
            else:
                self._insertar(actual.der, dato)

    def mostrar(self, nodo=None, nivel=0):
        if self.raiz is None:
            print("Árbol vacío.")
            return

        if nodo is None:
            nodo = self.raiz

        if nodo.der is not None:
            self.mostrar(nodo.der, nivel + 1)

        print('    ' * nivel + f'[{nodo.dato}]')

        if nodo.izq is not None:
            self.mostrar(nodo.izq, nivel + 1)

    def graficar(self):
        if self.raiz is None:
            print("Árbol vacío.")
            return

        G = nx.DiGraph()
        self._agregar_aristas(G, self.raiz)
        pos = hierarchy_pos(G, self.raiz.dato)
        nx.draw(G, pos, with_labels=True, arrows=False, node_size=1800, node_color="skyblue")
        plt.show()

    def _agregar_aristas(self, G, nodo):
        if nodo is None:
            return
        if nodo.izq:
            G.add_edge(nodo.dato, nodo.izq.dato)
            self._agregar_aristas(G, nodo.izq)
        if nodo.der:
            G.add_edge(nodo.dato, nodo.der.dato)
            self._agregar_aristas(G, nodo.der)

    def buscar(self, dato):
        return self._buscar(self.raiz, dato)

    def _buscar(self, nodo, dato):
        if nodo is None:
            return False
        if nodo.dato == dato:
            return True
        elif dato < nodo.dato:
            return self._buscar(nodo.izq, dato)
        else:
            return self._buscar(nodo.der, dato)

    def preorden(self, nodo):
        if nodo:
            print(nodo.dato, end=" ")
            self.preorden(nodo.izq)
            self.preorden(nodo.der)

    def inorden(self, nodo):
        if nodo:
            self.inorden(nodo.izq)
            print(nodo.dato, end=" ")
            self.inorden(nodo.der)

    def postorden(self, nodo):
        if nodo:
            self.postorden(nodo.izq)
            self.postorden(nodo.der)
            print(nodo.dato, end=" ")

    def eliminar(self, dato, metodo="predecesor"):
        self.raiz = self._eliminar(self.raiz, dato, metodo)

    def _eliminar(self, nodo, dato, metodo):
        if nodo is None:
            return nodo
        if dato < nodo.dato:
            nodo.izq = self._eliminar(nodo.izq, dato, metodo)
        elif dato > nodo.dato:
            nodo.der = self._eliminar(nodo.der, dato, metodo)
        else:
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq
            if metodo == "predecesor":
                max_izq = self._maxValor(nodo.izq)
                nodo.dato = max_izq.dato
                nodo.izq = self._eliminar(nodo.izq, nodo.dato, metodo)
            else:  
                min_der = self._minValor(nodo.der)
                nodo.dato = min_der.dato
                nodo.der = self._eliminar(nodo.der, nodo.dato, metodo)
        return nodo

    def _minValor(self, nodo):
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo

    def _maxValor(self, nodo):
        while nodo.der is not None:
            nodo = nodo.der
        return nodo

    def recorridoNiveles(self):
        if self.raiz is None:
            print("Árbol vacío.")
            return
        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()
            print(actual.dato, end=" ")
            if actual.izq:
                cola.append(actual.izq)
            if actual.der:
                cola.append(actual.der)

    def altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self.altura(nodo.izq), self.altura(nodo.der))

    def contarHojas(self, nodo):
        if nodo is None:
            return 0
        if nodo.izq is None and nodo.der is None:
            return 1
        return self.contarHojas(nodo.izq) + self.contarHojas(nodo.der)

    def contarNodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self.contarNodos(nodo.izq) + self.contarNodos(nodo.der)

    def esCompleto(self, nodo):
        if nodo is None:
            return True
        cola = deque([nodo])
        bandera = False
        while cola:
            actual = cola.popleft()
            if actual.izq:
                if bandera:
                    return False
                cola.append(actual.izq)
            else:
                bandera = True
            if actual.der:
                if bandera:
                    return False
                cola.append(actual.der)
            else:
                bandera = True
        return True

    def esLleno(self, nodo):
        if nodo is None:
            return True
        if nodo.izq is None and nodo.der is None:
            return True
        if nodo.izq is not None and nodo.der is not None:
            return self.esLleno(nodo.izq) and self.esLleno(nodo.der)
        return False

    def eliminarArbol(self):
        self.raiz = None


def hierarchy_pos(G, root, width=1.0, vert_gap=0.3, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.successors(root))
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos, parent=root)
    return pos



if __name__ == "__main__":
    arbol = ArbolBinario()

    while True:
        print("\n=== MENÚ ÁRBOL BINARIO ===")
        print("1. Insertar elemento")
        print("2. Mostrar árbol acostado")
        print("3. Graficar árbol completo")
        print("4. Buscar elemento")
        print("5. Recorrer PreOrden")
        print("6. Recorrer InOrden")
        print("7. Recorrer PostOrden")
        print("8. Eliminar nodo (Predecesor)")
        print("9. Eliminar nodo (Sucesor)")
        print("10. Recorrido por niveles")
        print("11. Altura del árbol")
        print("12. Cantidad de hojas")
        print("13. Cantidad de nodos")
        print("15. Revisar si es completo")
        print("16. Revisar si es lleno")
        print("17. Eliminar árbol")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            dato = int(input("Ingrese el valor a insertar: "))
            arbol.insertar(dato)
        elif opcion == "2":
            arbol.mostrar()
        elif opcion == "3":
            arbol.graficar()
        elif opcion == "4":
            dato = int(input("Dato a buscar: "))
            print("Encontrado" if arbol.buscar(dato) else "No encontrado")
        elif opcion == "5":
            arbol.preorden(arbol.raiz)
            print()
        elif opcion == "6":
            arbol.inorden(arbol.raiz)
            print()
        elif opcion == "7":
            arbol.postorden(arbol.raiz)
            print()
        elif opcion == "8":
            dato = int(input("Nodo a eliminar (predecesor): "))
            arbol.eliminar(dato, "predecesor")
        elif opcion == "9":
            dato = int(input("Nodo a eliminar (sucesor): "))
            arbol.eliminar(dato, "sucesor")
        elif opcion == "10":
            arbol.recorridoNiveles()
            print()
        elif opcion == "11":
            print("Altura:", arbol.altura(arbol.raiz))
        elif opcion == "12":
            print("Hojas:", arbol.contarHojas(arbol.raiz))
        elif opcion == "13":
            print("Nodos:", arbol.contarNodos(arbol.raiz))
        elif opcion == "15":
            print("¿Es completo?:", arbol.esCompleto(arbol.raiz))
        elif opcion == "16":
            print("¿Es lleno?:", arbol.esLleno(arbol.raiz))
        elif opcion == "17":
            arbol.eliminarArbol()
            print("Árbol eliminado.")
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")
