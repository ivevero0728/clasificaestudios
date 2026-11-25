import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sistema de Alerta Temprana Escolar ", page_icon="🎓", layout="wide")

st.title("🎓 Sistgema de Alerta Temprana Escolar")
st.caption("lo que les vamos a presentar es una aplicacion de sistemas de alerta temprana escolar como su nombre lo meniona lo que hace esta aplicacion es presentar los semestres, grupos, alumnos por cada salon,y tambien nos va a vencionar quienes son los estudiantes que estan en peligro y cuales no, esto nos lo va a representar con los colores (rojo, amarillo, verde) esto nos lo va a marcar por grupo ya que  en cada salon hay sierta cantida de estudiantes los cuales la mayoria son 17 o 16 tambien, cuenta con 4 grupos loa cuales son A , B, C , D, esto nos permite tener un mejor control para los datos de los estudiantes para ubicarlos de manera mas facil esto nos permite ver si los alumnos nececitan ayuda o si van bien,  ya que en ocaciones es mas dificil para los maestros ubicar a los estudiantes que necesitan ayuda, cada estudiante dependendiendo sus color tiene su propopio plan personal de estudios o tambien alertas en caso de que su caso necesite ir a direccion lo que hace mas facil la identificacion de los estudiantes en riesgo esto ayuda a los maestros encargados de la AREA DE CONTROL ESCOLAR  puedan revisar que alumno tiene mas problemas y que segumiento tiene que tener ")

# =========================================================
# 1. DATOS - 200 ALUMNOS REPARTIDOS EN 12 SALONES
# =========================================================
@st.cache_data
def crear_todos_los_datos():
    np.random.seed(123)
    lista = []

    nombres = ["Ana", "Luis", "Maria", "Carlos", "Sofia", "Diego", "Valeria", "Juan", "Camila", "Miguel", "Fernanda", "Alejandro", "Lucia", "Pedro", "Daniela", "Jorge", "Paola", "Ricardo", "Andrea", "Fernando", "Gabriela", "Hugo", "Karina", "Oscar", "Elena", "Brenda", "Ivan", "Monica", "Saul", "Diana", "Rosa", "Andres"]
    ap_paterno = ["Garcia", "Hernandez", "Martinez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Vazquez", "Reyes", "Morales", "Jimenez", "Herrera", "Cruz", "Mendoza", "Castro", "Ortiz", "Rojas", "Delgado", "Vega", "Guerrero", "Medina", "Rios", "Navarro", "Campos", "Luna", "Aguilar", "Salazar", "Pineda", "Cabrera"]
    ap_materno = ["Gomez", "Diaz", "Ruiz", "Alvarez", "Romero", "Juarez", "Castillo", "Silva", "Mendez", "Chavez", "Ortega", "Leon", "Vargas", "Ramos", "Gutierrez", "Dominguez", "Serrano", "Cortes", "Peña", "Lara", "Fuentes", "Pacheco", "Acosta", "Blanco", "Cabrera", "Zamora", "Figueroa", "Padilla", "Mejia", "Bautista", "Rosales", "Nieto"]

    # Salones con su semestre y cuántos alumnos lleva cada uno para sumar 200
    # Primero = 1er Semestre, Tercero = 3er Semestre, Quinto = 5to Semestre
    salones_con_cantidad = [
        ("Primero", "A", "1er Semestre", 17),
        ("Primero", "B", "1er Semestre", 17),
        ("Primero", "C", "1er Semestre", 17),
        ("Primero", "D", "1er Semestre", 17),
        ("Tercero", "A", "3er Semestre", 17),
        ("Tercero", "B", "3er Semestre", 17),
        ("Tercero", "C", "3er Semestre", 16),
        ("Tercero", "D", "3er Semestre", 16),
        ("Quinto", "A", "5to Semestre", 17),
        ("Quinto", "B", "5to Semestre", 17),
        ("Quinto", "C", "5to Semestre", 16),
        ("Quinto", "D", "5to Semestre", 16),
    ]

    for idx_salon, (grado, grupo, semestre, cantidad) in enumerate(salones_con_cantidad):
        for i in range(1, cantidad + 1):
            n1 = nombres[(i - 1 + idx_salon * 3) % len(nombres)]
            a1 = ap_paterno[(i - 1 + idx_salon * 5) % len(ap_paterno)]
            a2 = ap_materno[(i * 2 + idx_salon * 4) % len(ap_materno)]
            nombre_inv = f"{n1} {a1} {a2}"

            calif = round(np.random.uniform(4.0, 10.0), 1)
            asist = int(np.random.randint(50, 101))
            tareas = int(np.random.randint(40, 101))
            faltas = int(np.random.randint(0, 15))

            lista.append({
                "matricula": f"{grado[:3].upper()}-{grupo}-{i:02d}",
                "nombre": nombre_inv,
                "grado": grado,
                "grupo": grupo,
                "semestre": semestre,
                "salon": f"{grado} {grupo}",
                "calificacion": calif,
                "asistencia": asist,
                "tareas": tareas,
                "faltas": faltas
            })
    return pd.DataFrame(lista)

