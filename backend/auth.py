"""
Módulo de autenticación con JWT.
"""
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from config import JWT_SECRET, JWT_EXPIRATION_HOURS
from database import get_connection


def hash_password(password: str) -> str:
    """Genera hash bcrypt de una contraseña."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    """Verifica contraseña contra hash bcrypt."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def generate_token(user_id: int, username: str, rol: str) -> str:
    """Genera un token JWT."""
    payload = {
        'user_id': user_id,
        'username': username,
        'rol': rol,
        'exp': datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def decode_token(token: str) -> dict:
    """Decodifica un token JWT."""
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])


def login_required(f):
    """Decorador para rutas protegidas."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Buscar token en header Authorization
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token de autenticación requerido'}), 401

        try:
            data = decode_token(token)
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado, inicie sesión nuevamente'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Decorador para rutas que requieren rol admin."""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if request.user.get('rol') != 'admin':
            return jsonify({'error': 'Se requiere rol de administrador'}), 403
        return f(*args, **kwargs)
    return decorated


def authenticate_user(username: str, password: str):
    """Autentica un usuario contra la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT ID_USUARIO, USERNAME, PASSWORD_HASH, ROL FROM APP_USUARIOS "
            "WHERE USERNAME = :username AND ACTIVO = 'S'",
            {'username': username}
        )
        row = cursor.fetchone()

        if row and check_password(password, row[2]):
            return {
                'id': row[0],
                'username': row[1],
                'rol': row[3]
            }
        return None
    finally:
        cursor.close()
        conn.close()
