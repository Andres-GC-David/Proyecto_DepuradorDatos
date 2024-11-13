from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.fileRuleSelectionController import FileRuleSelectionController
from App.View.ruleActionDialog import Ui_RuleActionDialog
from App.View.ruleActionEmailDialog import Ui_RuleActionEmailDialog
from App.View.ruleActionCedulaDialog import Ui_RuleActionCedulaDialog
from App.View.ruleActionDuplicatesDialog import Ui_RuleActionDuplicatesDialog
from App.View.manageRulesDialog import Ui_ManageRulesDialog

class Ui_Dialog(object):
    
    def __init__(self, main_window=None, file_controller=None):
        self.main_window = main_window  
        self.controller = FileRuleSelectionController(main_window, file_controller, self)

    def setupUi(self, Dialog, summayOfDataTable):
        Dialog.setObjectName("Dialog")
        Dialog.resize(907, 775)
        Dialog.setStyleSheet("background-color: rgb(58, 99, 140);")

        self.ruleSelectionWindowLabel = QtWidgets.QLabel(parent=Dialog)
        self.ruleSelectionWindowLabel.setGeometry(QtCore.QRect(110, 20, 671, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        self.ruleSelectionWindowLabel.setFont(font)
        self.ruleSelectionWindowLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.ruleSelectionWindowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ruleSelectionWindowLabel.setObjectName("ruleSelectionWindowLabel")

        self.ruleOptionContainer = QtWidgets.QFrame(parent=Dialog)
        self.ruleOptionContainer.setGeometry(QtCore.QRect(50, 90, 801, 291))
        self.ruleOptionContainer.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "border-radius: 4px;\n"
                                               "border: 1px solid black;")
        self.ruleOptionContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ruleOptionContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ruleOptionContainer.setObjectName("ruleOptionContainer")

        self.dataSelectedLabel = QtWidgets.QLabel(parent=self.ruleOptionContainer)
        self.dataSelectedLabel.setGeometry(QtCore.QRect(30, 20, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.dataSelectedLabel.setFont(font)
        self.dataSelectedLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.dataSelectedLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dataSelectedLabel.setObjectName("dataSelectedLabel")

        self.ruleOptionsLabel = QtWidgets.QLabel(parent=self.ruleOptionContainer)
        self.ruleOptionsLabel.setGeometry(QtCore.QRect(530, 20, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.ruleOptionsLabel.setFont(font)
        self.ruleOptionsLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.ruleOptionsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ruleOptionsLabel.setObjectName("ruleOptionsLabel")

        self.columnOptionsLabel = QtWidgets.QLabel(parent=self.ruleOptionContainer)
        self.columnOptionsLabel.setGeometry(QtCore.QRect(330, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.columnOptionsLabel.setFont(font)
        self.columnOptionsLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.columnOptionsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.columnOptionsLabel.setObjectName("columnOptionsLabel")

        self.dataSelectedTable = QtWidgets.QTableWidget(parent=self.ruleOptionContainer)
        self.dataSelectedTable.setGeometry(QtCore.QRect(20, 80, 221, 151))
        self.dataSelectedTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "border: 1px solid black;")
        self.dataSelectedTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.dataSelectedTable.setObjectName("dataSelectedTable")
        self.dataSelectedTable.setColumnCount(1)
        self.dataSelectedTable.setRowCount(3)
        self.dataSelectedTable.setColumnWidth(0, 200)
        self.dataSelectedTable.setRowHeight(0, 40)
        self.dataSelectedTable.setRowHeight(1, 40)
        self.dataSelectedTable.setRowHeight(2, 40)

        self.columnsOptionsTable = QtWidgets.QTableWidget(parent=self.ruleOptionContainer)
        self.columnsOptionsTable.setGeometry(QtCore.QRect(275, 80, 221, 151))
        self.columnsOptionsTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "border: 1px solid black;")
        self.columnsOptionsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.columnsOptionsTable.setObjectName("columnsOptionsTable")
        self.columnsOptionsTable.setColumnCount(1)
        self.columnsOptionsTable.setRowCount(0)
        self.columnsOptionsTable.horizontalHeader().setStretchLastSection(True)
        self.columnsOptionsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.columnsOptionsTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.columnsOptionsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.ruleOptionsTable = QtWidgets.QTableWidget(parent=self.ruleOptionContainer)
        self.ruleOptionsTable.setGeometry(QtCore.QRect(530, 80, 221, 151))
        self.ruleOptionsTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "color: rgb(0, 0, 0);\n"
                                            "border: 1px solid black;")
        self.ruleOptionsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ruleOptionsTable.setObjectName("ruleOptionsTable")
        self.ruleOptionsTable.setColumnCount(1)
        self.ruleOptionsTable.setRowCount(4)
        self.ruleOptionsTable.horizontalHeader().setStretchLastSection(True)
        self.ruleOptionsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.ruleOptionsTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.ruleOptionsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.ruleOptionsTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ruleOptionsTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.addRulesButton = QtWidgets.QPushButton(parent=self.ruleOptionContainer)
        self.addRulesButton.setGeometry(QtCore.QRect(255, 240, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.addRulesButton.setFont(font)
        self.addRulesButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.addRulesButton.setStyleSheet("background-color: rgb(58, 99, 140);\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "border-radius: 4px;\n")
        self.addRulesButton.setObjectName("addRulesButton")
        self.addRulesButton.clicked.connect(self.add_selected_options)
        
        self.manageRulesButton = QtWidgets.QPushButton(parent=Dialog)
        self.manageRulesButton.setGeometry(QtCore.QRect(30, 10, 140, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.manageRulesButton.setFont(font)
        self.manageRulesButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.manageRulesButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "border-radius: 4px;\n"
                                             "border: 1px solid black;")
        self.manageRulesButton.setObjectName("manageRulesButton")
        self.manageRulesButton.setText("Gestionar Reglas")
        self.manageRulesButton.clicked.connect(self.open_manage_rules_dialog)
        
        self.ruleSummaryLabel = QtWidgets.QLabel(parent=Dialog)
        self.ruleSummaryLabel.setGeometry(QtCore.QRect(60, 400, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        self.ruleSummaryLabel.setFont(font)
        self.ruleSummaryLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.ruleSummaryLabel.setObjectName("ruleSummaryLabel")

        self.summaryOfOptionsTable = QtWidgets.QTableWidget(parent=Dialog)
        #self.summaryOfOptionsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.summaryOfOptionsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.summaryOfOptionsTable.setGeometry(QtCore.QRect(50, 450, 801, 192))
        self.summaryOfOptionsTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                "color: rgb(0, 0, 0);\n"
                                                "border: 1px solid black;")
        self.summaryOfOptionsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.summaryOfOptionsTable.setObjectName("summaryOfOptionsTable")
        self.summaryOfOptionsTable.setColumnCount(4)  # Cambiar a 4 columnas para incluir el botón "Eliminar"
        self.summaryOfOptionsTable.setHorizontalHeaderLabels(["Nombre Modificacion", "Modificacion", "Columna", ""])  # Añadir columna "Eliminar"
        self.summaryOfOptionsTable.setRowCount(0)
        self.summaryOfOptionsTable.setColumnWidth(0, 266)
        self.summaryOfOptionsTable.setColumnWidth(1, 266)
        self.summaryOfOptionsTable.setColumnWidth(2, 266)

        self.acceptRulesButton = QtWidgets.QPushButton(parent=Dialog)
        self.acceptRulesButton.setGeometry(QtCore.QRect(290, 690, 321, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.acceptRulesButton.setFont(font)
        self.acceptRulesButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.acceptRulesButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "border-radius: 4px;\n"
                                             "border: 1px solid black;")
        self.acceptRulesButton.setObjectName("acceptRulesButton")
        self.acceptRulesButton.clicked.connect(lambda: self.transfer_to_main_window(Dialog))
        
        selected_rules = self.main_window.controller.selected_rules
        existing_rules = set()

        # Evitar reglas duplicadas en la tabla de opciones
        for row in range(self.summaryOfOptionsTable.rowCount()):
            rule_name = self.summaryOfOptionsTable.item(row, 0).text()
            column_name = self.summaryOfOptionsTable.item(row, 1).text()
            existing_rules.add((rule_name, column_name))

        # Solo agregar reglas que no estén ya presentes en la tabla
        if selected_rules:
            for rule in selected_rules:
                if (rule[0], rule[1]) not in existing_rules:  # Si la regla no está en la tabla
                    row_position = self.summaryOfOptionsTable.rowCount()
                    self.summaryOfOptionsTable.insertRow(row_position)
                    self.summaryOfOptionsTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(rule[0]))
                    self.summaryOfOptionsTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(rule[1]))
                    if isinstance(rule[2], dict):
                        description = str(rule[2])  # Convertir el dict a una cadena legible
                    else:
                        description = rule[2]  # Asumimos que es una cadena

                    self.summaryOfOptionsTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(description))  # Columna 2: Descripción de la regla
                    delete_button = QtWidgets.QPushButton("Eliminar")
                    delete_button.setStyleSheet("background-color: red; color: white;")
                    delete_button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
                    delete_button.clicked.connect(lambda checked, row=row_position: self.controller.remove_rule(self.summaryOfOptionsTable, row))
                    self.summaryOfOptionsTable.setCellWidget(row_position, 3, delete_button)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.controller.fill_data_selected_table(self.dataSelectedTable, summayOfDataTable)
        self.controller.fill_rule_options_table(self.ruleOptionsTable, summayOfDataTable)
        self.controller.load_columns_from_uploaded_file(self.columnsOptionsTable, summayOfDataTable)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ruleSelectionWindowLabel.setText(_translate("Dialog", "Seleccion de Reglas de Negocio a Utilizar"))
        self.dataSelectedLabel.setText(_translate("Dialog", "Datos"))
        self.ruleOptionsLabel.setText(_translate("Dialog", "Opciones"))
        self.columnOptionsLabel.setText(_translate("Dialog", "Columnas"))
        self.addRulesButton.setText(_translate("Dialog", "Agregar"))
        self.ruleSummaryLabel.setText(_translate("Dialog", "Seleccionados"))
        self.acceptRulesButton.setText(_translate("Dialog", "Aceptar"))
        


    def add_selected_options(self):
        # Obtiene los elementos seleccionados de las tablas
        rule_item = self.ruleOptionsTable.currentItem()  # Selección de la tabla de reglas
        column_item = self.columnsOptionsTable.currentItem()  # Selección de la tabla de columnas

        if rule_item is None or column_item is None:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Debe seleccionar una opción y una columna.")
            return

        # Llama al método del controlador y pasa las referencias a los objetos de tabla
        self.controller.add_selected_options(self.ruleOptionsTable, self.columnsOptionsTable, self.summaryOfOptionsTable)


    def open_manage_rules_dialog(self):
        self.controller.open_manage_rules_dialog()

    def transfer_to_main_window(self, dialog):
        self.controller.transfer_to_main_window(dialog, self.summaryOfOptionsTable)

    def update_summary_of_options_table(self, selected_rules, source_type="file"):
        self.ruleOptionsTable.setRowCount(0)  
        for i, rule in enumerate(selected_rules):
            self.ruleOptionsTable.insertRow(i)
            self.ruleOptionsTable.setItem(i, 0, QtWidgets.QTableWidgetItem(rule))