datos_todos = crear_todos_los_datos()

def obtener_semaforo(calif, asist, faltas):
    if calif < 6 or asist < 60 or faltas >= 10:
        return "🔴 ROJO"
    elif calif < 7.5 or asist < 75:
        return "🟡 AMARILLO"
    else:
        return "🟢 VERDE"

def obtener_recomendacion(color):
    if color == "🔴 ROJO":
        return "🚨 MANDAR A DIRECCIÓN | Llamar a papás, canalizar a tutoría, plan urgente, seguimiento semanal"
    elif color == "🟡 AMARILLO":
        return "🟡 LO MANEJA EL DOCENTE | Hablar con alumno, asesoría 30 min, compromiso de asistencia y tareas. Si en 2 semanas no mejora, pasa a ROJO"
    else:
        return "🟢 TODO BIEN | Felicitarlo, puede ayudar a compañeros, seguimiento normal"

# =========================================================
# 2. ELEGIR SALÓN Y SEMESTRE
# =========================================================
st.subheader("1. Elige el Salón")

col_g1, col_g2 = st.columns(2)
with col_g1:
    grado_sel = st.selectbox("Grado / Semestre", ["Primero", "Tercero", "Quinto"])
with col_g2:
    grupo_sel = st.selectbox("Grupo", ["A", "B", "C", "D"])

salon_sel = f"{grado_sel} {grupo_sel}"
filtrados = datos_todos[datos_todos["salon"] == salon_sel].copy()
filtrados["semaforo"] = filtrados.apply(lambda r: obtener_semaforo(r["calificacion"], r["asistencia"], r["faltas"]), axis=1)
filtrados["recomendacion"] = filtrados["semaforo"].apply(obtener_recomendacion)

total_salon = len(filtrados)
semestre_sel = filtrados["semestre"].iloc[0] if total_salon > 0 else ""

st.success(f"Estás viendo: **{salon_sel} - {semestre_sel}** | Tiene **{total_salon} alumnos**")

c_rojo = len(filtrados[filtrados["semaforo"] == "🔴 ROJO"])
c_ama = len(filtrados[filtrados["semaforo"] == "🟡 AMARILLO"])
c_ver = len(filtrados[filtrados["semaforo"] == "🟢 VERDE"])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Salón", total_salon)
m2.metric("🔴 En ROJO", c_rojo)
m3.metric("🟡 En AMARILLO", c_ama)
m4.metric("🟢 En VERDE", c_ver)

# =========================================================
# 3. ELEGIR ALUMNO
# =========================================================
st.subheader("2. Elige al Estudiante")
alumno_nombre = st.selectbox("Alumno", filtrados["nombre"].tolist())
alumno = filtrados[filtrados["nombre"] == alumno_nombre].iloc[0]

# =========================================================
# 4. PESTAÑAS - TODO INTEGRADO
# =========================================================
tab1, tab2, tab3 = st.tabs([
    "📋 1. DATOS ORIGINALES - NO SE TOCAN",
    "🎛️ 2. SIMULADOR - AQUÍ SÍ MUEVES TODO",
    "📊 3. TODOS LOS DEL SALÓN"
])

with tab1:
    st.warning(f"DATOS ORIGINALES INTEGRADOS de {alumno['nombre']} | Salón {salon_sel} - {alumno['semestre']} | Estos NO se pueden modificar, son tu respaldo real.")
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Matrícula", alumno["matricula"])
    a2.metric("Calificación Original", alumno["calificacion"])
    a3.metric("Asistencia Original", f"{alumno['asistencia']}%")
    a4.metric("Faltas Originales", alumno["faltas"])
    b1, b2, b3 = st.columns(3)
    b1.metric("Salón", alumno["salon"])
    b2.metric("Tareas Originales", f"{alumno['tareas']}%")
    b3.metric("Semáforo Original", alumno["semaforo"])
    st.markdown(f"### Clasificación Original: {alumno['semaforo']}")
    st.info(alumno["recomendacion"])

