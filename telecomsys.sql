-- ============================================================
-- TELECOMSYS - Sistema de Gestión para Telecomunicaciones
-- Base de datos: telecomsys
-- Módulos: Clientes, Planes, Contratos, Facturas
-- ============================================================

CREATE DATABASE IF NOT EXISTS telecomsys;
USE telecomsys;

DROP TABLE IF EXISTS FacturaDetalle;
DROP TABLE IF EXISTS Facturas;
DROP TABLE IF EXISTS Contratos;
DROP TABLE IF EXISTS Planes;
DROP TABLE IF EXISTS Clientes;

START TRANSACTION;

-- ============================================================
-- TABLA: Clientes
-- ============================================================
CREATE TABLE Clientes (
    ClienteID       INTEGER PRIMARY KEY AUTO_INCREMENT,
    Tipo            ENUM('Personal', 'Empresarial') NOT NULL DEFAULT 'Personal',
    NombreRazon     VARCHAR(100) NOT NULL,
    Documento       VARCHAR(20)  NOT NULL UNIQUE,
    FechaNacConst   DATE,
    Direccion       VARCHAR(100),
    Telefono        VARCHAR(20),
    Email           VARCHAR(80),
    FechaRegistro   DATE         NOT NULL DEFAULT (CURRENT_DATE),
    ClasifCrediticia ENUM('A','B','C','D') NOT NULL DEFAULT 'B',
    Estado          ENUM('Activo','Inactivo') NOT NULL DEFAULT 'Activo',
    Foto            VARCHAR(100)
);

-- ============================================================
-- TABLA: Planes
-- ============================================================
CREATE TABLE Planes (
    PlanID          INTEGER PRIMARY KEY AUTO_INCREMENT,
    Codigo          VARCHAR(20)  NOT NULL UNIQUE,
    NombreComercial VARCHAR(80)  NOT NULL,
    Tipo            ENUM('Telefonía Móvil','Internet Fijo','Televisión','Paquete') NOT NULL,
    Descripcion     VARCHAR(500),
    TarifaMensual   DECIMAL(10,2) NOT NULL,
    Permanencia     INTEGER       NOT NULL DEFAULT 0 COMMENT 'Meses de permanencia mínima',
    Promocion       VARCHAR(200),
    Estado          ENUM('Vigente','Descontinuado') NOT NULL DEFAULT 'Vigente',
    Imagen          VARCHAR(100)
);

-- ============================================================
-- TABLA: Contratos
-- ============================================================
CREATE TABLE Contratos (
    ContratoID      INTEGER PRIMARY KEY AUTO_INCREMENT,
    NumeroContrato  VARCHAR(20)  NOT NULL UNIQUE,
    FechaFirma      DATE         NOT NULL,
    ClienteID       INTEGER      NOT NULL,
    PlanID          INTEGER      NOT NULL,
    DirInstalacion  VARCHAR(100),
    EquiposIncluidos VARCHAR(200),
    CondicionesEsp  VARCHAR(300),
    FechaInicio     DATE         NOT NULL,
    DuracionMeses   INTEGER      NOT NULL DEFAULT 12,
    MontoMensual    DECIMAL(10,2) NOT NULL,
    Estado          ENUM('Activo','Suspendido','Cancelado','Vencido') NOT NULL DEFAULT 'Activo',
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID),
    FOREIGN KEY (PlanID)    REFERENCES Planes(PlanID)
);

-- ============================================================
-- TABLA: Facturas
-- ============================================================
CREATE TABLE Facturas (
    FacturaID       INTEGER PRIMARY KEY AUTO_INCREMENT,
    NumeroFactura   VARCHAR(20)  NOT NULL UNIQUE,
    PeriodoFacturado VARCHAR(20) NOT NULL COMMENT 'Ej: 2025-01',
    FechaEmision    DATE         NOT NULL,
    FechaVencimiento DATE        NOT NULL,
    ClienteID       INTEGER      NOT NULL,
    ContratoID      INTEGER      NOT NULL,
    CargosFijos     DECIMAL(10,2) NOT NULL DEFAULT 0,
    CargosVariables DECIMAL(10,2) NOT NULL DEFAULT 0,
    Descuentos      DECIMAL(10,2) NOT NULL DEFAULT 0,
    Impuestos       DECIMAL(10,2) NOT NULL DEFAULT 0,
    TotalPagar      DECIMAL(10,2) NOT NULL DEFAULT 0,
    EstadoPago      ENUM('Pendiente','Pagada','Vencida','Anulada') NOT NULL DEFAULT 'Pendiente',
    FormaPago       ENUM('Efectivo','Transferencia','Tarjeta','Débito Automático') DEFAULT NULL,
    FechaPago       DATE         DEFAULT NULL,
    FOREIGN KEY (ClienteID)  REFERENCES Clientes(ClienteID),
    FOREIGN KEY (ContratoID) REFERENCES Contratos(ContratoID)
);

