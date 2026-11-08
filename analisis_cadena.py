"""Ítem 2 – ¿Se puede alcanzar un estado estable?
Se analiza el grafo de transición: irreducibilidad y periodicidad."""
from collections import deque
from math import gcd

import networkx as nx


def construir_grafo(P):
    """Cada bioma es un nodo; hay arista i → j si P[i, j] > 0."""
    G = nx.DiGraph()
    n = P.shape[0]
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(n):
            if P[i, j] > 0:
                G.add_edge(i, j, peso=P[i, j])
    return G


def es_irreducible(G):
    """Irreducible = desde cualquier bioma se puede llegar a cualquier otro
    (el grafo es fuertemente conexo)."""
    return nx.is_strongly_connected(G)


def clases_comunicantes(G):
    """Grupos de biomas que se comunican entre sí."""
    return [sorted(c) for c in nx.strongly_connected_components(G)]


def calcular_periodo(G, inicio=0):
    """Periodo = MCD de las longitudes de todos los ciclos.
    Truco: se hace BFS para dar a cada nodo su 'nivel' (distancia desde el inicio).
    Para cada arista u → v, (nivel[u] + 1 - nivel[v]) es la diferencia de largo
    entre dos caminos que llegan a v. El MCD de esas diferencias es el periodo."""
    nivel = {inicio: 0}
    cola = deque([inicio])
    while cola:
        u = cola.popleft()
        for v in G.successors(u):
            if v not in nivel:
                nivel[v] = nivel[u] + 1
                cola.append(v)

    periodo = 0
    for u, v in G.edges():
        if u in nivel and v in nivel:
            periodo = gcd(periodo, nivel[u] + 1 - nivel[v])
    return periodo


def analizar_cadena(P):
    """Resumen del diagnóstico de convergencia."""
    G = construir_grafo(P)
    irreducible = es_irreducible(G)
    periodo = calcular_periodo(G) if irreducible else None
    return {
        "grafo": G,
        "irreducible": irreducible,
        "periodo": periodo,
        "aperiodica": periodo == 1,
        # Irreducible + aperiódica => converge a una única π desde cualquier inicio
        "ergodica": irreducible and periodo == 1,
        "clases": clases_comunicantes(G),
    }
