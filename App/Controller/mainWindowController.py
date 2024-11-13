import pandas as pd
from PyQt6 import QtWidgets
from App.Controller.databaseController import DatabaseController
from App.Controller.fileController import FileController
from PyQt6.QtWidgets import QMessageBox
import pandas as pd
from App.Controller.ruleDepurationController import RuleDepurationController  
from PyQt6.QtWidgets import QFileDialog

class MainWindowController:
    
    def __init__(self):
        self.rule_depuration_controller = RuleDepurationController()
        self.database_controller = DatabaseController()
        self.selected_rules = []
    def apply_depuration(self, ui_main_window):
        try:
            parameter_table = ui_main_window.summaryOfParameterTable
            if parameter_table.rowCount() == 0 or self._is_table_empty(parameter_table):
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("Error")
                msg_box.setText("No hay reglas de negocio definidas para aplicar la depuración.")
                msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg_box.exec()
                return
            
            self.selected_rules = self._extract_rules_with_parameters(parameter_table)
            df = self._extract_table_data_as_dataframe(ui_main_window.actualDataContainer)
            rules = self._extract_rules_with_parameters(parameter_table)
            try:
                modified_df = self.rule_depuration_controller.apply_rules(df, rules, ui_main_window.centralwidget)
                self._populate_table_with_data(ui_main_window.newDataContainer.findChild(QtWidgets.QTableWidget), modified_df)
            except Exception as depuration_error:
                # Captura cualquier error de depuración y muestra un mensaje
                QtWidgets.QMessageBox.warning(
                    ui_main_window.centralwidget, 
                    "Error en Depuración", 
                    f"Error al aplicar depuración: {str(depuration_error)}"
                )
            

        except Exception as e:
            QtWidgets.QMessageBox.warning(ui_main_window.centralwidget, "Error", f"Error al aplicar depuración: {str(e)}")

    def download_data(self, ui_main_window):
        try:
            new_data_table = ui_main_window.newDataContainer.findChild(QtWidgets.QTableWidget)
            if new_data_table.rowCount() == 0 or self._is_table_empty(new_data_table):
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("Error")
                msg_box.setText("No hay datos modificados para descargar.")
                msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg_box.exec()
                return

            data_type = ui_main_window.summayOfDataTable.item(0, 0).text().lower()
            data_name = ui_main_window.summayOfDataTable.item(0, 2).text()
            db_name_item = ui_main_window.summayOfDataTable.item(0, 2)
            if db_name_item is None or not db_name_item.text().strip():
                raise ValueError("No se encontró el nombre de la base de datos.")
            
            db_name = db_name_item.text().strip()

            if data_type == "archivo":
                file_filter = "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
            elif data_type == "base de datos":
                file_filter = "SQL Files (*.sql);;All Files (*)"
            else:
                raise ValueError("Tipo de dato no reconocido.")
            
            save_path, _ = QFileDialog.getSaveFileName(
                None, 
                "Guardar archivo", 
                f"{data_name}", 
                file_filter  
            )

            if not save_path:
                return

            if data_type == "archivo":
                self._download_cleaned_file(ui_main_window, save_path)
            elif data_type == "base de datos":
                self._download_sql_script(ui_main_window, db_name, save_path)
            else:
                raise ValueError("Tipo de dato no reconocido.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(ui_main_window.centralwidget, "Error", f"Error al descargar los datos: {str(e)}")
   
            
        
    def _is_table_empty(self, table_widget):
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item and item.text().strip():  
                    return False
        return True

    def _download_cleaned_file(self, ui_main_window, save_path):
        try:
            file_controller = FileController()
            table_widget = ui_main_window.newDataContainer.findChild(QtWidgets.QTableWidget)
            data = self._extract_table_data_as_list(table_widget)
            column_headers = self._extract_column_headers(ui_main_window.newDataContainer)
            cleaned_file_name = file_controller.download_cleaned_file(save_path, data, column_headers)
            
            QtWidgets.QMessageBox.information(
                ui_main_window.centralwidget, 
                "Descarga Completa", 
                f"El archivo ha sido guardado en {cleaned_file_name}."
            )

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                ui_main_window.centralwidget, 
                "Error", 
                f"Error al descargar el archivo: {str(e)}"
            )

    def _download_sql_script(self, ui_main_window, db_name, save_path):
        try:
            original_df = self._extract_table_data_as_dataframe(ui_main_window.actualDataContainer)
            modified_df = self._extract_table_data_as_dataframe(ui_main_window.newDataContainer)

            if original_df.empty or modified_df.empty:
                raise ValueError("Los datos originales o modificados están vacíos.")
            if list(original_df.columns) != list(modified_df.columns):
                raise ValueError("Las columnas de los datos originales y modificados no coinciden.")
            table_name_item = ui_main_window.summayOfDataTable.item(0, 2)
            if table_name_item is None or not table_name_item.text().strip():
                raise ValueError("No se encontró el nombre de la tabla.")

            table_name = table_name_item.text().strip()

            # Verifica si "Estandarización de Cédulas" está en selected_rules y extrae el nombre de la columna
            column_name = ui_main_window.summaryOfParameterTable.item(0, 1).text().strip()
            
            if column_name and ', ' in column_name:
                ruleSelectedForDepuration, columnsSelectedForDepuration = column_name.split(', ')
                if ruleSelectedForDepuration != "Estandarizacion de Cedulas":
                    columnsSelectedForDepuration = None
            else:
                ruleSelectedForDepuration = column_name
                columnsSelectedForDepuration = None

            sql_file_name = self.database_controller.generate_sql_script(db_name, table_name, original_df, modified_df, save_path, columnsSelectedForDepuration)

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Éxito")
            msg_box.setText(f"Script SQL generado en direccion: {sql_file_name}")
            msg_box.exec()
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText(f"Error al generar el script SQL: {str(e)}")
            msg_box.exec()

    def _extract_table_data_as_list(self, table_widget):
        data = []
        for row in range(table_widget.rowCount()):
            row_data = [table_widget.item(row, col).text() if table_widget.item(row, col) else "" for col in range(table_widget.columnCount())]
            data.append(row_data)
        return data

    def load_data_from_file(self, ui_main_window, file_path):
        try:
            file_extension = self._get_file_extension(file_path)
            data, column_headers = self._read_file_data(file_path, file_extension)

            actual_data_table = ui_main_window.actualDataContainer.findChild(QtWidgets.QTableWidget)
            self._populate_table_with_file_data(actual_data_table, data, column_headers)
        except ValueError as ve:
            QtWidgets.QMessageBox.warning(ui_main_window.centralwidget, "Error", str(ve))
        except Exception as e:
            QtWidgets.QMessageBox.critical(ui_main_window.centralwidget, "Error", f"Error al cargar el archivo: {str(e)}")

    def load_data_in_actual_table(self, ui_main_window, data, column_headers):
        try:
            if not data or not column_headers:
                raise ValueError("Datos o encabezados vacíos.")

            actual_data_table = ui_main_window.actualDataContainer.findChild(QtWidgets.QTableWidget)
            self._populate_table_with_data(actual_data_table, pd.DataFrame(data, columns=column_headers))
        except Exception as e:
            QtWidgets.QMessageBox.warning(ui_main_window.centralwidget, "Error", f"Error al cargar datos en la tabla: {str(e)}")

    def reset_actual_data_table(self, ui_main_window):
        try:
            actual_new_layout = ui_main_window.actual_new_layout
            new_data_container = ui_main_window.newDataContainer

            actual_new_layout.removeWidget(ui_main_window.actualDataContainer)
            actual_new_layout.removeWidget(new_data_container)

            ui_main_window.actualDataContainer.deleteLater()
            ui_main_window.actualDataContainer = ui_main_window.create_data_container("Esquema Actual", 10, 10)

            actual_new_layout.addWidget(ui_main_window.actualDataContainer)
            actual_new_layout.addWidget(new_data_container)
        except Exception as e:
            QtWidgets.QMessageBox.warning(ui_main_window.centralwidget, "Error", f"Error al resetear la tabla: {str(e)}")
            
    def reset_new_data_table(self, ui_main_window):
        try:

            actual_new_layout = ui_main_window.actual_new_layout
            actual_data_container = ui_main_window.actualDataContainer
            actual_new_layout.removeWidget(ui_main_window.newDataContainer)
            ui_main_window.newDataContainer.deleteLater()
            ui_main_window.newDataContainer = ui_main_window.create_data_container("Esquema Modificado", 10, 10)

            actual_new_layout.addWidget(ui_main_window.newDataContainer)

        except Exception as e:
            QtWidgets.QMessageBox.warning(ui_main_window.centralwidget, "Error", f"Error al resetear la tabla: {str(e)}")


    def _extract_table_data(self, data_container):
        table_widget = data_container.findChild(QtWidgets.QTableWidget)
        data = []
        for row in range(table_widget.rowCount()):
            row_data = [table_widget.item(row, col).text() if table_widget.item(row, col) else "" 
                        for col in range(table_widget.columnCount())]
            data.append(row_data)
        return data

    def _extract_column_headers(self, data_container):
        table_widget = data_container.findChild(QtWidgets.QTableWidget)
        return [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]

    def _extract_rules(self, parameter_table):
        rules = []
        for row in range(parameter_table.rowCount()):
            rule_name_item = parameter_table.item(row, 0)
            column_item = parameter_table.item(row, 1)
            if rule_name_item and column_item:
                rules.append((rule_name_item.text(), column_item.text()))
        return rules

    def _get_file_extension(self, file_path):
        if not file_path:
            raise ValueError("No se proporcionó una ruta de archivo.")
        return file_path.split('.')[-1].lower()

    def _read_file_data(self, file_path, file_extension):
        if file_extension == 'csv':
            data = pd.read_csv(file_path)
        elif file_extension == 'xlsx':
            data = pd.read_excel(file_path)
        elif file_extension == 'txt':
            data = pd.read_csv(file_path, delimiter='\t')
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file_extension}")
        return data.values, data.columns.tolist()

    def _populate_table_with_data(self, table_widget, data_df):
        table_widget.setRowCount(0)
        table_widget.setColumnCount(len(data_df.columns))
        table_widget.setHorizontalHeaderLabels(data_df.columns.tolist())

        for row_num, row_data in data_df.iterrows():
            table_widget.insertRow(row_num)
            for col_num, value in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(value)))

    def _populate_table_with_file_data(self, table_widget, data, column_headers):
        table_widget.setRowCount(0)
        table_widget.setColumnCount(len(column_headers))
        table_widget.setHorizontalHeaderLabels(column_headers)

        for row_num, row_data in enumerate(data):
            table_widget.insertRow(row_num)
            for col_num, value in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(value)))
    def _extract_table_data_as_dataframe(self, data_container):

        table_widget = data_container.findChild(QtWidgets.QTableWidget)
        data = []
        for row in range(table_widget.rowCount()):
            row_data = [table_widget.item(row, col).text() if table_widget.item(row, col) else ""
                        for col in range(table_widget.columnCount())]
            data.append(row_data)
        column_headers = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]
        return pd.DataFrame(data, columns=column_headers)
    
    def _extract_rules_with_parameters(self, parameter_table, parent_widget=None):
        rules = []

        for row in range(parameter_table.rowCount()):
            rule_name_item = parameter_table.item(row, 0) 
            column_item = parameter_table.item(row, 2) 
            modification_item = parameter_table.item(row, 1)  

            if rule_name_item is None:
                self._show_message(f"Fila {row}: No se encontró el nombre de la regla.", parent_widget)
                continue

            if column_item is None:
                self._show_message(f"Fila {row}: No se encontró la columna.", parent_widget)
                continue

            if modification_item is None:
                self._show_message(f"Fila {row}: No se encontró la descripción de la regla.", parent_widget)
                continue

            params = {"action": rule_name_item.text(), "modification": modification_item.text()}

            rules.append((rule_name_item.text(), column_item.text(), params))

        if not rules:
            self._show_message("No se extrajeron reglas.", parent_widget)
            return

        return rules

    
    def _show_message(self, message, parent_widget=None):
        
        msg_box = QtWidgets.QMessageBox(parent_widget)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Advertencia")
        msg_box.setText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg_box.exec()
