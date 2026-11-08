"""Ítem 3 – Cálculo y verificación de la distribución estacionaria π."""
import numpy as np


def distribucion_estacionaria(P):
    """Resuelve πP = π con Σπ = 1.
    πP = π  <=>  (Pᵀ - I) πᵀ = 0. Ese sistema tiene una ecuación redundante,
    así que reemplazamos la última por la condición de normalización Σπ = 1."""
    n = P.shape[0]
    A = P.T - np.eye(n)
    A[-1, :] = 1.0          # última ecuación: π1 + π2 + ... + πn = 1
    b = np.zeros(n)
    b[-1] = 1.0
    pi = np.linalg.solve(A, b)
    pi[np.abs(pi) < 1e-12] = 0.0   # limpiar ceros numéricos (-0.0000)
    return pi


def verificar_estacionaria(P, pi):
    """Comprueba que π sume 1 y que πP ≈ π."""
    return {
        "suma": pi.sum(),
        "error_max": np.abs(pi @ P - pi).max(),
        "no_negativa": bool((pi >= 0).all()),
    }
