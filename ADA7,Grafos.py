import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
from math import radians, cos, sin, asin, sqrt
import random

sys.setrecursionlimit(2000)


ventana = tk.Tk()
ventana.title("Grafo Interactivo - Mapa de México")
ventana.geometry("1100x700")

# Crear figura con Basemap
fig, ax = plt.subplots(figsize=(7, 6))
# Configuración de Basemap para México
m = Basemap(projection="merc", llcrnrlon=-118, llcrnrlat=14,
            urcrnrlon=-86, urcrnrlat=33, resolution="i", ax=ax)

canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# -------------------------------
# DATOS BASE
# -------------------------------
estados_coords = {
    "BCN": (32.5, -115.5), "BCS": (24.0, -111.7), 
    "SON": (29.1, -110.9), "CHI": (28.6, -106.1), 
    "COA": (27.0, -102.0), "NLE": (25.7, -100.3), 
    "TAM": (24.3, -98.7), "SIN": (25.8, -108.0), 
    "DUR": (24.0, -104.7), "ZAC": (22.8, -102.6), 
    "SLP": (22.2, -100.9), "NAY": (21.8, -104.9), 
    "JAL": (20.7, -103.3), "COL": (19.2, -103.7), 
    "MIC": (19.7, -101.2), "GUA": (20.9, -101.3), 
    "QUE": (20.6, -100.4), "HID": (20.1, -98.7), 
    "VER": (19.2, -96.1), "PUE": (19.0, -98.2), 
    "TLA": (19.3, -98.2), "CDMX": (19.4, -99.1), 
    "MOR": (18.9, -99.2), "GUE": (17.5, -99.5), 
    "OAX": (17.1, -96.7), "CHP": (16.7, -93.1), 
    "TAB": (17.9, -92.6), "CAM": (19.8, -90.5), 
    "YUC": (20.9, -89.0), "ROO": (19.6, -88.0), 
    "AGS": (21.9, -102.3)
}

# -------------------------------
# GRAFO Y VARIABLES
# -------------------------------
grafo = nx.Graph()
posiciones = {} # Coordenadas proyectadas del mapa
coordenadas_geograficas = {} 
adj = {} 
seleccionados = [] 

# Variables para el TSP
mejor_ruta_a = [[]]
mejor_costo_a = [float('inf')]

# -------------------------------
# FUNCIONES MATEMÁTICAS Y DE LÓGICA
# -------------------------------
def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia de gran círculo entre dos puntos en la Tierra (km)."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 
    return round(c * r)

def actualizar_grafo_global():
    """Actualiza la estructura de adyacencia para los cálculos de recorrido."""
    global adj
    adj = nx.to_dict_of_dicts(grafo)

def encontrar_camino_hamiltoniano_minimo(inicio, objetivo, ruta_actual, costo_actual):
    """Algoritmo de Backtracking para el Camino Hamiltoniano (sin repetir)."""
    ruta_actual.append(objetivo)
    N = len(grafo.nodes)
    
    if len(ruta_actual) == N:
        if costo_actual < mejor_costo_a[0]:
            mejor_costo_a[0] = costo_actual
            mejor_ruta_a[0] = list(ruta_actual)
        ruta_actual.pop()
        return

    for vecino, datos in adj[objetivo].items():
        if vecino not in ruta_actual:
            nuevo_costo = costo_actual + datos['peso']
            if nuevo_costo < mejor_costo_a[0]:
                encontrar_camino_hamiltoniano_minimo(inicio, vecino, ruta_actual, nuevo_costo)
    ruta_actual.pop()

def ejecutar_inciso_a_calculo():
    """Ejecuta la búsqueda del Camino Hamiltoniano Mínimo."""
    global mejor_costo_a, mejor_ruta_a
    mejor_costo_a = [float('inf')]
    mejor_ruta_a = [[]]
    nodos = list(grafo.nodes)
    
    if len(nodos) < 2:
        return None, None
        
    for estado_inicio in nodos:
        encontrar_camino_hamiltoniano_minimo(estado_inicio, estado_inicio, [], 0)
        
    return mejor_ruta_a[0], mejor_costo_a[0]


