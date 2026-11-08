# 🧭 MarkovCraft: Explorador de Biomas

Simulador de cadenas de Markov (Procesos Estocásticos – UPB) que calcula la
distribución estacionaria y el Mixing Time de una cadena de 5 biomas.

## Ejecutar en el computador

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre en http://localhost:8501

## Publicar en la web (gratis)

1. Crear un repositorio en GitHub (p. ej. `markovcraft`) y subir **todos** estos
   archivos, incluida la carpeta `.streamlit/`.
2. Entrar a https://share.streamlit.io con la cuenta de GitHub.
3. **Create app → Deploy a public app from GitHub** → elegir el repo, rama `main`,
   archivo `app.py` → **Deploy**.
4. Queda una URL tipo `https://markovcraft.streamlit.app`.

> Si nadie la usa por varios días, la app "se duerme": ábranla unos minutos antes
> de la exposición y presionen *Wake up*.

## Estructura (igual a la sección 4 del reporte)

| Archivo | Ítem de la rúbrica | Qué hace |
|---|---|---|
| `validacion.py` | 1 | Matrices de ejemplo y validación (rango [0,1], filas suman 1) |
| `analisis_cadena.py` | 2 | Grafo, irreducibilidad (NetworkX) y periodo (BFS + MCD) |
| `estacionaria.py` | 3 | Resuelve πP = π con Σπ = 1 (`np.linalg.solve`) |
| `mixing_time.py` | 4 | Distancia de variación total y t_mix(ε) |
| `aventura.py` | 5 | Recorrido aleatorio del explorador y frecuencias |
| `graficas.py` | – | Gráficas (Matplotlib) |
| `app.py` | – | Interfaz Streamlit; muestra el código real de cada función |

## Guion sugerido para la exposición

1. **Pestaña ①** – Cargar "Ejemplo del reporte". Cambiar una celda para que la fila
   no sume 1 y mostrar el mensaje de error. Restaurar.
2. **Pestaña ②** – Explicar el grafo, irreducible y periodo = 1. Luego cargar
   "Periódica" (periodo 2) y "Reducible" (Océano absorbente) y mostrar los avisos.
3. **Pestaña ③** – π = (0.2131, 0.1827, 0.2131, 0.1124, 0.2787) y la verificación πP ≈ π.
4. **Pestaña ④** – t_mix = 5 con ε = 0.01 (d(4) ≈ 0.0133, d(5) ≈ 0.0047). Cambiar ε
   a 0.001 y ver que aumenta. Mover el slider de Pᵗ: en t = 0 es la identidad y en
   t ≈ 5 todas las filas son iguales a π. Con la matriz periódica, d(t) se queda en 0.5.
5. **Pestaña ⑤** – Aventura con 50 movimientos (se aleja de π) y con 20 000 (se acerca):
   ley de grandes números.

Repartición sugerida: cada integrante domina 1–2 archivos y su pestaña.
