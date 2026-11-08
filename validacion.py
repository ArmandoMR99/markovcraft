"""Ítem 1 – Lectura y validación de la matriz estocástica."""
import numpy as np

BIOMAS = ["Bosque", "Desierto", "Montaña", "Océano", "Llanura"]
EMOJIS = ["🌲", "🏜️", "⛰️", "🌊", "🌾"]
COLORES = ["#3fb26b", "#e3b55b", "#9aa5b8", "#4a90e2", "#b8db6a"]

# Matriz de prueba de la sección 5 del reporte de especificación
MATRIZ_EJEMPLO = np.array([
    [0.40, 0.10, 0.20, 0.00, 0.30],
    [0.10, 0.40, 0.10, 0.10, 0.30],
    [0.20, 0.10, 0.40, 0.10, 0.20],
    [0.10, 0.10, 0.10, 0.40, 0.30],
    [0.20, 0.20, 0.20, 0.10, 0.30],
])

# Cadena periódica (periodo 2): {Bosque, Montaña, Llanura} <-> {Desierto, Océano}
MATRIZ_PERIODICA = np.array([
    [0.00, 0.60, 0.00, 0.40, 0.00],
    [0.30, 0.00, 0.40, 0.00, 0.30],
    [0.00, 0.50, 0.00, 0.50, 0.00],
    [0.50, 0.00, 0.20, 0.00, 0.30],
    [0.00, 0.70, 0.00, 0.30, 0.00],
])

# Cadena reducible: el Océano es absorbente (una vez allí, no se sale)
MATRIZ_REDUCIBLE = np.array([
    [0.40, 0.10, 0.20, 0.00, 0.30],
    [0.10, 0.40, 0.10, 0.10, 0.30],
    [0.20, 0.10, 0.40, 0.10, 0.20],
    [0.00, 0.00, 0.00, 1.00, 0.00],
    [0.20, 0.20, 0.20, 0.10, 0.30],
])


def validar_matriz(P, tolerancia=1e-3):
    """Revisa que P sea estocástica. Devuelve (es_valida, lista_de_errores).
    No corrige nada: solo informa dónde está el problema."""
    errores = []
    n = len(BIOMAS)

    if P.shape != (n, n):
        return False, [f"La matriz debe ser de {n} x {n}."]

    # 1) Cada celda debe ser un número entre 0 y 1
    for i in range(n):
        for j in range(n):
            valor = P[i, j]
            if np.isnan(valor):
                errores.append(f"Celda ({BIOMAS[i]} → {BIOMAS[j]}) está vacía o no es numérica.")
            elif valor < 0 or valor > 1:
                errores.append(f"Celda ({BIOMAS[i]} → {BIOMAS[j]}) = {valor} está fuera de [0, 1].")

    # 2) Cada fila debe sumar 1 (con una pequeña tolerancia por redondeo)
    sumas = np.nansum(P, axis=1)
    for i, suma in enumerate(sumas):
        if abs(suma - 1) > tolerancia:
            errores.append(f"La fila {BIOMAS[i]} suma {suma:.4f}; debe sumar 1.")

    return len(errores) == 0, errores