# -------------------------------
# FUNCIONES DE VISUALIZACIÓN E INTERACCIÓN
# -------------------------------
# -------------------------------
# FUNCIONES DE VISUALIZACIÓN E INTERACCIÓN
# -------------------------------
def dibujar_mapa(ruta_resaltada=None, color_ruta='blue'):
    """Redibuja el mapa, los nodos seleccionados y el grafo."""
    ax.clear()
    
    # Dibujar el mapa base
    m.drawmapboundary(fill_color="#CEE0A6")
    m.fillcontinents(color="#FFE0B2", lake_color="#A6CAE0")
    m.drawcountries(linewidth=1)
    m.drawstates(linewidth=0.5)

    nodos_grafo = list(grafo.nodes)
    for estado, (lat, lon) in estados_coords.items():
        # Calcular coordenadas proyectadas solo si es necesario
        if estado not in posiciones:
            x, y = m(lon, lat)
            posiciones[estado] = (x, y)
        else:
            x, y = posiciones[estado]
            
        # Determinar el estilo de dibujo para CADA estado
        if estado in seleccionados:
            color_dot = "#4A1EE9" if estado in nodos_grafo else "#077BFF"
            markersize = 8
            fontcolor = color_dot
            fontweight = 'bold'
        else:
            color_dot = "#82AF4C"
            markersize = 2
            fontcolor = "black"
            fontweight = 'normal'

        # Dibujar punto
        ax.plot(x, y, "o", color=color_dot, markersize=markersize, zorder=5)
        
        # Dibujar etiqueta para TODOS (más fácil de encontrar)
        ax.text(x, y, estado, fontsize=8, ha="center", va="bottom", color=fontcolor, weight=fontweight, zorder=6)
    
    # Dibujar las ARISTAS del grafo
    if grafo.edges:
        # Dibujar todas las aristas del grafo en color gris
        nx.draw_networkx_edges(grafo, posiciones, edge_color="gray", style="--", width=1, ax=ax)
        
        # ===> CORRECCIÓN 1: Evita UnboundLocalError al verificar ruta_resaltada
        if ruta_resaltada and len(ruta_resaltada) > 1:
            path_edges = list(zip(ruta_resaltada, ruta_resaltada[1:]))
            
            # ===> CORRECCIÓN 2: Elimina zorder=10 (o déjalo si actualizaste NetworkX)
            # Versión sin zorder (más compatible con versiones antiguas de NetworkX):
            nx.draw_networkx_edges(grafo, posiciones, edgelist=path_edges, edge_color=color_ruta, width=3, ax=ax) 
            
            # Si actualizaste NetworkX a 2.5 o superior, puedes usar zorder=10:
            # nx.draw_networkx_edges(grafo, posiciones, edgelist=path_edges, edge_color=color_ruta, width=3, zorder=10, ax=ax)


        # Etiquetas de costo
        etiquetas = nx.get_edge_attributes(grafo, 'peso')
        nx.draw_networkx_edge_labels(grafo, posiciones, edge_labels=etiquetas, font_color='darkgreen', font_size=8, ax=ax)

    ax.set_title(f"Grafo de Conexiones ({len(nodos_grafo)} Estados Conectados / Máx 7)")
    canvas.draw()
    actualizar_grafo_global()

def click_mapa(event):
    """Maneja el evento de click para seleccionar o deseleccionar estados."""
    x_click, y_click = event.xdata, event.ydata
    if x_click is None or y_click is None:
        return

    estado_mas_cercano = None
    min_dist_sq = float("inf")
    
    # Umbral de distancia al cuadrado (ajustado para ser más permisivo)
    # Valor empírico basado en el tamaño del mapa de México
    umbral_dist_sq = 150000000 
    
    # 1. Buscar el estado más cercano al click
    for estado, (x, y) in posiciones.items():
        dist_sq = (x - x_click)**2 + (y - y_click)**2
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            estado_mas_cercano = estado
            
    # 2. Verificar si el punto más cercano está dentro del umbral de selección
    if min_dist_sq > umbral_dist_sq:
        # El clic fue muy lejos de cualquier punto, no hacemos nada
        return

    # 3. Procesar la selección/deselección
    if estado_mas_cercano in seleccionados:
        # Deseleccionar: Eliminar el nodo y sus aristas del grafo
        seleccionados.remove(estado_mas_cercano)
        if estado_mas_cercano in grafo.nodes:
            grafo.remove_node(estado_mas_cercano)
    elif len(seleccionados) < 7:
        # Seleccionar
        seleccionados.append(estado_mas_cercano)
        if len(seleccionados) == 7:
            messagebox.showinfo("¡Límite alcanzado!", "Seleccionaste 7 estados. Ahora usa el botón 'Conectar Automático'.")
    else:
        messagebox.showwarning("Límite", "Ya seleccionaste el máximo de 7 estados.")
    
    dibujar_mapa()

canvas.mpl_connect("button_press_event", click_mapa)

def agregar_aristas_automaticas():
    """Conecta automáticamente TODOS los estados seleccionados entre sí."""
    if len(seleccionados) < 2:
        messagebox.showwarning("Advertencia", "Selecciona al menos 2 estados (máx. 7) primero.")
        return

    grafo.clear()
    coordenadas_geograficas.clear() 
    
    for i in range(len(seleccionados)):
        estado1 = seleccionados[i]
        lat1, lon1 = estados_coords[estado1]
        grafo.add_node(estado1)
        coordenadas_geograficas[estado1] = (lat1, lon1)
        
        for j in range(i+1, len(seleccionados)):
            estado2 = seleccionados[j]
            lat2, lon2 = estados_coords[estado2]
            distancia = calcular_distancia_haversine(lat1, lon1, lat2, lon2)
            grafo.add_edge(estado1, estado2, peso=distancia)
            
    actualizar_grafo_global()
    dibujar_mapa()
    messagebox.showinfo("Conexión Completa", f"Se crearon {len(grafo.edges)} conexiones entre los {len(seleccionados)} estados.")


