import os
import json
import pandas as pd
from PyQt6 import QtWidgets
from App.View.ruleActionDialog import Ui_RuleActionDialog
from App.View.ruleActionEmailDialog import Ui_RuleActionEmailDialog
from App.View.ruleActionCedulaDialog import Ui_RuleActionCedulaDialog
from App.View.ruleActionDuplicatesDialog import Ui_RuleActionDuplicatesDialog
from App.View.manageRulesDialog import Ui_ManageRulesDialog
from App.Controller.ruleManegementController import RuleController

class FileRuleSelectionController:
    
    def __init__(self, main_window, file_controller, ui_dialog):
        self.main_window = main_window
        self.file_controller = file_controller
        self.rule_controller = RuleController()
        self.df = None
        self.ui_dialog = ui_dialog
        self.rules_data_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'rules.JSON')
        self.rules_data = self.load_rules()
        
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

    def load_columns_from_uploaded_file(self, columns_table, summayOfDataTable):
        file_name_item = summayOfDataTable.item(0, 2)
        
        if file_name_item is None:
            QtWidgets.QMessageBox.warning(None, "Error", "No se ha seleccionado ningún archivo.")
            return

        file_name = file_name_item.text()

        try:
            if file_name.endswith('.csv'):
                self.df = pd.read_csv(file_name)
            elif file_name.endswith('.xlsx'):
                self.df = pd.read_excel(file_name)
            elif file_name.endswith('.txt'):
                self.df = pd.read_csv(file_name, delimiter='\t')
            else:
                raise ValueError("Formato de archivo no soportado")

            columns_table.setRowCount(0)
            
            for i, column_name in enumerate(self.df.columns):
                columns_table.insertRow(i)
                columns_table.setItem(i, 0, QtWidgets.QTableWidgetItem(column_name))
        
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"No se pudo cargar el archivo: {str(e)}")

    def fill_data_selected_table(self, data_selected_table, summayOfDataTable):
        for row in range(summayOfDataTable.rowCount()):
            for col in range(summayOfDataTable.columnCount()):
                item = summayOfDataTable.item(row, col)
                if item is not None:
                    new_item = QtWidgets.QTableWidgetItem(item.text())
                    data_selected_table.setItem(row, col, new_item)

    def fill_rule_options_table(self, rule_options_table, summayOfDataTable):
        file_name_item = summayOfDataTable.item(0, 1)
        
        if file_name_item is None:
            QtWidgets.QMessageBox.warning(None, "Error", "No se ha seleccionado ningún archivo.")
            return
        file_type = file_name_item.text().split('.')[-1].upper()
        parameter_options = self.file_controller.get_parameterOptions(file_type)

        if not parameter_options:
            QtWidgets.QMessageBox.warning(None, "Error", f"No se encontraron opciones de parámetro para el archivo '{file_type}'.")
            return

        rule_options_table.setRowCount(len(parameter_options))
        rule_options_table.setColumnCount(1)
        rule_options_table.setHorizontalHeaderLabels(["Opciones de Parámetro"])

        for row, option in enumerate(parameter_options):
            item = QtWidgets.QTableWidgetItem(option)
            rule_options_table.setItem(row, 0, item)

    def add_selected_options(self, rule_options_table, columns_options_table, summary_of_options_table):
        rule_item = rule_options_table.currentItem()  
        column_item = columns_options_table.currentItem() 

        if rule_item is None or column_item is None:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Debe seleccionar una opción y una columna.")
            return
        for row in range(summary_of_options_table.rowCount()):
            existing_column_item = summary_of_options_table.item(row, 1)  
            if existing_column_item and existing_column_item.text() == column_item.text():
                QtWidgets.QMessageBox.warning(None, "Advertencia", f"La columna '{column_item.text()}' ya tiene una regla aplicada.")
                return
        description = self.get_rule_description(rule_item.text())
        if description is None:
            return
        if isinstance(description, dict):
            description = str(description)  
        row_position = summary_of_options_table.rowCount()
        summary_of_options_table.insertRow(row_position)
        summary_of_options_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(rule_item.text()))  
        summary_of_options_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(column_item.text()))  
        summary_of_options_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(description))  

        delete_button = QtWidgets.QPushButton("Eliminar")
        delete_button.setStyleSheet("background-color: red; color: white;")
        delete_button.clicked.connect(lambda: self.remove_rule(summary_of_options_table, row_position))

        summary_of_options_table.setCellWidget(row_position, 3, delete_button)
        self.main_window.controller.selected_rules.append((rule_item.text(), column_item.text(), description))

    def remove_rule(self, summary_of_options_table, row_position):
        summary_of_options_table.removeRow(row_position)
        if row_position < len(self.main_window.controller.selected_rules):
            del self.main_window.controller.selected_rules[row_position]
        self.update_main_window_table()
        QtWidgets.QMessageBox.information(None, "Eliminar", "La regla ha sido eliminada exitosamente.")

    def update_main_window_table(self):
        self.main_window.summaryOfParameterTable.setRowCount(0)
        for rule in self.main_window.controller.selected_rules:
            row_position = self.main_window.summaryOfParameterTable.rowCount()
            self.main_window.summaryOfParameterTable.insertRow(row_position)
            self.main_window.summaryOfParameterTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(rule[0])) 
            description = str(rule[2]) if isinstance(rule[2], dict) else rule[2]
            
            self.main_window.summaryOfParameterTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(description))
            self.main_window.summaryOfParameterTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(rule[1]))


    def get_rule_description(self, rule_text):
        if rule_text == "Estandarizacion de Telefonos":
            dialog = QtWidgets.QDialog(self.main_window)
            ui = Ui_RuleActionDialog()
            ui.setupUi(dialog, rule_text)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                return ui.get_description()
        elif rule_text == "Validacion Correos":
            dialog = QtWidgets.QDialog(self.main_window)
            ui = Ui_RuleActionEmailDialog()
            ui.setupUi(dialog, "Validar Correos")

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                return ui.get_description()
        elif rule_text == "Estandarizacion de Cedulas":
            dialog = QtWidgets.QDialog(self.main_window)
            ui = Ui_RuleActionCedulaDialog()
            ui.setupUi(dialog, "Estandarizar cédulas")

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                return ui.get_description()
        elif rule_text == "Eliminacion de Duplicados":
            dialog = QtWidgets.QDialog(self.main_window)
            columns = self.get_columns_from_actual_data_table()  
            ui = Ui_RuleActionDuplicatesDialog(columns) 
            ui.setupUi(dialog, "Eliminacion de Duplicados")

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                return ui.get_description()
            
        else:
            for rule in self.rules_data.get("general_rules_pool", []):
                
                if isinstance(rule, str):
                    if rule == rule_text:
                        description = self.find_description_in_files_or_tables(rule)
                        if description:
                            return description
                        else:
                            return f"Esta es la descripción genérica para la regla {rule}"

                elif isinstance(rule, dict) and "rule" in rule:
                    if rule.get("rule") == rule_text:
                        return rule.get("description")


        QtWidgets.QMessageBox.warning(None, "Error", "Regla no reconocida.")
        return None
    
    def find_description_in_files_or_tables(self, rule_text):
        for file_type, rules in self.rules_data.get("file_rules", {}).items():
            for rule in rules:
                if rule.get("rule") == rule_text:
                    return rule.get("description")

        for table_name, rules in self.rules_data.get("table_rules", {}).items():
            for rule in rules:
                if rule.get("rule") == rule_text:
                    return rule.get("description")

        return None

    def open_manage_rules_dialog(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_ManageRulesDialog(self.file_controller, self.ui_dialog, is_file=True, from_rule_configuration=False) 
        ui.setupUi(dialog)
        dialog.exec()
        
    def transfer_to_main_window(self, dialog, summary_of_options_table):
        existing_rules = set()

        for row in range(self.main_window.summaryOfParameterTable.rowCount()):
            rule_name = self.main_window.summaryOfParameterTable.item(row, 0).text()
            column_name = self.main_window.summaryOfParameterTable.item(row, 2).text()
            existing_rules.add((rule_name, column_name))

        for row in range(summary_of_options_table.rowCount()):
            rule_item = summary_of_options_table.item(row, 0)  
            column_selected = summary_of_options_table.item(row, 1) 
            modification_item = summary_of_options_table.item(row, 2)  

            if rule_item and modification_item:
                if (rule_item.text(), column_selected.text()) not in existing_rules:
                    new_row_position = self.main_window.summaryOfParameterTable.rowCount()
                    self.main_window.summaryOfParameterTable.insertRow(new_row_position)
                    self.main_window.summaryOfParameterTable.setItem(new_row_position, 0, QtWidgets.QTableWidgetItem(rule_item.text()))  
                    self.main_window.summaryOfParameterTable.setItem(new_row_position, 1, QtWidgets.QTableWidgetItem(modification_item.text()))  
                    self.main_window.summaryOfParameterTable.setItem(new_row_position, 2, QtWidgets.QTableWidgetItem(column_selected.text()))  
        self.add_buttons_to_existing_rows(summary_of_options_table)
        dialog.close()

    def add_buttons_to_existing_rows(self, summary_of_options_table):
        row_count = summary_of_options_table.rowCount()
        for row_position in range(row_count):
            delete_button = QtWidgets.QPushButton("Eliminar")
            delete_button.setStyleSheet("background-color: red; color: white;")
            delete_button.clicked.connect(lambda checked, row=row_position: self.remove_rule(summary_of_options_table, row))
            summary_of_options_table.setCellWidget(row_position, 3, delete_button)

        
    def get_columns_from_actual_data_table(self):
        actual_data_table = self.main_window.actualDataContainer.findChild(QtWidgets.QTableWidget)
        
        columns = []
        for i in range(actual_data_table.columnCount()):
            header_item = actual_data_table.horizontalHeaderItem(i)
            if header_item:
                columns.append(header_item.text())
        
        return columns
