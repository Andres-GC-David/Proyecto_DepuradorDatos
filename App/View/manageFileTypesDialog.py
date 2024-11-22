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

        self.file_types_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'fileTypes.json')
        self.file_types = self.load_file_types()

        self.layout = QVBoxLayout(self)

        self.new_file_type_label = QLabel("Agregar nuevo tipo de archivo:")
        self.new_file_type_label.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.new_file_type_label.setStyleSheet("color: white;")
        
        self.new_file_type_input = QLineEdit(self)
        self.new_file_type_input.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.add_file_type_button = QPushButton("Agregar")
        self.add_file_type_button.setStyleSheet("color: rgb(255, 255, 255);")
        self.add_file_type_button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.add_file_type_button.clicked.connect(self.add_file_type)

        self.file_types_list = QListWidget(self)
        self.file_types_list.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.populate_file_types()  

        self.remove_file_type_button = QPushButton("Eliminar seleccionado")
        self.remove_file_type_button.setStyleSheet("color: rgb(255, 255, 255);")
        self.remove_file_type_button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.remove_file_type_button.clicked.connect(self.remove_selected_file_type)

        self.layout.addWidget(self.new_file_type_label)
        self.layout.addWidget(self.new_file_type_input)
        self.layout.addWidget(self.add_file_type_button)
        self.layout.addWidget(self.file_types_list)
        self.layout.addWidget(self.remove_file_type_button)

    def load_file_types(self):
        if os.path.exists(self.file_types_path):
            with open(self.file_types_path, 'r') as file:
                return json.load(file)
        return [
            {"type": "txt", "filter": "Archivos de texto (*.txt)"},
            {"type": "csv", "filter": "Archivos CSV (*.csv)"},
            {"type": "xlsx", "filter": "Archivos Excel (*.xlsx)"}
        ]

    def save_file_types(self):
        with open(self.file_types_path, 'w') as file:
            json.dump(self.file_types, file, indent=4)

    def populate_file_types(self):
        self.file_types_list.clear()
        for file_type in self.file_types:
            self.file_types_list.addItem(file_type["type"])

    def add_file_type(self):
        new_file_type = self.new_file_type_input.text().strip()
        if new_file_type:
            new_filter = f"Archivos {new_file_type.upper()} (*.{new_file_type})"
            self.file_types.append({"type": new_file_type, "filter": new_filter})
            self.file_types_list.addItem(new_file_type)
            self.new_file_type_input.clear()
            self.save_file_types()

    def remove_selected_file_type(self):
        selected_items = self.file_types_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            file_type = item.text()
            self.file_types_list.takeItem(self.file_types_list.row(item))
            self.file_types = [ft for ft in self.file_types if ft["type"] != file_type]
            self.save_file_types()

