import sqlite3
import json
import os
from typing import List, Dict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class DBManager:
    def __init__(self, db_path: str = str(BASE_DIR / "data" / "vacantes.db")):
        self.db_path = db_path
        # Asegurar que la carpeta exista
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.crear_tablas()

    def crear_tablas(self):
        """Crea la tabla de vacantes si no existe."""
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uri_aplicacion TEXT UNIQUE,
                titulo TEXT,
                empresa TEXT,
                descripcion TEXT,
                porcentaje_compatibilidad INTEGER,
                requisitos_cumplidos TEXT,
                requisitos_faltantes TEXT,
                notas_match TEXT,
                recomendaciones_ats TEXT,
                fecha_guardado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conexion.commit()
        conexion.close()

    def vacante_existe(self, uri_aplicacion: str) -> bool:
        """Verifica si una vacante ya fue procesada basándose en su URI."""
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('SELECT 1 FROM vacantes WHERE uri_aplicacion = ?', (uri_aplicacion,))
        existe = cursor.fetchone() is not None
        conexion.close()
        return existe

    def filtrar_vacantes_nuevas(self, vacantes: List[Dict]) -> List[Dict]:
        """Recibe una lista de vacantes y devuelve solo las que no están en la DB."""
        return [v for v in vacantes if not self.vacante_existe(v["uri_aplicacion"])]

    def guardar_vacantes_evaluadas(self, vacantes_raw: List[Dict], evaluaciones_ia: List[Dict]):
        """Guarda la información cruda junto con la evaluación de la IA."""
        # Convertir evaluaciones_ia en un diccionario por uri_aplicacion para acceso rápido
        mapa_evaluaciones = {ev.get("uri_aplicacion"): ev for ev in evaluaciones_ia if ev.get("uri_aplicacion")}
        
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()

        for raw in vacantes_raw:
            uri = raw.get("uri_aplicacion")
            if not uri:
                continue
                
            evaluacion = mapa_evaluaciones.get(uri, {})
            
            # Convertir listas a strings JSON para SQLite
            req_cump = json.dumps(evaluacion.get("requisitos_cumplidos", []), ensure_ascii=False)
            req_falt = json.dumps(evaluacion.get("requisitos_faltantes", []), ensure_ascii=False)
            recom = json.dumps(evaluacion.get("recomendaciones_ats", []), ensure_ascii=False)
            
            try:
                cursor.execute('''
                    INSERT INTO vacantes (
                        uri_aplicacion, titulo, empresa, descripcion, 
                        porcentaje_compatibilidad, requisitos_cumplidos, 
                        requisitos_faltantes, notas_match, recomendaciones_ats
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    uri,
                    raw.get("titulo", ""),
                    raw.get("empresa", ""),
                    raw.get("descripcion", ""),
                    evaluacion.get("porcentaje_compatibilidad", 0),
                    req_cump,
                    req_falt,
                    evaluacion.get("notas_match", ""),
                    recom
                ))
            except sqlite3.IntegrityError:
                # Ya existe (puede pasar si intentamos guardar dos veces la misma vacante)
                pass
                
        conexion.commit()
        conexion.close()
