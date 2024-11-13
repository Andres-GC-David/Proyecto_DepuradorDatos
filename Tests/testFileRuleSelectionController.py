import unittest
from unittest.mock import patch, MagicMock, mock_open, call, ANY
from PyQt6 import QtWidgets
import sys
import os
import pandas as pd
from PyQt6 import QtWidgets, QtCore
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App.Controller.fileRuleSelectionController import FileRuleSelectionController
import pandas as pd

class TestFileRuleSelectionController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication(sys.argv)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        # Configurar `file_controller` como MagicMock en lugar de `patch` en cada prueba
        self.file_controller = MagicMock()
        self.controller = FileRuleSelectionController(None, self.file_controller, None)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"file_rules": {}, "table_rules": {}}')
    def test_load_rules_file_exists(self, mock_open, mock_exists):
        rules_data = self.controller.load_rules()
        self.assertIn("file_rules", rules_data)
        self.assertIn("table_rules", rules_data)

    def test_load_columns_from_uploaded_file_no_file_selected(self):
        columns_table = MagicMock()
        summayOfDataTable = MagicMock()
        summayOfDataTable.item.return_value = None
        result = self.controller.load_columns_from_uploaded_file(columns_table, summayOfDataTable)
        self.assertIsNone(result)

    @patch("pandas.read_csv")
    def test_load_columns_from_uploaded_file_load_csv(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(columns=["Column1", "Column2"])
        columns_table = MagicMock()
        summayOfDataTable = MagicMock()
        summayOfDataTable.item.return_value.text.return_value = "file.csv"
        self.controller.load_columns_from_uploaded_file(columns_table, summayOfDataTable)
        
        expected_calls = [
            call(0, 0, ANY),
            call(1, 0, ANY),
        ]
        columns_table.setItem.assert_has_calls(expected_calls, any_order=True)

    def test_fill_rule_options_table_with_parameters(self):
        rule_options_table = MagicMock()
        summayOfDataTable = MagicMock()
        summayOfDataTable.item.return_value.text.return_value = "file.csv"
        self.file_controller.get_parameterOptions.return_value = ["Rule1", "Rule2"]
        
        self.controller.fill_rule_options_table(rule_options_table, summayOfDataTable)
        
        rule_options_table.setRowCount.assert_called_once_with(2)
        expected_calls = [
            call(0, 0, ANY),
            call(1, 0, ANY),
        ]
        rule_options_table.setItem.assert_has_calls(expected_calls, any_order=True)

    @patch("App.Controller.fileRuleSelectionController.FileRuleSelectionController.get_rule_description", return_value="Descripción")
    def test_add_selected_options_success(self, mock_get_description):
        main_window_mock = MagicMock()
        controller = FileRuleSelectionController(main_window_mock, self.file_controller, None)
        rule_options_table = MagicMock()
        columns_options_table = MagicMock()
        summary_of_options_table = MagicMock()

        # Simulación de selección de regla y columna
        rule_item = MagicMock()
        rule_item.text.return_value = "Rule1"
        rule_options_table.currentItem.return_value = rule_item
        column_item = MagicMock()
        column_item.text.return_value = "Column1"
        columns_options_table.currentItem.return_value = column_item

        # Configurar rowCount para devolver un valor fijo
        summary_of_options_table.rowCount.return_value = 0
        
        controller.add_selected_options(rule_options_table, columns_options_table, summary_of_options_table)
        
        summary_of_options_table.insertRow.assert_called_once_with(0)
        expected_calls = [
            call(0, 0, ANY),
            call(0, 1, ANY),
            call(0, 2, ANY),
        ]
        summary_of_options_table.setItem.assert_has_calls(expected_calls, any_order=True)

if __name__ == "__main__":
    unittest.main()