with tab2:
    st.info("SIMULADOR: Aquí mueves las barritas para probar. Los datos originales de la Pestaña 1 NO cambian.")
    s1, s2 = st.columns(2)
    with s1:
        calif_sim = st.slider("Calificación simulada", 0.0, 10.0, float(alumno["calificacion"]), 0.1)
        asist_sim = st.slider("Asistencia simulada %", 0, 100, int(alumno["asistencia"]))
    with s2:
        tareas_sim = st.slider("Tareas simuladas %", 0, 100, int(alumno["tareas"]))
        faltas_sim = st.slider("Faltas simuladas", 0, 30, int(alumno["faltas"]))

    color_sim = obtener_semaforo(calif_sim, asist_sim, faltas_sim)
    rec_sim = obtener_recomendacion(color_sim)
    st.divider()
    st.markdown(f"## Resultado Simulado: {color_sim}")
    st.write(f"Calificación: Antes {alumno['calificacion']} -> Ahora {calif_sim} | Asistencia: Antes {alumno['asistencia']}% -> Ahora {asist_sim}% | Faltas: Antes {alumno['faltas']} -> Ahora {faltas_sim}")

    if color_sim == "🔴 ROJO":
        st.error("🚨 ALERTA PARA DIRECCIÓN")
        st.write("1. Mandar reporte a Dirección / Tutoría")
        st.write("2. Llamar a papás / tutor")
        st.write("3. Plan de recuperación urgente")
        st.write("4. Seguimiento cada semana")
        mensaje = f"ALERTA DIRECCIÓN: Alumno {alumno['nombre']} - Salón {salon_sel} - {alumno['semestre']} - Matrícula {alumno['matricula']} en ROJO. Calif simulada: {calif_sim}, Asistencia: {asist_sim}%, Faltas: {faltas_sim}. Se solicita intervención de Dirección."
        st.text_area("Mensaje listo para copiar y mandar a Dirección:", mensaje, height=90)
    elif color_sim == "🟡 AMARILLO":
        st.warning("🟡 ATENCIÓN DEL DOCENTE - NO ES PARA DIRECCIÓN TODAVÍA")
        st.write("1. Hablar con el alumno esta semana")
        st.write("2. Asesoría de 30 min, ver qué tema le cuesta")
        st.write("3. Compromiso de asistencia y tareas")
        st.write("4. Revisar en 2 semanas, si no mejora pasa a ROJO y sí se avisa a Dirección")
    else:
        st.success("🟢 TODO BIEN")
        st.write("1. Felicitarlo en clase")
        st.write("2. Puede apoyar a compañeros que están en amarillo")
        st.write("3. Seguimiento normal, sin reporte")
    st.info(f"Recomendación: {rec_sim}")

with tab3:
    st.subheader(f"Todos los alumnos de {salon_sel} - {semestre_sel} - Todos con su semáforo y recomendación")
    filtro = st.selectbox("Filtrar por semáforo", ["Todos", "🔴 ROJO", "🟡 AMARILLO", "🟢 VERDE"])
    tabla_mostrar = filtrados
    if filtro != "Todos":
        tabla_mostrar = filtrados[filtrados["semaforo"] == filtro]
    st.dataframe(tabla_mostrar[["matricula", "nombre", "salon", "semestre", "calificacion", "asistencia", "tareas", "faltas", "semaforo", "recomendacion"]], use_container_width=True)
    st.write(f"- En ROJO hay que mandar a Dirección: {c_rojo} alumnos")
    st.write(f"- En AMARILLO los maneja el docente: {c_ama} alumnos")
    st.write(f"- En VERDE todo bien: {c_ver} alumnos")

st.divider()
st.subheader("Resumen de los 12 Salones - 200 alumnos en total")
resumen = datos_todos.copy()
resumen["semaforo"] = resumen.apply(lambda r: obtener_semaforo(r["calificacion"], r["asistencia"], r["faltas"]), axis=1)
tabla_resumen = resumen.groupby(["salon", "semaforo"]).size().unstack(fill_value=0)
for col in ["🔴 ROJO", "🟡 AMARILLO", "🟢 VERDE"]:
    if col not in tabla_resumen.columns:
        tabla_resumen[col] = 0
tabla_resumen["Total"] = tabla_resumen["🔴 ROJO"] + tabla_resumen["🟡 AMARILLO"] + tabla_resumen["🟢 VERDE"]
st.dataframe(tabla_resumen, use_container_width=True)

st.caption("Clasifica Estudios | TODO EN UN SOLO CÓDIGO | 12 Salones | 200 alumnos | 1er, 3er y 5to Semestre | Nombres inventados | Datos originales separados del simulador")
