-- ============================================================
-- 02_seed_data.sql
-- Datos iniciales: departamentos, roles y datos de prueba
-- Proyecto Final - Base de Datos Avanzadas (UNAM)
-- ============================================================

-- Asegurar que las inserciones caigan en el PDB y esquema correctos.
ALTER SESSION SET CONTAINER = XEPDB1;
ALTER SESSION SET CURRENT_SCHEMA = PROYECTO_USR;

-- ============================
-- DEPARTAMENTOS
-- ============================

INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Recursos Humanos', 'Edificio A - Piso 1', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Tecnología', 'Edificio B - Piso 3', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Finanzas', 'Edificio A - Piso 2', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Ventas', 'Edificio C - Piso 1', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Marketing', 'Edificio C - Piso 2', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Operaciones', 'Edificio D - Piso 1', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Legal', 'Edificio A - Piso 4', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Investigación', 'Edificio B - Piso 5', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Soporte', 'Edificio D - Piso 2', 'A');
INSERT INTO DEPARTAMENTOS (NOMBRE, UBICACION, ESTADO) VALUES ('Dirección General', 'Edificio A - Piso 5', 'A');

-- ============================
-- ROLES
-- ============================

INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Gerente', 'Responsable de la dirección del departamento');
INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Desarrollador', 'Desarrollo de software y sistemas');
INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Analista', 'Análisis de datos y procesos');
INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Contador', 'Gestión contable y financiera');
INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Vendedor', 'Atención y ventas a clientes');
INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Soporte Técnico', 'Soporte y mantenimiento de sistemas');
INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Investigador', 'Investigación y desarrollo');
INSERT INTO ROLES (NOMBRE_ROL, DESCRIPCION) VALUES ('Abogado', 'Asesoría legal y normativa');

-- ============================
-- EMPLEADOS DE PRUEBA
-- ============================

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Carlos', 'García López', 'carlos.garcia@empresa.com', DATE '2020-03-15', 45000.00, 2, 'S', 'INTERNO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('María', 'Hernández Ruiz', 'maria.hernandez@empresa.com', DATE '2019-07-01', 52000.00, 1, 'S', 'INTERNO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('José', 'Martínez Sánchez', 'jose.martinez@empresa.com', DATE '2021-01-10', 38000.00, 3, 'S', 'PUBLICO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Ana', 'López Torres', 'ana.lopez@empresa.com', DATE '2022-05-20', 61000.00, 2, 'S', 'RESTRINGIDO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Pedro', 'Ramírez Flores', 'pedro.ramirez@empresa.com', DATE '2018-11-03', 43000.00, 4, 'S', 'INTERNO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Laura', 'Díaz Morales', 'laura.diaz@empresa.com', DATE '2023-02-14', 35000.00, 5, 'S', 'PUBLICO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Roberto', 'Jiménez Castro', 'roberto.jimenez@empresa.com', DATE '2020-08-22', 47000.00, 6, 'S', 'INTERNO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Sofía', 'Vargas Mendoza', 'sofia.vargas@empresa.com', DATE '2024-01-08', 55000.00, 7, 'S', 'RESTRINGIDO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Miguel', 'Torres Aguilar', 'miguel.torres@empresa.com', DATE '2019-04-17', 41000.00, 8, 'S', 'INTERNO');

INSERT INTO EMPLEADOS (NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD)
VALUES ('Gabriela', 'Cruz Romero', 'gabriela.cruz@empresa.com', DATE '2021-09-30', 39000.00, 9, 'N', 'PUBLICO');

-- ============================
-- ASIGNACIÓN DE ROLES A EMPLEADOS
-- ============================

INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (1, 2);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (2, 1);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (3, 4);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (4, 2);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (5, 5);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (6, 3);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (7, 6);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (8, 8);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (9, 7);
INSERT INTO EMPLEADO_ROL (ID_EMPLEADO, ID_ROL) VALUES (10, 6);

-- ============================
-- USUARIO ADMIN PARA LA APP WEB
-- (password: admin123 → hash bcrypt se genera en la app)
-- Aquí se inserta un hash pre-generado
-- ============================

-- El hash será generado por el backend al iniciar
-- Se usa un INSERT con un hash conocido de 'admin123'
INSERT INTO APP_USUARIOS (USERNAME, PASSWORD_HASH, ROL, ACTIVO)
VALUES ('admin', '$2b$12$DrC3qYD3ibZCj5IyprF8x.saSZaV9WzaSZeUOO/5.Gu6ypk/wWp1y', 'admin', 'S');

INSERT INTO APP_USUARIOS (USERNAME, PASSWORD_HASH, ROL, ACTIVO)
VALUES ('analista', '$2b$12$DrC3qYD3ibZCj5IyprF8x.saSZaV9WzaSZeUOO/5.Gu6ypk/wWp1y', 'analista', 'S');

INSERT INTO APP_USUARIOS (USERNAME, PASSWORD_HASH, ROL, ACTIVO)
VALUES ('auditor', '$2b$12$DrC3qYD3ibZCj5IyprF8x.saSZaV9WzaSZeUOO/5.Gu6ypk/wWp1y', 'auditor', 'S');

COMMIT;
