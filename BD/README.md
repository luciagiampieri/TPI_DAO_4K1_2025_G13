### POR SI ALGUIEN NECESITA CREAR LA BD LOCAL! (guardarla como alquiler_autos)

DROP DATABASE IF EXISTS alquiler_autos;
CREATE DATABASE alquiler_autos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE alquiler_autos;

# ----------------------------------------------------------
#  TABLA: AMBITO
# ----------------------------------------------------------
CREATE TABLE AMBITO (
    ID_AMBITO INT PRIMARY KEY AUTO_INCREMENT,
    TX_AMBITO VARCHAR(100) NOT NULL
);

# ----------------------------------------------------------
#  TABLA: ESTADO
# ----------------------------------------------------------
CREATE TABLE ESTADO (
    ID_ESTADO INT PRIMARY KEY AUTO_INCREMENT,
    TX_ESTADO VARCHAR(100) NOT NULL,
    ID_AMBITO INT NOT NULL,
    FOREIGN KEY (ID_AMBITO) REFERENCES AMBITO(ID_AMBITO)
);

# ----------------------------------------------------------
#  TABLA: CATEGORIA
# ----------------------------------------------------------
CREATE TABLE CATEGORIA (
    ID_CATEGORIA INT PRIMARY KEY AUTO_INCREMENT,
    TX_CATEGORIA VARCHAR(100) NOT NULL
);

# ----------------------------------------------------------
#  TABLA: CARACTERISTICAVEHICULO
# ----------------------------------------------------------
CREATE TABLE CARACTERISTICAVEHICULO (
    ID_DETALLE_VEHICULO INT PRIMARY KEY AUTO_INCREMENT,
    MODELO VARCHAR(100) NOT NULL,
    ANIO INT NOT NULL,
    ID_CATEGORIA INT NOT NULL,
    FOREIGN KEY (ID_CATEGORIA) REFERENCES CATEGORIA(ID_CATEGORIA)
);

# ----------------------------------------------------------
#  TABLA: CLIENTE
# ----------------------------------------------------------
CREATE TABLE CLIENTE (
    ID_CLIENTE INT PRIMARY KEY AUTO_INCREMENT,
    NOMBRE VARCHAR(150) NOT NULL,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    TELEFONO VARCHAR(30),
    MAIL VARCHAR(150)
);

# ----------------------------------------------------------
#  TABLA: EMPLEADO
# ----------------------------------------------------------
CREATE TABLE EMPLEADO (
    ID_EMPLEADO INT PRIMARY KEY AUTO_INCREMENT,
    NOMBRE VARCHAR(150) NOT NULL,
    DNI VARCHAR(20) NOT NULL,
    MAIL VARCHAR(150)
);

# ----------------------------------------------------------
#  TABLA: VEHICULO
# ----------------------------------------------------------
CREATE TABLE VEHICULO (
    ID_VEHICULO INT PRIMARY KEY AUTO_INCREMENT,
    ID_DETALLE_VEHICULO INT NOT NULL,
    ID_ESTADO INT NOT NULL,
    PATENTE VARCHAR(20) NOT NULL,
    KILOMETRAJE INT NOT NULL,
    COSTO_DIARIO_ALQUILER DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ID_DETALLE_VEHICULO) 
        REFERENCES CARACTERISTICAVEHICULO(ID_DETALLE_VEHICULO),
    FOREIGN KEY (ID_ESTADO) 
        REFERENCES ESTADO(ID_ESTADO)
);

# ----------------------------------------------------------
#  TABLA: TIPO_INCIDENTE
# ----------------------------------------------------------
CREATE TABLE TIPO_INCIDENTE (
    ID_TIPO_INCIDENTE INT PRIMARY KEY AUTO_INCREMENT,
    TX_INCIDENTE VARCHAR(150) NOT NULL
);

# ----------------------------------------------------------
#  TABLA: TIPO_MANTENIMIENTO
# ----------------------------------------------------------
CREATE TABLE TIPO_MANTENIMIENTO (
    ID_TIPO_MANTENIMIENTO INT PRIMARY KEY AUTO_INCREMENT,
    TX_TIPO_MANTENIMIENTO VARCHAR(150) NOT NULL
);

# ----------------------------------------------------------
#  TABLA: ALQUILER
# ----------------------------------------------------------
CREATE TABLE ALQUILER (
    ID_ALQUILER INT PRIMARY KEY AUTO_INCREMENT,
    ID_VEHICULO INT NOT NULL,
    ID_EMPLEADO INT NOT NULL,
    ID_CLIENTE INT NOT NULL,
    FEC_INICIO DATETIME NOT NULL,
    FEC_FIN DATETIME NOT NULL,
    COSTO_TOTAL DECIMAL(10,2) NOT NULL,
    ID_ESTADO INT NOT NULL,
    FOREIGN KEY (ID_VEHICULO) REFERENCES VEHICULO(ID_VEHICULO),
    FOREIGN KEY (ID_EMPLEADO) REFERENCES EMPLEADO(ID_EMPLEADO),
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
    FOREIGN KEY (ID_ESTADO)   REFERENCES ESTADO(ID_ESTADO)
);

