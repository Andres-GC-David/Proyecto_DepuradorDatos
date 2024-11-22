from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.ruleActionDuplicatesController import RuleActionDuplicatesController

class Ui_RuleActionDuplicatesDialog(object):

    def __init__(self, column_headers):
        self.column_headers = column_headers
        self.controller = RuleActionDuplicatesController()

    def setupUi(self, Dialog, rule_name):
        Dialog.setObjectName("Dialog")
        Dialog.resize(520, 380) 
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        # Título
        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(25, 20, 470, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("color: white;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setText(f"Configuración de Regla: {rule_name}")

        self.setup_duplicate_options(Dialog)

        self.columnList = QtWidgets.QListWidget(Dialog)
        self.columnList.setGeometry(QtCore.QRect(50, 180, 420, 120))
        self.columnList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.columnList.setStyleSheet("background-color: white; color: black;")
        self.columnList.setEnabled(False)


        for column in self.column_headers:
            item = QtWidgets.QListWidgetItem(column)
            self.columnList.addItem(item)

        self.acceptButton = QtWidgets.QPushButton("Aceptar", Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(200, 320, 100, 30))
        self.acceptButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.acceptButton.setStyleSheet("background-color: white; color: black; border-radius: 10px;")
        self.acceptButton.clicked.connect(lambda: self.on_accept(Dialog))

    def setup_duplicate_options(self, Dialog):
        self.duplicateOptionsContainer = QtWidgets.QFrame(Dialog)
        self.duplicateOptionsContainer.setGeometry(QtCore.QRect(45, 80, 430, 80))
        self.duplicateOptionsContainer.setStyleSheet("background-color: white; border-radius: 10px;")
        self.duplicateOptionsContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        self.duplicateOptionsLabel = QtWidgets.QLabel("Opciones para duplicados", parent=self.duplicateOptionsContainer)
        self.duplicateOptionsLabel.setGeometry(QtCore.QRect(20, 10, 400, 30))
        self.duplicateOptionsLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.duplicateOptionsLabel.setStyleSheet("color: black;")

        self.generalDuplicatesRadio = QtWidgets.QRadioButton("Eliminar duplicados generales", self.duplicateOptionsContainer)
        self.generalDuplicatesRadio.setGeometry(QtCore.QRect(20, 50, 180, 20))
        self.generalDuplicatesRadio.setStyleSheet("color: black;")
        self.generalDuplicatesRadio.toggled.connect(self.on_general_duplicates_toggled)

        self.columnDuplicatesRadio = QtWidgets.QRadioButton("Eliminar duplicados por columnas", self.duplicateOptionsContainer)
        self.columnDuplicatesRadio.setGeometry(QtCore.QRect(220, 50, 200, 20))
        self.columnDuplicatesRadio.setStyleSheet("color: black;")
        self.columnDuplicatesRadio.toggled.connect(self.on_column_duplicates_toggled)

    def on_general_duplicates_toggled(self):
        if self.generalDuplicatesRadio.isChecked():
            self.columnList.setEnabled(False)
            self.controller.set_remove_duplicates_general(True)

    def on_column_duplicates_toggled(self):
        if self.columnDuplicatesRadio.isChecked():
            self.columnList.setEnabled(True)
            self.controller.set_remove_duplicates_general(False)

    def on_accept(self, dialog):
        if self.columnDuplicatesRadio.isChecked():
            selected_columns = [item.text() for item in self.columnList.selectedItems()]
            if not selected_columns:
                QtWidgets.QMessageBox.warning(None, "Error", "Debe seleccionar al menos una columna para eliminar duplicados.")
                return
            self.controller.set_remove_duplicates_by_columns(True, selected_columns)
        else:
            self.controller.set_remove_duplicates_by_columns(False, [])

        self.controller.accept()
        dialog.accept()

    def get_description(self):
        return self.controller.generate_description()
    
    def get_accepted(self):
        return self.controller.is_accepted()
