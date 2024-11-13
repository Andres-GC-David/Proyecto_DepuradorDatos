import unittest
from unittest.mock import patch, mock_open, call
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6.QtWidgets import QApplication
from App.Controller.addRuleController import RuleConfigurationController  


class TestAddRuleController(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Inicializa una instancia de QApplication para que funcione con los widgets de PyQt
        cls.app = QApplication(sys.argv)
        
    @classmethod
    def tearDownClass(cls):
        # Cierra la instancia de QApplication después de las pruebas
        cls.app.quit()
        
    def setUp(self):
        self.controller = RuleConfigurationController()

    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_save_rule_new_file(self, mock_message_box, mock_open, mock_exists):
        rule_name = "SampleRule"
        description = "Sample description"
        code = "print('Sample')"
        file_types = ["txt"]
        selected_tables = ["table1"]

        self.controller.save_rule(rule_name, description, code, file_types, selected_tables)

        mock_open.assert_any_call(self.controller.rules_data_path, "w")

    @patch("os.path.exists", side_effect=[True, False])
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "general_rules_pool": [],
        "file_rules": {},
        "table_rules": {}
    }))
    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_save_rule_existing_file(self, mock_message_box, mock_open, mock_exists):
        rule_name = "NewRule"
        description = "New description"
        code = "print('New Code')"
        file_types = ["pdf"]
        selected_tables = ["db.table2"]

        self.controller.save_rule(rule_name, description, code, file_types, selected_tables)

        mock_open.assert_any_call(self.controller.rules_data_path, "r+")
        mock_message_box.information.assert_called_once_with(None, "Éxito", "La regla fue guardada correctamente.")

    @patch("os.path.exists", side_effect=[True, True])
    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_save_rule_code_success(self, mock_message_box, mock_open, mock_exists):
        rule_name = "CodeRule"
        code = "print('Rule Code')"

        self.controller.save_rule_code(rule_name, code)

        mock_open.assert_called_with(self.controller.created_rules_file, "r+")
        mock_message_box.information.assert_not_called()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_save_rule_code_with_exception(self, mock_message_box, mock_open, mock_exists):
        mock_open.side_effect = IOError("Test IOError")
        rule_name = "ExceptionRule"
        code = "print('Exception Code')"

        self.controller.save_rule_code(rule_name, code)

        mock_message_box.warning.assert_called_once_with(None, "Error", "Error al guardar el código: Test IOError")


if __name__ == "__main__":
    unittest.main()
