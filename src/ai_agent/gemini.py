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

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=json.dumps(vacantes_data, ensure_ascii=False, indent=2),
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2,
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError(f"La respuesta del modelo no es JSON válido: {response.text}")
