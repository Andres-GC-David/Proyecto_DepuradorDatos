import os
import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PyQt6 import QtWidgets, QtCore
from PyQt6 import QtGui

class ManageFileTypesDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Tipos de Archivos")
        self.setModal(True)
        self.resize(400, 300)

        # Cargar los tipos de archivo desde el archivo JSON
        self.file_types_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'fileTypes.json')
        self.file_types = self.load_file_types()

        # Layout principal
        self.layout = QVBoxLayout(self)

        # Widget de entrada para agregar un nuevo tipo de archivo
        self.new_file_type_label = QLabel("Agregar nuevo tipo de archivo:")
        self.new_file_type_label.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.new_file_type_label.setStyleSheet("color: white;")
        
        self.new_file_type_input = QLineEdit(self)
        self.new_file_type_input.setStyleSheet("background-color: rgb(255, 255, 255);")

        # Botón para agregar un nuevo tipo de archivo
        self.add_file_type_button = QPushButton("Agregar")
        self.add_file_type_button.setStyleSheet("color: rgb(255, 255, 255);")
        self.add_file_type_button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.add_file_type_button.clicked.connect(self.add_file_type)

        # Lista de tipos de archivo existentes
        self.file_types_list = QListWidget(self)
        self.file_types_list.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.populate_file_types()  # Llenar la lista con tipos existentes

        # Botón para eliminar tipos de archivo seleccionados
        self.remove_file_type_button = QPushButton("Eliminar seleccionado")
        self.remove_file_type_button.setStyleSheet("color: rgb(255, 255, 255);")
        self.remove_file_type_button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.remove_file_type_button.clicked.connect(self.remove_selected_file_type)

        # Agregar widgets al layout
        self.layout.addWidget(self.new_file_type_label)
        self.layout.addWidget(self.new_file_type_input)
        self.layout.addWidget(self.add_file_type_button)
        self.layout.addWidget(self.file_types_list)
        self.layout.addWidget(self.remove_file_type_button)

    def load_file_types(self):
        # Si el archivo de tipos existe, cargarlo
        if os.path.exists(self.file_types_path):
            with open(self.file_types_path, 'r') as file:
                return json.load(file)
        # Si no, devolver los valores predeterminados
        return [
            {"type": "txt", "filter": "Archivos de texto (*.txt)"},
            {"type": "csv", "filter": "Archivos CSV (*.csv)"},
            {"type": "xlsx", "filter": "Archivos Excel (*.xlsx)"}
        ]

    def save_file_types(self):
        # Guardar los tipos de archivo en el archivo JSON
        with open(self.file_types_path, 'w') as file:
            json.dump(self.file_types, file, indent=4)

    def populate_file_types(self):
        # Llenar la lista de tipos de archivo con los actuales
        self.file_types_list.clear()
        for file_type in self.file_types:
            self.file_types_list.addItem(file_type["type"])

    def add_file_type(self):
        # Agregar un nuevo tipo de archivo
        new_file_type = self.new_file_type_input.text().strip()
        if new_file_type:
            new_filter = f"Archivos {new_file_type.upper()} (*.{new_file_type})"
            self.file_types.append({"type": new_file_type, "filter": new_filter})
            self.file_types_list.addItem(new_file_type)
            self.new_file_type_input.clear()
            self.save_file_types()

    def remove_selected_file_type(self):
        # Eliminar el tipo de archivo seleccionado
        selected_items = self.file_types_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            file_type = item.text()
            self.file_types_list.takeItem(self.file_types_list.row(item))
            self.file_types = [ft for ft in self.file_types if ft["type"] != file_type]
            self.save_file_types()

