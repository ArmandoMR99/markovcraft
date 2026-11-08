"""Ítem 4 – Distancia de variación total y tiempo de mezcla."""
import numpy as np


def distancia_variacion_total(mu, nu):
    """‖μ − ν‖_TV = ½ Σⱼ |μⱼ − νⱼ|"""
    return 0.5 * np.abs(mu - nu).sum()


def distancia_maxima(Pt, pi):
    """d(t) = maxᵢ ‖Pᵗ(i, ·) − π‖_TV  → el peor bioma inicial."""
    return max(distancia_variacion_total(Pt[i], pi) for i in range(len(pi)))


def calcular_mixing_time(P, pi, epsilon=0.01, max_iter=1000):
    """t_mix(ε) = min { t ≥ 0 : d(t) ≤ ε }.
    Devuelve (t_mix o None si no se alcanzó, lista con d(0), d(1), ...)."""
    n = P.shape[0]
    Pt = np.eye(n)          # P⁰ = I: cada fila = 'empiezo seguro en el bioma i'
    historial = []
    for t in range(max_iter + 1):
        d = distancia_maxima(Pt, pi)
        historial.append(d)
        if d <= epsilon:
            return t, historial
        Pt = Pt @ P         # Pᵗ⁺¹ = Pᵗ · P
    return None, historial
