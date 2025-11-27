import time
import random

def mostrar_paso(paso, lista, comentario=""):
    print(f"   [{paso}] {lista}  <-- {comentario}")

def burbuja(arr, ver_pasos=True):
    lista = arr.copy()
    n = len(lista)
    contador_pasos = 0
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                swapped = True
                contador_pasos += 1
                if ver_pasos:
                    mostrar_paso(contador_pasos, lista, f"Intercambio {lista[j]} y {lista[j+1]}")
        
        if not swapped:
            break
            
    return lista, contador_pasos

def insercion(arr, ver_pasos=True):
    lista = arr.copy()
    contador_pasos = 0
    
    for i in range(1, len(lista)):
        key = lista[i]
        j = i - 1
        moved = False
        
        while j >= 0 and key < lista[j]:
            lista[j + 1] = lista[j]
            j -= 1
            moved = True
            contador_pasos += 1
            
        lista[j + 1] = key
        
        if ver_pasos and moved:
            mostrar_paso(contador_pasos, lista, f"Insertamos {key}")
            
    return lista, contador_pasos

def seleccion(arr, ver_pasos=True):
    lista = arr.copy()
    contador_pasos = 0
    
    for i in range(len(lista)):
        min_idx = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[min_idx]:
                min_idx = j
                
        if min_idx != i:
            lista[i], lista[min_idx] = lista[min_idx], lista[i]
            contador_pasos += 1
            if ver_pasos:
                mostrar_paso(contador_pasos, lista, f"Mínimo encontrado: {lista[i]}")
                
    return lista, contador_pasos

def pedir_numeros_manual():
    try:
        cantidad = int(input("\n¿Cuántos números deseas ingresar? "))
        numeros = []
        print(f"Ingresa los {cantidad} números:")
        for i in range(cantidad):
            num = int(input(f"  Dato {i+1}: "))
            numeros.append(num)
        return numeros, True
    except ValueError:
        print("Error: Solo números enteros.")
        return [], False

def generar_aleatorios_1000():
    print("\nGenerando 1000 números aleatorios...")
    numeros = [random.randint(1, 10000) for _ in range(1000)]
    return numeros, False

def main():
    lista_actual = []
    ver_pasos = True

    while True:
        print("\n==========================================")
        print("   MASTER DE ORDENAMIENTO (3 METODOS)    ")
        print("==========================================")
        print("1. Ingresar números manualmente")
        print("2. Generar 1000 números aleatorios")
        print("3. Salir")
        
        opcion_entrada = input("\nOpcion (1-3): ")

        if opcion_entrada == '3':
            break

        if opcion_entrada == '1':
            resultado_tupla = pedir_numeros_manual()
            lista_actual = resultado_tupla[0]
            ver_pasos = resultado_tupla[1]
        elif opcion_entrada == '2':
            resultado_tupla = generar_aleatorios_1000()
            lista_actual = resultado_tupla[0]
            ver_pasos = resultado_tupla[1]
        else:
            print("Opción no válida.")
            continue

        if not lista_actual:
            continue

        print("\n--- Selecciona el algoritmo ---")
        print("a. Burbuja")
        print("b. Inserción")
        print("c. Selección")
        
        algo = input("Elige (a, b, c): ").lower()
        
        inicio = time.time()
        
        pasos_totales = 0
        
        if algo == 'a':
            
            resultado, pasos_totales = burbuja(lista_actual, ver_pasos)
            metodo = "Burbuja"
        elif algo == 'b':
            resultado, pasos_totales = insercion(lista_actual, ver_pasos)
            metodo = "Inserción"
        elif algo == 'c':
            
            resultado, pasos_totales = seleccion(lista_actual, ver_pasos)
            metodo = "Selección"
        else:
            print("Opción inválida")
            continue
            
        fin = time.time()
        tiempo_total = fin - inicio

        print("-" * 50)
        if ver_pasos:
            print(f"LISTA ORDENADA: {resultado}")
        else:
            print(f"LISTA ORDENADA (Inicio): {resultado[:15]}...")
            print(f"LISTA ORDENADA (Final): ... {resultado[-15:]}")
        
        print(f"\nPASOS TOTALES REALIZADOS: {pasos_totales}")
        print(f"TIEMPO DE EJECUCIÓN ({metodo}): {tiempo_total:.5f} segundos")
        print("-" * 50)
        input("Enter para continuar...")

if __name__ == "__main__":
    main()
