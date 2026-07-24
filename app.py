import streamlit as st
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent

from src.db.db_manager import DBManager

# Configuracion de la pagina
st.set_page_config(
    page_title="JobSync IA - Headhunter",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Mostrar mensajes de exito pendientes ---
if 'mensaje_exito' in st.session_state:
    st.toast(st.session_state.mensaje_exito, icon="✅")
    del st.session_state.mensaje_exito

# --- Funciones Auxiliares ---

def cargar_json(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def guardar_json(ruta, datos):
    """Guarda el JSON creando primero un backup con timestamp del archivo anterior."""
    ruta = Path(ruta)
    if ruta.exists():
        backup_dir = ruta.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy(ruta, backup_dir / f"{ruta.stem}_{timestamp}{ruta.suffix}")
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def ejecutar_agente():
    with st.spinner("Buscando y evaluando vacantes con IA..."):
        try:
            result = subprocess.run(
                [sys.executable, str(BASE_DIR / "src" / "main.py")],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                st.success("Analisis completado con exito.")
            else:
                st.error(f"Error en la ejecucion:\n{result.stderr}")
        except Exception as e:
            st.error(f"Error inesperado: {e}")

def actualizar_estado(uri, nuevo_estado):
    db = DBManager()
    db.actualizar_estado_vacante(uri, nuevo_estado)

def lista_a_texto(lista):
    """Convierte una lista de strings a texto con un elemento por linea."""
    if not lista: return ""
    return "\n".join(str(x) for x in lista)

def texto_a_lista(texto):
    """Convierte texto con un elemento por linea a una lista de strings, sin lineas vacias."""
    return [linea.strip() for linea in texto.split("\n") if linea.strip()]

# --- Función Auxiliar para Data Editors ---
def procesar_data_editor(datos_previos, datos_editados, columnas_requeridas):
    nueva_lista = []
    for i, fila in enumerate(datos_editados):
        # Chequear si la fila tiene datos
        if any(str(v).strip() for v in fila.values() if v is not None):
            obj = dict(datos_previos[i]) if i < len(datos_previos) else {}
            for k in columnas_requeridas:
                if k in fila:
                    obj[k] = fila[k]
            nueva_lista.append(obj)
    return nueva_lista

# --- Editor estructurado del CV ---

def render_editor_cv(cv_data):
    cv_data = dict(cv_data)
    
    # 1. Informacion Personal
    if "informacion_personal" not in cv_data: cv_data["informacion_personal"] = {}
    info = cv_data["informacion_personal"]
    if "contacto" not in info: info["contacto"] = {}

    st.markdown("##### Datos Generales")
    col1, col2 = st.columns(2)
    with col1:
        info["nombre"] = st.text_input("Nombre completo", info.get("nombre", ""))
        info["titulo_profesional"] = st.text_input("Titulo profesional", info.get("titulo_profesional", ""))
        info["ubicacion"] = st.text_input("Ubicacion", info.get("ubicacion", ""))
    with col2:
        info["contacto"]["email"] = st.text_input("Email", info["contacto"].get("email", ""))
        info["contacto"]["telefono"] = st.text_input("Telefono", info["contacto"].get("telefono", ""))
        info["contacto"]["linkedin"] = st.text_input("LinkedIn", info["contacto"].get("linkedin", ""))
        info["contacto"]["portfolio_o_github"] = st.text_input("Portfolio / GitHub", info["contacto"].get("portfolio_o_github", ""))

    st.markdown("##### Idiomas")
    idiomas_prev = info.get("idiomas", [])
    idiomas_norm = [{"idioma": i.get("idioma", ""), "nivel": i.get("nivel", "")} for i in idiomas_prev] if idiomas_prev else [{"idioma": "", "nivel": ""}]
    idiomas_ed = st.data_editor(idiomas_norm, num_rows="dynamic", use_container_width=True, key="idiomas_ed")
    info["idiomas"] = procesar_data_editor(idiomas_prev, idiomas_ed, ["idioma", "nivel"])

    cv_data["resumen_profesional"] = st.text_area("Resumen Profesional", cv_data.get("resumen_profesional", ""), height=100)

    # 2. Habilidades Tecnicas
    st.markdown("##### Habilidades Tecnicas")
    if "habilidades_tecnicas" not in cv_data: cv_data["habilidades_tecnicas"] = {}
    ht = cv_data["habilidades_tecnicas"]
    
    col_ht1, col_ht2 = st.columns(2)
    with col_ht1:
        ht["software_herramientas"] = texto_a_lista(st.text_area("Software y Herramientas (Una por linea)", lista_a_texto(ht.get("software_herramientas", []))))
        ht["metodologias"] = texto_a_lista(st.text_area("Metodologias (Una por linea)", lista_a_texto(ht.get("metodologias", []))))
    with col_ht2:
        ht["normativas_estandares"] = texto_a_lista(st.text_area("Normativas y Estandares (Una por linea)", lista_a_texto(ht.get("normativas_estandares", []))))
        ht["otras"] = texto_a_lista(st.text_area("Otras (Una por linea)", lista_a_texto(ht.get("otras", []))))

    # 3. Habilidades Blandas
    st.markdown("##### Habilidades Blandas")
    cv_data["habilidades_blandas"] = texto_a_lista(st.text_area("Habilidades Blandas (Una por linea)", lista_a_texto(cv_data.get("habilidades_blandas", [])), height=100))

    # 4. Experiencia Laboral
    st.markdown("##### Experiencia Laboral")
    exp_prev = cv_data.get("experiencia_laboral", [])
    exp_norm = [{"puesto": e.get("puesto", ""), "empresa": e.get("empresa", ""), "fecha_inicio": e.get("fecha_inicio", ""), "fecha_fin": e.get("fecha_fin", "")} for e in exp_prev] if exp_prev else [{"puesto": "", "empresa": "", "fecha_inicio": "", "fecha_fin": ""}]
    exp_ed = st.data_editor(exp_norm, num_rows="dynamic", use_container_width=True, key="exp_ed")
    cv_data["experiencia_laboral"] = procesar_data_editor(exp_prev, exp_ed, ["puesto", "empresa", "fecha_inicio", "fecha_fin"])

    # 5. Educacion
    st.markdown("##### Educacion")
    edu_prev = cv_data.get("educacion", [])
    edu_norm = [{"grado": e.get("grado", ""), "institucion": e.get("institucion", ""), "promedio": e.get("promedio", ""), "fecha_graduacion": e.get("fecha_graduacion", "")} for e in edu_prev] if edu_prev else [{"grado": "", "institucion": "", "promedio": "", "fecha_graduacion": ""}]
    edu_ed = st.data_editor(edu_norm, num_rows="dynamic", use_container_width=True, key="edu_ed")
    cv_data["educacion"] = procesar_data_editor(edu_prev, edu_ed, ["grado", "institucion", "promedio", "fecha_graduacion"])

    # 6. Certificaciones
    st.markdown("##### Certificaciones")
    cert_prev = cv_data.get("certificaciones", [])
    cert_norm = [{"nombre": c.get("nombre", ""), "entidad": c.get("entidad", ""), "fecha_obtencion": c.get("fecha_obtencion", ""), "credencial_url": c.get("credencial_url", "")} for c in cert_prev] if cert_prev else [{"nombre": "", "entidad": "", "fecha_obtencion": "", "credencial_url": ""}]
    cert_ed = st.data_editor(cert_norm, num_rows="dynamic", use_container_width=True, key="cert_ed")
    cv_data["certificaciones"] = procesar_data_editor(cert_prev, cert_ed, ["nombre", "entidad", "fecha_obtencion", "credencial_url"])

    # 7. Proyectos Destacados
    st.markdown("##### Proyectos Destacados")
    proy_prev = cv_data.get("proyectos_destacados", [])
    proy_norm = [{"nombre": p.get("nombre", ""), "descripcion": p.get("descripcion", ""), "fecha": p.get("fecha", ""), "url_o_evidencia": p.get("url_o_evidencia", "")} for p in proy_prev] if proy_prev else [{"nombre": "", "descripcion": "", "fecha": "", "url_o_evidencia": ""}]
    proy_ed = st.data_editor(proy_norm, num_rows="dynamic", use_container_width=True, key="proy_ed")
    cv_data["proyectos_destacados"] = procesar_data_editor(proy_prev, proy_ed, ["nombre", "descripcion", "fecha", "url_o_evidencia"])

    # 8. Disponibilidad
    st.markdown("##### Disponibilidad")
    if "disponibilidad" not in cv_data: cv_data["disponibilidad"] = {}
    disp = cv_data["disponibilidad"]
    
    col_disp1, col_disp2 = st.columns(2)
    with col_disp1:
        disp["modalidad"] = texto_a_lista(st.text_area("Modalidades (Una por linea)", lista_a_texto(disp.get("modalidad", [])), height=80))
    with col_disp2:
        disp["tipo_contrato"] = texto_a_lista(st.text_area("Tipos de contrato (Una por linea)", lista_a_texto(disp.get("tipo_contrato", [])), height=80))
    disp["fecha_disponible"] = st.text_input("Fecha disponible", disp.get("fecha_disponible", ""))

    return cv_data

# --- Editor estructurado de Parametros ---

def render_editor_parametros(params_data):
    params_data = dict(params_data)
    if "busqueda_api" not in params_data: params_data["busqueda_api"] = {}
    if "criterios_evaluacion_ia" not in params_data: params_data["criterios_evaluacion_ia"] = {}
    if "configuracion_ranking" not in params_data: params_data["configuracion_ranking"] = {}
    
    busqueda = params_data["busqueda_api"]
    criterios = params_data["criterios_evaluacion_ia"]
    ranking = params_data["configuracion_ranking"]

    st.markdown("##### Busqueda en Google Jobs (SerpApi)")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        busqueda["ubicacion"] = st.text_input("Ubicacion de busqueda", busqueda.get("ubicacion", ""))
        busqueda["modalidad"] = texto_a_lista(st.text_area("Modalidad permitida (Una por linea)", lista_a_texto(busqueda.get("modalidad", [])), height=80))
    with col_b2:
        busqueda["antiguedad_publicacion_dias"] = st.number_input("Antiguedad maxima de la vacante (dias)", value=int(busqueda.get("antiguedad_publicacion_dias", 15)), step=1)
    
    col_b3, col_b4 = st.columns(2)
    with col_b3:
        busqueda["palabras_clave_incluir"] = texto_a_lista(st.text_area("Palabras clave a INCLUIR (Una por linea)", lista_a_texto(busqueda.get("palabras_clave_incluir", [])), height=100))
    with col_b4:
        busqueda["palabras_clave_excluir"] = texto_a_lista(st.text_area("Palabras clave a EXCLUIR (Una por linea)", lista_a_texto(busqueda.get("palabras_clave_excluir", [])), height=100))

    st.markdown("##### Criterios de Evaluacion (IA Gemini)")
    
    # Nivel Experiencia
    if "nivel_experiencia" not in criterios: criterios["nivel_experiencia"] = {}
    ne = criterios["nivel_experiencia"]
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1: ne["categoria"] = st.text_input("Categoria esperada (Ej. Junior)", ne.get("categoria", ""))
    with col_e2: ne["anos_minimos"] = st.number_input("Anos min de exp", value=int(ne.get("anos_minimos", 0)), step=1)
    with col_e3: ne["anos_maximos"] = st.number_input("Anos max de exp", value=int(ne.get("anos_maximos", 5)), step=1)

    # Requisitos Vacante
    st.write("**Requisitos que la vacante debe mencionar**")
    req_prev = criterios.get("requisitos_vacante_debe_mencionar", [])
    req_norm = [{"requisito": r.get("requisito", ""), "prioridad": r.get("prioridad", "deseable")} for r in req_prev] if req_prev else [{"requisito": "", "prioridad": "deseable"}]
    req_ed = st.data_editor(req_norm, num_rows="dynamic", use_container_width=True, key="req_ed")
    criterios["requisitos_vacante_debe_mencionar"] = procesar_data_editor(req_prev, req_ed, ["requisito", "prioridad"])

    # Beneficios Deseados
    st.write("**Beneficios Deseados**")
    ben_prev = criterios.get("beneficios_deseados", [])
    ben_norm = [{"beneficio": b.get("beneficio", ""), "prioridad": b.get("prioridad", "deseable")} for b in ben_prev] if ben_prev else [{"beneficio": "", "prioridad": "deseable"}]
    ben_ed = st.data_editor(ben_norm, num_rows="dynamic", use_container_width=True, key="ben_ed")
    criterios["beneficios_deseados"] = procesar_data_editor(ben_prev, ben_ed, ["beneficio", "prioridad"])

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        criterios["habilidades_propias_a_destacar"] = texto_a_lista(st.text_area("Tus habilidades a destacar (Una por linea)", lista_a_texto(criterios.get("habilidades_propias_a_destacar", [])), height=120))
    with col_r2:
        criterios["sectores_a_evitar"] = texto_a_lista(st.text_area("Sectores a evitar (Una por linea)", lista_a_texto(criterios.get("sectores_a_evitar", [])), height=120))

    # Salario
    if "rango_salarial_esperado" not in criterios: criterios["rango_salarial_esperado"] = {}
    sal = criterios["rango_salarial_esperado"]
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1: sal["minimo"] = st.number_input("Salario Min", value=int(sal.get("minimo", 0)), step=1000)
    with col_s2: sal["maximo"] = st.number_input("Salario Max", value=int(sal.get("maximo", 0)), step=1000)
    with col_s3: sal["moneda"] = st.text_input("Moneda", sal.get("moneda", "MXN"))
    with col_s4: sal["negociable"] = st.checkbox("Negociable", value=bool(sal.get("negociable", True)))

    st.markdown("##### Configuracion de Ranking")
    ranking["descartar_si_falta_indispensable"] = st.checkbox("Descartar vacante si falta algun requisito 'indispensable'", value=bool(ranking.get("descartar_si_falta_indispensable", True)))
    
    st.write("Orden de prioridad para puntaje ATS")
    ranking["orden_prioridad_criterios"] = texto_a_lista(st.text_area("Criterios de prioridad (Uno por linea)", lista_a_texto(ranking.get("orden_prioridad_criterios", [])), height=120))

    return params_data

# --- Interfaz Principal ---
st.title("JobSync IA - Tu Headhunter Personal")
st.markdown("Analiza vacantes de forma inteligente, descubre tu nivel de compatibilidad y haz seguimiento de tus aplicaciones.")

# --- Barra Lateral ---
with st.sidebar:
    st.header("Configuracion")

    if st.button("Ejecutar Busqueda y Evaluacion", type="primary", use_container_width=True):
        ejecutar_agente()

    st.divider()
    st.subheader("Archivos de Datos")

    ruta_cv = BASE_DIR / "data" / "cv.json"
    ruta_params = BASE_DIR / "data" / "parametros.json"

    cv_data = cargar_json(ruta_cv) or {}
    params_data = cargar_json(ruta_params) or {}

    # --- CV ---
    with st.expander("Editar CV", expanded=False):
        modo_avanzado_cv = st.checkbox("Modo avanzado (editar JSON directo)", key="modo_avanzado_cv")

        if modo_avanzado_cv:
            cv_text = st.text_area(
                "Contenido cv.json",
                value=json.dumps(cv_data, indent=4, ensure_ascii=False),
                height=300,
                key="cv_area",
            )
            if st.button("Guardar CV (JSON)", key="btn_cv_json"):
                try:
                    nuevo_cv = json.loads(cv_text)
                    guardar_json(ruta_cv, nuevo_cv)
                    st.session_state.mensaje_exito = "CV guardado correctamente."
                    st.rerun()
                except json.JSONDecodeError as e:
                    st.error(f"JSON invalido en la linea {e.lineno}, columna {e.colno}: {e.msg}")
        else:
            with st.form("form_cv", border=False):
                cv_editado = render_editor_cv(cv_data)
                guardar_cv = st.form_submit_button("Guardar CV", type="primary")
                if guardar_cv:
                    guardar_json(ruta_cv, cv_editado)
                    st.session_state.mensaje_exito = "CV guardado correctamente."
                    st.rerun()

    # --- Parametros ---
    with st.expander("Editar Parametros", expanded=False):
        modo_avanzado_params = st.checkbox("Modo avanzado (editar JSON directo)", key="modo_avanzado_params")

        if modo_avanzado_params:
            params_text = st.text_area(
                "Contenido parametros.json",
                value=json.dumps(params_data, indent=4, ensure_ascii=False),
                height=300,
                key="params_area",
            )
            if st.button("Guardar Parametros (JSON)", key="btn_params_json"):
                try:
                    nuevos_params = json.loads(params_text)
                    guardar_json(ruta_params, nuevos_params)
                    st.session_state.mensaje_exito = "Parámetros guardados correctamente."
                    st.rerun()
                except json.JSONDecodeError as e:
                    st.error(f"JSON invalido en la linea {e.lineno}, columna {e.colno}: {e.msg}")
        else:
            with st.form("form_params", border=False):
                params_editado = render_editor_parametros(params_data)
                guardar_params = st.form_submit_button("Guardar Parametros", type="primary")
                if guardar_params:
                    guardar_json(ruta_params, params_editado)
                    st.session_state.mensaje_exito = "Parámetros guardados correctamente."
                    st.rerun()

    # --- Backups disponibles ---
    backups_dir = BASE_DIR / "data" / "backups"
    if backups_dir.exists() and any(backups_dir.iterdir()):
        with st.expander("Historial de backups"):
            archivos_backup = sorted(backups_dir.iterdir(), key=os.path.getmtime, reverse=True)
            for archivo in archivos_backup[:10]:
                st.caption(f"{archivo.name}")

# --- Contenido Principal ---
db = DBManager()
vacantes = db.obtener_todas_vacantes()
ESTADOS_PERMITIDOS = ["Pendiente", "Aplicada", "En proceso", "Rechazada", "Aceptada"]

if vacantes:
    st.header("Resultados de la Evaluacion")

    opciones_filtro = ["Activas (Ocultar Rechazadas)", "Todas"] + ESTADOS_PERMITIDOS
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        estado_filtro = st.selectbox("Filtrar por estado:", opciones_filtro)
    with col_f2:
        umbral_minimo = st.slider("Ocultar menores a (%)", min_value=0, max_value=100, value=0, step=10)

    if estado_filtro == "Activas (Ocultar Rechazadas)":
        vacantes = [v for v in vacantes if v.get("estado", "Pendiente") != "Rechazada"]
    elif estado_filtro != "Todas":
        vacantes = [v for v in vacantes if v.get("estado", "Pendiente") == estado_filtro]
        
    vacantes = [v for v in vacantes if v.get("porcentaje_compatibilidad", 0) >= umbral_minimo]

    col1, col2, col3 = st.columns(3)
    col1.metric("Vacantes Mostradas", len(vacantes))

    mejores_matches = len([v for v in vacantes if v.get("porcentaje_compatibilidad", 0) >= 80])
    col2.metric("Mejores Matches (>= 80%)", mejores_matches)

    st.divider()

    for i, vacante in enumerate(vacantes):
        titulo = vacante.get("titulo_vacante") or vacante.get("titulo", "Sin Titulo")
        empresa = vacante.get("empresa", "Empresa Desconocida")
        compatibilidad = vacante.get("porcentaje_compatibilidad", 0)
        enlace = vacante.get("uri_aplicacion") or "#"
        estado_actual = vacante.get("estado") or "Pendiente"

        with st.container(border=True):
            col_izq, col_der, col_estado = st.columns([2.5, 1, 1.5])
            with col_izq:
                st.subheader(f"{titulo}")
                st.caption(f"Empresa: {empresa}")
            with col_der:
                st.metric("Compatibilidad", f"{compatibilidad}%")
            with col_estado:
                indice_estado = ESTADOS_PERMITIDOS.index(estado_actual) if estado_actual in ESTADOS_PERMITIDOS else 0
                nuevo_estado = st.selectbox(
                    "Estado de aplicacion:",
                    ESTADOS_PERMITIDOS,
                    index=indice_estado,
                    key=f"estado_{i}_{enlace}",
                )

                if nuevo_estado != estado_actual:
                    actualizar_estado(enlace, nuevo_estado)
                    st.rerun()

                if enlace and enlace != "#":
                    st.link_button("Ir a la Vacante", url=enlace, use_container_width=True)
                else:
                    st.button("Sin enlace", disabled=True, key=f"btn_{i}", use_container_width=True)

            tab1, tab2, tab3, tab4 = st.tabs(["Analisis", "Requisitos", "Recomendaciones ATS", "Descripcion Original"])

            with tab1:
                st.write(vacante.get("notas_match", "Sin notas del evaluador."))

            with tab2:
                col_req1, col_req2 = st.columns(2)
                with col_req1:
                    st.markdown("**Cumples con:**")
                    for req in vacante.get("requisitos_cumplidos", []):
                        st.markdown(f"- {req}")
                with col_req2:
                    st.markdown("**Te falta/Opcional:**")
                    faltantes = vacante.get("requisitos_faltantes", [])
                    if faltantes:
                        for req in faltantes:
                            st.markdown(f"- {req}")
                    else:
                        st.markdown("*- Ninguno importante -*")

            with tab3:
                st.markdown("**Consejos para tu CV:**")
                for rec in vacante.get("recomendaciones_ats", []):
                    st.markdown(f"- {rec}")
                    
            with tab4:
                st.write(vacante.get("descripcion", "La descripcion original no esta disponible."))
else:
    st.info("Aun no hay resultados en la base de datos. Configura tu CV y Parametros, luego ejecuta el agente desde el menu lateral.")
