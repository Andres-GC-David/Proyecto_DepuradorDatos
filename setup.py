from cx_Freeze import setup, Executable
import os

# Especifica tu archivo principal como ejecutable
executables = [
    Executable(
        "main.py",                       # Archivo principal
        base="Win32GUI",                 # Elimina la consola (solo en Windows)
        target_name="DepuradorDatosApp.exe",  # Nombre del ejecutable
        icon="App/Images/depuradorDatosIcon.ico"        # Ruta al archivo de icono .ico (opcional)
    )
]

# Lista de archivos y carpetas adicionales a incluir en el build
include_files = [
    ("App/Files", "App/Files"),  # Incluye la carpeta App/Files
]

# Opciones para el build
build_options = {
    'packages': ["PyQt6", "os", "sys", "shutil", "glob"],  # Agrega los paquetes necesarios
    'include_files': include_files,  # Archivos adicionales
}

# Configuración de setup con el parámetro correcto
setup(
    name="DepuradorDatosApp",
    version="1.0",
    description="Aplicación de Depurador de Datos",
    options={"build_exe": build_options},
    executables=executables
)
