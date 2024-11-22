from PyQt6 import QtWidgets, QtCore
from App.Controller.databaseController import DatabaseController

class Ui_TableColumnManagementDialog(object):
    def __init__(self, schema_name, table_name, databaseController):
        self.schema_name = schema_name
        self.table_name = table_name
        self.databaseController = databaseController
        self.all_columns = self.databaseController.get_all_columns_for_table(schema_name, table_name)
        self.selected_columns = self.databaseController.schema_table_data[schema_name][table_name]

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setWindowTitle(f"Modificar Columnas - {self.table_name}")
        Dialog.resize(600, 400)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        # Etiqueta: Todas las columnas
        self.allColumnsLabel = QtWidgets.QLabel(Dialog)
        self.allColumnsLabel.setText("Todas las Columnas")
        self.allColumnsLabel.setGeometry(QtCore.QRect(20, 20, 150, 25))
        self.allColumnsLabel.setStyleSheet("color: white;")

        # Lista de todas las columnas
        self.allColumnsList = QtWidgets.QListWidget(Dialog)
        self.allColumnsList.setGeometry(QtCore.QRect(20, 60, 200, 200))
        self.allColumnsList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.load_all_columns()

        # Botón para agregar columnas seleccionadas
        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setGeometry(QtCore.QRect(240, 100, 40, 30))
        self.addButton.setText("→")
        self.addButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.addButton.clicked.connect(self.add_column)

        # Botón para eliminar columnas seleccionadas
        self.removeButton = QtWidgets.QPushButton(Dialog)
        self.removeButton.setGeometry(QtCore.QRect(240, 160, 40, 30))
        self.removeButton.setText("←")
        self.removeButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.removeButton.clicked.connect(self.remove_column)

        # Etiqueta: Columnas seleccionadas
        self.selectedColumnsLabel = QtWidgets.QLabel(Dialog)
        self.selectedColumnsLabel.setText("Columnas Seleccionadas")
        self.selectedColumnsLabel.setGeometry(QtCore.QRect(300, 20, 150, 25))
        self.selectedColumnsLabel.setStyleSheet("color: white;")

        # Lista de columnas seleccionadas
        self.selectedColumnsList = QtWidgets.QListWidget(Dialog)
        self.selectedColumnsList.setGeometry(QtCore.QRect(300, 60, 200, 200))
        self.selectedColumnsList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.load_selected_columns()

        # Botón de aceptar
        self.acceptButton = QtWidgets.QPushButton(Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(250, 320, 100, 30))
        self.acceptButton.setText("Aceptar")
        self.acceptButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.acceptButton.clicked.connect(self.accept_changes)

    def load_all_columns(self):
        self.allColumnsList.clear()
        for column in self.all_columns:
            if column not in self.selected_columns:
                self.allColumnsList.addItem(column)

    def load_selected_columns(self):
        self.selectedColumnsList.clear()
        # Extrae solo los valores de "clave" y "campos" para mostrar en la lista
        clave = self.selected_columns["clave"]
        campos = self.selected_columns["campos"]
        
        # Agrega el "clave" solo si no está en "campos"
        if clave not in campos:
            self.selectedColumnsList.addItem(clave)
        
        # Agrega cada campo de "campos" a la lista visual
        for campo in campos:
            self.selectedColumnsList.addItem(campo)



    def add_column(self):
        selected_item = self.allColumnsList.currentItem()
        if selected_item:
            column = selected_item.text()
            self.allColumnsList.takeItem(self.allColumnsList.row(selected_item))
            self.selectedColumnsList.addItem(column)

    def remove_column(self):
        selected_item = self.selectedColumnsList.currentItem()
        if selected_item:
            column = selected_item.text()
            
            # Verifica si el campo es parte de "campos" y no es "clave"
            if column != self.selected_columns["clave"]:
                # Remueve el campo de la lista visual y lo agrega a la lista de todas las columnas
                self.selectedColumnsList.takeItem(self.selectedColumnsList.row(selected_item))
                self.allColumnsList.addItem(column)
                # Remueve el campo de "campos" en la estructura de datos
                if column in self.selected_columns["campos"]:
                    self.selected_columns["campos"].remove(column)

    def accept_changes(self):
        # Extrae solo las columnas en "campos", excluyendo "clave"
        campos_seleccionados = [
            self.selectedColumnsList.item(i).text()
            for i in range(self.selectedColumnsList.count())
            if self.selectedColumnsList.item(i).text() != self.selected_columns["clave"]
        ]
        
        # Asegúrate de actualizar solo "campos" en el diccionario `self.selected_columns`
        self.selected_columns["campos"] = campos_seleccionados
        
        # Guarda la estructura completa de `self.schema_table_data` sin modificar la clave ni la estructura general
        self.databaseController.save_database_management_data()
        self.Dialog.accept()

