-- ============================================================
-- 04_carga_masiva.sql
-- Carga masiva de 50,000 empleados con datos sintéticos
-- Proyecto Final - Base de Datos Avanzadas (UNAM)
-- ============================================================

DECLARE
  v_nombre   VARCHAR2(100);
  v_apellido VARCHAR2(100);
  v_email    VARCHAR2(150);
  v_fecha    DATE;
  v_salario  NUMBER(12,2);
  v_dep      NUMBER;
BEGIN
  FOR i IN 1..50000 LOOP
    v_nombre   := 'NOMBRE_'   || DBMS_RANDOM.STRING('U', 8);
    v_apellido := 'APELLIDO_' || DBMS_RANDOM.STRING('U', 10);
    v_email    := LOWER('emp' || i || '_' || DBMS_RANDOM.STRING('L',5) || '@empresa.com');
    v_fecha    := DATE '2018-01-01' + TRUNC(DBMS_RANDOM.VALUE(0, 3000));
    v_salario  := ROUND(DBMS_RANDOM.VALUE(8000, 85000), 2);
    v_dep      := TRUNC(DBMS_RANDOM.VALUE(1, 11));

    INSERT INTO EMPLEADOS (
      NOMBRE, APELLIDO, EMAIL, FECHA_INGRESO, SALARIO, ID_DEPARTAMENTO, ACTIVO, NIVEL_SEGURIDAD
    ) VALUES (
      v_nombre, v_apellido, v_email, v_fecha, v_salario, v_dep,
      CASE WHEN DBMS_RANDOM.VALUE(0,1) > 0.1 THEN 'S' ELSE 'N' END,
      CASE WHEN DBMS_RANDOM.VALUE(0,1) > 0.8 THEN 'RESTRINGIDO' ELSE 'INTERNO' END
    );

    IF MOD(i, 1000) = 0 THEN
      COMMIT;
    END IF;
  END LOOP;
  COMMIT;

  DBMS_OUTPUT.PUT_LINE('✅ Carga masiva completada: 50,000 registros insertados.');
END;
/