-- ============================================================
-- TABLA: FacturaDetalle
-- ============================================================
CREATE TABLE FacturaDetalle (
    DetalleID       INTEGER PRIMARY KEY AUTO_INCREMENT,
    FacturaID       INTEGER      NOT NULL,
    Descripcion     VARCHAR(200) NOT NULL,
    Cantidad        DECIMAL(10,2) NOT NULL DEFAULT 1,
    PrecioUnitario  DECIMAL(10,2) NOT NULL,
    Subtotal        DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (FacturaID) REFERENCES Facturas(FacturaID)
);

-- ============================================================
-- DATOS DE PRUEBA
-- ============================================================

INSERT INTO Clientes VALUES
(1,'Personal','Juan Carlos Pérez','1098765432','1990-05-15','Calle 45 # 23-10, Medellín','3001234567','juan.perez@email.com','2023-01-10','A','Activo',NULL),
(2,'Personal','María Fernanda López','1087654321','1985-08-22','Carrera 70 # 12-34, Bogotá','3109876543','mflopez@gmail.com','2023-02-14','B','Activo',NULL),
(3,'Empresarial','Comercializadora Andes S.A.S','900123456-1','2010-03-01','Av. El Poblado # 5-100, Medellín','6044567890','info@andescomercial.com','2023-03-20','A','Activo',NULL),
(4,'Personal','Carlos Andrés Rodríguez','1076543210','1995-11-30','Calle 80 # 50-20, Cali','3157654321','candres.rod@outlook.com','2023-04-05','C','Activo',NULL),
(5,'Empresarial','Tech Solutions Colombia Ltda','900654321-2','2015-06-15','Cra 7 # 32-15, Bogotá','6013456789','contacto@techsol.co','2023-05-18','B','Activo',NULL),
(6,'Personal','Laura Milena Torres','1065432109','1992-02-28','Transversal 39 # 7-11, Bucaramanga','3204321098','lauratm@hotmail.com','2023-06-01','B','Inactivo',NULL),
(7,'Personal','Andrés Felipe Gómez','1054321098','1988-09-10','Calle 12 # 8-45, Barranquilla','3013210987','afgomez@yahoo.com','2023-07-22','A','Activo',NULL),
(8,'Empresarial','Distribuidora Central Ltda','800987654-3','2008-11-20','Zona Industrial, Manizales','6086543210','gerencia@distcentral.com','2023-08-30','B','Activo',NULL);

INSERT INTO Planes VALUES
(1,'PLN-MOV-01','Móvil Básico 2GB','Telefonía Móvil','2GB datos, llamadas ilimitadas red, 100 min otras redes',35000,0,'Primer mes gratis','Vigente',NULL),
(2,'PLN-MOV-02','Móvil Plus 8GB','Telefonía Móvil','8GB datos, llamadas y SMS ilimitados, roaming incluido',65000,6,'Doble datos primer mes','Vigente',NULL),
(3,'PLN-INT-01','Internet Hogar 50MB','Internet Fijo','Fibra óptica 50 Mbps simétrico, IP fija, router incluido',89000,12,'Instalación gratis','Vigente',NULL),
(4,'PLN-INT-02','Internet Hogar 200MB','Internet Fijo','Fibra óptica 200 Mbps, IP fija, router WiFi 6 incluido',129000,12,'3 meses sin cuota','Vigente',NULL),
(5,'PLN-TV-01','TV Básico 80CH','Televisión','80 canales HD, 2 decodificadores, grabación en nube',55000,6,NULL,'Vigente',NULL),
(6,'PLN-TV-02','TV Premium 150CH','Televisión','150 canales HD+4K, 3 decos, Netflix incluido 6 meses',95000,12,'Netflix 6 meses gratis','Vigente',NULL),
(7,'PLN-PKG-01','Paquete Hogar Total','Paquete','Internet 100MB + TV 100CH + Telefonía fija ilimitada',159000,24,'2 meses sin cobro','Vigente',NULL),
(8,'PLN-PKG-02','Paquete Empresarial Pro','Paquete','Internet 500MB + 5 líneas móviles + IP fija + soporte 24/7',450000,24,'Equipos sin costo','Vigente',NULL),
(9,'PLN-MOV-00','Móvil Prepago','Telefonía Móvil','Plan prepago recargable, tarifa por uso',0,0,NULL,'Descontinuado',NULL);

