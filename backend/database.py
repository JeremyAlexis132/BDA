"""
Módulo de conexión a Oracle Database.
Usa oracledb (driver nativo de Python para Oracle).
"""
import oracledb
from config import ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN


def get_connection():
    """Obtiene una conexión a Oracle Database."""
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        return conn
    except oracledb.Error as e:
        print(f"❌ Error de conexión a Oracle: {e}")
        raise


def test_connection():
    """Prueba la conexión a la base de datos."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 'Conexión exitosa' FROM DUAL")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return True, result[0]
    except Exception as e:
        return False, str(e)
