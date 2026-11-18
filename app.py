# ============================================================
# CLASIFICAESTUDIOS - APP INTERACTIVA - 1A, 1B, 1C
# ============================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ClasificaEstudios", layout="wide")
st.title("📚 CLASIFICAESTUDIOS")
st.write("Mueve las calificaciones y las faltas y mira cómo cambia el promedio, el color y la recomendación al instante.")

materias = ["Matematicas","Espanol","Ciencias","Historia","Ingles","Ed_Fisica","Artes","Computacion"]
materias_cortas = ["Mat","Esp","Cie","His","Ing","E.F.","Art","Com"]

def color_calif(c):
    return "ROJO" if c < 6 else "AMARILLO" if c < 7.5 else "VERDE"

def color_alumno(prom, faltas):
    if prom < 6 or faltas >= 11:
        return "ROJO"
    elif prom < 7.5 or faltas >= 6:
        return "AMARILLO"
    else:
        return "VERDE"

def recomendacion(color, rojas, amarillas):
    if color == "ROJO":
        return f"¿NECESITA AYUDA? SÍ - PLAN RESCATE: Llamar a papás, asesoría 3x semana en {', '.join(rojas) if rojas else 'materias reprobadas'}"
    elif color == "AMARILLO":
        lista = rojas + amarillas
        return f"¿NECESITA AYUDA? SÍ - PLAN PREVENCIÓN: Asesoría 2x semana en {', '.join(lista) if lista else 'materias bajas'}, 30 min diario"
    else:
        return "¿NECESITA AYUDA? NO - PLAN MANTENER: Felicitarlo y ponerlo de tutor"

