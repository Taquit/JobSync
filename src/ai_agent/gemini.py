#Archivo para forzar el json 
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def evaluar_vacantes_con_ia(system_prompt, vacantes_data):
    batch_size = 10
    todas_las_evaluaciones = []
    
    print(f"[*] Enviando {len(vacantes_data)} vacantes a Gemini en lotes de {batch_size}...")
    
    for i in range(0, len(vacantes_data), batch_size):
        lote = vacantes_data[i:i + batch_size]
        print(f"    -> Procesando lote {i//batch_size + 1} de {(len(vacantes_data)-1)//batch_size + 1} ({len(lote)} vacantes)...")
        
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=json.dumps(lote, ensure_ascii=False, indent=2),
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2,
                    response_mime_type="application/json"
                )
            )
            
            data = json.loads(response.text)
            evaluaciones = data.get("vacantes_evaluadas", [])
            todas_las_evaluaciones.extend(evaluaciones)
            print(f"       + {len(evaluaciones)} vacantes evaluadas correctamente en este lote.")
            
        except json.JSONDecodeError:
            print(f"       [!] Error: Gemini devolvió un JSON inválido en el lote {i//batch_size + 1}. Saltando.")
        except Exception as e:
            print(f"       [!] Error al comunicarse con Gemini en el lote {i//batch_size + 1}: {e}")

    return {"vacantes_evaluadas": todas_las_evaluaciones}
