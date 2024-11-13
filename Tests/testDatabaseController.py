import unittest
import cx_Oracle
import pandas as pd
import sys
import os
import json
from unittest.mock import patch, MagicMock, mock_open
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from App.Controller.databaseController import DatabaseController  


class TestDatabaseController(unittest.TestCase):
    def setUp(self):
        self.db_controller = DatabaseController()

    @patch("cx_Oracle.connect")
    @patch("cx_Oracle.makedsn")
    def test_connect_successful(self, mock_makedsn, mock_connect):
        self.db_controller.username = "user"
        self.db_controller.password = "pass"
        self.db_controller.host = "host"
        self.db_controller.port = "port"
        self.db_controller.service_name = "service"

        mock_connect.return_value = MagicMock()
        self.db_controller.connect()
        
        mock_makedsn.assert_called_once_with("host", "port", service_name="service")
        mock_connect.assert_called_once()
        self.assertIsNotNone(self.db_controller.connection)

    @patch("cx_Oracle.connect", side_effect=cx_Oracle.DatabaseError("DB Error"))
    def test_connect_failure(self, mock_connect):
        with self.assertRaises(Exception) as context:
            self.db_controller.connect()
        self.assertIn("Error al conectar", str(context.exception))

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"test_db": {"table1": []}}))
    def test_load_database_management_data(self, mock_open, mock_exists):
        data = self.db_controller._load_database_management_data()
        self.assertEqual(data, {"test_db": {"table1": []}})

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"table_rules": {"table1": ["rule1"]}}))
    def test_load_rules_from_file(self, mock_open, mock_exists):
        rules = self.db_controller._load_rules_from_file()
        self.assertEqual(rules, {"table1": ["rule1"]})

    @patch("cx_Oracle.connect")
    def test_execute_query_success(self, mock_connect):
        connection_mock = MagicMock()
        mock_connect.return_value = connection_mock
        cursor_mock = connection_mock.cursor.return_value
        cursor_mock.fetchall.return_value = [("row1",), ("row2",)]
        
        self.db_controller.connect()
        result = self.db_controller.execute_query("SELECT * FROM test_table")
        
        cursor_mock.execute.assert_called_once_with("SELECT * FROM test_table")
        self.assertEqual(result, [("row1",), ("row2",)])

    @patch("cx_Oracle.connect")
    def test_execute_query_no_connection(self, mock_connect):
        with self.assertRaises(Exception) as context:
            self.db_controller.execute_query("SELECT * FROM test_table")
        self.assertIn("No se ha establecido una conexión", str(context.exception))

    @patch("cx_Oracle.connect")
    def test_close_connection(self, mock_connect):
        # Simula una conexión activa configurando 'connection' como un MagicMock
        self.db_controller.connection = MagicMock()
        self.db_controller.close_connection()
        self.assertIsNone(self.db_controller.connection)


    def test_get_databases(self):
        # Configuración simulada para el test
        self.db_controller.schema_table_data = {"db1": {}, "db2": {}}
        databases = self.db_controller.get_databases()
        self.assertEqual(databases, ["db1", "db2"])

    def test_get_tables(self):
        # Configuración simulada para el test
        self.db_controller.schema_table_data = {"db1": {"table1": []}}
        tables = self.db_controller.get_tables("db1")
        self.assertEqual(list(tables), ["table1"])

    def test_get_all_tables(self):
        # Configuración simulada para el test
        self.db_controller.schema_table_data = {"db1": {"table1": []}, "db2": {"table2": []}}
        tables = self.db_controller.get_all_tables()
        self.assertEqual(tables, ["table1", "table2"])

    def test_add_rule_to_table(self):
        # Configuración simulada para el test
        self.db_controller.rules_by_table = {"table1": ["rule1"]}
        with patch.object(self.db_controller, '_save_rules_to_file') as mock_save_rules:
            self.db_controller.add_rule_to_table("table1", "rule2")
            self.assertIn("rule2", self.db_controller.rules_by_table["table1"])
            mock_save_rules.assert_called_once()  # Verifica que se llama al método sin modificar el archivo

    def test_remove_rule_from_table(self):
        # Configuración simulada para el test
        self.db_controller.rules_by_table = {"table1": ["rule1", "rule2"]}
        with patch.object(self.db_controller, '_save_rules_to_file') as mock_save_rules:
            self.db_controller.remove_rule_from_table("table1", "rule1")
            self.assertNotIn("rule1", self.db_controller.rules_by_table["table1"])
            mock_save_rules.assert_called_once()  # Verifica que se llama al método sin modificar el archivo

if __name__ == "__main__":
    unittest.main()