# --- DATOS ---
datos_1A = [
    ["Ana García", 4, 8.7, 8.0, 6.9, 9.2, 9.0, 7.2, 9.3, 6.6],
    ["Luis Pérez", 14, 6.9, 6.2, 4.6, 7.7, 6.6, 5.9, 5.8, 6.8],
    ["María López", 6, 7.0, 5.8, 6.5, 8.7, 8.6, 8.0, 7.3, 9.1],
    ["Carlos Ruiz", 4, 7.2, 8.4, 9.8, 9.1, 7.6, 8.0, 8.2, 9.6],
    ["Sofía Hernández", 1, 8.1, 6.8, 8.2, 7.2, 6.8, 6.7, 7.2, 8.9],
    ["Diego Martínez", 9, 6.8, 6.9, 8.2, 6.4, 7.5, 4.9, 7.1, 8.3],
    ["Valentina Torres", 8, 6.2, 8.1, 5.8, 5.9, 6.2, 8.9, 8.5, 8.1],
    ["Juan Sánchez", 0, 7.9, 8.8, 8.6, 10.0, 8.5, 9.5, 8.1, 10.0],
    ["Camila Ramírez", 2, 7.6, 10.0, 8.5, 8.7, 8.8, 7.2, 10.0, 9.0],
    ["Andrés Flores", 12, 6.8, 4.6, 5.5, 6.6, 5.8, 4.4, 6.4, 5.5],
    ["Paola Mendoza", 5, 6.1, 9.0, 7.6, 7.6, 8.3, 6.8, 6.0, 7.6],
    ["Bruno Castro", 4, 7.3, 6.2, 7.4, 6.1, 9.1, 7.2, 8.5, 8.0],
    ["Elena Vargas", 0, 6.7, 8.9, 6.9, 7.4, 10.0, 7.9, 7.8, 9.0],
    ["Marco Díaz", 5, 6.9, 6.7, 8.1, 5.8, 6.9, 9.2, 7.9, 7.3],
    ["Lucía Ortiz", 10, 7.7, 7.7, 7.9, 6.1, 6.6, 5.5, 7.4, 6.5],
]
datos_1B = [
    ["Ángel Torres", 5, 8.6, 6.7, 8.6, 6.1, 7.2, 8.7, 6.4, 6.8],
    ["Bianca Luna", 2, 6.9, 9.4, 8.1, 9.1, 8.0, 7.0, 7.1, 9.5],
    ["Cristian Vega", 9, 6.8, 5.8, 6.2, 5.1, 6.3, 5.1, 6.8, 4.6],
    ["Diana Paredes", 2, 8.4, 8.5, 8.8, 7.7, 8.9, 9.2, 9.6, 8.4],
    ["Esteban Ríos", 3, 8.5, 6.5, 9.1, 7.6, 9.2, 8.1, 6.5, 6.5],
    ["Fátima Gómez", 13, 4.3, 4.1, 5.6, 5.7, 5.2, 4.8, 4.2, 7.0],
    ["Gael Medina", 11, 7.9, 6.5, 5.4, 6.2, 8.5, 8.1, 6.8, 6.0],
    ["Hanna Cruz", 7, 8.3, 7.3, 7.1, 6.8, 6.3, 6.6, 7.1, 5.8],
    ["Iker Salazar", 2, 7.3, 7.5, 8.1, 8.6, 7.5, 8.1, 9.2, 8.9],
    ["Julia Ortiz", 13, 7.1, 6.5, 7.6, 7.3, 6.4, 4.7, 7.8, 6.5],
    ["Kevin Bravo", 3, 7.7, 6.9, 7.5, 8.7, 8.1, 6.1, 7.1, 6.6],
    ["Luna Herrera", 8, 8.9, 6.5, 6.6, 8.8, 8.3, 7.5, 6.6, 6.9],
    ["Miguel Ángel Soto", 10, 6.4, 7.4, 7.5, 6.9, 7.2, 7.1, 8.1, 8.3],
    ["Nadia Peña", 2, 10.0, 9.4, 8.0, 7.1, 10.0, 8.0, 7.5, 9.8],
    ["Omar Fuentes", 4, 7.4, 8.4, 7.8, 6.6, 7.3, 8.1, 6.5, 6.2],
    ["Paula Cabrera", 4, 9.1, 9.1, 7.6, 6.6, 7.4, 7.5, 8.7, 8.4],
    ["Quetzal Méndez", 11, 8.2, 5.8, 5.1, 6.0, 5.8, 7.2, 7.1, 7.6],
    ["Rosa Jiménez", 9, 7.4, 6.4, 6.9, 6.2, 7.2, 5.8, 8.4, 6.8],
]
datos_1C = [
    ["Alejandro Ríos", 2, 9.2, 8.8, 7.4, 7.9, 8.3, 9.3, 7.0, 9.6],
    ["Fernanda Cruz", 4, 8.6, 7.7, 7.1, 7.8, 7.5, 6.3, 7.4, 9.1],
    ["Gabriel Soto", 0, 8.8, 8.8, 8.1, 6.4, 8.3, 7.3, 8.3, 7.7],
    ["Isabella Luna", 8, 8.5, 8.6, 5.8, 6.1, 8.7, 7.2, 7.6, 7.3],
    ["Mateo Herrera", 6, 5.8, 5.7, 5.7, 7.5, 6.0, 5.8, 6.0, 7.6],
    ["Renata Peña", 1, 7.4, 9.9, 7.3, 8.2, 9.0, 8.9, 7.4, 7.4],
    ["Emiliano Vega", 7, 8.5, 6.1, 7.3, 6.3, 8.3, 6.9, 6.1, 7.9],
    ["Natalia Campos", 3, 8.6, 7.0, 7.2, 7.4, 9.2, 7.2, 8.7, 8.5],
    ["Sebastián Núñez", 4, 8.6, 7.7, 6.9, 7.7, 8.4, 6.4, 8.6, 7.8],
    ["Daniela Reyes", 8, 7.6, 8.8, 6.3, 6.1, 7.4, 5.7, 7.4, 6.0],
    ["Rodrigo Aguilar", 2, 8.2, 7.1, 9.5, 10.0, 8.5, 7.8, 8.1, 9.4],
    ["Valeria Morales", 10, 5.2, 5.3, 7.7, 7.2, 8.0, 7.9, 6.6, 5.5],
    ["Iván Jiménez", 2, 9.7, 6.8, 10.0, 8.3, 7.5, 7.7, 10.0, 7.8],
    ["Carmen Delgado", 8, 5.6, 6.8, 7.5, 6.9, 6.3, 7.3, 6.6, 6.5],
    ["Óscar Bravo", 6, 7.2, 9.1, 6.3, 8.6, 8.4, 8.5, 8.9, 6.3],
    ["Jimena Salazar", 4, 7.7, 10.0, 7.5, 7.4, 8.2, 8.6, 6.8, 7.3],
    ["Pablo Fuentes", 5, 8.0, 8.0, 8.6, 9.2, 6.8, 7.9, 7.6, 9.2],
    ["Andrea Ponce", 8, 8.1, 8.4, 7.6, 8.4, 8.0, 7.9, 5.7, 5.5],
    ["Hugo Cabrera", 1, 7.9, 7.0, 8.5, 8.5, 6.9, 7.2, 9.4, 7.2],
    ["Sara Medina", 2, 9.4, 7.3, 6.7, 9.6, 9.5, 7.1, 10.0, 9.5],
]

