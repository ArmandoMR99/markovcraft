"""MarkovCraft: Explorador de Biomas – interfaz Streamlit.
Ejecutar con:  streamlit run app.py"""
import inspect

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import analisis_cadena
import aventura
import estacionaria
import graficas
import mixing_time
import validacion
from validacion import BIOMAS, COLORES, EMOJIS

st.set_page_config(page_title="MarkovCraft · Explorador de Biomas", page_icon="🧭", layout="wide")

# ---------------------------------------------------------------- estilos
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');
.block-container {padding-top: 3.5rem; max-width: 1400px;}
.hdr {display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;
      border-bottom:1px solid #2a2a2f; padding-bottom:1.2rem; margin-bottom:1.4rem; flex-wrap:wrap;}
.hdr h1 {font-size:2.3rem; margin:0; padding:0; font-weight:700; letter-spacing:-0.01em;}
.hdr .sub {color:#9aa0a8; font-size:1.05rem; margin-top:.35rem;}
.hdr .team {font-family:'JetBrains Mono', monospace; font-size:.85rem; color:#b9bec6;
            text-align:right; line-height:1.65;}
.hdr .team b {color:#e6e8eb; font-weight:600;}
.card {background:#1c1c1f; border:1px solid #2a2a2f; border-radius:10px; padding:1rem 1.2rem;
       margin-bottom:.8rem;}
.card .t {font-size:.75rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; letter-spacing:.08em; text-transform:uppercase; color:#9aa0a8;}
.card .v {font-family:'JetBrains Mono', monospace; font-size:1.65rem; margin-top:.35rem;}
.chip {display:inline-block; padding:.18rem .5rem; margin:.15rem; border-radius:6px;
       font-size:.82rem; background:#232327; border:1px solid #2f2f35;}
.nota {color:#9aa0a8; font-size:.9rem;}
h3 {font-size:1.25rem !important;}
</style>
""", unsafe_allow_html=True)


def tarjeta(titulo, valor, color="#e6e8eb", tam="1.65rem"):
    st.markdown(f"<div class='card'><div class='t'>{titulo}</div>"
                f"<div class='v' style='color:{color}; font-size:{tam}'>{valor}</div></div>",
                unsafe_allow_html=True)


def mostrar_codigo(*funciones, archivo=None):
    """Muestra el código fuente real de las funciones que ejecuta la app."""
    if archivo:
        st.caption(f"📄 {archivo}")
    st.code("\n\n".join(inspect.getsource(f) for f in funciones), language="python", wrap_lines=True,
            line_numbers=True)


def figura(fig):
    st.pyplot(fig, width="stretch")
    plt.close(fig)


VERDE, ROJO, AZUL, AMARILLO = "#6fdcaa", "#ef8a8a", "#5b9cf6", "#e3c25b"

# ---------------------------------------------------------------- encabezado
st.markdown("""
<div class="hdr">
  <div>
    <h1>🧭 MarkovCraft: Explorador de Biomas</h1>
    <div class="sub">Simulador de cadenas de Markov · Distribución estacionaria y Mixing Time</div>
  </div>
  <div class="team">Integrantes:<br>
    &gt; <b>Carlos Felipe Feria Chaparro</b><br>
    &gt; <b>Armando Marulanda Rua</b><br>
    &gt; <b>Miguel Angel Jaramillo Hurtado</b><br>
    <span style="color:#7b818a">Procesos Estocásticos · UPB · Docente: Vivian C. Zapata T.</span>
  </div>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    c1, c2 = st.columns([1.35, 1])
    with c1:
        st.markdown("### Planteamiento del problema")
        st.markdown(
            "Un explorador recorre un mundo de **cinco biomas**. En cada paso puede quedarse donde "
            "está o moverse a otro bioma según una **matriz de transición** P, donde "
            "`P[i, j] = P(Xₜ₊₁ = j | Xₜ = i)`. Queremos saber si, después de muchos pasos, la "
            "probabilidad de estar en cada bioma se **estabiliza** (distribución estacionaria π) "
            "y **cuántos pasos** tarda en olvidar dónde empezó (**Mixing Time**)."
        )
    with c2:
        st.markdown("### Biomas (estados)")
        st.markdown(" ".join(
            f"<span class='chip' style='border-color:{COLORES[i]}'>S{i + 1} · {EMOJIS[i]} {b}</span>"
            for i, b in enumerate(BIOMAS)), unsafe_allow_html=True)
        st.markdown("<p class='nota' style='margin-top:.6rem'><b>Metodología:</b> validación de P, "
                    "análisis del grafo (irreducibilidad y periodo), solución de πP = π y "
                    "distancia de variación total para t<sub>mix</sub>(ε).</p>",
                    unsafe_allow_html=True)

st.write("")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "① Matriz estocástica", "② ¿Estado estable?", "③ Distribución estacionaria",
    "④ Mixing Time", "⑤ Aventura del explorador"])

# ================================================================ ① MATRIZ
if "P_base" not in st.session_state:
    st.session_state.P_base = validacion.MATRIZ_EJEMPLO.copy()
    st.session_state.version = 0


def cargar(P):
    st.session_state.P_base = np.round(P, 4)
    st.session_state.version += 1
    st.session_state.pop("recorrido", None)


with tab1:
    izq, der = st.columns([1, 1.15], gap="large")
    with der:
        st.markdown("### Entorno: ingrese la matriz P")
        b1, b2, b3, b4 = st.columns(4)
        if b1.button("Ejemplo del reporte", width="stretch"):
            cargar(validacion.MATRIZ_EJEMPLO)
        if b2.button("Periódica", width="stretch"):
            cargar(validacion.MATRIZ_PERIODICA)
        if b3.button("Reducible", width="stretch"):
            cargar(validacion.MATRIZ_REDUCIBLE)
        if b4.button("Aleatoria 🎲", width="stretch"):
            cargar(np.random.default_rng().dirichlet(np.ones(5), size=5))

        df = pd.DataFrame(st.session_state.P_base, index=BIOMAS, columns=BIOMAS)
        editado = st.data_editor(
            df, key=f"editor_{st.session_state.version}", width="stretch",
            column_config={b: st.column_config.NumberColumn(b, format="%.4f", step=0.01)
                           for b in BIOMAS})
        P = editado.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
        st.caption("Filas = bioma actual · Columnas = bioma siguiente. Edite cualquier celda.")

        valida, errores = validacion.validar_matriz(P)
        sumas = np.nansum(P, axis=1)
        st.markdown(" ".join(
            f"<span class='chip' style='color:{VERDE if abs(s - 1) <= 1e-3 else ROJO}'>"
            f"Σ {BIOMAS[i]} = {s:.4f}</span>" for i, s in enumerate(sumas)),
            unsafe_allow_html=True)
        if valida:
            st.success("✅ Matriz estocástica válida: todas las entradas en [0, 1] y cada fila suma 1.")
        else:
            st.error("❌ La matriz no es válida. Corrija lo siguiente:\n\n" +
                     "\n".join(f"- {e}" for e in errores))

    with izq:
        st.markdown("### Lógica de implementación")
        st.markdown("Se reciben los 25 valores desde una tabla editable. La función **no corrige** "
                    "los datos: revisa cada celda y la suma de cada fila, y reporta exactamente "
                    "dónde está el error.")
        mostrar_codigo(validacion.validar_matriz, archivo="validacion.py")

if not valida:
    for t in (tab2, tab3, tab4, tab5):
        with t:
            st.warning("Primero corrija la matriz en la pestaña ① para continuar.")
    st.stop()

analisis = analisis_cadena.analizar_cadena(P)
pi = estacionaria.distribucion_estacionaria(P) if analisis["irreducible"] else None

# ================================================================ ② ESTADO ESTABLE
with tab2:
    izq, der = st.columns([1, 1.15], gap="large")
    with izq:
        st.markdown("### Lógica de implementación")
        st.markdown(
            "Se construye un **grafo dirigido** (arista i → j si `P[i,j] > 0`).\n"
            "- **Irreducible**: todos los biomas se comunican → π es **única**.\n"
            "- **Aperiódica** (periodo = 1): no hay oscilaciones forzadas.\n"
            "- Irreducible **+** aperiódica → converge a π **desde cualquier bioma**.")
        mostrar_codigo(analisis_cadena.construir_grafo, analisis_cadena.es_irreducible,
                       analisis_cadena.calcular_periodo, archivo="analisis_cadena.py")
    with der:
        st.markdown("### Diagnóstico de la cadena")
        k1, k2, k3 = st.columns(3)
        with k1:
            tarjeta("Irreducible", "Sí" if analisis["irreducible"] else "No",
                    VERDE if analisis["irreducible"] else ROJO)
        with k2:
            per = analisis["periodo"]
            tarjeta("Periodo", per if per is not None else "—",
                    VERDE if per == 1 else (ROJO if per else "#9aa0a8"))
        with k3:
            tarjeta("Estado estable", "Alcanzable" if analisis["ergodica"] else "No garantizado",
                    VERDE if analisis["ergodica"] else AMARILLO)

        if analisis["ergodica"]:
            st.success("La cadena es **irreducible y aperiódica**: existe una única distribución "
                       "estacionaria y la cadena converge a ella desde cualquier bioma inicial.")
        elif analisis["irreducible"]:
            st.warning(f"La cadena es irreducible pero **periódica (periodo {analisis['periodo']})**. "
                       "Existe una π única, pero las distribuciones **oscilan** y no convergen.")
        else:
            clases = " | ".join("{" + ", ".join(BIOMAS[i] for i in c) + "}" for c in analisis["clases"])
            st.error("La cadena es **reducible**: no todos los biomas se comunican. No se puede "
                     f"garantizar una π única. Clases comunicantes: {clases}")
        figura(graficas.grafica_grafo(analisis["grafo"], pi))
        st.caption("Grosor de flecha ∝ probabilidad de transición. Borde blanco = el bioma puede "
                   "quedarse en sí mismo (lazo, garantiza aperiodicidad). Tamaño del nodo ∝ πᵢ.")

# ================================================================ ③ ESTACIONARIA
with tab3:
    izq, der = st.columns([1, 1.15], gap="large")
    with izq:
        st.markdown("### Lógica de implementación")
        st.latex(r"\pi P = \pi \;\Longleftrightarrow\; (P^{T}-I)\,\pi^{T}=0,\qquad \sum_i \pi_i = 1")
        st.markdown("Una de las ecuaciones de `(Pᵀ − I)πᵀ = 0` es redundante, así que se reemplaza "
                    "por la normalización y se resuelve el sistema lineal con `np.linalg.solve`.")
        mostrar_codigo(estacionaria.distribucion_estacionaria, estacionaria.verificar_estacionaria,
                       archivo="estacionaria.py")
    with der:
        st.markdown("### Resultado")
        if pi is None:
            st.error("La matriz es reducible: puede haber más de una distribución estacionaria, "
                     "por lo que no se reporta una π única con este criterio.")
        else:
            if not analisis["aperiodica"]:
                st.warning("π es única, pero al ser periódica la cadena no converge a ella "
                           "(π se interpreta como proporción de tiempo a largo plazo).")
            cols = st.columns(5)
            for i, c in enumerate(cols):
                with c:
                    tarjeta(BIOMAS[i], f"{pi[i]:.4f}", COLORES[i], tam="1.15rem")
            figura(graficas.grafica_barras_pi(pi))
            v = estacionaria.verificar_estacionaria(P, pi)
            k1, k2, k3 = st.columns(3)
            with k1:
                tarjeta("Σ πᵢ", f"{v['suma']:.6f}", VERDE)
            with k2:
                tarjeta("max |πP − π|", f"{v['error_max']:.1e}", VERDE)
            with k3:
                tarjeta("π ≥ 0", "Sí" if v["no_negativa"] else "No",
                        VERDE if v["no_negativa"] else ROJO)
            st.dataframe(pd.DataFrame({"Bioma": BIOMAS, "π (decimal)": pi.round(4),
                                       "π (%)": [f"{x:.2%}" for x in pi]}),
                         hide_index=True, width="stretch")

# ================================================================ ④ MIXING TIME
with tab4:
    izq, der = st.columns([1, 1.15], gap="large")
    with izq:
        st.markdown("### Lógica de implementación")
        st.latex(r"d(t)=\max_i \tfrac12\sum_j \left|(P^t)_{ij}-\pi_j\right| \qquad "
                 r"t_{mix}(\varepsilon)=\min\{t\ge0 : d(t)\le\varepsilon\}")
        st.markdown("Se calcula Pᵗ paso a paso. Cada fila de Pᵗ es la distribución después de t "
                    "pasos si se empezó en ese bioma. Se toma el **peor caso** (máximo) y se "
                    "detiene en el primer t con d(t) ≤ ε.")
        mostrar_codigo(mixing_time.distancia_variacion_total, mixing_time.distancia_maxima,
                       mixing_time.calcular_mixing_time, archivo="mixing_time.py")
    with der:
        st.markdown("### Entorno de simulación")
        if pi is None:
            st.error("Sin una π única (cadena reducible) no se puede calcular el Mixing Time "
                     "global con este método.")
        else:
            with st.container(border=True):
                a, b = st.columns(2)
                epsilon = a.number_input("Tolerancia ε", min_value=1e-6, max_value=0.5,
                                         value=0.01, step=0.005, format="%.4f")
                max_iter = b.number_input("Máx. iteraciones", 10, 10000, 1000, step=100)
            t_mix, hist = mixing_time.calcular_mixing_time(P, pi, epsilon, int(max_iter))

            if not analisis["aperiodica"]:
                st.warning("Cadena **periódica**: d(t) no baja a cero, oscila. No se reporta un "
                           "Mixing Time de convergencia. Vea la gráfica (primeros 30 pasos).")
                figura(graficas.grafica_mixing(hist[:31], epsilon))
            else:
                k1, k2, k3 = st.columns(3)
                with k1:
                    tarjeta("Mixing Time", f"{t_mix} pasos" if t_mix is not None else "No alcanzado",
                            VERDE if t_mix is not None else ROJO)
                with k2:
                    tarjeta("ε usado", f"{epsilon:g}", AZUL)
                with k3:
                    tarjeta("d(t_mix)", f"{hist[-1]:.5f}")
                if t_mix is None:
                    st.warning(f"No se alcanzó ε dentro de {max_iter} iteraciones.")
                mostrar = hist[: max(t_mix + 4, 8)] if t_mix is not None else hist[:60]
                figura(graficas.grafica_mixing(mostrar, epsilon, t_mix))

                with st.expander("📋 Tabla d(t) paso a paso", expanded=False):
                    st.dataframe(pd.DataFrame({"t": range(len(mostrar)),
                                               "d(t)": np.round(mostrar, 6),
                                               "¿≤ ε?": ["✅" if d <= epsilon else "—" for d in mostrar]}),
                                 hide_index=True, width="stretch")

            st.markdown("#### Ver Pᵗ: las filas se vuelven iguales a π")
            t_ver = st.slider("Paso t", 0, 30, min(t_mix or 3, 30))
            figura(graficas.grafica_heatmap_Pt(np.linalg.matrix_power(P, t_ver), t_ver))

# ================================================================ ⑤ AVENTURA
with tab5:
    izq, der = st.columns([1, 1.15], gap="large")
    with izq:
        st.markdown("### Funcionalidad particular")
        st.markdown("El explorador parte de un bioma y en cada movimiento se **sortea** el "
                    "siguiente bioma con la fila de P del bioma actual. Así comparamos una "
                    "trayectoria real (simulación Monte Carlo) contra la π teórica.")
        mostrar_codigo(aventura.simular_aventura, aventura.contar_visitas, archivo="aventura.py")
    with der:
        st.markdown("### Entorno de simulación")
        with st.container(border=True):
            a, b, c = st.columns([1.2, 1, 1])
            inicio = a.selectbox("Bioma inicial", range(5),
                                 format_func=lambda i: f"{EMOJIS[i]} {BIOMAS[i]}")
            pasos = b.number_input("Movimientos", 1, 200000, 500, step=100)
            semilla_txt = c.text_input("Semilla (opcional)", "")
            if st.button("🧭 Iniciar aventura", type="primary", width="stretch"):
                semilla = int(semilla_txt) if semilla_txt.strip().isdigit() else None
                st.session_state.recorrido = aventura.simular_aventura(P, inicio, int(pasos), semilla)

        rec = st.session_state.get("recorrido")
        if rec is None:
            st.info("Configure la aventura y presione **Iniciar aventura**.")
        else:
            visitas, frec = aventura.contar_visitas(rec, 5)
            st.markdown(f"**Recorrido** ({len(rec) - 1} movimientos"
                        f"{', se muestran los primeros 60' if len(rec) > 61 else ''}):")
            st.markdown("".join(f"<span class='chip' title='{BIOMAS[s]}'>{EMOJIS[s]}</span>"
                                for s in rec[:61]), unsafe_allow_html=True)
            figura(graficas.grafica_comparacion(frec, pi))
            tabla = pd.DataFrame({"Bioma": [f"{EMOJIS[i]} {BIOMAS[i]}" for i in range(5)],
                                  "Visitas": visitas,
                                  "Frecuencia observada": [f"{x:.2%}" for x in frec]})
            if pi is not None:
                tabla["π teórica"] = [f"{x:.2%}" for x in pi]
                tabla["Diferencia"] = [f"{f - p:+.2%}" for f, p in zip(frec, pi)]
                st.dataframe(tabla, hide_index=True, width="stretch")
                tarjeta("Distancia TV (observada vs π)",
                        f"{mixing_time.distancia_variacion_total(frec, pi):.4f}", AZUL)
            else:
                st.dataframe(tabla, hide_index=True, width="stretch")
            st.markdown("#### Convergencia de la frecuencia (ley de grandes números)")
            figura(graficas.grafica_frecuencia_acumulada(aventura.frecuencia_acumulada(rec, 5), pi))
            st.caption("⚠️ Una sola aventura es una trayectoria aleatoria: no tiene por qué coincidir "
                       "exactamente con π, sobre todo con pocos movimientos. Al aumentar los "
                       "movimientos, las líneas se acercan a las punteadas (π).")
