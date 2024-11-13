import json
import os

class RuleController:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'rules.JSON')
        self.rules_data = self._load_rules_from_file()

    def _load_rules_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {"general_rules_pool": [], "file_rules": {}, "table_rules": {}}

    def get_available_rules(self):
        return self.rules_data.get("general_rules_pool", [])

    def get_rules_for_file_type(self, file_type):
        return self.rules_data["file_rules"].get(file_type.upper(), [])

    def get_rules_for_table(self, table_name):
        return self.rules_data["table_rules"].get(table_name.lower(), [])

    def add_rule(self, source, rule, description, is_file=True):
        rule_data = {"rule": rule, "description": description}
        if is_file:
            if source.upper() not in self.rules_data["file_rules"]:
                self.rules_data["file_rules"][source.upper()] = []
            self.rules_data["file_rules"][source.upper()].append(rule_data)
        else:
            if source.lower() not in self.rules_data["table_rules"]:
                self.rules_data["table_rules"][source.lower()] = []
            self.rules_data["table_rules"][source.lower()].append(rule_data)

        self._save_rules_to_file()

    def remove_rule(self, source, rule, is_file=True):
        if is_file:
            if source.upper() in self.rules_data["file_rules"]:
                self.rules_data["file_rules"][source.upper()] = [
                    r for r in self.rules_data["file_rules"][source.upper()] if r['rule'] != rule
                ]
        else:
            if source.lower() in self.rules_data["table_rules"]:
                self.rules_data["table_rules"][source.lower()] = [
                    r for r in self.rules_data["table_rules"][source.lower()] if r['rule'] != rule
                ]

        self._save_rules_to_file()


    def _save_rules_to_file(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.rules_data, file, indent=4)

    def rule_exists_in_applied(self, rule_text, applied_rules):
        return rule_text in applied_rules
