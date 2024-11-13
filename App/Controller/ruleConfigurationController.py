import json
import os
from PyQt6 import QtWidgets

class RuleConfigurationController:
    def __init__(self):
        self.rules_data_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'rules.JSON')
        self.created_rules_file = os.path.join(os.path.dirname(__file__), '..', 'Files', 'createdRules.JSON')

    def get_rules(self):
        try:
            with open(self.rules_data_path, 'r') as file:
                rules_data = json.load(file)
                general_rules = rules_data.get('general_rules_pool', [])
                file_rules = rules_data.get('file_rules', {})
                table_rules = rules_data.get('table_rules', {})

                all_rules = []
                for rule_name in general_rules:
                    rule_info = {
                        'rule': rule_name,
                        'description': self._get_rule_description(rule_name, file_rules, table_rules)
                    }
                    all_rules.append(rule_info)

                return all_rules
        except (FileNotFoundError, json.JSONDecodeError):
            QtWidgets.QMessageBox.warning(None, "Error", "No se pudo cargar las reglas.")
            return []

    def _get_rule_description(self, rule_name, file_rules, table_rules):
        for file_type, rules in file_rules.items():
            for rule in rules:
                if rule['rule'] == rule_name:
                    return rule.get('description', 'No hay descripción')

        for table_name, rules in table_rules.items():
            for rule in rules:
                if rule['rule'] == rule_name:
                    return rule.get('description', 'No hay descripción')

        return "No hay descripción"

    def get_rule_code(self, rule_name):
        try:
            with open(self.created_rules_file, 'r') as file:
                rules_code_data = json.load(file)
                for rule in rules_code_data:
                    if rule['rule_name'] == rule_name:
                        return rule['code']
            return "No se encontró código para esta regla."
        except (FileNotFoundError, json.JSONDecodeError):
            return "No se pudo cargar el código de la regla."

    def delete_rule(self, rule_name):
        try:
            with open(self.rules_data_path, 'r+') as file:
                rules_data = json.load(file)

                if rule_name in rules_data.get('general_rules_pool', []):
                    rules_data['general_rules_pool'].remove(rule_name)

                for file_type, rules in rules_data.get('file_rules', {}).items():
                    rules_data['file_rules'][file_type] = [rule for rule in rules if rule['rule'] != rule_name]

                for table_name, rules in rules_data.get('table_rules', {}).items():
                    rules_data['table_rules'][table_name] = [rule for rule in rules if rule['rule'] != rule_name]

                file.seek(0)
                file.truncate()
                json.dump(rules_data, file, indent=4)

            with open(self.created_rules_file, 'r+') as file:
                rules_code_data = json.load(file)
                rules_code_data = [rule for rule in rules_code_data if rule['rule_name'] != rule_name]

                file.seek(0)
                file.truncate()
                json.dump(rules_code_data, file, indent=4)

        except (FileNotFoundError, json.JSONDecodeError):
            QtWidgets.QMessageBox.warning(None, "Error", "No se pudo eliminar la regla.")
