import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from PyQt6.QtWidgets import QApplication, QTableWidget, QMessageBox
import sys
from PyQt6.QtWidgets import QTableWidgetItem
import os

# Configura la ruta para importar el módulo MainWindowController
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App.Controller.mainWindowController import MainWindowController

class TestMainWindowController(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)  # Inicializa QApplication para los widgets de PyQt
    
    @classmethod
    def tearDownClass(cls):
        cls.app.quit()  # Cierra QApplication después de todas las pruebas

    def setUp(self):
        self.controller = MainWindowController()
        self.ui_main_window = MagicMock()
        self.ui_main_window.summaryOfParameterTable = QTableWidget()
        self.ui_main_window.actualDataContainer = QTableWidget()
        self.ui_main_window.newDataContainer = MagicMock(findChild=MagicMock(return_value=QTableWidget()))
        self.ui_main_window.centralwidget = MagicMock()
        self.ui_main_window.summayOfDataTable = QTableWidget()

    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_apply_depuration_shows_message_if_table_empty(self, mock_message_box):
        # Test de apply_depuration para cuando la tabla está vacía
        self.controller._is_table_empty = MagicMock(return_value=True)
        self.controller.apply_depuration(self.ui_main_window)
        mock_message_box.return_value.exec.assert_called_once()

    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_download_data_shows_message_if_no_data(self, mock_message_box):
        # Test de download_data para cuando no hay datos modificados
        self.controller._is_table_empty = MagicMock(return_value=True)
        self.controller.download_data(self.ui_main_window)
        mock_message_box.return_value.exec.assert_called_once()

    def test_is_table_empty_returns_true_if_no_data(self):
        # Test de _is_table_empty para validar que devuelve True si no hay datos
        table = QTableWidget()
        self.assertTrue(self.controller._is_table_empty(table))

    @patch("App.Controller.fileController.FileController.download_cleaned_file")
    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_download_cleaned_file_saves_file(self, mock_message_box, mock_download_file):
        # Test de _download_cleaned_file para verificar que llama a download_cleaned_file
        self.controller._extract_table_data_as_list = MagicMock(return_value=[["data1", "data2"]])
        self.controller._extract_column_headers = MagicMock(return_value=["col1", "col2"])
        self.controller._download_cleaned_file(self.ui_main_window, "path/to/save.csv")
        mock_download_file.assert_called_once()

    @patch("App.Controller.databaseController.DatabaseController.generate_sql_script")
    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_download_sql_script_generates_script(self, mock_message_box, mock_generate_sql):
        # Configura los mocks necesarios para el test
        test_df = pd.DataFrame({"col1": [1], "col2": [2]})
        self.controller._extract_table_data_as_dataframe = MagicMock(return_value=test_df)
        self.ui_main_window.summayOfDataTable.item = MagicMock(side_effect=[QTableWidgetItem("test_table")])

        # Llama al método
        self.controller._download_sql_script(self.ui_main_window, "test_db", "path/to/script.sql")
        
        # Verifica que generate_sql_script fue llamado
        self.assertTrue(mock_generate_sql.called)

        # Verifica los argumentos sin comparar DataFrames directamente
        called_args = mock_generate_sql.call_args[0]
        self.assertEqual(called_args[0], "test_db")  # Verifica db_name
        self.assertEqual(called_args[1], "test_table")  # Verifica table_name
        self.assertEqual(called_args[4], "path/to/script.sql")  # Verifica save_path
        
        # Compara DataFrames utilizando pandas.testing
        pd.testing.assert_frame_equal(called_args[2], test_df)  # Verifica original_df
        pd.testing.assert_frame_equal(called_args[3], test_df)  # Verifica modified_df


    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_reset_actual_data_table_resets_table(self, mock_message_box):
        # Configura el layout y el contenedor de datos
        self.ui_main_window.actual_new_layout = MagicMock()
        original_container = self.ui_main_window.actualDataContainer

        # Llama al método
        self.controller.reset_actual_data_table(self.ui_main_window)
        
        # Verifica que el contenedor original fue removido
        self.ui_main_window.actual_new_layout.removeWidget.assert_any_call(original_container)


    @patch("PyQt6.QtWidgets.QMessageBox")
    def test_reset_new_data_table_resets_table(self, mock_message_box):
        # Configura el layout y el contenedor de datos
        self.ui_main_window.actual_new_layout = MagicMock()
        original_container = self.ui_main_window.newDataContainer

        # Llama al método
        self.controller.reset_new_data_table(self.ui_main_window)
        
        # Verifica que el contenedor original fue removido
        self.ui_main_window.actual_new_layout.removeWidget.assert_called_with(original_container)



if __name__ == "__main__":
    unittest.main()
