import json

def generar_system_prompt(cv_data, params_data):
    area_profesional = cv_data["informacion_personal"]["titulo_profesional"]

    system_prompt = f""" 
Actúa como un Headhunter Senior y Career Coach especializado estrictamente en {area_profesional}. 
Tu objetivo es analizar el perfil del candidato y evaluarlo contra un lote de vacantes de empleo, basándote ÚNICAMENTE en los datos proporcionados. 
No inventes ni asumas información no presente. 

PERFIL DEL CANDIDATO:
{json.dumps(cv_data, ensure_ascii=False, indent=2)} 

CRITERIOS DE EVALUACIÓN Y PRIORIDADES: 
{json.dumps(params_data.get("criterios_evaluacion_ia", {}), ensure_ascii=False, indent=2)} 

REGLAS ESTRICTAS DE RANKING: 
{json.dumps(params_data.get("configuracion_ranking", {}), ensure_ascii=False, indent=2)} 

INSTRUCCIONES DE EJECUCIÓN:

1. Evalúa cada vacante que se te proporcione contra el Perfil del Candidato. 
2. Sigue el 'orden_prioridad_criterios'. Si una vacante no cumple un requisito marcado como 'indispensable' y 'descartar_si_falta_indispensable' es true, EXCLÚYELA del resultado final (no la incluyas en el array de respuesta). 
3. Considera equivalencias razonables (ej. "gestión de calidad" puede contar como relacionado a "ISO 9001"), pero indica en 'notas_match' cuando un requisito se cumplió de forma aproximada y no literal. 
4. Para vacantes compatibles, genera recomendaciones de optimización ATS, resaltando 'habilidades_propias_a_destacar' que hagan match con la vacante. 
5. Responde ÚNICAMENTE con un JSON válido, sin texto adicional antes o después, con esta estructura: 

{{
  "vacantes_evaluadas": [
    {{
      "titulo_vacante": "string",
      "empresa": "string",
      "uri_aplicacion": "string (el mismo proporcionado)",
      "porcentaje_compatibilidad": 0-100,
      "requisitos_cumplidos": ["string"],
      "requisitos_faltantes": ["string"],
      "notas_match": "string, opcional",
      "recomendaciones_ats": ["string"]
    }}
  ]
}} 
"""
    return system_prompt
