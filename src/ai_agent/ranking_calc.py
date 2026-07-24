# services/ranking_calculator.py
def calcular_compatibilidad(vacante: dict, config: dict, descripcion: str = "", habilidades: list = None) -> int:
    if habilidades is None:
        habilidades = []
    pesos = config["pesos"]
    pen = config["penalizacion_experiencia"]

    indisp = [r for r in vacante.get("requisitos", []) if r.get("tipo") == "indispensable"]
    desea  = [r for r in vacante.get("requisitos", []) if r.get("tipo") == "deseable"]

    score_i = sum(r.get("cumplido", False) for r in indisp) / len(indisp) if indisp else 0
    score_d = sum(r.get("cumplido", False) for r in desea) / len(desea) if desea else 0

    # Keyword analysis
    descripcion_lower = descripcion.lower()
    habilidades_limpias = [h.strip(",").lower() for h in habilidades if h.strip()]
    matches = sum(1 for h in habilidades_limpias if h in descripcion_lower)
    score_keywords = matches / len(habilidades_limpias) if habilidades_limpias else 0

    peso_k = pesos.get("peso_keywords", 0.0)
    
    score = score_i * pesos["peso_indispensable"] + score_d * pesos["peso_deseable"] + score_keywords * peso_k

    penalizacion = min(
        vacante.get("brecha_experiencia_anios", 0) * pen["porcentaje_por_anio_faltante"] / 100,
        pen["tope_maximo_penalizacion"] / 100
    )
    score -= penalizacion
    return round(max(0, min(1, score)) * 100)