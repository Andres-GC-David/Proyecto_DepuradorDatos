from PyQt6 import QtCore, QtGui, QtWidgets
import json
import os
from App.Controller.databaseController import DatabaseController
from App.View.tableColumnManagement import Ui_TableColumnManagementDialog 
from App.View.tableIndexSelection import Ui_TableIndexSelectionDialog 
import re

class Ui_DataBaseManagementDialog(object):

    def __init__(self, database_controller):
        self.databaseController = database_controller
        self.schema_table_data = self.databaseController.schema_table_data
        self.protected_schemas = ["axiscoope", "coopegua", "coopesa"]
        self.protected_tables = {
            "axiscoope": ["cl_personas", "cl_ubicaciones"],
            "coopegua": ["cliente", "usuario_cliente", "proveedor", "empleado"],
            "coopesa": ["cliente", "proveedor", "empleado"]
        }

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 700)
        Dialog.setWindowTitle("Gestión de Esquemas y Tablas")
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        # Título
        self.titleLabel = QtWidgets.QLabel("Gestión de Esquemas y Tablas", Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(100, 10, 450, 40))  # Ancho ajustado
        self.titleLabel.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Weight.Bold))
        self.titleLabel.setStyleSheet("color: white;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Panel para Esquemas
        self.schemaPanel = QtWidgets.QWidget(Dialog)
        self.schemaPanel.setGeometry(QtCore.QRect(20, 70, 610, 260))  # Panel más ancho
        self.schemaPanel.setStyleSheet("background-color: white; border-radius: 8px;")

        # Título de lista de esquemas
        self.schemaListLabel = QtWidgets.QLabel("Esquemas", self.schemaPanel)
        self.schemaListLabel.setGeometry(QtCore.QRect(20, 10, 100, 25))
        self.schemaListLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.schemaListLabel.setStyleSheet("color: black;")

        # Botón agregar esquema al inicio
        self.addSchemaButton = QtWidgets.QPushButton("Agregar Esquema", self.schemaPanel)
        self.addSchemaButton.setGeometry(QtCore.QRect(440, 10, 140, 30))  # Más espacio para el botón
        self.addSchemaButton.setStyleSheet("background-color: green; color: white; padding: 6px; border-radius: 4px;")
        self.addSchemaButton.clicked.connect(self.add_schema)

        # Lista de esquemas sin bordes
        self.schemaList = QtWidgets.QListWidget(self.schemaPanel)
        self.schemaList.setGeometry(QtCore.QRect(20, 50, 570, 180))  # Ajuste del ancho
        self.schemaList.setStyleSheet("""
            QListWidget::item {
                border: none;
                padding: 12px;
                background-color: white;
                height: 40px;
            }
            QListWidget::item:selected {
                background-color: lightgray;
                border: none;
            }
            QListWidget {
                outline: 0;
            }
        """)
        self.load_schemas()

        # Panel para Tablas
        self.tablePanel = QtWidgets.QWidget(Dialog)
        self.tablePanel.setGeometry(QtCore.QRect(20, 350, 610, 260))  # Panel más ancho
        self.tablePanel.setStyleSheet("background-color: white; border-radius: 8px;")

        # Título de lista de tablas
        self.tableListLabel = QtWidgets.QLabel("Tablas del Esquema", self.tablePanel)
        self.tableListLabel.setGeometry(QtCore.QRect(20, 10, 150, 25))
        self.tableListLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.tableListLabel.setStyleSheet("color: black;")

        # Botón agregar tabla al inicio
        self.addTableButton = QtWidgets.QPushButton("Agregar Tabla", self.tablePanel)
        self.addTableButton.setGeometry(QtCore.QRect(440, 10, 140, 30))  # Más espacio para el botón
        self.addTableButton.setStyleSheet("background-color: green; color: white; padding: 6px; border-radius: 4px;")
        self.addTableButton.clicked.connect(self.add_table)

        # Lista de tablas sin bordes
        self.tableList = QtWidgets.QListWidget(self.tablePanel)
        self.tableList.setGeometry(QtCore.QRect(20, 50, 570, 250))  # Ajuste del ancho
        self.tableList.setStyleSheet("""
            QListWidget::item {
                border: none;
                padding: 12px;
                background-color: white;
                height: 40px;
            }
            QListWidget::item:selected {
                background-color: lightgray;
                border: none;
            }
            QListWidget {
                outline: 0;
            }
        """)
        self.schemaList.currentItemChanged.connect(self.load_tables)

    def add_schema(self):
        schema_name, ok = QtWidgets.QInputDialog.getText(None, "Agregar Esquema", "Nombre del Esquema:")
        if ok and schema_name:
            if self.validate_input(schema_name):
                if schema_name not in self.schema_table_data:
                    self.schema_table_data[schema_name] = {}
                    self.save_schema_table_data()
                    self.load_schemas()
            else:
                QtWidgets.QMessageBox.warning(None, "Advertencia", "El nombre del esquema contiene caracteres no permitidos o palabras clave SQL.")

    def add_table(self):
        schema_name = self.schemaList.currentItem().text() if self.schemaList.currentItem() else None
        if not schema_name:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Seleccione un esquema primero.")
            return
        table_name, ok = QtWidgets.QInputDialog.getText(None, "Agregar Tabla", f"Nombre de la Tabla para {schema_name}:")
        if ok and table_name:
            if self.validate_input(table_name):
                # Inicializa la estructura de la nueva tabla con `clave` vacío y `campos` como lista vacía
                self.schema_table_data[schema_name][table_name] = {
                    "clave": "",
                    "campos": []
                }
                self.save_schema_table_data()
                self.load_tables()
            else:
                QtWidgets.QMessageBox.warning(None, "Advertencia", "El nombre de la tabla contiene caracteres no permitidos o palabras clave SQL.")


    def validate_input(self, input_value):
        """ Valida que el nombre de esquemas o tablas no contenga caracteres peligrosos ni palabras clave SQL """
        # No permitir caracteres peligrosos
        if re.search(r"[\"';]", input_value) or "--" in input_value:
            return False
        
        # No permitir palabras clave SQL
        if re.search(r"\b(SELECT|INSERT|DELETE|DROP|UPDATE|ALTER|EXEC)\b", input_value, re.IGNORECASE):
            return False
        
        # Limitar la longitud de los nombres
        if len(input_value) > 75:
            return False
        
        # Permitir solo letras, números, y guiones bajos
        if not re.match(r"^[a-zA-Z0-9_]+$", input_value):
            return False
        
        return True

    def delete_schema(self, schema_name):
        if schema_name and schema_name in self.schema_table_data:
            del self.schema_table_data[schema_name]
            self.save_schema_table_data()
            self.load_schemas()

    def delete_table(self, schema_name, table_name):
        if schema_name and table_name:
            del self.schema_table_data[schema_name][table_name]
            self.save_schema_table_data()
            self.load_tables()

    def view_table_data(self, schema_name, table_name):
        # Método para ver datos de una tabla
        QtWidgets.QMessageBox.information(None, "Ver Tabla", f"Datos de la tabla {table_name} del esquema {schema_name}")

    def modify_columns(self, schema_name, table_name):
        dialog = QtWidgets.QDialog()
        ui = Ui_TableColumnManagementDialog(schema_name, table_name, self.databaseController)  # Usamos el nuevo diálogo
        ui.setupUi(dialog)
        dialog.exec()

    def load_schemas(self):
        self.schemaList.clear()
        for schema in self.schema_table_data.keys():
            item = QtWidgets.QListWidgetItem(schema)
            widget = self.create_schema_widget(schema)
            self.schemaList.addItem(item)
            self.schemaList.setItemWidget(item, widget)

    def create_schema_widget(self, schema_name):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()

        # Etiqueta con el nombre del esquema
        schemaLabel = QtWidgets.QLabel(schema_name)
        schemaLabel.setStyleSheet("color: black;")

        # Botón de eliminar esquema (solo para nuevos)
        deleteButton = QtWidgets.QPushButton("Eliminar")
        deleteButton.setFont(QtGui.QFont("Segoe UI", 12))
        deleteButton.setStyleSheet("background-color: red; color: white; padding: 6px; border-radius: 4px;")
        if schema_name in self.protected_schemas:
            deleteButton.setEnabled(False)
            deleteButton.setStyleSheet("background-color: gray; color: white; padding: 6px; border-radius: 4px;")

        deleteButton.clicked.connect(lambda: self.delete_schema(schema_name))

        layout.addWidget(schemaLabel)
        layout.addWidget(deleteButton)
        layout.setContentsMargins(5, 5, 5, 5)  # Márgenes ajustados
        layout.setSpacing(20)  # Espaciado entre los elementos

        widget.setLayout(layout)
        widget.setFixedHeight(40)
        return widget

    def load_tables(self):
        self.tableList.clear()
        schema_name = self.schemaList.currentItem().text() if self.schemaList.currentItem() else None
        if schema_name and schema_name in self.schema_table_data:
            for table in self.schema_table_data[schema_name]:
                item = QtWidgets.QListWidgetItem(table)
                widget = self.create_table_widget(schema_name, table)
                self.tableList.addItem(item)
                self.tableList.setItemWidget(item, widget)

    def create_table_widget(self, schema_name, table_name):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()

        # Etiqueta con el nombre de la tabla
        tableLabel = QtWidgets.QLabel(table_name)
        tableLabel.setStyleSheet("color: black;")

        modifyButton = QtWidgets.QPushButton("Modificar Columnas")
        modifyButton.setFont(QtGui.QFont("Segoe UI", 10))
        modifyButton.setStyleSheet("background-color: green; color: white; padding: 6px; border-radius: 4px;")
        modifyButton.clicked.connect(lambda: self.modify_columns(schema_name, table_name))

        # Nuevo botón para "Definir Indicador"
        defineIndicatorButton = QtWidgets.QPushButton("Definir Indicador")
        defineIndicatorButton.setFont(QtGui.QFont("Segoe UI", 10))
        defineIndicatorButton.setStyleSheet("background-color: blue; color: white; padding: 6px; border-radius: 4px;")
        defineIndicatorButton.clicked.connect(lambda: self.define_indicator(schema_name, table_name))

        # Botón de eliminar tabla
        deleteButton = QtWidgets.QPushButton("Eliminar")
        deleteButton.setFont(QtGui.QFont("Segoe UI", 12))
        deleteButton.setStyleSheet("background-color: red; color: white; padding: 6px; border-radius: 4px;")
        if schema_name in self.protected_tables and table_name in self.protected_tables[schema_name]:
            deleteButton.setEnabled(False)
            deleteButton.setStyleSheet("background-color: gray; color: white; padding: 6px; border-radius: 4px;")

        deleteButton.clicked.connect(lambda: self.delete_table(schema_name, table_name))

        layout.addWidget(tableLabel)
        layout.addWidget(modifyButton)
        layout.addWidget(defineIndicatorButton)  # Agregar el nuevo botón al layout
        layout.addWidget(deleteButton)
        layout.setContentsMargins(5, 5, 5, 5)  
        layout.setSpacing(20) 

        widget.setLayout(layout)
        widget.setFixedHeight(40)
        return widget


    def define_indicator(self, schema_name, table_name):
        dialog = QtWidgets.QDialog()
        ui = Ui_TableIndexSelectionDialog(schema_name, table_name, self.databaseController)  # Crea una instancia del nuevo diálogo
        ui.setupUi(dialog)
        dialog.exec()

    def save_schema_table_data(self):
        with open(self.databaseController.database_management_path, "w") as file:
            json.dump(self.schema_table_data, file, indent=4)
