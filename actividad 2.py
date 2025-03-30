import networkx as nx
from collections import deque

def construir_grafo():
    G = nx.Graph()
    
    # Agregar conexiones entre ciudades servidas por Libertadores
    conexiones = [
        ("Bogotá", "Tunja", 130), ("Tunja", "Duitama", 50), ("Duitama", "Sogamoso", 20),
        ("Bogotá", "Villavicencio", 120), ("Villavicencio", "Yopal", 250),
        ("Bogotá", "Neiva", 300), ("Neiva", "Florencia", 230),
        ("Tunja", "Bucaramanga", 400), ("Bucaramanga", "Cúcuta", 200),
        ("Bogotá", "Pereira", 320), ("Pereira", "Manizales", 50), ("Manizales", "Medellín", 200),
    ]
    
    for u, v, peso in conexiones:
        G.add_edge(u, v, weight=peso)
    
    return G

def encontrar_mejor_ruta(G, inicio, destino):
    try:
        ruta = nx.shortest_path(G, source=inicio, target=destino, weight='weight')
        distancia = nx.shortest_path_length(G, source=inicio, target=destino, weight='weight')
        return ruta, distancia
    except nx.NetworkXNoPath:
        return None, float('inf')

# Construcción del grafo
G = construir_grafo()

# Punto de partida y destino
inicio, destino = "Bogotá", "Medellín"
mejor_ruta, distancia = encontrar_mejor_ruta(G, inicio, destino)

# Resultados
if mejor_ruta:
    print(f"La mejor ruta de {inicio} a {destino} es: {' -> '.join(mejor_ruta)} con una distancia de {distancia} km.")
else:
    print("No hay ruta disponible entre los puntos especificados.")