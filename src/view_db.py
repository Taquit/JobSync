import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data" / "vacantes.db"

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Leer las vacantes
cursor.execute("SELECT id, titulo, empresa, porcentaje_compatibilidad FROM vacantes LIMIT 10")
filas = cursor.fetchall()

if not filas:
    print("La base de datos está vacía. ¡Corre python main.py para poblarla!")
else:
    print(f"{'ID':<5} | {'TITULO':<40} | {'EMPRESA':<20} | {'COMPATIBILIDAD'}")
    print("-" * 90)
    for fila in filas:
        id_vacante, titulo, empresa, compat = fila
        titulo_corto = (titulo[:37] + '...') if len(titulo) > 40 else titulo
        empresa_corta = (empresa[:17] + '...') if len(empresa) > 20 else empresa
        print(f"{id_vacante:<5} | {titulo_corto:<40} | {empresa_corta:<20} | {compat}%")

# Mostrar total guardadas
cursor.execute("SELECT count(*) FROM vacantes")
total = cursor.fetchone()[0]
print(f"\nTotal de vacantes evaluadas y guardadas: {total}")

conn.close()
