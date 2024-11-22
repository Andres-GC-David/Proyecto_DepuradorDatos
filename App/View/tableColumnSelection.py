from PyQt6 import QtWidgets, QtCore
from App.Controller.databaseController import DatabaseController

class Ui_TableColumnSelectionDialog(object):
    def __init__(self, schema_name, table_name, database_controller):
        self.schema_name = schema_name
        self.table_name = table_name
        self.database_controller = database_controller
        self.all_columns = self.database_controller.get_all_columns_for_table(schema_name, table_name)
        self.selected_column = None  # Solo se permite seleccionar una columna

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setWindowTitle(f"Seleccionar Columna - {self.table_name}")
        Dialog.resize(400, 300)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        # Etiqueta: Selección de columna
        self.columnLabel = QtWidgets.QLabel(Dialog)
        self.columnLabel.setText("Seleccione una Columna")
        self.columnLabel.setGeometry(QtCore.QRect(20, 20, 150, 25))
        self.columnLabel.setStyleSheet("color: white;")

        # Lista de todas las columnas
        self.columnList = QtWidgets.QListWidget(Dialog)
        self.columnList.setGeometry(QtCore.QRect(20, 60, 360, 150))
        self.columnList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.load_all_columns()

        # Botón de aceptar
        self.acceptButton = QtWidgets.QPushButton(Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(150, 230, 100, 30))
        self.acceptButton.setText("Aceptar")
        self.acceptButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.acceptButton.clicked.connect(self.accept_selection)

    def load_all_columns(self):
        """Carga todas las columnas en la lista."""
        self.columnList.clear()
        for column in self.all_columns:
            self.columnList.addItem(column)

    def accept_selection(self):
        """Guarda la columna seleccionada y cierra el diálogo."""
        selected_item = self.columnList.currentItem()
        if selected_item:
            self.selected_column = selected_item.text()
            self.Dialog.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self.Dialog, "Selección de Columna", "Debe seleccionar una columna antes de continuar."
            )
