import pandas as pd
import re
import json
import os

class FileController:
    
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'rules.JSON')
        self.rules_data = self._load_rules_from_file()
        self.rules_by_file_type = self._load_file_rules()  

    def _load_rules_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {"file_rules": {}, "table_rules": {}}

    def _load_file_rules(self):
        return {file_type: [rule['rule'] for rule in rules] for file_type, rules in self.rules_data['file_rules'].items()}

    def get_parameterOptions(self, file_type):
        return self.rules_by_file_type.get(file_type.upper(), [])

    def add_rule_to_file_type(self, file_type, rule):
        file_type = file_type.upper()
        if file_type not in self.rules_data['file_rules']:
            self.rules_data['file_rules'][file_type] = []

        if not any(existing_rule['rule'] == rule for existing_rule in self.rules_data['file_rules'][file_type]):
            self.rules_data['file_rules'][file_type].append({"rule": rule, "description": ""}) 
            self._save_rules_to_file()

    def remove_rule_from_file_type(self, file_type, rule):
        file_type = file_type.upper()
        if file_type in self.rules_data['file_rules']:
            self.rules_data['file_rules'][file_type] = [r for r in self.rules_data['file_rules'][file_type] if r['rule'] != rule]
            self._save_rules_to_file()

    def _save_rules_to_file(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.rules_data, file, indent=4)

    def download_cleaned_file(self, original_file_name, data, column_headers):
        file_type = original_file_name.split('.')[-1]
        cleaned_file_name = f"{original_file_name.split('.')[0]}_Depurado.{file_type}"

        df = pd.DataFrame(data, columns=column_headers)

        if file_type == "csv":
            df.to_csv(cleaned_file_name, index=False)
        elif file_type == "xlsx":
            df.to_excel(cleaned_file_name, index=False)
        elif file_type == "txt":
            df.to_csv(cleaned_file_name, index=False, sep='\t')
        
        return cleaned_file_name
