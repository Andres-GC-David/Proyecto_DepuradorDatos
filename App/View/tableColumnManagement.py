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

        self.allColumnsLabel = QtWidgets.QLabel(Dialog)
        self.allColumnsLabel.setText("Todas las Columnas")
        self.allColumnsLabel.setGeometry(QtCore.QRect(20, 20, 150, 25))
        self.allColumnsLabel.setStyleSheet("color: white;")

        self.allColumnsList = QtWidgets.QListWidget(Dialog)
        self.allColumnsList.setGeometry(QtCore.QRect(20, 60, 200, 200))
        self.allColumnsList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.load_all_columns()

        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setGeometry(QtCore.QRect(240, 100, 40, 30))
        self.addButton.setText("→")
        self.addButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.addButton.clicked.connect(self.add_column)

        self.removeButton = QtWidgets.QPushButton(Dialog)
        self.removeButton.setGeometry(QtCore.QRect(240, 160, 40, 30))
        self.removeButton.setText("←")
        self.removeButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.removeButton.clicked.connect(self.remove_column)

        self.selectedColumnsLabel = QtWidgets.QLabel(Dialog)
        self.selectedColumnsLabel.setText("Columnas Seleccionadas")
        self.selectedColumnsLabel.setGeometry(QtCore.QRect(300, 20, 150, 25))
        self.selectedColumnsLabel.setStyleSheet("color: white;")

        self.selectedColumnsList = QtWidgets.QListWidget(Dialog)
        self.selectedColumnsList.setGeometry(QtCore.QRect(300, 60, 200, 200))
        self.selectedColumnsList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.load_selected_columns()

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
        clave = self.selected_columns["clave"]
        campos = self.selected_columns["campos"]
        
        if clave not in campos:
            self.selectedColumnsList.addItem(clave)
        
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
            
            if column != self.selected_columns["clave"]:
                self.selectedColumnsList.takeItem(self.selectedColumnsList.row(selected_item))
                self.allColumnsList.addItem(column)
                if column in self.selected_columns["campos"]:
                    self.selected_columns["campos"].remove(column)

    def accept_changes(self):
        campos_seleccionados = [
            self.selectedColumnsList.item(i).text()
            for i in range(self.selectedColumnsList.count())
            if self.selectedColumnsList.item(i).text() != self.selected_columns["clave"]
        ]
        
        self.selected_columns["campos"] = campos_seleccionados
        
        self.databaseController.save_database_management_data()
        self.Dialog.accept()