salones = {"1A": datos_1A, "1B": datos_1B, "1C": datos_1C}

col1, col2 = st.columns(2)
with col1:
    salon = st.selectbox("Elige el salón:", ["1A", "1B", "1C"])
with col2:
    nombres = [f[0] for f in salones[salon]]
    nombre_sel = st.selectbox("Elige el alumno:", nombres)

alumno = [f for f in salones[salon] if f[0] == nombre_sel][0]
faltas_orig, notas_orig = alumno[1], alumno[2:]

st.markdown("---")
st.subheader(f"✏️ Modifica a {nombre_sel} - Salón {salon}")
st.write("Mueve las barritas. El resultado cambia al instante.")

faltas = st.slider("Faltas", 0, 15, int(faltas_orig))
nuevas_notas = []
cols = st.columns(4)
for i, m in enumerate(materias):
    with cols[i % 4]:
        v = st.slider(m, 0.0, 10.0, float(notas_orig[i]), step=0.1)
        nuevas_notas.append(v)

prom = round(sum(nuevas_notas) / len(nuevas_notas), 1)
color = color_alumno(prom, faltas)
rojas = [materias[i] for i, v in enumerate(nuevas_notas) if v < 6]
amarillas = [materias[i] for i, v in enumerate(nuevas_notas) if 6 <= v < 7.5]

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Promedio", prom)
c2.metric("Faltas", faltas)
with c3:
    if color == "ROJO":
        st.error(f"🔴 COLOR: {color}")
    elif color == "AMARILLO":
        st.warning(f"🟡 COLOR: {color}")
    else:
        st.success(f"🟢 COLOR: {color}")

st.info(recomendacion(color, rojas, amarillas))

df_alumno = pd.DataFrame({"Materia": materias, "Calificación": nuevas_notas, "Color": [color_calif(v) for v in nuevas_notas]})
st.dataframe(df_alumno, use_container_width=True)

fig, ax = plt.subplots(figsize=(10, 4))
colores = ["#e74c3c" if v < 6 else "#f1c40f" if v < 7.5 else "#2ecc71" for v in nuevas_notas]
ax.bar(materias_cortas, nuevas_notas, color=colores, edgecolor="black")
for i, v in enumerate(nuevas_notas):
    ax.text(i, v + 0.3, str(v), ha="center", fontweight="bold")
ax.axhline(6.0, color="#e74c3c", linestyle="--")
ax.axhline(7.5, color="#2ecc71", linestyle="--")
ax.set_ylim(0, 11)
ax.set_ylabel("Calificación")
ax.set_title(f"{nombre_sel} - {salon} - Prom: {prom} - {color}")
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)

st.markdown("---")
st.subheader(f"📊 Promedio del salón {salon} (datos originales)")
prom_materias = [round(sum(f[2+i] for f in salones[salon]) / len(salones[salon]), 2) for i in range(8)]
prom_salon = round(sum(prom_materias) / 8, 2)
st.write(f"**Promedio del salón {salon}: {prom_salon} - {color_calif(prom_salon)}**")

fig2, ax2 = plt.subplots(figsize=(10, 4))
colores2 = ["#e74c3c" if v < 6 else "#f1c40f" if v < 7.5 else "#2ecc71" for v in prom_materias]
ax2.bar(materias_cortas, prom_materias, color=colores2, edgecolor="black")
for i, v in enumerate(prom_materias):
    ax2.text(i, v + 0.3, str(v), ha="center", fontweight="bold")
ax2.axhline(6.0, color="#e74c3c", linestyle="--")
ax2.axhline(7.5, color="#2ecc71", linestyle="--")
ax2.set_ylim(0, 11)
ax2.set_title(f"PROMEDIO DEL SALON {salon} = {prom_salon} | {color_calif(prom_salon)}")
ax2.grid(axis="y", alpha=0.3)
st.pyplot(fig2)
