# 🏛️ Proyecto Final — Base de Datos Avanzadas (UNAM)

## Diseño, Seguridad y Optimización de un Sistema de Gestión de Empleados en Oracle

**Facultad de Ingeniería, UNAM**  
**Asignatura:** Base de Datos Avanzadas  
**Entorno de ejecución:** Oracle Database 21c XE en Docker  
**Profesor:** Mtro. Gerardo Gabriel Carrasco Zúñiga

---

## 📋 Tabla de Contenido

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Requisitos Previos](#requisitos-previos)
4. [Instalación Paso a Paso](#instalación-paso-a-paso)
5. [Levantar la Base de Datos con Docker](#levantar-la-base-de-datos-con-docker)
6. [Probar la Base de Datos](#probar-la-base-de-datos)
7. [Ejecutar el Backend (Flask)](#ejecutar-el-backend-flask)
8. [Usar la Aplicación Web](#usar-la-aplicación-web)
9. [API REST - Endpoints](#api-rest---endpoints)
10. [Scripts SQL Avanzados](#scripts-sql-avanzados)
11. [Subir a GitHub](#subir-a-github)
12. [Usuarios de Prueba](#usuarios-de-prueba)
13. [Solución de Problemas](#solución-de-problemas)

---

## 📝 Descripción del Proyecto

Sistema completo de gestión de empleados que integra:

- **Modelado avanzado:** tablas con constraints, vistas, triggers de auditoría
- **Seguridad multinivel:** usuarios con diferentes roles (admin, analista, auditor) — RBAC/DAC/MAC
- **Carga masiva:** script PL/SQL para generar 50,000+ registros sintéticos
- **Optimización:** queries complejos con EXPLAIN PLAN, índices B-Tree y Bitmap
- **Gestión de almacenamiento:** monitoreo de tablespaces, autoextensión, rebuild de índices
- **Aplicación web:** frontend HTML + backend Flask con API REST

---

## 📁 Estructura del Proyecto

```
bda_project/
├── README.md                          # Este archivo
├── docker-compose.yml                 # Docker Compose para Oracle 21c XE
├── requirements.txt                   # Dependencias Python
├── .gitignore                         # Archivos ignorados por Git
│
├── backend/                           # Backend Flask (Python)
│   ├── app.py                         # Aplicación principal (rutas API)
│   ├── config.py                      # Configuración (BD, JWT, Flask)
│   ├── database.py                    # Conexión a Oracle Database
│   └── auth.py                        # Autenticación JWT + bcrypt
│
├── frontend/                          # Frontend (HTML/CSS/JS)
│   ├── index.html                     # Página principal
│   ├── css/
│   │   └── styles.css                 # Estilos
│   └── js/
│       └── app.js                     # Lógica JavaScript
│
├── db/
│   ├── init/                          # Scripts de inicialización automática
│   │   ├── 01_schema.sql              # Creación de tablas, vistas, triggers
│   │   └── 02_seed_data.sql           # Datos iniciales de prueba
│   └── scripts/                       # Scripts manuales adicionales
│       ├── 03_seguridad_usuarios.sql  # Usuarios Oracle y RBAC (ejecutar como SYSTEM)
│       ├── 04_carga_masiva.sql        # Carga de 50,000 registros
│       └── 05_queries_optimizacion.sql # Queries + EXPLAIN PLAN
│
└── docs/                              # Documentación adicional
```

---

## ✅ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

| Software | Versión mínima | Descarga |
|----------|---------------|----------|
| **Docker Desktop** | 20.10+ | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Docker Compose** | 2.0+ | Incluido en Docker Desktop |
| **Python** | 3.9+ | [python.org](https://www.python.org/downloads/) |
| **Git** | 2.0+ | [git-scm.com](https://git-scm.com/) |

### Verificar instalación

```bash
docker --version
docker compose version
python3 --version
git --version
```

---

## 🚀 Instalación Paso a Paso

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/JeremyAlexis132/BDA.git
cd BDA
```

### Paso 2: Crear entorno virtual de Python (recomendado)

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

---

## 🐳 Levantar la Base de Datos con Docker

### Paso 1: Iniciar el contenedor de Oracle

```bash
docker compose up -d
```

> ⏳ **IMPORTANTE:** La primera vez tarda entre 2-5 minutos en descargar la imagen y configurar Oracle. Espera a que el contenedor esté saludable.

### Paso 2: Verificar que el contenedor esté corriendo

```bash
docker compose ps
```

Deberías ver algo como:
```
NAME              STATUS              PORTS
oracle-proyecto   Up (healthy)        0.0.0.0:1521->1521/tcp, 0.0.0.0:5500->5500/tcp
```

### Paso 3: Verificar los logs

```bash
docker compose logs -f oracle-db
```

Espera hasta ver el mensaje: `DATABASE IS READY TO USE!`

### Paso 4: Detener el contenedor (cuando ya no lo necesites)

```bash
docker compose down
```

> 💡 Los datos persisten gracias al volumen `oracle-data`. Para borrar todo:
> ```bash
> docker compose down -v
> ```

---

## 🧪 Probar la Base de Datos

### Conectarse por línea de comandos

```bash
# Conectarse como usuario de la aplicación
docker exec -it oracle-proyecto sqlplus proyecto_usr/Proyecto1234@//localhost:1521/XEPDB1

# Conectarse como SYSTEM (administrador)
docker exec -it oracle-proyecto sqlplus SYSTEM/Admin1234@//localhost:1521/XEPDB1
```

### Verificar las tablas creadas

```sql
-- Ver empleados
SELECT * FROM EMPLEADOS;

-- Ver departamentos
SELECT * FROM DEPARTAMENTOS;

-- Ver vista de empleados activos
SELECT * FROM VW_EMPLEADOS_ACTIVOS;

-- Ver auditoría
SELECT * FROM AUDIT_EMPLEADOS;
```

> Si entras como `SYSTEM`, esas consultas sin prefijo no apuntan al esquema de la app.
> Para revisar los datos como administrador usa `SELECT * FROM PROYECTO_USR.EMPLEADOS;` o conecta directamente como `proyecto_usr`.

### Ejecutar scripts avanzados manualmente

```bash
# Seguridad: Crear usuarios Oracle (como SYSTEM)
docker exec -it oracle-proyecto sqlplus SYSTEM/Admin1234@//localhost:1521/XEPDB1 @/container-entrypoint-initdb.d/../scripts/03_seguridad_usuarios.sql

# Carga masiva: 50,000 registros (como proyecto_usr)
docker exec -i oracle-proyecto sqlplus proyecto_usr/Proyecto1234@//localhost:1521/XEPDB1 < db/scripts/04_carga_masiva.sql

# Queries de optimización
docker exec -i oracle-proyecto sqlplus proyecto_usr/Proyecto1234@//localhost:1521/XEPDB1 < db/scripts/05_queries_optimizacion.sql
```

### Conectar con SQL Developer

| Parámetro | Valor |
|-----------|-------|
| **Hostname** | `localhost` |
| **Port** | `1521` |
| **Service Name** | `XEPDB1` |
| **Usuario** | `proyecto_usr` |
| **Contraseña** | `Proyecto1234` |

### Oracle Enterprise Manager Express

Abre en tu navegador: `https://localhost:5500/em`
- **Usuario:** `SYSTEM`
- **Contraseña:** `Admin1234`
- **Container:** `XEPDB1`

---

## 🖥️ Ejecutar el Backend (Flask)

### Paso 1: Asegúrate de que Docker esté corriendo

```bash
docker compose ps  # Debe mostrar "Up (healthy)"
```

### Paso 2: Ejecutar el servidor

```bash
cd backend
python app.py
```

Deberías ver:
```
============================================================
  Sistema de Gestión de Empleados - BDA UNAM
  Backend Flask iniciando...
  URL: http://localhost:5000
============================================================
  ✅ Base de datos: Conexión exitosa
============================================================
```

### Paso 3: Abrir la aplicación

Abre tu navegador en: **http://localhost:5000**

---

## 🌐 Usar la Aplicación Web

### Login

Usa uno de los usuarios de prueba (ver sección [Usuarios de Prueba](#usuarios-de-prueba)).

### Funcionalidades por Rol

| Funcionalidad | Admin | Analista | Auditor |
|---------------|:-----:|:--------:|:-------:|
| Ver Dashboard | ✅ | ✅ | ✅ |
| Ver empleados | ✅ | ✅ | ✅ |
| Agregar empleados | ✅ | ❌ | ❌ |
| Editar empleados | ✅ | ❌ | ❌ |
| Eliminar empleados | ✅ | ❌ | ❌ |
| Ver departamentos | ✅ | ✅ | ✅ |
| Agregar departamentos | ✅ | ❌ | ❌ |
| Ver auditoría | ✅ | ✅ | ✅ |

---

## 📡 API REST — Endpoints

| Método | Endpoint | Descripción | Rol requerido |
|--------|----------|-------------|---------------|
| `POST` | `/api/login` | Iniciar sesión | Público |
| `GET` | `/api/health` | Estado del servidor | Público |
| `GET` | `/api/empleados` | Listar empleados | Autenticado |
| `GET` | `/api/empleados/:id` | Detalle de empleado | Autenticado |
| `POST` | `/api/empleados` | Crear empleado | Admin |
| `PUT` | `/api/empleados/:id` | Actualizar empleado | Admin |
| `DELETE` | `/api/empleados/:id` | Desactivar empleado | Admin |
| `GET` | `/api/departamentos` | Listar departamentos | Autenticado |
| `POST` | `/api/departamentos` | Crear departamento | Admin |
| `GET` | `/api/auditoria` | Registros de auditoría | Autenticado |
| `GET` | `/api/estadisticas` | Estadísticas generales | Autenticado |

### Ejemplo con curl

```bash
# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Listar empleados (con token)
curl http://localhost:5000/api/empleados \
  -H "Authorization: Bearer <tu-token>"

# Crear empleado
curl -X POST http://localhost:5000/api/empleados \
  -H "Authorization: Bearer <tu-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@empresa.com",
    "fecha_ingreso": "2024-01-15",
    "salario": 35000,
    "id_departamento": 1
  }'
```

---

## 📜 Scripts SQL Avanzados

| Script | Ubicación | Propósito |
|--------|-----------|-----------|
| `01_schema.sql` | `db/init/` | Tablas, vistas, triggers, índices (se ejecuta automáticamente) |
| `02_seed_data.sql` | `db/init/` | Datos iniciales: departamentos, roles, empleados (automático) |
| `03_seguridad_usuarios.sql` | `db/scripts/` | Usuarios Oracle, roles RBAC (ejecutar como SYSTEM) |
| `04_carga_masiva.sql` | `db/scripts/` | Inserción de 50,000 registros con PL/SQL |
| `05_queries_optimizacion.sql` | `db/scripts/` | Queries complejos con EXPLAIN PLAN |

---

## 📤 Subir a GitHub

### Opción 1: Si ya tienes el repositorio clonado

```bash
# Agregar todos los archivos
git add .

# Crear commit
git commit -m "Proyecto completo: Backend Flask + Frontend + Oracle Docker + SQL Scripts"

# Subir a GitHub
git push origin main
```

### Opción 2: Si necesitas conectar con un repositorio nuevo

```bash
# Inicializar Git (si no está inicializado)
git init

# Agregar remoto
git remote add origin https://github.com/JeremyAlexis132/BDA.git

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "Proyecto completo: Sistema de Gestión de Empleados - BDA UNAM"

# Subir (primera vez)
git branch -M main
git push -u origin main
```

---

## 👤 Usuarios de Prueba

### Usuarios de la Aplicación Web

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `admin123` | Administrador | CRUD completo |
| `analista` | `admin123` | Analista | Solo lectura |
| `auditor` | `admin123` | Auditor | Solo lectura |

### Usuarios Oracle (para demostración de seguridad)

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `SYSTEM` | `Admin1234` | Superadmin |
| `proyecto_usr` | `Proyecto1234` | Usuario aplicación |
| `USR_ADMIN` | `Admin#2026` | Admin BD |
| `USR_ANALISTA` | `Analista#2026` | Analista BD |
| `USR_AUDITOR` | `Auditor#2026` | Auditor BD |

---

## 🔧 Solución de Problemas

### El contenedor Docker no arranca

```bash
# Ver logs detallados
docker compose logs oracle-db

# Reiniciar desde cero
docker compose down -v
docker compose up -d
```

### Error de conexión a Oracle desde Python

1. Verifica que Docker esté corriendo: `docker compose ps`
2. Verifica el puerto: `netstat -tlnp | grep 1521`
3. Espera a que el contenedor esté `healthy` (puede tardar 2-3 minutos)

### Error "ORA-12541: TNS:no listener"

El contenedor aún está inicializándose. Espera a que los logs muestren `DATABASE IS READY TO USE!`

### Error de dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Puerto 1521 o 5000 ocupado

```bash
# Cambiar puertos en docker-compose.yml y config.py
# O detener el proceso que usa el puerto:
lsof -i :1521
kill -9 <PID>
```

---

## 📄 Licencia

Proyecto académico — Universidad Nacional Autónoma de México (UNAM)  
Facultad de Ingeniería — Base de Datos Avanzadas — 2026