INSERT INTO Contratos VALUES
(1,'CTR-2023-001','2023-01-15',1,3,'Calle 45 # 23-10, Medellín','Router Huawei HG8245H','Sin condiciones especiales','2023-02-01',12,89000,'Activo'),
(2,'CTR-2023-002','2023-02-20',2,7,'Carrera 70 # 12-34, Bogotá','Router + 2 decos + teléfono VoIP','Cliente VIP: descuento 5%','2023-03-01',24,159000,'Activo'),
(3,'CTR-2023-003','2023-03-25',3,8,'Av. El Poblado # 5-100, Medellín','5 SIMs corporativas + router enterprise','Soporte prioritario incluido','2023-04-01',24,450000,'Activo'),
(4,'CTR-2023-004','2023-04-10',4,2,'Calle 80 # 50-20, Cali','SIM card','Portabilidad desde Claro','2023-04-15',6,65000,'Activo'),
(5,'CTR-2023-005','2023-05-20',5,4,'Cra 7 # 32-15, Bogotá','Router WiFi 6 + switch 8 puertos','IP estática empresarial','2023-06-01',12,129000,'Activo'),
(6,'CTR-2023-006','2023-06-05',6,1,'Transversal 39 # 7-11, Bucaramanga','SIM card','Ninguna','2023-06-10',0,35000,'Suspendido'),
(7,'CTR-2023-007','2023-07-22',7,6,'Calle 12 # 8-45, Barranquilla','Router + 3 decos 4K','Netflix 6 meses incluido','2023-08-01',12,95000,'Activo'),
(8,'CTR-2023-008','2023-08-30',8,7,'Zona Industrial, Manizales','Router + 2 decos + teléfono','Facturación al final de mes','2023-09-01',24,159000,'Activo');

INSERT INTO Facturas VALUES
(1,'FAC-2024-0001','2024-01','2024-01-01','2024-01-20',1,1,89000,0,0,16910,105910,'Pagada','Transferencia','2024-01-18'),
(2,'FAC-2024-0002','2024-01','2024-01-01','2024-01-20',2,2,159000,0,7950,28690,179740,'Pagada','Débito Automático','2024-01-05'),
(3,'FAC-2024-0003','2024-01','2024-01-01','2024-01-20',3,3,450000,25000,0,89775,564775,'Pagada','Transferencia','2024-01-15'),
(4,'FAC-2024-0004','2024-01','2024-01-01','2024-01-20',4,4,65000,5000,0,13300,83300,'Pagada','Efectivo','2024-01-20'),
(5,'FAC-2024-0005','2024-01','2024-01-01','2024-01-20',5,5,129000,0,0,24510,153510,'Pagada','Tarjeta','2024-01-10'),
(6,'FAC-2024-0006','2024-02','2024-02-01','2024-02-20',1,1,89000,0,0,16910,105910,'Pagada','Transferencia','2024-02-17'),
(7,'FAC-2024-0007','2024-02','2024-02-01','2024-02-20',2,2,159000,0,7950,28690,179740,'Pagada','Débito Automático','2024-02-05'),
(8,'FAC-2024-0008','2024-02','2024-02-01','2024-02-20',3,3,450000,18000,0,88920,556920,'Pagada','Transferencia','2024-02-14'),
(9,'FAC-2024-0009','2024-03','2024-03-01','2024-03-20',1,1,89000,0,0,16910,105910,'Pagada','Transferencia','2024-03-19'),
(10,'FAC-2024-0010','2024-03','2024-03-01','2024-03-20',4,4,65000,8000,0,13870,86870,'Vencida',NULL,NULL),
(11,'FAC-2024-0011','2024-04','2024-04-01','2024-04-20',2,2,159000,0,7950,28690,179740,'Pagada','Débito Automático','2024-04-05'),
(12,'FAC-2024-0012','2024-04','2024-04-01','2024-04-20',5,5,129000,0,0,24510,153510,'Pendiente',NULL,NULL);

