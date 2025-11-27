import time
import random

# --- FUNCIONES DE IMPRESIÓN ---
def mostrar_paso(paso, lista, comentario=""):
    """Solo imprime si estamos en modo manual (pocos números)"""
    print(f"   [{paso}] {lista}  <-- {comentario}")
    # time.sleep(0.2) # Descomenta si quieres que vaya lento en modo manual

# --- 1. BURBUJA ---
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
                
                if ver_pasos:
                    contador_pasos += 1
                    mostrar_paso(contador_pasos, lista, f"Intercambio {lista[j]} y {lista[j+1]}")
        
        if not swapped:
            break
            
    return lista

# --- 2. INSERCIÓN ---
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
            
        lista[j + 1] = key
        
        if ver_pasos:
            contador_pasos += 1
            if moved:
                mostrar_paso(contador_pasos, lista, f"Insertamos {key}")
            
    return lista

# --- 3. SELECCIÓN ---
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
            if ver_pasos:
                contador_pasos += 1
                mostrar_paso(contador_pasos, lista, f"Mínimo encontrado: {lista[i]}")
                
    return lista

# --- GENERADORES DE LISTAS ---
def pedir_numeros_manual():
    try:
        cantidad = int(input("\n¿Cuántos números deseas ingresar? "))
        numeros = []
        print(f"Ingresa los {cantidad} números:")
        for i in range(cantidad):
            num = int(input(f"  Dato {i+1}: "))
            numeros.append(num)
        return numeros, True  # True activa el "ver_pasos"
    except ValueError:
        print("❌ Error: Solo números enteros.")
        return [], False

def generar_aleatorios_1000():
    print("\n🎲 Generando 1000 números aleatorios entre 1 y 10,000...")
    # Crea una lista de 1000 números al azar
    numeros = [random.randint(1, 10000) for _ in range(1000)]
    print(f"Listos (Primeros 10: {numeros[:10]}...)")
    return numeros, False # False desactiva "ver_pasos" para no saturar

# --- MENÚ PRINCIPAL ---
def main():
    lista_actual = []
    ver_pasos = True

    while True:
        print("\n==========================================")
        print("   MASTER DE ORDENAMIENTO (ALGORITMOS)    ")
        print("==========================================")
        print("1. Ingresar números manualmente (Paso a paso)")
        print("2. Generar 1000 números aleatorios (Prueba de velocidad)")
        print("3. Salir")
        
        opcion_entrada = input("\n👉 ¿Qué deseas hacer? (1-3): ")

        if opcion_entrada == '3':
            print("¡Adiós!")
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

        # Sub-menú para elegir algoritmo
        print("\n--- Selecciona el algoritmo para ordenar ---")
        print("a. Burbuja")
        print("b. Inserción")
        print("c. Selección")
        
        algo = input("👉 Elige (a, b, c): ").lower()
        
        inicio = time.time() # Iniciamos cronómetro
        
        if algo == 'a':
            resultado = burbuja(lista_actual, ver_pasos)
            metodo = "Burbuja"
        elif algo == 'b':
            resultado = insercion(lista_actual, ver_pasos)
            metodo = "Inserción"
        elif algo == 'c':
            resultado = seleccion(lista_actual, ver_pasos)
            metodo = "Selección"
        else:
            print("Opción inválida")
            continue
            
        fin = time.time() # Paramos cronómetro
        tiempo_total = fin - inicio

        print("-" * 50)
        if ver_pasos:
            print(f"✅ LISTA ORDENADA: {resultado}")
        else:
            # Si son 1000, solo mostramos una parte para no llenar la pantalla
            print(f"✅ LISTA ORDENADA (Mostrando primeros 20): {resultado[:20]} ...")
            print(f"✅ LISTA ORDENADA (Mostrando últimos 20): ... {resultado[-20:]}")
        
        print(f"\n⏱️  TIEMPO DE EJECUCIÓN ({metodo}): {tiempo_total:.5f} segundos")
        print("-" * 50)
        input("Presiona ENTER para continuar...")

if __name__ == "__main__":
    main()