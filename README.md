Requisitos del sistema:

Python 3.9 o superior
MySQL 8.0+ o MariaDB 10.5+
Las dependencias listadas abajo

(con comando de instalacion en cmd)
pip install mysql-connector-python tkcalendar Pillow openpyxl reportlab

1. Editar database.py con tus credenciales:
   python
   DB_CONFIG = {
       "host":     "localhost",
       "user":     "root",
       "password": "TU_PASSWORD",
       "database": "telecomsys",
   }

