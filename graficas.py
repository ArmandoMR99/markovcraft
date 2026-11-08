"""Visualizaciones de convergencia y resultados (Matplotlib + NetworkX)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from validacion import BIOMAS, COLORES

FONDO = "#1c1c1f"
TEXTO = "#c9cdd4"
REJILLA = "#2c2c31"
AZUL = "#5b9cf6"
ROJO = "#ef8a8a"
VERDE = "#6fdcaa"


def _estilo(ax, fig):
    fig.patch.set_facecolor(FONDO)
    ax.set_facecolor(FONDO)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=TEXTO, labelsize=9)
    ax.grid(color=REJILLA, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.xaxis.label.set_color(TEXTO)
    ax.yaxis.label.set_color(TEXTO)
    ax.title.set_color("#f0f2f5")


def grafica_grafo(G, pi=None):
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    fig.patch.set_facecolor(FONDO)
    ax.set_facecolor(FONDO)
    ax.axis("off")
    pos = nx.circular_layout(G)
    tam = [900 + 5000 * pi[i] for i in G.nodes()] if pi is not None else 1400
    aristas = [(u, v) for u, v in G.edges() if u != v]
    lazos = [(u, v) for u, v in G.edges() if u == v]
    anchos = [0.6 + 4 * G[u][v]["peso"] for u, v in aristas]
    nx.draw_networkx_edges(G, pos, edgelist=aristas, width=anchos, edge_color="#6b7280",
                           arrows=True, arrowsize=14, connectionstyle="arc3,rad=0.12",
                           node_size=tam, ax=ax, alpha=0.85)
    nx.draw_networkx_nodes(G, pos, node_color=[COLORES[i] for i in G.nodes()],
                           node_size=tam, edgecolors="#f0f2f5",
                           linewidths=[2.5 if (i, i) in lazos else 0 for i in G.nodes()], ax=ax)
    nx.draw_networkx_labels(G, pos, labels={i: BIOMAS[i] for i in G.nodes()},
                            font_size=9, font_color="#111", font_weight="bold", ax=ax)
    ax.margins(0.18)
    return fig


def grafica_barras_pi(pi):
    fig, ax = plt.subplots(figsize=(6, 3.4))
    _estilo(ax, fig)
    barras = ax.bar(BIOMAS, pi, color=COLORES, width=0.62)
    for b, v in zip(barras, pi):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.006, f"{v:.2%}",
                ha="center", color=TEXTO, fontsize=9, family="monospace")
    ax.set_ylabel("π")
    ax.set_ylim(0, max(pi) * 1.22 + 0.01)
    return fig


def grafica_mixing(historial, epsilon, t_mix=None):
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    _estilo(ax, fig)
    t = np.arange(len(historial))
    ax.plot(t, historial, color=AZUL, marker="o", markersize=4, linewidth=2, label="d(t)")
    ax.fill_between(t, historial, color=AZUL, alpha=0.12)
    ax.axhline(epsilon, color=ROJO, linestyle="--", linewidth=1.4, label=f"ε = {epsilon:g}")
    if t_mix is not None:
        ax.axvline(t_mix, color=VERDE, linestyle=":", linewidth=1.6)
        ax.scatter([t_mix], [historial[t_mix]], color=VERDE, s=70, zorder=5,
                   label=f"t_mix = {t_mix}")
    ax.set_xlabel("pasos t")
    ax.set_ylabel("d(t)  (distancia TV máxima)")
    ax.set_ylim(bottom=0)
    leg = ax.legend(facecolor=FONDO, edgecolor=REJILLA, labelcolor=TEXTO, fontsize=9)
    return fig


def grafica_heatmap_Pt(Pt, t):
    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    _estilo(ax, fig)
    ax.grid(False)
    cmap = LinearSegmentedColormap.from_list("mc", ["#202026", "#2d4f86", AZUL, "#bcd6ff"])
    ax.imshow(Pt, cmap=cmap, vmin=0, vmax=1)
    ax.set_xticks(range(len(BIOMAS)), BIOMAS, rotation=30, ha="right")
    ax.set_yticks(range(len(BIOMAS)), BIOMAS)
    for i in range(Pt.shape[0]):
        for j in range(Pt.shape[1]):
            ax.text(j, i, f"{Pt[i, j]:.3f}", ha="center", va="center", fontsize=8,
                    color="#0b0b0c" if Pt[i, j] > 0.7 else "#f0f2f5", family="monospace")
    ax.set_title(f"P^{t}   (fila = bioma inicial)", fontsize=10)
    return fig


def grafica_comparacion(frecuencia, pi):
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    _estilo(ax, fig)
    x = np.arange(len(BIOMAS))
    ax.bar(x - 0.2, frecuencia, width=0.38, color=COLORES, label="Observada (aventura)")
    if pi is not None:
        ax.bar(x + 0.2, pi, width=0.38, color="none", edgecolor="#f0f2f5",
               linewidth=1.4, hatch="//", label="Teórica π")
    ax.set_xticks(x, BIOMAS)
    ax.set_ylabel("frecuencia relativa")
    ax.legend(facecolor=FONDO, edgecolor=REJILLA, labelcolor=TEXTO, fontsize=9)
    return fig


def grafica_frecuencia_acumulada(acumulada, pi):
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    _estilo(ax, fig)
    t = np.arange(1, acumulada.shape[0] + 1)
    for j, nombre in enumerate(BIOMAS):
        ax.plot(t, acumulada[:, j], color=COLORES[j], linewidth=1.6, label=nombre)
        if pi is not None:
            ax.axhline(pi[j], color=COLORES[j], linestyle="--", linewidth=0.9, alpha=0.7)
    ax.set_xscale("log")
    ax.set_xlabel("número de movimientos (escala log)")
    ax.set_ylabel("frecuencia acumulada")
    ax.set_ylim(0, 1)
    ax.legend(facecolor=FONDO, edgecolor=REJILLA, labelcolor=TEXTO, fontsize=8, ncol=5,
              loc="upper center")
    return fig
