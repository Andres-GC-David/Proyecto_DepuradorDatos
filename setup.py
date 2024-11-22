from cx_Freeze import setup, Executable
import os

executables = [
    Executable(
        "main.py",                       
        base="Win32GUI",                 
        target_name="DepuradorDatosApp.exe",  
        icon="App/Images/depuradorDatosIcon.ico"        
    )
]


include_files = [
    ("App/Files", "App/Files"),  
    ("App/Images", "App/Images"),  
]

build_options = {
    'packages': ["PyQt6", "os", "sys", "shutil", "glob"],  
    'include_files': include_files,  
}

setup(
    name="DepuradorDatosApp",
    version="1.0",
    description="Aplicación de Depurador de Datos",
    options={"build_exe": build_options},
    executables=executables
)
