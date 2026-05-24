"""
Configuración del proyecto.
Variables de entorno para conexión a Oracle y JWT.
"""
import os

# Oracle Database
ORACLE_USER = os.getenv("ORACLE_USER", "proyecto_usr")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "Proyecto1234")
ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE", "XEPDB1")

ORACLE_DSN = f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"

# JWT Secret
JWT_SECRET = os.getenv("JWT_SECRET", "bda_unam_proyecto_secret_2026")
JWT_EXPIRATION_HOURS = 8

# Flask
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
