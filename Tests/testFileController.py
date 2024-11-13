import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App.Controller.fileController import FileController
import pandas as pd

class TestFileController(unittest.TestCase):
    def setUp(self):
        # Inicializamos el controlador de archivos
        self.file_controller = FileController()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"file_rules": {"CSV": [{"rule": "Rule1"}]}, "table_rules": {}}')
    def test_load_rules_from_file(self, mock_open, mock_exists):
        # Verifica que los datos de reglas se cargan correctamente
        rules_data = self.file_controller._load_rules_from_file()
        self.assertIn("file_rules", rules_data)
        self.assertIn("table_rules", rules_data)
        self.assertEqual(rules_data["file_rules"]["CSV"][0]["rule"], "Rule1")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"file_rules": {"CSV": [{"rule": "Rule1"}]}, "table_rules": {}}')
    def test_load_file_rules(self, mock_open, mock_exists):
        # Verifica la estructura de reglas por tipo de archivo
        self.file_controller.rules_data = self.file_controller._load_rules_from_file()
        file_rules = self.file_controller._load_file_rules()
        self.assertIn("CSV", file_rules)
        self.assertEqual(file_rules["CSV"], ["Rule1"])

    @patch("builtins.open", new_callable=mock_open)
    def test_get_parameterOptions(self, mock_open):
        # Prueba que devuelva las reglas correctas para un tipo de archivo dado
        self.file_controller.rules_by_file_type = {"CSV": ["Rule1"]}
        options = self.file_controller.get_parameterOptions("csv")
        self.assertEqual(options, ["Rule1"])

    @patch("App.Controller.fileController.FileController._save_rules_to_file")
    def test_add_rule_to_file_type(self, mock_save_rules):
        # Agrega una regla y verifica que se guarde sin modificar el archivo JSON
        self.file_controller.rules_data = {"file_rules": {"CSV": [{"rule": "Rule1"}]}}
        self.file_controller.add_rule_to_file_type("csv", "Rule2")
        
        self.assertIn({"rule": "Rule2", "description": ""}, self.file_controller.rules_data["file_rules"]["CSV"])
        mock_save_rules.assert_called_once()

    @patch("App.Controller.fileController.FileController._save_rules_to_file")
    def test_remove_rule_from_file_type(self, mock_save_rules):
        # Elimina una regla y verifica que se guarde sin modificar el archivo JSON
        self.file_controller.rules_data = {"file_rules": {"CSV": [{"rule": "Rule1"}, {"rule": "Rule2"}]}}
        self.file_controller.remove_rule_from_file_type("csv", "Rule1")
        
        self.assertNotIn({"rule": "Rule1", "description": ""}, self.file_controller.rules_data["file_rules"]["CSV"])
        mock_save_rules.assert_called_once()

    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.DataFrame.to_excel")
    def test_download_cleaned_file_csv(self, mock_to_excel, mock_to_csv):
        # Prueba para archivo CSV generado sin guardar en el sistema
        data = [["data1", "data2"], ["data3", "data4"]]
        columns = ["Col1", "Col2"]
        file_name = self.file_controller.download_cleaned_file("test.csv", data, columns)
        
        # Verifica que el nombre del archivo sea el esperado y que to_csv sea llamado
        self.assertEqual(file_name, "test_Depurado.csv")
        mock_to_csv.assert_called_once_with("test_Depurado.csv", index=False)

    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.DataFrame.to_excel")
    def test_download_cleaned_file_xlsx(self, mock_to_excel, mock_to_csv):
        # Prueba para archivo Excel generado sin guardar en el sistema
        data = [["data1", "data2"], ["data3", "data4"]]
        columns = ["Col1", "Col2"]
        file_name = self.file_controller.download_cleaned_file("test.xlsx", data, columns)
        
        # Verifica que el nombre del archivo sea el esperado y que to_excel sea llamado
        self.assertEqual(file_name, "test_Depurado.xlsx")
        mock_to_excel.assert_called_once_with("test_Depurado.xlsx", index=False)

    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.DataFrame.to_excel")
    def test_download_cleaned_file_txt(self, mock_to_excel, mock_to_csv):
        # Prueba para archivo TXT generado sin guardar en el sistema
        data = [["data1", "data2"], ["data3", "data4"]]
        columns = ["Col1", "Col2"]
        file_name = self.file_controller.download_cleaned_file("test.txt", data, columns)
        
        # Verifica que el nombre del archivo sea el esperado y que to_csv sea llamado con separador de tabulaciones
        self.assertEqual(file_name, "test_Depurado.txt")
        mock_to_csv.assert_called_once_with("test_Depurado.txt", index=False, sep='\t')


if __name__ == "__main__":
    unittest.main()
