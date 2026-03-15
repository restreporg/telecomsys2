Requisitos del sistema:

servidor local o remoto
Python 3.9 o superior
MySQL 
Las dependencias listadas abajo

se puede clonar con git clone https://github.com/restreporg/telecomsys2 desde un repositorio local 

(con comando de instalacion en cmd)
pip install mysql-connector-python tkcalendar Pillow openpyxl reportlab

1. Editar database.py con tus credenciales:
   python
   DB_CONFIG = {
       "host":     "localhost",
       "user":     "root",
       "password": "Tu contraseña",
       "database": "telecomsys",
   }

La interfaz está organizada en cuatro pestañas principales:

Clientes Permite registrar y gestionar información de clientes: ID, tipo, nombre, documento, dirección, teléfono, correo, clasificación crediticia, etc. Botones disponibles: Guardar, Actualizar, Eliminar, Limpiar.

Planes Gestión de planes comerciales: código, nombre, tipo de servicio, características, tarifa mensual, promociones y estado. Botones disponibles: Guardar, Actualizar, Eliminar, Limpiar.

Contratos Administración de contratos: número, fechas, cliente asociado, plan seleccionado, dirección de instalación, equipos incluidos, condiciones especiales, monto mensual y estado. Botones disponibles: Guardar, Actualizar, Eliminar, Limpiar.

Facturación Control de facturas: número, periodo facturado,fechas de emisión y vencimiento, cliente, servicios incluidos, cargos, descuentos, impuestos, total a pagar y forma de pago. Botones disponibles: Guardar, Actualizar, Eliminar, Limpiar.


 Temas: -
- Claro y Oscuro, intercambiables desde el sidebar
- Confirmaciones: Dialogs antes de Eliminar y Actualizar
- Validaciones: Email (regex), teléfono, fechas, numéricos, longitud de texto
- Auto-cálculo: El Total de la factura se calcula automáticamente
- Registrar Pago: Botón dedicado en Facturación para marcar pagos
- Stored Procedures: Todo el CRUD usa SPs, sin SQL directo en la app
- Treeview con filas alternas para mejor legibilidad
- Favicon: Coloca tu favicon.ico en assets/favicons/

Genera tu favicon en: https://www.favicon-generator.org/
Guárdalo como assets/favicons/favicon.ico
