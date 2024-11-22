from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.databaseController import DatabaseController
from App.View.ruleActionDialog import Ui_RuleActionDialog
from App.Controller.tableRuleSelectionController import TableRuleSelectionController
from App.View.ruleActionEmailDialog import Ui_RuleActionEmailDialog
from App.View.ruleActionCedulaDialog import Ui_RuleActionCedulaDialog
from App.View.ruleActionDuplicatesDialog import Ui_RuleActionDuplicatesDialog
from App.View.tableColumnSelection import Ui_TableColumnSelectionDialog
from App.View.manageRulesDialog import Ui_ManageRulesDialog
import os
import json

class Ui_Dialog(object):
    def __init__(self, database_controller=None, main_window=None):
        self.main_window = main_window  
        self.database_controller = database_controller
        self.controller = self.database_controller
        self.rule_selection_controller = TableRuleSelectionController(database_controller, main_window)
        self.rules_data_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'rules.JSON')
        self.rules_data = self.load_rules()
    def setupUi(self, Dialog, summayOfDataTable):
        Dialog.setObjectName("Dialog")
        Dialog.resize(907, 775)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

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
        self.dataSelectedLabel.setGeometry(QtCore.QRect(40, 20, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.dataSelectedLabel.setFont(font)
        self.dataSelectedLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.dataSelectedLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dataSelectedLabel.setObjectName("dataSelectedLabel")

        self.ruleOptionsLabel = QtWidgets.QLabel(parent=self.ruleOptionContainer)
        self.ruleOptionsLabel.setGeometry(QtCore.QRect(470, 20, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.ruleOptionsLabel.setFont(font)
        self.ruleOptionsLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.ruleOptionsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ruleOptionsLabel.setObjectName("ruleOptionsLabel")

        self.dataSelectedTable = QtWidgets.QTableWidget(parent=self.ruleOptionContainer)
        self.dataSelectedTable.setGeometry(QtCore.QRect(40, 80, 221, 151)) 
        self.dataSelectedTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "border: 1px solid black;")
        self.dataSelectedTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.dataSelectedTable.setObjectName("dataSelectedTable")
        self.dataSelectedTable.setColumnCount(1)
        self.dataSelectedTable.setRowCount(3)

        item = QtWidgets.QTableWidgetItem()
        self.dataSelectedTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.dataSelectedTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.dataSelectedTable.setVerticalHeaderItem(2, item)

        self.dataSelectedTable.setColumnWidth(0, 200)
        self.dataSelectedTable.setRowHeight(0, 40)
        self.dataSelectedTable.setRowHeight(1, 40)
        self.dataSelectedTable.setRowHeight(2, 40)

        self.ruleOptionsTable = QtWidgets.QTableWidget(parent=self.ruleOptionContainer)
        self.ruleOptionsTable.setGeometry(QtCore.QRect(470, 80, 281, 151))  
        self.ruleOptionsTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "color: rgb(0, 0, 0);\n"
                                            "border: 1px solid black;")
        self.ruleOptionsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ruleOptionsTable.setObjectName("ruleOptionsTable")
        self.ruleOptionsTable.setColumnCount(1)
        self.ruleOptionsTable.setRowCount(4)

        item = QtWidgets.QTableWidgetItem()
        self.ruleOptionsTable.setHorizontalHeaderItem(0, item)

        self.ruleOptionsTable.setColumnWidth(0, 280)
        self.ruleOptionsTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.ruleOptionsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.ruleOptionsTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ruleOptionsTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

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
        self.summaryOfOptionsTable.setGeometry(QtCore.QRect(50, 450, 801, 192))
        self.summaryOfOptionsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.summaryOfOptionsTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                "color: rgb(0, 0, 0);\n"
                                                "border: 1px solid black;")
        self.summaryOfOptionsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.summaryOfOptionsTable.setObjectName("summaryOfOptionsTable")
        self.summaryOfOptionsTable.setColumnCount(4) 
        self.summaryOfOptionsTable.setHorizontalHeaderLabels(["Nombre Modificación", "Modificación", "Columna", ""]) 
        self.summaryOfOptionsTable.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.summaryOfOptionsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.summaryOfOptionsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.summaryOfOptionsTable.setHorizontalHeaderItem(2, item)

        self.summaryOfOptionsTable.setColumnWidth(0, 399)
        self.summaryOfOptionsTable.setColumnWidth(1, 400)
        
        self.columnsOptionsLabel = QtWidgets.QLabel(parent=self.ruleOptionContainer)
        self.columnsOptionsLabel.setGeometry(QtCore.QRect(290, 20, 161, 41))  
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.columnsOptionsLabel.setFont(font)
        self.columnsOptionsLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.columnsOptionsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.columnsOptionsLabel.setObjectName("columnsOptionsLabel")
        
        self.columnsOptionsTable = QtWidgets.QTableWidget(parent=self.ruleOptionContainer)
        self.columnsOptionsTable.setGeometry(QtCore.QRect(290, 80, 161, 151)) 
        self.columnsOptionsTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "border: 1px solid black;")
        self.columnsOptionsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.columnsOptionsTable.setObjectName("columnsOptionsTable")
        self.columnsOptionsTable.setColumnCount(1)
        self.columnsOptionsTable.setRowCount(0)
        self.columnsOptionsTable.setHorizontalHeaderLabels(["Columna"])
        self.columnsOptionsTable.setColumnWidth(0, 160)
        self.columnsOptionsTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.columnsOptionsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

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
        
        self.addRulesButton = QtWidgets.QPushButton(parent=self.ruleOptionContainer)
        self.addRulesButton.setGeometry(QtCore.QRect(255, 245, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.addRulesButton.setFont(font)
        self.addRulesButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.addRulesButton.setStyleSheet("background-color: rgb(8,172,20);\n"
                                          "color: rgb(255, 255, 255);\n")
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
        
        selected_rules = self.main_window.controller.selected_rules
        print(f"selected_rules: {selected_rules}")
        existing_rules = set()

        for row in range(self.summaryOfOptionsTable.rowCount()):
            rule_name = self.summaryOfOptionsTable.item(row, 0).text()
            column_name = self.summaryOfOptionsTable.item(row, 1).text()
            existing_rules.add((rule_name, column_name))

        if selected_rules:
            for rule in selected_rules:
                if (rule[0], rule[1]) not in existing_rules:  
                    row_position = self.summaryOfOptionsTable.rowCount()
                    self.summaryOfOptionsTable.insertRow(row_position)
                    self.summaryOfOptionsTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(rule[0]))
                    self.summaryOfOptionsTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(rule[1]))
                    if isinstance(rule[2], dict):
                        description = str(rule[2])  
                    else:
                        description = rule[2]  

                    self.summaryOfOptionsTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(description))  
                    delete_button = QtWidgets.QPushButton("Eliminar")
                    delete_button.setStyleSheet("background-color: red; color: white;")
                    delete_button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
                    delete_button.clicked.connect(lambda: self.rule_selection_controller.remove_rule(self.summaryOfOptionsTable, row_position))
                    self.summaryOfOptionsTable.setCellWidget(row_position, 3, delete_button)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.fill_data_selected_table(summayOfDataTable)
        self.fill_rule_options_table(summayOfDataTable)
        self.fill_column_selection_table()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ruleSelectionWindowLabel.setText(_translate("Dialog", "Seleccion de Reglas de Negocio a Utilizar"))
        self.dataSelectedLabel.setText(_translate("Dialog", "Datos"))
        self.columnsOptionsLabel.setText(_translate("Dialog", "Columnas")) 
        self.ruleOptionsLabel.setText(_translate("Dialog", "Opciones"))
        item = self.ruleOptionsTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Tipo"))
        item = self.dataSelectedTable.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "Tipo Archivo"))
        item = self.dataSelectedTable.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "Tipo Dato"))
        item = self.dataSelectedTable.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "Nombre Del Archivo"))
        self.ruleSummaryLabel.setText(_translate("Dialog", "Seleccionados"))
        self.acceptRulesButton.setText(_translate("Dialog", "Aceptar"))
        self.addRulesButton.setText(_translate("Dialog", "Agregar"))
        item = self.summaryOfOptionsTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Nombre Modificacion"))
        item = self.summaryOfOptionsTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Modificacion"))
        item = self.summaryOfOptionsTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Columna"))
        
    def fill_data_selected_table(self, summayOfDataTable):
        for row in range(summayOfDataTable.rowCount()):
            for col in range(summayOfDataTable.columnCount()):
                item = summayOfDataTable.item(row, col)
                if item is not None:
                    new_item = QtWidgets.QTableWidgetItem(item.text())
                    self.dataSelectedTable.setItem(row, col, new_item)
                    
    def fill_column_selection_table(self):
        actual_data_table = self.main_window.actualDataContainer.findChild(QtWidgets.QTableWidget)
        column_count = actual_data_table.columnCount()

        self.columnsOptionsTable.setRowCount(column_count)
        for col in range(column_count):
            column_name = actual_data_table.horizontalHeaderItem(col).text()
            self.columnsOptionsTable.setItem(col, 0, QtWidgets.QTableWidgetItem(column_name))
                    
    def fill_rule_options_table(self, summay_of_data_table):
        table_name = self.rule_selection_controller.validate_selected_database(summay_of_data_table)
        if table_name:
            parameter_options = self.rule_selection_controller.get_parameter_options_with_description(table_name)
            if parameter_options:
                self.ruleOptionsTable.setRowCount(len(parameter_options))
                self.ruleOptionsTable.setColumnCount(1)
                self.ruleOptionsTable.setHorizontalHeaderLabels(["Nombre de la Regla"])

                for row, option in enumerate(parameter_options):
                    if isinstance(option, dict):
                        rule_name = option.get('rule', '')  
                    elif isinstance(option, str):
                        rule_name = option.split(':')[0]  
                    else:
                        rule_name = ''  
                        
                    name_item = QtWidgets.QTableWidgetItem(rule_name.strip()) 
                    self.ruleOptionsTable.setItem(row, 0, name_item)
                    
    def open_manage_rules_dialog(self):
        table_name_item = self.dataSelectedTable.item(2, 0) 
        table_name = table_name_item.text()
        if table_name_item:
            table_name = table_name_item.text()

            dialog = QtWidgets.QDialog()
            ui = Ui_ManageRulesDialog(self.database_controller, self, is_file=False, from_rule_configuration=False)
            ui.setupUi(dialog)
            dialog.exec()
            self.fill_rule_options_table(self.main_window.summayOfDataTable)
      
    def update_summary_of_options_table(self, selected_rules, source_type="table"):
        self.ruleOptionsTable.setRowCount(0)  
        for i, rule in enumerate(selected_rules):
            self.ruleOptionsTable.insertRow(i)
            self.ruleOptionsTable.setItem(i, 0, QtWidgets.QTableWidgetItem(rule))  
            
    def add_selected_options(self):
        rule_row = self.ruleOptionsTable.currentRow()
        rule_name_item = self.ruleOptionsTable.item(rule_row, 0)
        column_name_item = self.columnsOptionsTable.currentItem()

        rule_name = self.rule_selection_controller.validate_selected_rule(rule_name_item)
        if not rule_name:
            return
        
        description = "Modificación pendiente"
        if rule_name_item.text() == "Estandarizacion de Telefonos":
            dialog = QtWidgets.QDialog(self.main_window)
            ui = Ui_RuleActionDialog()
            ui.setupUi(dialog, rule_name_item.text())
            dialog.exec()
            if ui.get_accepted():  
                description = ui.get_description()  
            else:
                return  
        elif rule_name_item.text() == "Estandarizacion de Cedulas":
            dialog = QtWidgets.QDialog(self.main_window)
            ui = Ui_RuleActionCedulaDialog()
            ui.setupUi(dialog, rule_name_item.text())
            dialog.exec()
            if ui.get_accepted():
                description = ui.get_description()
                
                table_name_item = self.dataSelectedTable.item(2, 0)  
                table_name = table_name_item.text() if table_name_item else None

                if table_name:
                    try:
                        schema_name = self.database_controller.get_schema_by_table(table_name)  
                        column_dialog = QtWidgets.QDialog(self.main_window)
                        column_selection_ui = Ui_TableColumnSelectionDialog(schema_name, table_name, self.database_controller)
                        column_selection_ui.setupUi(column_dialog)
                        if column_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted and column_selection_ui.selected_column:
                            column_name = column_selection_ui.selected_column
                            description = ui.get_description()
                            description += f", {column_name}"  
                        else:
                            return  
                    except ValueError as e:
                        QtWidgets.QMessageBox.warning(self.main_window, "Error", str(e))
                        return
                else:
                    QtWidgets.QMessageBox.warning(self.main_window, "Error", "No se ha seleccionado una tabla válida.")
                    return
            else:
                return
        elif rule_name_item.text() == "Eliminacion de Duplicados":
            dialog = QtWidgets.QDialog(self.main_window)
            columns = self.get_columns_from_actual_data_table()
            ui = Ui_RuleActionDuplicatesDialog(columns)
            ui.setupUi(dialog, rule_name_item.text())
            dialog.exec()
            if ui.get_accepted():
                description = ui.get_description()
            else:
                return
        elif rule_name_item.text() == "Validacion Correos":
            dialog = QtWidgets.QDialog(self.main_window)
            ui = Ui_RuleActionEmailDialog()
            ui.setupUi(dialog, rule_name_item.text())
            dialog.exec()
            if ui.get_accepted():
                description = ui.get_description()
            else:
                return
        else:
            for rule in self.rules_data.get("general_rules_pool", []):
                if isinstance(rule, str):
                    if rule == rule_name_item.text():
                        description = self.find_description_in_files_or_tables(rule)
                        if description is None:
                            QtWidgets.QMessageBox.warning(None, "Error", "No hay descripción para la regla")
                            return
                elif isinstance(rule, dict) and "rule" in rule:
                    if rule.get("rule") != rule_name_item.text():
                        QtWidgets.QMessageBox.warning(None, "Error", "No hay regla guardada con este nombre")
                        return
        if description is None:
            return

        row_position = self.summaryOfOptionsTable.rowCount()
        self.summaryOfOptionsTable.insertRow(row_position)
        self.summaryOfOptionsTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(rule_name_item.text()))
        self.summaryOfOptionsTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(description))
        self.summaryOfOptionsTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(column_name_item.text()))
        
        delete_button = QtWidgets.QPushButton("Eliminar")
        delete_button.setStyleSheet("background-color: red; color: white;")
        delete_button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        delete_button.clicked.connect(lambda: self.rule_selection_controller.remove_rule(self.summaryOfOptionsTable, row_position))
        self.summaryOfOptionsTable.setCellWidget(row_position, 3, delete_button)

    def transfer_to_main_window(self, dialog):
        self.rule_selection_controller.transfer_data_to_main_window(self.summaryOfOptionsTable)
        dialog.close()
    def get_columns_from_actual_data_table(self):
        actual_data_table = self.main_window.actualDataContainer.findChild(QtWidgets.QTableWidget)
        
        columns = []
        for i in range(actual_data_table.columnCount()):
            header_item = actual_data_table.horizontalHeaderItem(i)
            if header_item:
                columns.append(header_item.text())
        
        return columns
    
    def find_description_in_files_or_tables(self, rule_text):


        for table_name, rules in self.rules_data.get("table_rules", {}).items():
            for rule in rules:
                if rule.get("rule") == rule_text:
                    return rule.get("description")

        return None
    
    def load_rules(self):
        try:
            if not os.path.exists(self.rules_data_path):
                return []
            with open(self.rules_data_path, 'r') as file:
                rules_data = json.load(file)
            return rules_data
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Error al cargar las reglas: {str(e)}")
            return []

