from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.ruleActionController import RuleActionController
import re

class Ui_RuleActionDialog(object):

    def __init__(self):
        self.controller = RuleActionController()

    def setupUi(self, Dialog, rule_name):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 700)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        # Título principal
        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(50, 20, 500, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(13)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("color: white;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setText(f"Configuración de Regla: {rule_name}")

        # Configuración de opciones
        self.setup_phone_options(Dialog)
        self.setup_null_options(Dialog)
        self.setup_format_options(Dialog)

        # Botón Aceptar
        self.acceptButton = QtWidgets.QPushButton("Aceptar", Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(250, 630, 100, 40))
        self.acceptButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.acceptButton.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        self.acceptButton.clicked.connect(lambda: self.on_accept(Dialog))

    def setup_phone_options(self, Dialog):
        # Contenedor de opciones de teléfono
        self.phoneOptionsContainer = QtWidgets.QFrame(Dialog)
        self.phoneOptionsContainer.setGeometry(QtCore.QRect(50, 80, 500, 120))
        self.phoneOptionsContainer.setStyleSheet("""
            background-color: white; 
            border-radius: 10px; 
            border: 1px solid white;
            padding: 10px;
        """)
        self.phoneOptionsContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        # Etiqueta de descripción para opciones de teléfono
        self.phoneOptionsLabel = QtWidgets.QLabel("Opciones de validación de número de teléfono", parent=self.phoneOptionsContainer)
        self.phoneOptionsLabel.setGeometry(QtCore.QRect(10, 10, 480, 38))
        self.phoneOptionsLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.phoneOptionsLabel.setStyleSheet("color: black;")

        # Opción para verificar longitud de teléfono
        self.checkPhoneLengthBox = QtWidgets.QCheckBox("Verificar longitud del número", self.phoneOptionsContainer)
        self.checkPhoneLengthBox.setGeometry(QtCore.QRect(20, 50, 250, 35))
        self.checkPhoneLengthBox.setStyleSheet("color: black;")

        # Input para ingresar la longitud
        self.phoneLengthLabel = QtWidgets.QLabel("Longitud esperada:", self.phoneOptionsContainer)
        self.phoneLengthLabel.setGeometry(QtCore.QRect(240, 50, 150, 35))
        self.phoneLengthLabel.setStyleSheet("color: black;")
        self.phoneLengthLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.phoneLengthInput = QtWidgets.QLineEdit(self.phoneOptionsContainer)
        self.phoneLengthInput.setGeometry(QtCore.QRect(380, 50, 80, 35))
        self.phoneLengthInput.setStyleSheet("background-color: white; color: black; border: 1px solid #BBBBBB; border-radius: 5px;")
        self.phoneLengthInput.setValidator(QtGui.QIntValidator(1, 15))  # Solo números, longitud máxima de un número de teléfono
        self.phoneLengthInput.setEnabled(False)

        self.checkPhoneLengthBox.stateChanged.connect(self.toggle_phone_length_input)

    def setup_null_options(self, Dialog):
        # Contenedor de opciones de conversión a nulo
        self.nullOptionsContainer = QtWidgets.QFrame(Dialog)
        self.nullOptionsContainer.setGeometry(QtCore.QRect(50, 230, 500, 220))
        self.nullOptionsContainer.setStyleSheet("""
            background-color: white; 
            border-radius: 10px; 
            border: 1px solid white;
            padding: 10px;
        """)
        self.nullOptionsContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        # Etiqueta para opciones de nulo
        self.nullOptionsLabel = QtWidgets.QLabel("Opciones para convertir a nulo o reemplazar", parent=self.nullOptionsContainer)
        self.nullOptionsLabel.setGeometry(QtCore.QRect(10, 10, 480, 38))
        self.nullOptionsLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.nullOptionsLabel.setStyleSheet("color: black;")

        self.nullButtonGroup = QtWidgets.QButtonGroup(self.nullOptionsContainer)

        # Opción para convertir 0 o 00 a nulo
        self.convertZeroRadio = QtWidgets.QRadioButton("Convertir teléfonos con 0 o 00 a nulo", self.nullOptionsContainer)
        self.convertZeroRadio.setGeometry(QtCore.QRect(20, 50, 250, 35))
        self.convertZeroRadio.setStyleSheet("color: black;")
        self.nullButtonGroup.addButton(self.convertZeroRadio)

        # Opción para convertir a nulo si coincide con valor personalizado
        self.customNullRadio = QtWidgets.QRadioButton("Convertir si coincide con valor personalizado", self.nullOptionsContainer)
        self.customNullRadio.setGeometry(QtCore.QRect(20, 90, 300, 35))
        self.customNullRadio.setStyleSheet("color: black;")
        self.nullButtonGroup.addButton(self.customNullRadio)

        # Input para valor personalizado
        self.customNullLabel = QtWidgets.QLabel("Convertir a:", self.nullOptionsContainer)
        self.customNullLabel.setGeometry(QtCore.QRect(25, 130, 150, 35))
        self.customNullLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.customNullLabel.setStyleSheet("color: black;")

        self.customNullInput = QtWidgets.QLineEdit(self.nullOptionsContainer)
        self.customNullInput.setGeometry(QtCore.QRect(350, 90, 100, 35))
        self.customNullInput.setStyleSheet("background-color: white; color: black; border: 1px solid #BBBBBB; border-radius: 5px;")
        self.customNullInput.setEnabled(False)

        # Validar el valor personalizado
        self.customNullInput.textChanged.connect(self.validate_custom_null_value)

        # Opción para convertir a nulo o reemplazar
        self.nullOrReplaceBox = QtWidgets.QComboBox(self.nullOptionsContainer)
        self.nullOrReplaceBox.setGeometry(QtCore.QRect(190, 130, 150, 35))
        self.nullOrReplaceBox.setStyleSheet("background-color: white; color: black; border: 1px solid #BBBBBB; border-radius: 5px;")
        self.nullOrReplaceBox.addItems(["Convertir a nulo", "Reemplazar con valor personalizado"])
        self.nullOrReplaceBox.setEnabled(False)

        # Input para valor de reemplazo
        self.replaceValueLabel = QtWidgets.QLabel("Valor de reemplazo:", self.nullOptionsContainer)
        self.replaceValueLabel.setGeometry(QtCore.QRect(25, 170, 150, 35))
        self.replaceValueLabel.setStyleSheet("color: black;")
        self.replaceValueLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.replaceValueInput = QtWidgets.QLineEdit(self.nullOptionsContainer)
        self.replaceValueInput.setGeometry(QtCore.QRect(190, 170, 100, 35))
        self.replaceValueInput.setStyleSheet("background-color: white; color: black; border: 1px solid #BBBBBB; border-radius: 5px;")
        self.replaceValueInput.setEnabled(False)

        # Validar el valor de reemplazo
        self.replaceValueInput.textChanged.connect(self.validate_replace_value)

        self.customNullRadio.toggled.connect(self.toggle_custom_null_options)
        self.nullOrReplaceBox.currentIndexChanged.connect(self.toggle_replace_value_input)

    def setup_format_options(self, Dialog):
        # Contenedor de opciones de formato
        self.formatOptionsContainer = QtWidgets.QFrame(Dialog)
        self.formatOptionsContainer.setGeometry(QtCore.QRect(50, 460, 500, 150))
        self.formatOptionsContainer.setStyleSheet("""
            background-color: white; 
            border-radius: 10px; 
            border: 1px solid white;
            padding: 10px;
        """)
        self.formatOptionsContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        # Etiqueta para opciones de formato
        self.formatOptionsLabel = QtWidgets.QLabel("Opciones para formato de teléfono", parent=self.formatOptionsContainer)
        self.formatOptionsLabel.setGeometry(QtCore.QRect(10, 10, 480, 38))
        self.formatOptionsLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.formatOptionsLabel.setStyleSheet("color: black;")

        # Opción para aplicar formato
        self.applyFormatCheckBox = QtWidgets.QCheckBox("Aplicar cambio de formato", self.formatOptionsContainer)
        self.applyFormatCheckBox.setGeometry(QtCore.QRect(20, 50, 220, 35))
        self.applyFormatCheckBox.setStyleSheet("color: black;")

        # Opciones de formato
        self.formatComboBox = QtWidgets.QComboBox(self.formatOptionsContainer)
        self.formatComboBox.setGeometry(QtCore.QRect(250, 50, 200, 35))
        self.formatComboBox.setStyleSheet("background-color: white; color: black; border: 1px solid #BBBBBB; border-radius: 5px;")
        self.formatComboBox.addItems(["Sin separadores", "Formato personalizado"])
        self.formatComboBox.setEnabled(False)

        # Input para formato personalizado
        self.customFormatLabel = QtWidgets.QLabel("Formato personalizado:", self.formatOptionsContainer)
        self.customFormatLabel.setGeometry(QtCore.QRect(20, 90, 200, 35))
        self.customFormatLabel.setStyleSheet("color: black;")

        self.customFormatInput = QtWidgets.QLineEdit(self.formatOptionsContainer)
        self.customFormatInput.setGeometry(QtCore.QRect(250, 90, 200, 35))
        self.customFormatInput.setToolTip("Ejemplo: ####-####")
        self.customFormatInput.setStyleSheet("background-color: white; color: black; border: 1px solid #BBBBBB; border-radius: 5px;")
        self.customFormatInput.setEnabled(False)

        # Validar formato personalizado
        self.customFormatInput.textChanged.connect(self.validate_custom_format)

        self.applyFormatCheckBox.stateChanged.connect(self.toggle_format_options)
        self.formatComboBox.currentIndexChanged.connect(self.toggle_custom_format_input)

    # Métodos para validaciones y activación de inputs
    def toggle_phone_length_input(self):
        self.phoneLengthInput.setEnabled(self.checkPhoneLengthBox.isChecked())

    def toggle_custom_null_options(self):
        is_checked = self.customNullRadio.isChecked()
        self.customNullInput.setEnabled(is_checked)
        self.nullOrReplaceBox.setEnabled(is_checked)

    def toggle_replace_value_input(self):
        self.replaceValueInput.setEnabled(self.nullOrReplaceBox.currentText() == "Reemplazar con valor personalizado")

    def toggle_format_options(self):
        is_checked = self.applyFormatCheckBox.isChecked()
        self.formatComboBox.setEnabled(is_checked)
        self.customFormatInput.setEnabled(is_checked and self.formatComboBox.currentText() == "Formato personalizado")

    def toggle_custom_format_input(self):
        is_custom_format = self.formatComboBox.currentText() == "Formato personalizado"
        self.customFormatInput.setEnabled(is_custom_format)

    # Validaciones adicionales
    def validate_custom_null_value(self):
        value = self.customNullInput.text()
        if re.search(r"[\"';]", value):
            self.customNullInput.clear()

    def validate_replace_value(self):
        value = self.replaceValueInput.text()
        if re.search(r"[\"';]", value):
            self.replaceValueInput.clear()

    def validate_custom_format(self):
        format_value = self.customFormatInput.text()
        if not re.match(r"^[#\-]+$", format_value):
            self.customFormatInput.clear()


    def on_accept(self, dialog):
        if self.checkPhoneLengthBox.isChecked() and not self.phoneLengthInput.text():
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Debe ingresar una longitud válida para el teléfono.")
            return

        self.controller.set_phone_length_validation(self.checkPhoneLengthBox.isChecked(), self.phoneLengthInput.text())
        self.controller.set_convert_zero_to_null(self.convertZeroRadio.isChecked())
        self.controller.set_custom_null_value(self.customNullRadio.isChecked(), self.customNullInput.text())
        self.controller.set_null_or_replace(self.nullOrReplaceBox.currentText(), self.replaceValueInput.text())
        self.controller.set_phone_format(self.applyFormatCheckBox.isChecked(), self.formatComboBox.currentText(), self.customFormatInput.text())

        self.controller.accept()
        dialog.accept()

    def get_accepted(self):
        return self.controller.is_accepted()

    def get_description(self):
        description = self.controller.generate_description()
        return description