import json
import PyPDF2
from .gemini import client
from google.genai import types

def extraer_texto_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def parsear_cv_desde_pdf(pdf_file):
    texto_cv = extraer_texto_pdf(pdf_file)
    
    system_prompt = """
Actúa como un experto en extracción de datos de currículums.
Se te proporcionará el texto extraído de un CV en PDF.
Tu tarea es mapear esa información EXACTAMENTE a la siguiente estructura JSON.
Si no encuentras información para algún campo, déjalo vacío o usa el valor predeterminado del esquema (null, "", o listas vacías []).
NO inventes información. Si hay información en el PDF que parece encajar mejor en una categoría específica, colócala ahí.
Para las 'modalidades' y 'tipo_contrato' en disponibilidad, si no se menciona, puedes sugerir o dejar los del ejemplo.
Responde ÚNICAMENTE con un JSON válido.

Estructura requerida (Usa esta base y llénala con los datos del PDF):
{
    "informacion_personal": {
        "nombre": "Nombre Apellido",
        "titulo_profesional": "Cargo o título",
        "ubicacion": "Ciudad, País",
        "contacto": {
            "email": "",
            "telefono": "",
            "linkedin": "",
            "portfolio_o_github": ""
        },
        "idiomas": [
            {
                "idioma": "Ej. Inglés",
                "nivel": "Ej. B2"
            }
        ]
    },
    "resumen_profesional": "Resumen extraído o generado a partir de la experiencia",
    "habilidades_tecnicas": {
        "software_herramientas": [
            "Lista de lenguajes, herramientas, frameworks (todo en un solo string separado por comas o varios strings)"
        ],
        "metodologias": [],
        "normativas_estandares": [],
        "maquinaria_equipo": [],
        "otras": []
    },
    "habilidades_blandas": [
        "habilidad 1", "habilidad 2"
    ],
    "experiencia_laboral": [
        {
            "puesto": "",
            "empresa": "",
            "ubicacion": "",
            "fecha_inicio": "YYYY-MM o YYYY",
            "fecha_fin": "YYYY-MM, YYYY o null si es actual",
            "actualmente": false,
            "responsabilidades_y_logros": [
                {
                    "descripcion": "",
                    "metrica": ""
                }
            ],
            "herramientas_y_metodologias_usadas": []
        }
    ],
    "educacion": [
        {
            "grado": "",
            "institucion": "",
            "ubicacion": "",
            "fecha_inicio": "",
            "fecha_graduacion": "",
            "promedio": ""
        }
    ],
    "certificaciones": [
        {
            "nombre": "",
            "entidad": "",
            "fecha_obtencion": "",
            "fecha_expiracion": null,
            "credencial_url": ""
        }
    ],
    "proyectos_destacados": [
        {
            "nombre": "",
            "descripcion": "",
            "herramientas_o_tecnologias": [],
            "url_o_evidencia": "",
            "fecha": ""
        }
    ],
    "disponibilidad": {
        "modalidad": ["Remoto", "Presencial", "Híbrido"],
        "tipo_contrato": ["Tiempo completo", "Freelance"],
        "fecha_disponible": "Inmediata"
    }
}
"""

    prompt = f"Aquí está el texto del CV:\n\n{texto_cv}"

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            response_mime_type="application/json"
        )
    )
    
    nuevo_cv_data = json.loads(response.text)
    return nuevo_cv_data
