"""
Backend Flask - Sistema de Gestión de Empleados
Proyecto Final - Base de Datos Avanzadas (UNAM)

API REST con CRUD completo, autenticación JWT y validación de duplicados.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import get_connection, test_connection
from auth import (
    authenticate_user, generate_token, login_required,
    admin_required, hash_password
)
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)


# ============================
# RUTAS DEL FRONTEND
# ============================

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


# ============================
# HEALTH CHECK
# ============================

@app.route('/api/health', methods=['GET'])
def health():
    ok, msg = test_connection()
    return jsonify({
        'status': 'ok' if ok else 'error',
        'database': msg
    }), 200 if ok else 503


# ============================
# AUTENTICACIÓN
# ============================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400

    user = authenticate_user(data['username'], data['password'])
    if not user:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    token = generate_token(user['id'], user['username'], user['rol'])
    return jsonify({
        'message': 'Login exitoso',
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'rol': user['rol']
        }
    })


# ============================
# CRUD - EMPLEADOS
# ============================

@app.route('/api/empleados', methods=['GET'])
@login_required
def get_empleados():
    """Obtener todos los empleados activos con su departamento."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT e.ID_EMPLEADO, e.NOMBRE, e.APELLIDO, e.EMAIL,
                   TO_CHAR(e.FECHA_INGRESO, 'YYYY-MM-DD') AS FECHA_INGRESO,
                   e.SALARIO, e.ID_DEPARTAMENTO, d.NOMBRE AS DEPARTAMENTO,
                   e.ACTIVO, e.NIVEL_SEGURIDAD
            FROM EMPLEADOS e
            JOIN DEPARTAMENTOS d ON d.ID_DEPARTAMENTO = e.ID_DEPARTAMENTO
            ORDER BY e.ID_EMPLEADO DESC
        """)
        columns = [col[0].lower() for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify({'empleados': rows, 'total': len(rows)})
    finally:
        cursor.close()
        conn.close()


@app.route('/api/empleados/<int:id>', methods=['GET'])
@login_required
def get_empleado(id):
    """Obtener un empleado por ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT e.ID_EMPLEADO, e.NOMBRE, e.APELLIDO, e.EMAIL,
                   TO_CHAR(e.FECHA_INGRESO, 'YYYY-MM-DD') AS FECHA_INGRESO,
                   e.SALARIO, e.ID_DEPARTAMENTO, d.NOMBRE AS DEPARTAMENTO,
                   e.ACTIVO, e.NIVEL_SEGURIDAD
            FROM EMPLEADOS e
            JOIN DEPARTAMENTOS d ON d.ID_DEPARTAMENTO = e.ID_DEPARTAMENTO
            WHERE e.ID_EMPLEADO = :id
        """, {'id': id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        columns = [col[0].lower() for col in cursor.description]
        return jsonify({'empleado': dict(zip(columns, row))})
    finally:
        cursor.close()
        conn.close()


@app.route('/api/empleados', methods=['POST'])
@admin_required
def create_empleado():
    """Crear un nuevo empleado con validación de duplicados."""
    data = request.get_json()

    # Validaciones
    required = ['nombre', 'apellido', 'email', 'fecha_ingreso', 'salario', 'id_departamento']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo requerido: {field}'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar email duplicado
        cursor.execute(
            "SELECT COUNT(*) FROM EMPLEADOS WHERE EMAIL = :email",
            {'email': data['email']}
        )
        if cursor.fetchone()[0] > 0:
            return jsonify({'error': f'El email {data["email"]} ya está registrado'}), 409

        # Insertar
        id_out = cursor.var(int)
        cursor.execute("""
            INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO,
                                   SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
            VALUES (:nombre, :apellido, :email, TO_DATE(:fecha_ingreso, 'YYYY-MM-DD'),
                    :salario, :id_departamento, :activo, :nivel_seguridad)
            RETURNING ID_EMPLEADO INTO :id_out
        """, {
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'email': data['email'],
            'fecha_ingreso': data['fecha_ingreso'],
            'salario': float(data['salario']),
            'id_departamento': int(data['id_departamento']),
            'activo': data.get('activo', 'S'),
            'nivel_seguridad': data.get('nivel_seguridad', 'INTERNO'),
            'id_out': id_out
        })
        new_id = id_out.getvalue()[0]
        conn.commit()
        return jsonify({
            'message': 'Empleado creado exitosamente',
            'id_empleado': new_id
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error al crear empleado: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/empleados/<int:id>', methods=['PUT'])
@admin_required
def update_empleado(id):
    """Actualizar un empleado existente."""
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar que exista
        cursor.execute("SELECT COUNT(*) FROM EMPLEADOS WHERE ID_EMPLEADO = :id", {'id': id})
        if cursor.fetchone()[0] == 0:
            return jsonify({'error': 'Empleado no encontrado'}), 404

        # Verificar email duplicado (si se cambió)
        if data.get('email'):
            cursor.execute(
                "SELECT COUNT(*) FROM EMPLEADOS WHERE EMAIL = :email AND ID_EMPLEADO != :id",
                {'email': data['email'], 'id': id}
            )
            if cursor.fetchone()[0] > 0:
                return jsonify({'error': f'El email {data["email"]} ya está en uso'}), 409

        cursor.execute("""
            UPDATE EMPLEADOS SET
                NOMBRE = :nombre,
                APELLIDO = :apellido,
                EMAIL = :email,
                FECHA_INGRESO = TO_DATE(:fecha_ingreso, 'YYYY-MM-DD'),
                SALARIO = :salario,
                ID_DEPARTAMENTO = :id_departamento,
                ACTIVO = :activo,
                NIVEL_SEGURIDAD = :nivel_seguridad
            WHERE ID_EMPLEADO = :id
        """, {
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'email': data['email'],
            'fecha_ingreso': data['fecha_ingreso'],
            'salario': float(data['salario']),
            'id_departamento': int(data['id_departamento']),
            'activo': data.get('activo', 'S'),
            'nivel_seguridad': data.get('nivel_seguridad', 'INTERNO'),
            'id': id
        })
        conn.commit()
        return jsonify({'message': 'Empleado actualizado exitosamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error al actualizar: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/empleados/<int:id>', methods=['DELETE'])
@admin_required
def delete_empleado(id):
    """Eliminar un empleado (borrado lógico: ACTIVO='N')."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM EMPLEADOS WHERE ID_EMPLEADO = :id", {'id': id})
        if cursor.fetchone()[0] == 0:
            return jsonify({'error': 'Empleado no encontrado'}), 404

        # Primero eliminar relaciones en EMPLEADO_ROL
        cursor.execute("DELETE FROM EMPLEADO_ROL WHERE ID_EMPLEADO = :id", {'id': id})

        # Borrado lógico
        cursor.execute(
            "UPDATE EMPLEADOS SET ACTIVO = 'N' WHERE ID_EMPLEADO = :id",
            {'id': id}
        )
        conn.commit()
        return jsonify({'message': 'Empleado desactivado exitosamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error al eliminar: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()


# ============================
# CRUD - DEPARTAMENTOS
# ============================

@app.route('/api/departamentos', methods=['GET'])
@login_required
def get_departamentos():
    """Obtener todos los departamentos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT ID_DEPARTAMENTO, NOMBRE, UBICACION, ESTADO
            FROM DEPARTAMENTOS ORDER BY NOMBRE
        """)
        columns = [col[0].lower() for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify({'departamentos': rows})
    finally:
        cursor.close()
        conn.close()


@app.route('/api/departamentos', methods=['POST'])
@admin_required
def create_departamento():
    """Crear un nuevo departamento."""
    data = request.get_json()
    if not data.get('nombre'):
        return jsonify({'error': 'Nombre del departamento requerido'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar duplicado
        cursor.execute(
            "SELECT COUNT(*) FROM DEPARTAMENTOS WHERE UPPER(NOMBRE) = UPPER(:nombre)",
            {'nombre': data['nombre']}
        )
        if cursor.fetchone()[0] > 0:
            return jsonify({'error': f'El departamento "{data["nombre"]}" ya existe'}), 409

        cursor.execute("""
            INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO)
            VALUES (:nombre, :ubicacion, :estado)
        """, {
            'nombre': data['nombre'],
            'ubicacion': data.get('ubicacion', ''),
            'estado': data.get('estado', 'A')
        })
        conn.commit()
        return jsonify({'message': 'Departamento creado exitosamente'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ============================
# AUDITORÍA
# ============================

@app.route('/api/auditoria', methods=['GET'])
@login_required
def get_auditoria():
    """Obtener registros de auditoría."""
    limit = request.args.get('limit', 100, type=int)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT AUDIT_ID, ID_EMPLEADO, USUARIO_BD, ACCION,
                   TO_CHAR(FECHA_EVENTO, 'YYYY-MM-DD HH24:MI:SS') AS FECHA_EVENTO,
                   SALARIO_ANT, SALARIO_NVO, ACTIVO_ANT, ACTIVO_NVO
            FROM AUDIT_EMPLEADOS
            ORDER BY FECHA_EVENTO DESC
            FETCH FIRST :limit ROWS ONLY
        """, {'limit': limit})
        columns = [col[0].lower() for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify({'auditoria': rows, 'total': len(rows)})
    finally:
        cursor.close()
        conn.close()


# ============================
# ESTADÍSTICAS
# ============================

@app.route('/api/estadisticas', methods=['GET'])
@login_required
def get_estadisticas():
    """Obtener estadísticas generales del sistema."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        stats = {}

        cursor.execute("SELECT COUNT(*) FROM EMPLEADOS WHERE ACTIVO = 'S'")
        stats['empleados_activos'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM EMPLEADOS WHERE ACTIVO = 'N'")
        stats['empleados_inactivos'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM DEPARTAMENTOS WHERE ESTADO = 'A'")
        stats['departamentos'] = cursor.fetchone()[0]

        cursor.execute("SELECT ROUND(AVG(SALARIO), 2) FROM EMPLEADOS WHERE ACTIVO = 'S'")
        stats['salario_promedio'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM AUDIT_EMPLEADOS")
        stats['total_auditorias'] = cursor.fetchone()[0]

        # Top departamentos por empleados
        cursor.execute("""
            SELECT d.NOMBRE, COUNT(*) AS total
            FROM EMPLEADOS e
            JOIN DEPARTAMENTOS d ON d.ID_DEPARTAMENTO = e.ID_DEPARTAMENTO
            WHERE e.ACTIVO = 'S'
            GROUP BY d.NOMBRE
            ORDER BY total DESC
            FETCH FIRST 5 ROWS ONLY
        """)
        stats['top_departamentos'] = [
            {'nombre': row[0], 'total': row[1]}
            for row in cursor.fetchall()
        ]

        return jsonify({'estadisticas': stats})
    finally:
        cursor.close()
        conn.close()


# ============================
# MAIN
# ============================

if __name__ == '__main__':
    print("=" * 60)
    print("  Sistema de Gestión de Empleados - BDA UNAM")
    print("  Backend Flask iniciando...")
    print(f"  URL: http://localhost:{FLASK_PORT}")
    print("=" * 60)

    # Verificar conexión a la BD
    ok, msg = test_connection()
    if ok:
        print(f"  ✅ Base de datos: {msg}")
    else:
        print(f"  ⚠️  Base de datos no disponible: {msg}")
        print("  El servidor iniciará de todas formas.")

    print("=" * 60)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
