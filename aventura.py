"""Ítem 5 – Funcionalidad particular: la aventura del explorador."""
import numpy as np


def simular_aventura(P, bioma_inicial, pasos, semilla=None):
    """Recorrido aleatorio: en cada paso se sortea el siguiente bioma
    usando la fila del bioma actual como distribución de probabilidad."""
    rng = np.random.default_rng(semilla)
    n = P.shape[0]
    actual = bioma_inicial
    recorrido = [actual]
    for _ in range(pasos):
        fila = P[actual] / P[actual].sum()   # ajuste numérico mínimo para el sorteo
        actual = int(rng.choice(n, p=fila))
        recorrido.append(actual)
    return recorrido


def contar_visitas(recorrido, n):
    """Número de visitas y frecuencia relativa observada de cada bioma."""
    visitas = np.bincount(recorrido, minlength=n)
    frecuencia = visitas / visitas.sum()
    return visitas, frecuencia


def frecuencia_acumulada(recorrido, n):
    """Frecuencia relativa de cada bioma después de 1, 2, ..., T pasos."""
    recorrido = np.array(recorrido)
    indicadoras = np.eye(n)[recorrido]                 # matriz T x n de 0/1
    acumulado = indicadoras.cumsum(axis=0)
    return acumulado / np.arange(1, len(recorrido) + 1)[:, None]
