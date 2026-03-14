"""
main.py – Punto de entrada de TelecomSys
Ejecutar desde la carpeta telecomsys/:
    python main.py
"""
import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.crud import MainView

if __name__ == "__main__":
    app = MainView()
    app.mainloop()
