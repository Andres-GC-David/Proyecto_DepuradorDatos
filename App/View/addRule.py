from PyQt6 import QtWidgets, QtCore, QtGui
from App.Controller.addRuleController import RuleConfigurationController
from App.Controller.databaseController import DatabaseController
import re

class AddRule(object):
    def __init__(self):
        self.controller = RuleConfigurationController()
        self.database_controller = DatabaseController()

    def setupUi(self, Dialog):
        Dialog.setObjectName("RuleConfigurationDialog")
        Dialog.resize(620, 520)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")
        Dialog.setWindowTitle("Configuración de Reglas de Negocio")
        
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.titleLabel = QtWidgets.QLabel("Nueva Regla de Negocio", Dialog)
        self.titleLabel.setFont(QtGui.QFont("Segoe UI", 15, QtGui.QFont.Weight.Bold))
        self.titleLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.titleLabel)
        
        self.loadExampleButton = QtWidgets.QPushButton(Dialog)
        self.loadExampleButton.setGeometry(QtCore.QRect(10, 10, 140, 30))  # Arriba a la izquierda
        self.loadExampleButton.setText("Cargar Ejemplo")
        self.loadExampleButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.loadExampleButton.setStyleSheet("background-color: white; color: black; border-radius: 5px;")
        self.loadExampleButton.clicked.connect(self.load_example)  # Conectar el botón a la función para cargar el ejemplo
        
        # Help button in the top-right corner
        self.helpButton = QtWidgets.QPushButton(Dialog)
        self.helpButton.setGeometry(QtCore.QRect(580, 10, 30, 30))
        self.helpButton.setText("?")
        self.helpButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.helpButton.setStyleSheet("background-color: white; color: black; border-radius: 15px;")
        self.helpButton.clicked.connect(self.show_help_modal)

        self.nameLabel = QtWidgets.QLabel("Nombre de la Regla:", Dialog)
        self.nameLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.nameLabel.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.nameLabel)

        self.nameInput = QtWidgets.QLineEdit(Dialog)
        self.nameInput.setFont(QtGui.QFont("Segoe UI", 12))
        self.nameInput.setStyleSheet("background-color: white; color: black;")
        self.main_layout.addWidget(self.nameInput)
        self.nameInput.textChanged.connect(self.validate_rule_name) 

        self.descriptionLabel = QtWidgets.QLabel("Descripción de la Regla:", Dialog)
        self.descriptionLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.descriptionLabel.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.descriptionLabel)

        self.descriptionInput = QtWidgets.QTextEdit(Dialog)
        self.descriptionInput.setFont(QtGui.QFont("Segoe UI", 12))
        self.descriptionInput.setStyleSheet("background-color: white; color: black;")
        self.main_layout.addWidget(self.descriptionInput)
        self.descriptionInput.textChanged.connect(self.validate_description)

        self.codeLabel = QtWidgets.QLabel("Código de la Regla:", Dialog)
        self.codeLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.codeLabel.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.codeLabel)

        self.codeInput = QtWidgets.QTextEdit(Dialog)
        self.codeInput.setFont(QtGui.QFont("Segoe UI", 12))
        self.codeInput.setStyleSheet("background-color: white; color: black;")
        self.main_layout.addWidget(self.codeInput)
        self.codeInput.textChanged.connect(self.validate_code)

        self.fileTypeLabel = QtWidgets.QLabel("A qué tipo de archivos se puede aplicar:", Dialog)
        self.fileTypeLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.fileTypeLabel.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.fileTypeLabel)

        self.fileTypeOptions = QtWidgets.QHBoxLayout()

        self.csvCheckbox = QtWidgets.QCheckBox("CSV", Dialog)
        self.csvCheckbox.setFont(QtGui.QFont("Segoe UI", 12))
        self.csvCheckbox.setStyleSheet("color: white;")
        self.fileTypeOptions.addWidget(self.csvCheckbox)

        self.xlsxCheckbox = QtWidgets.QCheckBox("XLSX", Dialog)
        self.xlsxCheckbox.setFont(QtGui.QFont("Segoe UI", 12))
        self.xlsxCheckbox.setStyleSheet("color: white;")
        self.fileTypeOptions.addWidget(self.xlsxCheckbox)

        self.txtCheckbox = QtWidgets.QCheckBox("TXT", Dialog)
        self.txtCheckbox.setFont(QtGui.QFont("Segoe UI", 12))
        self.txtCheckbox.setStyleSheet("color: white;")
        self.fileTypeOptions.addWidget(self.txtCheckbox)

        self.main_layout.addLayout(self.fileTypeOptions)

        self.tableTypeLabel = QtWidgets.QLabel("Si son tablas, seleccione a cuáles se puede aplicar:", Dialog)
        self.tableTypeLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.tableTypeLabel.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.tableTypeLabel)

        self.tableSelection = QtWidgets.QListWidget(Dialog)
        self.tableSelection.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.tableSelection.setFont(QtGui.QFont("Segoe UI", 12))
        self.tableSelection.setStyleSheet("background-color: white; color: black;")
        self.main_layout.addWidget(self.tableSelection)

        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.saveButton = QtWidgets.QPushButton("Guardar", Dialog)
        self.saveButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.saveButton.setStyleSheet("background-color: white; color: black;")
        self.saveButton.clicked.connect(self.save_rule)
        self.buttonLayout.addWidget(self.saveButton)

        self.cancelButton = QtWidgets.QPushButton("Cancelar", Dialog)
        self.cancelButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.cancelButton.setStyleSheet("background-color: red; color: white;")
        self.cancelButton.clicked.connect(Dialog.reject)
        self.buttonLayout.addWidget(self.cancelButton)

        self.main_layout.addLayout(self.buttonLayout)
        self.load_tables()

    def show_help_modal(self):
        help_dialog = QtWidgets.QDialog()
        help_dialog.setWindowTitle("Ayuda para Agregar Reglas")
        help_dialog.resize(600, 400)
        help_dialog.setStyleSheet("background-color: rgb(255, 255, 255);")

        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea(help_dialog)
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the content
        content_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(content_widget)

        # Help label with the content
        help_label = QtWidgets.QLabel(content_widget)
        help_label.setText(self.get_help_text())
        help_label.setFont(QtGui.QFont("Segoe UI", 10))
        help_label.setStyleSheet("color: black;")
        help_label.setWordWrap(True)
        help_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        layout.addWidget(help_label)
        content_widget.setLayout(layout)

        scroll_area.setWidget(content_widget)

        modal_layout = QtWidgets.QVBoxLayout(help_dialog)
        modal_layout.addWidget(scroll_area)

        help_dialog.exec()

    def get_help_text(self):
        return (
            "<h2>Estructura del Código de las Reglas</h2>"
            "<p>Cada regla que creas tiene como propósito modificar o validar los datos de una columna específica en una tabla o archivo. "
            "El código que escribes se encarga de realizar esa modificación o validación, y sigue una estructura sencilla que te explico a continuación:</p>"
            "<h3>1. Qué es una columna y cómo se trabaja con ella</h3>"
            "<p>Piensa en una columna como una lista de datos que quieres cambiar o revisar. Por ejemplo, si tienes una columna con números de teléfono, "
            "puedes escribir una regla para asegurarte de que todos los números tengan un formato correcto o eliminar caracteres que no deberían estar ahí.</p>"
            "<h3>2. Estructura básica del código</h3>"
            "<p>El código de una regla sigue esta estructura básica:</p>"
            "<ul>"
            "<li>Accedemos a los datos de la columna y aplicamos una acción a cada valor (como un filtro o modificación).</li>"
            "<li>Usamos una función especial (apply) para hacer esto. Esta función se encarga de revisar cada valor uno por uno y aplicar las instrucciones que le damos.</li>"
            "</ul>"
            "<h3>Ejemplo básico:</h3>"
            "<pre>data[column] = data[column].apply(lambda x: x if &lt;condición&gt; else &lt;resultado&gt;)</pre>"
            "<p><strong>Qué significa esto:</strong></p>"
            "<ul>"
            "<li><strong>data[column]:</strong> Esto representa la columna en la que quieres trabajar.</li>"
            "<li><strong>apply:</strong> Le estamos diciendo al sistema que revise cada valor en esa columna.</li>"
            "<li><strong>lambda x:</strong> Esta parte define la acción que queremos aplicar. x es cada valor de la columna.</li>"
            "<li><strong>&lt;condición&gt;:</strong> Aquí defines lo que quieres revisar o modificar en los valores.</li>"
            "<li><strong>&lt;resultado&gt;:</strong> Este es el valor que le damos a x si no cumple la condición.</li>"
            "</ul>"
            "<h3>3. Qué puedes hacer con el código</h3>"
            "<p>Aquí te doy algunos ejemplos de lo que puedes hacer con las reglas:</p>"
            "<h4>Ejemplo 1: Validar correos electrónicos</h4>"
            "<pre>data[column] = data[column].apply(lambda x: x if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$', str(x)) else 'Correo inválido')</pre>"
            "<p><strong>Qué hace:</strong> Revisa si el correo tiene un formato válido. Si no lo tiene, reemplaza el valor por 'Correo inválido'.</p>"
            "<h4>Ejemplo 2: Eliminar guiones de un número de teléfono</h4>"
            "<pre>data[column] = data[column].apply(lambda x: ''.join(filter(str.isdigit, str(x))) if pd.notnull(x) else x)</pre>"
            "<p><strong>Qué hace:</strong> Quita todos los caracteres que no son números y deja solo los dígitos.</p>"
            "<h4>Ejemplo 3: Reemplazar valores nulos (vacíos) por un valor predeterminado</h4>"
            "<pre>data[column] = data[column].fillna('Desconocido')</pre>"
            "<p><strong>Qué hace:</strong> Reemplaza los valores vacíos o nulos en la columna por la palabra 'Desconocido'.</p>"
            "<h3>4. Cómo escribir tus propias reglas</h3>"
            "<p>Cuando escribas el código de una regla, asegúrate de seguir estas reglas básicas:</p>"
            "<ul>"
            "<li>Accede siempre a la columna que quieres modificar usando <em>data[column]</em>.</li>"
            "<li>Usa <em>apply</em> para aplicar una acción a cada valor de la columna.</li>"
            "<li>Define una condición (lo que quieres revisar) y un resultado (qué hacer si el valor no cumple la condición).</li>"
            "<li>Maneja los valores vacíos o nulos con cuidado para evitar errores inesperados.</li>"
            "</ul>"
        )

    def save_rule(self):
        rule_name = self.nameInput.text()
        description = self.descriptionInput.toPlainText()
        code = self.codeInput.toPlainText()

        file_types = []
        if self.csvCheckbox.isChecked():
            file_types.append("CSV")
        if self.xlsxCheckbox.isChecked():
            file_types.append("XLSX")
        if self.txtCheckbox.isChecked():
            file_types.append("TXT")

        selected_tables = [item.text() for item in self.tableSelection.selectedItems()]

        if not rule_name or not description or not code:
            QtWidgets.QMessageBox.warning(None, "Error", "Todos los campos son obligatorios.")
            return

        self.controller.save_rule(rule_name, description, code, file_types, selected_tables)
        QtWidgets.QApplication.activeWindow().close()
        
    def load_example(self):
        """ Carga un ejemplo predefinido en los campos de la interfaz """
        example_name = "Valida Correos"
        example_description = "Convierte a nulo correos que no cumplen validación de sintaxis"
        example_code = ("data[column] = data[column].apply(lambda x: x if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$', str(x))"
                        " else 'Correo invalido')")

        self.nameInput.setText(example_name)
        self.descriptionInput.setPlainText(example_description)
        self.codeInput.setPlainText(example_code)
        
    def validate_rule_name(self):
        """ Valida que el nombre de la regla no contenga caracteres peligrosos ni palabras reservadas de SQL. """
        rule_name = self.nameInput.text()

        # No permitir caracteres peligrosos
        if re.search(r"[\"';]", rule_name) or "--" in rule_name:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "El nombre de la regla contiene caracteres no permitidos.")
            self.nameInput.clear()

        # No permitir palabras clave SQL
        if re.search(r"\b(SELECT|INSERT|DELETE|DROP|UPDATE|ALTER)\b", rule_name, re.IGNORECASE):
            QtWidgets.QMessageBox.warning(None, "Advertencia", "El nombre de la regla contiene palabras clave SQL no permitidas.")
            self.nameInput.clear()

        # Limitar la longitud del nombre de la regla
        if len(rule_name) > 50:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "El nombre de la regla es demasiado largo (máximo 50 caracteres).")
            self.nameInput.clear()


    # Validar descripción de la regla
    def validate_description(self):
        """ Valida que la descripción no contenga caracteres peligrosos ni palabras reservadas de SQL. """
        description = self.descriptionInput.toPlainText()

        # No permitir caracteres peligrosos
        if re.search(r"[\"';]", description) or "--" in description:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "La descripción contiene caracteres no permitidos.")
            self.descriptionInput.clear()

        # Limitar la longitud de la descripción
        if len(description) > 500:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "La descripción es demasiado larga (máximo 500 caracteres).")
            self.descriptionInput.clear()

    # Validar código de la regla
    def validate_code(self):
        """ Valida que el código de la regla no contenga caracteres peligrosos ni palabras reservadas de SQL. """
        code = self.codeInput.toPlainText()
        
        if len(code) > 10000:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "El código es demasiado largo (máximo 1000 caracteres).")
            self.codeInput.clear()

    def load_tables(self):
        databases = self.database_controller.get_databases()
        
        for db_name in databases:
            tables = self.database_controller.get_tables(db_name)
            for table_name in tables:
                self.tableSelection.addItem(table_name)


