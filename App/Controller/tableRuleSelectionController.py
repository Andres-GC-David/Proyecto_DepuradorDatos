import os
import json
from PyQt6 import QtWidgets
from App.Controller.databaseController import DatabaseController

class TableRuleSelectionController:
    def __init__(self, database_controller, main_window):
        self.database_controller = DatabaseController()
        self.main_window = main_window
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

    def get_parameter_options_with_description(self, database_name):
        try:
            parameter_options = self.database_controller.get_parameterOptionsWithDescription(database_name)
            if not parameter_options:
                raise ValueError(f"No se encontraron opciones de parámetro para la base de datos '{database_name}'.")

            parameter_options_set = {option['rule'] for option in parameter_options}

            custom_rules = self.rules_data.get("table_rules", {}).get(database_name, [])
            for rule in custom_rules:
                rule_name = rule['rule']
                if rule_name not in parameter_options_set:
                    parameter_options_set.add(rule_name)  

            return list(parameter_options_set)
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", str(e))
            return None
        
    def validate_selected_database(self, summay_of_data_table):
        try:
            database_name_item = summay_of_data_table.item(0, 2)
            if database_name_item is None:
                raise ValueError("No se ha seleccionado ninguna base de datos.")
            return database_name_item.text()
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", str(e))
            return None

    def validate_selected_rule(self, rule_name_item):
        try:
            if rule_name_item is None:
                raise ValueError("Debe seleccionar una opción válida.")
            return rule_name_item.text()
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Advertencia", str(e))
            return None

    def add_rule(self, rule_name, description):
        try:
            if not rule_name or not description:
                raise ValueError("La regla o la descripción no puede estar vacía.")
            row_position = self.main_window.summaryOfParameterTable.rowCount()
            self.main_window.summaryOfParameterTable.insertRow(row_position)
            self.main_window.summaryOfParameterTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(rule_name))
            self.main_window.summaryOfParameterTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(description))
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", str(e))

    def transfer_data_to_main_window(self, summary_of_options_table):
        try:
            self.main_window.summaryOfParameterTable.setRowCount(0)
            selected_rules = []

            for row in range(summary_of_options_table.rowCount()):
                rule_item = summary_of_options_table.item(row, 0)
                column_item = summary_of_options_table.item(row, 1)
                column_selected = summary_of_options_table.item(row, 2)

                if rule_item and column_item and column_selected:
                    self.main_window.summaryOfParameterTable.insertRow(row)
                    self.main_window.summaryOfParameterTable.setItem(row, 0, QtWidgets.QTableWidgetItem(rule_item.text()))
                    self.main_window.summaryOfParameterTable.setItem(row, 1, QtWidgets.QTableWidgetItem(column_item.text()))
                    self.main_window.summaryOfParameterTable.setItem(row, 2, QtWidgets.QTableWidgetItem(column_selected.text()))
                    
                    delete_button = QtWidgets.QPushButton("Eliminar")
                    delete_button.setStyleSheet("background-color: red; color: white;")
                    delete_button.clicked.connect(lambda: self.remove_rule(summary_of_options_table, row))

                    self.main_window.summaryOfParameterTable.setCellWidget(row, 3, delete_button)  # Insertar botón en la columna 3
                    selected_rules.append((rule_item.text(), column_item.text(), column_selected.text()))

            self.main_window.controller.selected_rules = selected_rules

        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", str(e))
            
    def remove_rule(self, summary_of_options_table, row_position):
        summary_of_options_table.removeRow(row_position)
        if row_position < len(self.main_window.controller.selected_rules):
            del self.main_window.controller.selected_rules[row_position]
        QtWidgets.QMessageBox.information(None, "Eliminar", "La regla ha sido eliminada exitosamente.")


