from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseJobExtractor(ABC):
    """
    Clase base abstracta para todos los extractores de empleo.
    Define el contrato estricto que deben seguir todas las APIs o Scrapers 
    que agregues a tu proyecto.
    """

    def __init__(self, parametros_busqueda: Dict[str, Any]):
        """
        Inicializa el extractor con los parámetros de búsqueda (los que vienen de parametros.json).
        """
        self.parametros_busqueda = parametros_busqueda

    @abstractmethod
    def buscar_vacantes(self) -> List[Dict[str, str]]:
        """
        Método principal que OBLIGATORIAMENTE debe ser implementado por cada extractor hijo.
        Realizará la conexión a la fuente de datos y devolverá la lista de vacantes.
        """
        pass

    def estandarizar_vacante(self, titulo: str, empresa: str, descripcion: str, uri: str, requisitos: str = "No especificados") -> Dict[str, str]:
        """
        Lógica común para formatear la salida.
        Asegura que todas las vacantes, sin importar de dónde vengan, 
        tengan exactamente las mismas llaves antes de enviarlas a Gemini.
        """
        return {
            "titulo": titulo,
            "empresa": empresa,
            "descripcion": descripcion,
            "requisitos": requisitos,
            "uri_aplicacion": uri
        }