# ----------------------------------------------------------
#  TABLA: INCIDENTE
# ----------------------------------------------------------
CREATE TABLE INCIDENTE (
    ID_INCIDENTE INT PRIMARY KEY AUTO_INCREMENT,
    ID_TIPO_INCIDENTE INT NOT NULL,
    ID_ALQUILER INT NOT NULL,
    FEC_INCIDENTE DATETIME,
    DESCRIPCION VARCHAR(300),
    COSTO DECIMAL(10,2),
    FOREIGN KEY (ID_TIPO_INCIDENTE) REFERENCES TIPO_INCIDENTE(ID_TIPO_INCIDENTE),
    FOREIGN KEY (ID_ALQUILER)       REFERENCES ALQUILER(ID_ALQUILER)
);

# ----------------------------------------------------------
#  TABLA: MANTENIMIENTO
# ----------------------------------------------------------
CREATE TABLE MANTENIMIENTO (
    ID_MANTENIMIENTO INT PRIMARY KEY AUTO_INCREMENT,
    ID_VEHICULO INT NOT NULL,
    ID_TIPO_MANTENIMIENTO INT NOT NULL,
    FEC_INICIO DATETIME NOT NULL,
    FEC_FIN DATETIME,
    COSTO DECIMAL(10,2) NOT NULL,
    OBSERVACION VARCHAR(300),
    FOREIGN KEY (ID_VEHICULO) REFERENCES VEHICULO(ID_VEHICULO),
    FOREIGN KEY (ID_TIPO_MANTENIMIENTO) REFERENCES TIPO_MANTENIMIENTO(ID_TIPO_MANTENIMIENTO)
);



### POR SI ALGUIEN NECESITA CREAR LA BD LOCAL! ( carga de datos)

USE alquiler_autos;

-- ==========================================================
-- AMBITO
-- ==========================================================
TRUNCATE TABLE ESTADO;
TRUNCATE TABLE AMBITO;

INSERT INTO AMBITO (ID_AMBITO, TX_AMBITO) VALUES
(1, 'VEHICULO'),
(2, 'ALQUILER');

-- ==========================================================
-- ESTADO
-- ==========================================================
INSERT INTO ESTADO (ID_ESTADO, TX_ESTADO, ID_AMBITO) VALUES
-- Estados de VEHÍCULO (Ámbito 1)
(1, 'DISPONIBLE', 1),
(2, 'EN USO', 1),
(3, 'EN MANTENIMIENTO', 1),
(4, 'FUERA DE SERVICIO', 1),

-- Estados de ALQUILER (Ámbito 2)
(5, 'RESERVADO', 2),
(6, 'EN CURSO', 2),
(7, 'FINALIZADO', 2),
(8, 'CANCELADO', 2);

-- ==========================================================
-- CATEGORIA
-- ==========================================================
TRUNCATE TABLE CATEGORIA;

INSERT INTO CATEGORIA (ID_CATEGORIA, TX_CATEGORIA) VALUES
(1, 'ECONOMICO'),
(2, 'INTERMEDIO'),
(3, 'SUV'),
(4, 'PICKUP');

-- ==========================================================
-- CARACTERISTICAVEHICULO
-- ==========================================================
TRUNCATE TABLE CARACTERISTICAVEHICULO;

INSERT INTO CARACTERISTICAVEHICULO (ID_DETALLE_VEHICULO, MODELO, ANIO, ID_CATEGORIA) VALUES
(1, 'Ford Fiesta', 2018, 1),
(2, 'Toyota Corolla', 2020, 2),
(3, 'Renault Duster', 2019, 3),
(4, 'Toyota Hilux', 2021, 4);

-- ==========================================================
-- CLIENTE
-- ==========================================================
TRUNCATE TABLE CLIENTE;

INSERT INTO CLIENTE (ID_CLIENTE, NOMBRE, DNI, TELEFONO, MAIL) VALUES
(1, 'Juan Perez', '30111222', '1133445566', 'juan.perez@example.com'),
(2, 'Maria Lopez', '29222333', '1144556677', 'maria.lopez@example.com');

-- ==========================================================
-- EMPLEADO
-- ==========================================================
TRUNCATE TABLE EMPLEADO;

INSERT INTO EMPLEADO (ID_EMPLEADO, NOMBRE, DNI, MAIL) VALUES
(1, 'Carlos Ruiz', '27000111', 'carlos.ruiz@example.com'),
(2, 'Ana Torres', '28333444', 'ana.torres@example.com');

-- ==========================================================
-- VEHICULO
-- ==========================================================
TRUNCATE TABLE VEHICULO;

INSERT INTO VEHICULO (ID_VEHICULO, ID_DETALLE_VEHICULO, ID_ESTADO, PATENTE, KILOMETRAJE, COSTO_DIARIO_ALQUILER) VALUES
(1, 1, 1, 'AA123AA', 50000, 15000.00),
(2, 2, 1, 'AB456CD', 30000, 20000.00),
(3, 3, 3, 'AC789EF', 80000, 23000.00),
(4, 4, 1, 'AD321GH', 15000, 28000.00);