# -------------------------------
# FUNCIONES DE RECORRIDO (A y B)
# -------------------------------
def mostrar_recorrido_a():
    """Recorrer todos los 7 estados sin repetir ninguno (Camino Hamiltoniano Mínimo)."""
    if len(grafo.nodes) < 2:
        messagebox.showwarning("Advertencia", "Conecta los estados primero.")
        return
        
    # El algoritmo de búsqueda exhaustiva (TSP) puede tardar si hay muchos nodos.
    if len(grafo.nodes) > 10:
        messagebox.showwarning("Advertencia", "El cálculo del Recorrido A puede tardar mucho con más de 10 estados.")

    ruta, costo = ejecutar_inciso_a_calculo()
    
    if ruta and len(ruta) == len(grafo.nodes):
        ruta_str = ' → '.join(ruta)
        messagebox.showinfo(
            "Recorrido A (Sin Repetir)", 
            f"Ruta Óptima (Camino Hamiltoniano):\n{ruta_str}\n\nCosto Total: {costo} km"
        )
        dibujar_mapa(ruta_resaltada=ruta, color_ruta='#2196F3') # Azul
    else:
        messagebox.showwarning("Error en Inciso A", "No se encontró un Camino Hamiltoniano (ruta que visita todos los nodos sin repetir). Verifique las conexiones.")
        dibujar_mapa()

def mostrar_recorrido_b():
    """Recorrer los 7 estados repitiendo al menos uno de ellos (Ciclo Hamiltoniano)."""
    if len(grafo.nodes) < 2:
        messagebox.showwarning("Advertencia", "Conecta los estados primero.")
        return

    # 1. Encontrar la mejor ruta sin repetir (Camino Hamiltoniano)
    ruta_base, costo_base = ejecutar_inciso_a_calculo()
    
    if not ruta_base or len(ruta_base) != len(grafo.nodes):
        messagebox.showwarning("Error en Inciso B", "No se puede formar un ciclo porque no existe un camino base que visite todos los estados.")
        return

    # 2. Intentar cerrar el ciclo
    ultimo_estado = ruta_base[-1]
    primer_estado = ruta_base[0]
    
    if grafo.has_edge(ultimo_estado, primer_estado):
        costo_regreso = grafo[ultimo_estado][primer_estado]['peso']
        ruta_ciclo = ruta_base + [primer_estado]
        costo_total = costo_base + costo_regreso
        
        ruta_str = ' → '.join(ruta_ciclo)
        messagebox.showinfo(
            "Recorrido B (Con Repetición)", 
            f"Ciclo Hamiltoniano (Repite {primer_estado}):\n{ruta_str}\n\nCosto Total: {costo_total} km"
        )
        dibujar_mapa(ruta_resaltada=ruta_ciclo, color_ruta='#FF9800') # Naranja
    else:
        messagebox.showwarning(
            "No hay Ciclo", 
            f"No se puede formar un ciclo que visite todos y regrese. Falta la conexión directa entre {ultimo_estado} y {primer_estado}."
        )
        dibujar_mapa()


# -------------------------------
# PANEL DE CONTROL (sin cambios)
# -------------------------------
frame_control = tk.Frame(ventana, padx=10, pady=10, bg="#F0F0F0")
frame_control.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(frame_control, text="📍 1. Selecciona hasta 7 estados:", font=('Helvetica', 10, 'bold'), bg="#F0F0F0").pack(pady=(0,5), fill=tk.X)
tk.Label(frame_control, text=" Haz click sobre las abreviaturas en el mapa.", font=('Helvetica', 8), bg="#F0F0F0").pack(pady=(0,10), fill=tk.X)

tk.Label(frame_control, text="🔗 2. Conectar y Calcular:", font=('Helvetica', 12, 'bold'), bg="#F0F0F0").pack(pady=(10,5))
tk.Button(frame_control, text="Conectar Automático (Grafo Completo)", command=agregar_aristas_automaticas, bg="#00BCD4", fg="white").pack(fill=tk.X, pady=5)

tk.Frame(frame_control, height=2, bg="gray").pack(fill=tk.X, pady=10)

tk.Label(frame_control, text="✈️ 3. Ejecutar Recorridos:", font=('Helvetica', 12, 'bold'), bg="#F0F0F0").pack(pady=5)
tk.Button(frame_control, text="Recorrido A (Sin Repetir) | Costo", command=mostrar_recorrido_a, bg="#2196F3", fg="white").pack(fill=tk.X, pady=5)
tk.Button(frame_control, text="Recorrido B (Con Repetición) | Ciclo", command=mostrar_recorrido_b, bg="#FF9800", fg="white").pack(fill=tk.X, pady=5)

tk.Button(frame_control, text="Salir", command=ventana.destroy, bg="#F44336", fg="white").pack(fill=tk.X, pady=20)



dibujar_mapa()
ventana.mainloop()