-- ============================================================
-- 05_queries_optimizacion.sql
-- Queries complejos y análisis con EXPLAIN PLAN
-- Proyecto Final - Base de Datos Avanzadas (UNAM)
-- ============================================================

-- ============================
-- Q1: JOIN + Agregación por departamento
-- ============================
EXPLAIN PLAN FOR
SELECT d.NOMBRE AS DEPARTAMENTO,
       COUNT(*) AS TOTAL_EMPLEADOS,
       ROUND(AVG(e.SALARIO),2) AS SALARIO_PROMEDIO
FROM EMPLEADOS e
JOIN DEPARTAMENTOS d ON d.ID_DEPARTAMENTO = e.ID_DEPARTAMENTO
WHERE e.ACTIVO = 'S'
GROUP BY d.NOMBRE
ORDER BY TOTAL_EMPLEADOS DESC;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY());

-- ============================
-- Q2: Subconsulta correlacionada
-- ============================
EXPLAIN PLAN FOR
SELECT e.ID_EMPLEADO, e.NOMBRE, e.APELLIDO, e.SALARIO
FROM EMPLEADOS e
WHERE e.SALARIO > (
  SELECT AVG(e2.SALARIO)
  FROM EMPLEADOS e2
  WHERE e2.ID_DEPARTAMENTO = e.ID_DEPARTAMENTO
)
AND e.ACTIVO = 'S';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY());

-- ============================
-- Q3: JOIN múltiple + HAVING
-- ============================
EXPLAIN PLAN FOR
SELECT r.NOMBRE_ROL,
       COUNT(DISTINCT er.ID_EMPLEADO) AS EMPLEADOS_POR_ROL,
       ROUND(AVG(e.SALARIO),2) AS SALARIO_MEDIO
FROM EMPLEADO_ROL er
JOIN ROLES r ON r.ID_ROL = er.ID_ROL
JOIN EMPLEADOS e ON e.ID_EMPLEADO = er.ID_EMPLEADO
WHERE e.FECHA_INGRESO >= ADD_MONTHS(TRUNC(SYSDATE), -60)
GROUP BY r.NOMBRE_ROL
HAVING COUNT(DISTINCT er.ID_EMPLEADO) >= 50;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY());

-- ============================
-- ÍNDICES adicionales para optimización
-- ============================
-- B-Tree (alta cardinalidad)
-- CREATE INDEX IDX_EMP_FECHA_INGRESO ON EMPLEADOS(FECHA_INGRESO);
-- CREATE INDEX IDX_EMP_DEP_SALARIO   ON EMPLEADOS(ID_DEPARTAMENTO, SALARIO);

-- Bitmap (baja cardinalidad - analítica)
-- CREATE BITMAP INDEX IDX_EMP_ACTIVO_BM ON EMPLEADOS(ACTIVO);
-- CREATE BITMAP INDEX IDX_EMP_NIVEL_BM  ON EMPLEADOS(NIVEL_SEGURIDAD);
