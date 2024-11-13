import os
import json
from PyQt6 import QtWidgets

class RuleConfigurationController:
    def __init__(self):
        self.rules_data_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'rules.JSON')
        self.created_rules_file = os.path.join(os.path.dirname(__file__), '..', 'Files', 'createdRules.JSON')

    def save_rule(self, rule_name, description, code, file_types, selected_tables):
        new_rule = {
            "rule": rule_name,
            "description": description
        }
        try:
            if not os.path.exists(self.rules_data_path):
                with open(self.rules_data_path, "w") as file:
                    json.dump({"general_rules_pool": [], "file_rules": {}, "table_rules": {}}, file, indent=4)
            with open(self.rules_data_path, "r+") as file:
                rules_data = json.load(file)

                if rule_name not in rules_data["general_rules_pool"]:
                    rules_data["general_rules_pool"].append(rule_name)
                if file_types:
                    for file_type in file_types:
                        if file_type not in rules_data["file_rules"]:
                            rules_data["file_rules"][file_type] = []
                        if new_rule not in rules_data["file_rules"][file_type]:
                            rules_data["file_rules"][file_type].append(new_rule)
                if selected_tables:
                    for table in selected_tables:
                        table_name = table.split('.')[-1]
                        if table_name in rules_data["table_rules"]:
                            if new_rule not in rules_data["table_rules"][table_name]:
                                rules_data["table_rules"][table_name].append(new_rule)
                        else:
                            rules_data["table_rules"][table_name] = [new_rule]

                file.seek(0)  
                json.dump(rules_data, file, indent=4)

            self.save_rule_code(rule_name, code)

            QtWidgets.QMessageBox.information(None, "Éxito", "La regla fue guardada correctamente.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Error al guardar la regla: {e}")


    def save_rule_code(self, rule_name, code):
        new_code_entry = {
            "rule_name": rule_name,
            "code": code
        }

        try:
            if not os.path.exists(self.created_rules_file) or os.stat(self.created_rules_file).st_size == 0:
                with open(self.created_rules_file, "w") as file:
                    json.dump([], file, indent=4)

            with open(self.created_rules_file, "r+") as file:
                try:
                    rules_code_data = json.load(file)
                except json.JSONDecodeError:
                    rules_code_data = []

                rules_code_data.append(new_code_entry)

                file.seek(0)
                json.dump(rules_code_data, file, indent=4)

        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Error al guardar el código: {e}")