INSERT INTO FacturaDetalle VALUES
(1,1,'Cargo mensual Internet Hogar 50MB',1,89000,89000),
(2,2,'Cargo mensual Paquete Hogar Total',1,159000,159000),
(3,2,'Descuento cliente VIP 5%',1,-7950,-7950),
(4,3,'Cargo mensual Paquete Empresarial Pro',1,450000,450000),
(5,3,'Cargos adicionales roaming internacional',1,25000,25000),
(6,4,'Cargo mensual Móvil Plus 8GB',1,65000,65000),
(7,4,'SMS internacionales extra',1,5000,5000),
(8,5,'Cargo mensual Internet Hogar 200MB',1,129000,129000);

COMMIT;

-- ============================================================
-- STORED PROCEDURES
-- ============================================================

DELIMITER //

-- ============================================================
-- CLIENTES
-- ============================================================

CREATE PROCEDURE sp_InsertCliente(
    IN p_Tipo             ENUM('Personal','Empresarial'),
    IN p_NombreRazon      VARCHAR(100),
    IN p_Documento        VARCHAR(20),
    IN p_FechaNacConst    DATE,
    IN p_Direccion        VARCHAR(100),
    IN p_Telefono         VARCHAR(20),
    IN p_Email            VARCHAR(80),
    IN p_ClasifCrediticia ENUM('A','B','C','D'),
    IN p_Foto             VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    INSERT INTO Clientes(Tipo, NombreRazon, Documento, FechaNacConst, Direccion, Telefono, Email, FechaRegistro, ClasifCrediticia, Estado, Foto)
    VALUES(p_Tipo, p_NombreRazon, p_Documento, p_FechaNacConst, p_Direccion, p_Telefono, p_Email, CURRENT_DATE, p_ClasifCrediticia, 'Activo', p_Foto);
    COMMIT;
    SELECT LAST_INSERT_ID() AS ClienteID, 'Cliente registrado correctamente' AS Message;
END//

CREATE PROCEDURE sp_UpdateCliente(
    IN p_ClienteID        INTEGER,
    IN p_Tipo             ENUM('Personal','Empresarial'),
    IN p_NombreRazon      VARCHAR(100),
    IN p_Documento        VARCHAR(20),
    IN p_FechaNacConst    DATE,
    IN p_Direccion        VARCHAR(100),
    IN p_Telefono         VARCHAR(20),
    IN p_Email            VARCHAR(80),
    IN p_ClasifCrediticia ENUM('A','B','C','D'),
    IN p_Estado           ENUM('Activo','Inactivo'),
    IN p_Foto             VARCHAR(100)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Clientes WHERE ClienteID = p_ClienteID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cliente no existe';
    END IF;
    UPDATE Clientes
    SET Tipo=p_Tipo, NombreRazon=p_NombreRazon, Documento=p_Documento,
        FechaNacConst=p_FechaNacConst, Direccion=p_Direccion, Telefono=p_Telefono,
        Email=p_Email, ClasifCrediticia=p_ClasifCrediticia, Estado=p_Estado, Foto=p_Foto
    WHERE ClienteID = p_ClienteID;
    COMMIT;
    SELECT 'Cliente actualizado correctamente' AS Message;
END//

CREATE PROCEDURE sp_DeleteCliente(IN p_ClienteID INTEGER)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Clientes WHERE ClienteID = p_ClienteID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cliente no existe';
    END IF;
    SELECT COUNT(*) INTO v_count FROM Contratos WHERE ClienteID = p_ClienteID;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: el cliente tiene contratos asociados';
    END IF;
    DELETE FROM Clientes WHERE ClienteID = p_ClienteID;
    COMMIT;
    SELECT 'Cliente eliminado correctamente' AS Message;
END//

CREATE PROCEDURE sp_GetCliente(IN p_ClienteID INTEGER)
BEGIN
    SELECT ClienteID, Tipo, NombreRazon, Documento, FechaNacConst, Direccion,
           Telefono, Email, FechaRegistro, ClasifCrediticia, Estado, Foto
    FROM Clientes WHERE ClienteID = p_ClienteID;
END//

CREATE PROCEDURE sp_GetAllClientes()
BEGIN
    SELECT ClienteID, Tipo, NombreRazon, Documento, FechaNacConst, Direccion,
           Telefono, Email, FechaRegistro, ClasifCrediticia, Estado, Foto
    FROM Clientes ORDER BY NombreRazon;
END//

CREATE PROCEDURE sp_SearchClientes(IN p_Term VARCHAR(100))
BEGIN
    SELECT ClienteID, Tipo, NombreRazon, Documento, Telefono, Email, Estado
    FROM Clientes
    WHERE NombreRazon LIKE CONCAT('%',p_Term,'%')
       OR Documento   LIKE CONCAT('%',p_Term,'%')
       OR Email       LIKE CONCAT('%',p_Term,'%')
    ORDER BY NombreRazon;
END//

-- ============================================================
-- PLANES
-- ============================================================

CREATE PROCEDURE sp_InsertPlan(
    IN p_Codigo          VARCHAR(20),
    IN p_NombreComercial VARCHAR(80),
    IN p_Tipo            ENUM('Telefonía Móvil','Internet Fijo','Televisión','Paquete'),
    IN p_Descripcion     VARCHAR(500),
    IN p_TarifaMensual   DECIMAL(10,2),
    IN p_Permanencia     INTEGER,
    IN p_Promocion       VARCHAR(200),
    IN p_Imagen          VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    INSERT INTO Planes(Codigo, NombreComercial, Tipo, Descripcion, TarifaMensual, Permanencia, Promocion, Estado, Imagen)
    VALUES(p_Codigo, p_NombreComercial, p_Tipo, p_Descripcion, p_TarifaMensual, p_Permanencia, p_Promocion, 'Vigente', p_Imagen);
    COMMIT;
    SELECT LAST_INSERT_ID() AS PlanID, 'Plan registrado correctamente' AS Message;
END//

CREATE PROCEDURE sp_UpdatePlan(
    IN p_PlanID          INTEGER,
    IN p_Codigo          VARCHAR(20),
    IN p_NombreComercial VARCHAR(80),
    IN p_Tipo            ENUM('Telefonía Móvil','Internet Fijo','Televisión','Paquete'),
    IN p_Descripcion     VARCHAR(500),
    IN p_TarifaMensual   DECIMAL(10,2),
    IN p_Permanencia     INTEGER,
    IN p_Promocion       VARCHAR(200),
    IN p_Estado          ENUM('Vigente','Descontinuado'),
    IN p_Imagen          VARCHAR(100)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Planes WHERE PlanID = p_PlanID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El plan no existe';
    END IF;
    UPDATE Planes
    SET Codigo=p_Codigo, NombreComercial=p_NombreComercial, Tipo=p_Tipo,
        Descripcion=p_Descripcion, TarifaMensual=p_TarifaMensual, Permanencia=p_Permanencia,
        Promocion=p_Promocion, Estado=p_Estado, Imagen=p_Imagen
    WHERE PlanID = p_PlanID;
    COMMIT;
    SELECT 'Plan actualizado correctamente' AS Message;
END//

CREATE PROCEDURE sp_DeletePlan(IN p_PlanID INTEGER)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Planes WHERE PlanID = p_PlanID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El plan no existe';
    END IF;
    SELECT COUNT(*) INTO v_count FROM Contratos WHERE PlanID = p_PlanID;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: el plan tiene contratos asociados';
    END IF;
    DELETE FROM Planes WHERE PlanID = p_PlanID;
    COMMIT;
    SELECT 'Plan eliminado correctamente' AS Message;
END//

CREATE PROCEDURE sp_GetPlan(IN p_PlanID INTEGER)
BEGIN
    SELECT PlanID, Codigo, NombreComercial, Tipo, Descripcion, TarifaMensual, Permanencia, Promocion, Estado, Imagen
    FROM Planes WHERE PlanID = p_PlanID;
END//

CREATE PROCEDURE sp_GetAllPlanes()
BEGIN
    SELECT PlanID, Codigo, NombreComercial, Tipo, Descripcion, TarifaMensual, Permanencia, Promocion, Estado, Imagen
    FROM Planes ORDER BY NombreComercial;
END//

CREATE PROCEDURE sp_GetPlanesByTipo(IN p_Tipo ENUM('Telefonía Móvil','Internet Fijo','Televisión','Paquete'))
BEGIN
    SELECT PlanID, Codigo, NombreComercial, TarifaMensual, Permanencia, Estado
    FROM Planes WHERE Tipo = p_Tipo AND Estado = 'Vigente'
    ORDER BY TarifaMensual;
END//

CREATE PROCEDURE sp_SearchPlanes(IN p_Term VARCHAR(80))
BEGIN
    SELECT PlanID, Codigo, NombreComercial, Tipo, TarifaMensual, Estado
    FROM Planes
    WHERE NombreComercial LIKE CONCAT('%',p_Term,'%')
       OR Codigo          LIKE CONCAT('%',p_Term,'%')
    ORDER BY NombreComercial;
END//

-- ============================================================
-- CONTRATOS
-- ============================================================

CREATE PROCEDURE sp_InsertContrato(
    IN p_NumeroContrato  VARCHAR(20),
    IN p_FechaFirma      DATE,
    IN p_ClienteID       INTEGER,
    IN p_PlanID          INTEGER,
    IN p_DirInstalacion  VARCHAR(100),
    IN p_EquiposIncluidos VARCHAR(200),
    IN p_CondicionesEsp  VARCHAR(300),
    IN p_FechaInicio     DATE,
    IN p_DuracionMeses   INTEGER,
    IN p_MontoMensual    DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    INSERT INTO Contratos(NumeroContrato, FechaFirma, ClienteID, PlanID, DirInstalacion,
        EquiposIncluidos, CondicionesEsp, FechaInicio, DuracionMeses, MontoMensual, Estado)
    VALUES(p_NumeroContrato, p_FechaFirma, p_ClienteID, p_PlanID, p_DirInstalacion,
        p_EquiposIncluidos, p_CondicionesEsp, p_FechaInicio, p_DuracionMeses, p_MontoMensual, 'Activo');
    COMMIT;
    SELECT LAST_INSERT_ID() AS ContratoID, 'Contrato registrado correctamente' AS Message;
END//

CREATE PROCEDURE sp_UpdateContrato(
    IN p_ContratoID      INTEGER,
    IN p_NumeroContrato  VARCHAR(20),
    IN p_FechaFirma      DATE,
    IN p_ClienteID       INTEGER,
    IN p_PlanID          INTEGER,
    IN p_DirInstalacion  VARCHAR(100),
    IN p_EquiposIncluidos VARCHAR(200),
    IN p_CondicionesEsp  VARCHAR(300),
    IN p_FechaInicio     DATE,
    IN p_DuracionMeses   INTEGER,
    IN p_MontoMensual    DECIMAL(10,2),
    IN p_Estado          ENUM('Activo','Suspendido','Cancelado','Vencido')
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Contratos WHERE ContratoID = p_ContratoID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El contrato no existe';
    END IF;
    UPDATE Contratos
    SET NumeroContrato=p_NumeroContrato, FechaFirma=p_FechaFirma, ClienteID=p_ClienteID,
        PlanID=p_PlanID, DirInstalacion=p_DirInstalacion, EquiposIncluidos=p_EquiposIncluidos,
        CondicionesEsp=p_CondicionesEsp, FechaInicio=p_FechaInicio, DuracionMeses=p_DuracionMeses,
        MontoMensual=p_MontoMensual, Estado=p_Estado
    WHERE ContratoID = p_ContratoID;
    COMMIT;
    SELECT 'Contrato actualizado correctamente' AS Message;
END//

CREATE PROCEDURE sp_DeleteContrato(IN p_ContratoID INTEGER)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Contratos WHERE ContratoID = p_ContratoID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El contrato no existe';
    END IF;
    SELECT COUNT(*) INTO v_count FROM Facturas WHERE ContratoID = p_ContratoID;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: el contrato tiene facturas asociadas';
    END IF;
    DELETE FROM Contratos WHERE ContratoID = p_ContratoID;
    COMMIT;
    SELECT 'Contrato eliminado correctamente' AS Message;
END//

CREATE PROCEDURE sp_GetContrato(IN p_ContratoID INTEGER)
BEGIN
    SELECT c.ContratoID, c.NumeroContrato, c.FechaFirma,
           c.ClienteID, cl.NombreRazon AS ClienteNombre,
           c.PlanID, p.NombreComercial AS PlanNombre,
           c.DirInstalacion, c.EquiposIncluidos, c.CondicionesEsp,
           c.FechaInicio, c.DuracionMeses, c.MontoMensual, c.Estado
    FROM Contratos c
    INNER JOIN Clientes cl ON c.ClienteID = cl.ClienteID
    INNER JOIN Planes   p  ON c.PlanID    = p.PlanID
    WHERE c.ContratoID = p_ContratoID;
END//

CREATE PROCEDURE sp_GetAllContratos()
BEGIN
    SELECT c.ContratoID, c.NumeroContrato, c.FechaFirma,
           cl.NombreRazon AS ClienteNombre,
           p.NombreComercial AS PlanNombre,
           c.FechaInicio, c.DuracionMeses, c.MontoMensual, c.Estado
    FROM Contratos c
    INNER JOIN Clientes cl ON c.ClienteID = cl.ClienteID
    INNER JOIN Planes   p  ON c.PlanID    = p.PlanID
    ORDER BY c.FechaFirma DESC;
END//

CREATE PROCEDURE sp_GetContratosByCliente(IN p_ClienteID INTEGER)
BEGIN
    SELECT c.ContratoID, c.NumeroContrato, p.NombreComercial AS PlanNombre,
           c.FechaInicio, c.DuracionMeses, c.MontoMensual, c.Estado
    FROM Contratos c
    INNER JOIN Planes p ON c.PlanID = p.PlanID
    WHERE c.ClienteID = p_ClienteID
    ORDER BY c.FechaInicio DESC;
END//

-- ============================================================
-- FACTURAS
-- ============================================================

CREATE PROCEDURE sp_InsertFactura(
    IN p_NumeroFactura    VARCHAR(20),
    IN p_PeriodoFacturado VARCHAR(20),
    IN p_FechaEmision     DATE,
    IN p_FechaVencimiento DATE,
    IN p_ClienteID        INTEGER,
    IN p_ContratoID       INTEGER,
    IN p_CargosFijos      DECIMAL(10,2),
    IN p_CargosVariables  DECIMAL(10,2),
    IN p_Descuentos       DECIMAL(10,2),
    IN p_Impuestos        DECIMAL(10,2),
    IN p_TotalPagar       DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    INSERT INTO Facturas(NumeroFactura, PeriodoFacturado, FechaEmision, FechaVencimiento,
        ClienteID, ContratoID, CargosFijos, CargosVariables, Descuentos, Impuestos, TotalPagar, EstadoPago)
    VALUES(p_NumeroFactura, p_PeriodoFacturado, p_FechaEmision, p_FechaVencimiento,
        p_ClienteID, p_ContratoID, p_CargosFijos, p_CargosVariables, p_Descuentos, p_Impuestos, p_TotalPagar, 'Pendiente');
    COMMIT;
    SELECT LAST_INSERT_ID() AS FacturaID, 'Factura registrada correctamente' AS Message;
END//

CREATE PROCEDURE sp_UpdateFactura(
    IN p_FacturaID        INTEGER,
    IN p_NumeroFactura    VARCHAR(20),
    IN p_PeriodoFacturado VARCHAR(20),
    IN p_FechaEmision     DATE,
    IN p_FechaVencimiento DATE,
    IN p_ClienteID        INTEGER,
    IN p_ContratoID       INTEGER,
    IN p_CargosFijos      DECIMAL(10,2),
    IN p_CargosVariables  DECIMAL(10,2),
    IN p_Descuentos       DECIMAL(10,2),
    IN p_Impuestos        DECIMAL(10,2),
    IN p_TotalPagar       DECIMAL(10,2),
    IN p_EstadoPago       ENUM('Pendiente','Pagada','Vencida','Anulada'),
    IN p_FormaPago        ENUM('Efectivo','Transferencia','Tarjeta','Débito Automático'),
    IN p_FechaPago        DATE
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Facturas WHERE FacturaID = p_FacturaID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La factura no existe';
    END IF;
    UPDATE Facturas
    SET NumeroFactura=p_NumeroFactura, PeriodoFacturado=p_PeriodoFacturado,
        FechaEmision=p_FechaEmision, FechaVencimiento=p_FechaVencimiento,
        ClienteID=p_ClienteID, ContratoID=p_ContratoID, CargosFijos=p_CargosFijos,
        CargosVariables=p_CargosVariables, Descuentos=p_Descuentos, Impuestos=p_Impuestos,
        TotalPagar=p_TotalPagar, EstadoPago=p_EstadoPago, FormaPago=p_FormaPago, FechaPago=p_FechaPago
    WHERE FacturaID = p_FacturaID;
    COMMIT;
    SELECT 'Factura actualizada correctamente' AS Message;
END//

CREATE PROCEDURE sp_DeleteFactura(IN p_FacturaID INTEGER)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Facturas WHERE FacturaID = p_FacturaID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La factura no existe';
    END IF;
    SELECT COUNT(*) INTO v_count FROM Facturas WHERE FacturaID = p_FacturaID AND EstadoPago = 'Pagada';
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar una factura ya pagada';
    END IF;
    DELETE FROM FacturaDetalle WHERE FacturaID = p_FacturaID;
    DELETE FROM Facturas WHERE FacturaID = p_FacturaID;
    COMMIT;
    SELECT 'Factura eliminada correctamente' AS Message;
END//

CREATE PROCEDURE sp_GetFactura(IN p_FacturaID INTEGER)
BEGIN
    SELECT f.FacturaID, f.NumeroFactura, f.PeriodoFacturado, f.FechaEmision, f.FechaVencimiento,
           f.ClienteID, cl.NombreRazon AS ClienteNombre,
           f.ContratoID, c.NumeroContrato,
           f.CargosFijos, f.CargosVariables, f.Descuentos, f.Impuestos, f.TotalPagar,
           f.EstadoPago, f.FormaPago, f.FechaPago
    FROM Facturas f
    INNER JOIN Clientes  cl ON f.ClienteID  = cl.ClienteID
    INNER JOIN Contratos c  ON f.ContratoID = c.ContratoID
    WHERE f.FacturaID = p_FacturaID;
END//

CREATE PROCEDURE sp_GetAllFacturas()
BEGIN
    SELECT f.FacturaID, f.NumeroFactura, f.PeriodoFacturado, f.FechaEmision, f.FechaVencimiento,
           cl.NombreRazon AS ClienteNombre,
           c.NumeroContrato,
           f.TotalPagar, f.EstadoPago, f.FormaPago, f.FechaPago
    FROM Facturas f
    INNER JOIN Clientes  cl ON f.ClienteID  = cl.ClienteID
    INNER JOIN Contratos c  ON f.ContratoID = c.ContratoID
    ORDER BY f.FechaEmision DESC;
END//

CREATE PROCEDURE sp_GetFacturasByCliente(IN p_ClienteID INTEGER)
BEGIN
    SELECT f.FacturaID, f.NumeroFactura, f.PeriodoFacturado,
           f.FechaEmision, f.FechaVencimiento, f.TotalPagar, f.EstadoPago
    FROM Facturas f
    WHERE f.ClienteID = p_ClienteID
    ORDER BY f.FechaEmision DESC;
END//

CREATE PROCEDURE sp_GetFacturasByRangoFecha(
    IN p_FechaInicio DATE,
    IN p_FechaFin    DATE
)
BEGIN
    SELECT f.FacturaID, f.NumeroFactura, f.PeriodoFacturado, f.FechaEmision,
           cl.NombreRazon AS ClienteNombre,
           f.TotalPagar, f.EstadoPago
    FROM Facturas f
    INNER JOIN Clientes cl ON f.ClienteID = cl.ClienteID
    WHERE f.FechaEmision BETWEEN p_FechaInicio AND p_FechaFin
    ORDER BY f.FechaEmision DESC;
END//

CREATE PROCEDURE sp_PagarFactura(
    IN p_FacturaID  INTEGER,
    IN p_FormaPago  ENUM('Efectivo','Transferencia','Tarjeta','Débito Automático'),
    IN p_FechaPago  DATE
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT COUNT(*) INTO v_count FROM Facturas WHERE FacturaID = p_FacturaID;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La factura no existe';
    END IF;
    UPDATE Facturas
    SET EstadoPago='Pagada', FormaPago=p_FormaPago, FechaPago=p_FechaPago
    WHERE FacturaID = p_FacturaID;
    COMMIT;
    SELECT 'Pago registrado correctamente' AS Message;
END//

-- ============================================================
-- AUXILIARES
-- ============================================================

CREATE PROCEDURE sp_GetAllClientesCombo()
BEGIN
    SELECT ClienteID, NombreRazon, Documento FROM Clientes WHERE Estado='Activo' ORDER BY NombreRazon;
END//

CREATE PROCEDURE sp_GetAllPlanesCombo()
BEGIN
    SELECT PlanID, Codigo, NombreComercial, TarifaMensual FROM Planes WHERE Estado='Vigente' ORDER BY NombreComercial;
END//

CREATE PROCEDURE sp_GetAllContratosCombo()
BEGIN
    SELECT c.ContratoID, c.NumeroContrato, cl.NombreRazon AS ClienteNombre
    FROM Contratos c INNER JOIN Clientes cl ON c.ClienteID = cl.ClienteID
    WHERE c.Estado='Activo' ORDER BY c.NumeroContrato;
END//

DELIMITER ;

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================
/*
EJEMPLOS DE USO:
CALL sp_GetAllClientes();
CALL sp_GetAllPlanes();
CALL sp_GetAllContratos();
CALL sp_GetAllFacturas();
CALL sp_GetFacturasByRangoFecha('2024-01-01','2024-03-31');
CALL sp_PagarFactura(12,'Transferencia','2024-04-10');
*/