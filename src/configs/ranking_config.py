# config/ranking_config.py
RANKING_CONFIG = {
    "descartar_si_falta_indispensable": True,
    "pesos": {
        "peso_indispensable": 0.5,
        "peso_deseable": 0.2,
        "peso_keywords": 0.3
    },
    "penalizacion_experiencia": {
        "porcentaje_por_anio_faltante": 10,
        "tope_maximo_penalizacion": 40
    }
}