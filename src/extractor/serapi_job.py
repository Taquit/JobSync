import os 
import requests
from dotenv import load_dotenv, find_dotenv
from extractor.base_api import BaseJobExtractor

load_dotenv(find_dotenv())
SERAPI_KEY = os.getenv("SERPAPI_API_KEY")

class SerpApiJobExtractor(BaseJobExtractor):
    def buscar_vacantes(self):
        ubicacion = self.parametros_busqueda["ubicacion"]
        url = "https://serpapi.com/search.json"
        
        vacantes_limpias = []
        
        # Google Jobs funciona mejor con búsquedas individuales
        for kw in self.parametros_busqueda["palabras_clave_incluir"]:
            params = {
                "engine": "google_jobs",
                "q": f"{kw} {ubicacion}",
                "hl": "es",
                "api_key": SERAPI_KEY
            }
            
            try:
                respuesta = requests.get(url, params=params, timeout=15)
                respuesta.raise_for_status()
                datos = respuesta.json()
            except requests.exceptions.RequestException as e:
                print(f"Error al buscar '{kw}': {e}")
                continue
            
            if "jobs_results" in datos:
                for job in datos["jobs_results"]:
                    # Obtener link directo
                    apply_options = job.get("apply_options", [])
                    enlace_directo = apply_options[0].get("link") if apply_options else job.get("share_link", "Enlace no disponible")
                    
                    # Obtener extensiones
                    extensiones = job.get("detected_extensions", {})
                    tipo_horario = extensiones.get("schedule_type", "No especificado")
                    publicado_hace = extensiones.get("posted_at", "Fecha desconocida")

                    vacante = self.estandarizar_vacante(
                        titulo=job.get("title", "Sin título"),
                        empresa=job.get("company_name", "Empresa oculta"),
                        descripcion=job.get("description", "Sin descripción"),
                        uri=enlace_directo,
                        tipo_horario=tipo_horario,
                        publicado_hace=publicado_hace
                    )
                    vacantes_limpias.append(vacante)
                    
        return vacantes_limpias