import unittest
import pandas as pd
from PyQt6.QtWidgets import QApplication
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App.Controller.ruleDepurationController import RuleDepurationController

class TestRuleDepurationController(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize QApplication
        cls.app = QApplication([])

    def setUp(self):
        # Arrange
        self.controller = RuleDepurationController()

    def test_apply_cedula_rules_removes_separator(self):
        # Arrange
        series = pd.Series(['1-234-567', '8-765-432'])
        params = {"modification": "Eliminar separador '-'"}

        # Act
        result = self.controller._apply_cedula_rules(series, params)

        # Assert
        expected = pd.Series(['1234567', '8765432'])
        pd.testing.assert_series_equal(result, expected)

    def test_apply_phone_rules_valid_length(self):
        # Arrange
        series = pd.Series(["1234567890", "123456789"])  # '123456789' is of incorrect length
        params = {"modification": "Validar longitud de los teléfonos Longitud: 10"}
        expected = pd.Series(["1234567890", None])  # Expect None for incorrect length

        # Act
        result = self.controller._apply_phone_rules(series, params)
        
        # Assert
        pd.testing.assert_series_equal(result, expected)



    def test_apply_email_rules_convert_to_lowercase(self):
        # Arrange
        series = pd.Series(['Test@Domain.com', 'USER@domain.COM'])
        params = {"modification": "Convertir correos a minúsculas"}

        # Act
        result = self.controller._apply_email_rules(series, params)

        # Assert
        expected = pd.Series(['test@domain.com', 'user@domain.com'])
        pd.testing.assert_series_equal(result, expected)

    def test_correct_common_domains(self):
        # Arrange
        email = "user@gnail.com"

        # Act
        result = self.controller._correct_common_domains(email)

        # Assert
        expected = "user@gmail.com"
        self.assertEqual(result, expected)

    def test_handle_duplicates_remove_all(self):
        # Arrange
        df = pd.DataFrame({
            'col1': [1, 1, 2, 2, 3],
            'col2': ['a', 'a', 'b', 'b', 'c']
        })
        params = {"modification": "Eliminar duplicados generales"}

        # Act
        result = self.controller._handle_duplicates(df, 'col1', params)

        # Assert
        expected = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        }).reset_index(drop=True)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    def test_apply_custom_rule_executes_custom_rule(self):
        # Arrange
        custom_rule = {
            "rule_name": "Remove 'a' from column",
            "code": "data[column] = data[column].str.replace('a', '')"
        }
        self.controller.custom_rules = [custom_rule]
        df = pd.DataFrame({"col1": ["apple", "banana", "cherry"]})

        # Act
        result = self.controller._apply_custom_rule("Remove 'a' from column", df, "col1")

        # Assert
        expected = pd.DataFrame({"col1": ["pple", "bnn", "cherry"]})
        pd.testing.assert_frame_equal(result, expected)

    def test_validate_single_email_format(self):
        # Arrange
        email = "test@domain.com"
        invalid_value = "Invalid"

        # Act
        result = self.controller._validate_single_email_format(email, invalid_value)

        # Assert
        self.assertEqual(result, email)

    def test_remove_duplicates(self):
        # Arrange
        df = pd.DataFrame({
            'col1': [1, 1, 2, 3, 3],
            'col2': ['a', 'a', 'b', 'c', 'c']
        })

        # Act
        result = self.controller._remove_duplicates(df, 'col1')

        # Assert
        expected = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        }).reset_index(drop=True)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    @classmethod
    def tearDownClass(cls):
        # Cleanup QApplication after all tests
        cls.app.quit()


if __name__ == '__main__':
    unittest.main()
