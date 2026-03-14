import mysql.connector
from mysql.connector import Error

# ── Configuración de conexión ──────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",
    "database": "telecomsys",
    "charset":  "utf8mb4",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def call_procedure(proc_name: str, args: tuple = ()):
    """
    Ejecuta un stored procedure y retorna las filas del primer result-set
    """
    conn   = None
    cursor = None
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(proc_name, args)

        rows = []
        for result in cursor.stored_results():
            rows = result.fetchall()

        conn.commit()
        return rows

    except Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
