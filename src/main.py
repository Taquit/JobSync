import json
import os
from extractor.serapi_job import SerpApiJobExtractor
from ai_agent.gemini import evaluar_vacantes_con_ia
from ai_agent.prompts import generar_system_prompt  
from db.db_manager import DBManager
from pathlib import Path
from ai_agent.ranking_calc import calcular_compatibilidad
from configs.ranking_config import RANKING_CONFIG

BASE_DIR = Path(__file__).resolve().parent.parent

def cargar_json(ruta):
    """Carga un archivo JSON desde el disco."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)



def main():
    print("Iniciando el Agente de Búsqueda de Empleo con IA...\n")

    # 1. Cargar Inputs
    print("Cargando perfil y parámetros de búsqueda...")
    ruta_cv = BASE_DIR / "data" / "cv.json"
    ruta_params = BASE_DIR / "data" / "parametros.json"
    
    cv_data = cargar_json(ruta_cv)
    params_data = cargar_json(ruta_params)

    # 2. Extraer Vacantes
    print("Buscando vacantes en Google Jobs vía SerpApi...")
    extractor = SerpApiJobExtractor(params_data["busqueda_api"])
    vacantes_encontradas = extractor.buscar_vacantes()
    
    if not vacantes_encontradas:
        print(" No se encontraron vacantes con los parámetros actuales.")
        return

    # Base de datos: Filtrar vacantes ya procesadas
    db = DBManager()
    vacantes_nuevas = db.filtrar_vacantes_nuevas(vacantes_encontradas)

    if not vacantes_nuevas:
        print(f" Se encontraron {len(vacantes_encontradas)} vacantes, pero todas ya fueron evaluadas previamente.")
        return

    print(f"Se extrajeron {len(vacantes_encontradas)} vacantes. Filtradas {len(vacantes_nuevas)} nuevas. Pasando a la IA para evaluación...\n")

    # 3. Orquestación y Prompt Engineering
    system_prompt = generar_system_prompt(cv_data, params_data)

    # 4. Evaluación Estructurada con Gemini
    resultados_ia = evaluar_vacantes_con_ia(system_prompt, vacantes_nuevas)

    # 4.5 Cálculo de Compatibilidad y Análisis de Palabras Clave
    evaluaciones_ia = resultados_ia.get("vacantes_evaluadas", [])
    mapa_ev = {ev.get("uri_aplicacion"): ev for ev in evaluaciones_ia if ev.get("uri_aplicacion")}
    
    habilidades_cv = cv_data.get("habilidades_tecnicas", {}).get("software_herramientas", [])
    
    evaluaciones_finales = []
    for raw in vacantes_nuevas:
        uri = raw.get("uri_aplicacion")
        if not uri: continue
        
        # Si la IA la omitió por límite de tokens, le creamos una evaluación base
        ev = mapa_ev.get(uri, {
            "uri_aplicacion": uri,
            "titulo_vacante": raw.get("titulo", ""),
            "empresa": raw.get("empresa", ""),
            "requisitos": [],
            "brecha_experiencia_anios": 1,
            "notas_match": "Evaluación parcial (palabras clave) por límite de procesamiento de IA."
        })
        
        descripcion = raw.get("descripcion", "")
        ev["porcentaje_compatibilidad"] = calcular_compatibilidad(ev, RANKING_CONFIG, descripcion, habilidades_cv)
        evaluaciones_finales.append(ev)

    # Guardar en Base de Datos
    if evaluaciones_finales:
        db.guardar_vacantes_evaluadas(vacantes_nuevas, evaluaciones_finales)
        print(" Las vacantes evaluadas han sido guardadas en la base de datos.")

    # 5. Guardar o Presentar Resultados
    ruta_salida = BASE_DIR / "data" / "resultados_evaluacion.json"
    with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
        json.dump(resultados_ia, archivo_salida, ensure_ascii=False, indent=2)

    print(f"¡Proceso terminado! La IA ha evaluado las vacantes compatibles.")
    print(f"Revisa el archivo '{ruta_salida}' para ver el análisis de brechas y optimización ATS.")

if __name__ == "__main__":
    main()