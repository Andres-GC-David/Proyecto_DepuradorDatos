# tableIndexSelection.py
from PyQt6 import QtWidgets, QtCore
from App.Controller.databaseController import DatabaseController

class Ui_TableIndexSelectionDialog(object):
    def __init__(self, schema_name, table_name, database_controller):
        self.schema_name = schema_name
        self.table_name = table_name
        self.database_controller = database_controller
        self.all_columns = self.database_controller.get_all_columns_for_table(schema_name, table_name)
        self.selected_indicator = None 

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setWindowTitle(f"Seleccionar Indicador - {self.table_name}")
        Dialog.resize(400, 300)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        self.indicatorLabel = QtWidgets.QLabel(Dialog)
        self.indicatorLabel.setText("Seleccione un Indicador")
        self.indicatorLabel.setGeometry(QtCore.QRect(20, 20, 200, 25))
        self.indicatorLabel.setStyleSheet("color: white;")

        self.indicatorList = QtWidgets.QListWidget(Dialog)
        self.indicatorList.setGeometry(QtCore.QRect(20, 60, 360, 150))
        self.indicatorList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.load_all_columns()

        self.acceptButton = QtWidgets.QPushButton(Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(150, 230, 100, 30))
        self.acceptButton.setText("Aceptar")
        self.acceptButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.acceptButton.clicked.connect(self.accept_selection)

    def load_all_columns(self):
        self.indicatorList.clear()
        for column in self.all_columns:
            self.indicatorList.addItem(column)

    def accept_selection(self):
        selected_item = self.indicatorList.currentItem()
        if selected_item:
            self.selected_indicator = selected_item.text()
            self.database_controller.update_table_key(self.schema_name, self.table_name, self.selected_indicator)
            self.Dialog.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self.Dialog, "Selección de Indicador", "Debe seleccionar una columna como indicador antes de continuar."
            )

