from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.ruleActionEmailController import RuleActionEmailController
import re

class Ui_RuleActionEmailDialog(object):

    def __init__(self):
        self.controller = RuleActionEmailController()

    def setupUi(self, Dialog, rule_name):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 460)  # Aumentamos el tamaño para hacer espacio al input
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(20, 20, 450, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("color: white;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setText(f"Configuración de Regla: {rule_name}")

        self.emailOptionsContainer = QtWidgets.QFrame(Dialog)
        self.emailOptionsContainer.setGeometry(QtCore.QRect(50, 80, 400, 310))
        self.emailOptionsContainer.setStyleSheet("background-color: white; border-radius: 10px;")
        self.emailOptionsContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        self.emailOptionsLabel = QtWidgets.QLabel("Opciones para correos electrónicos", parent=self.emailOptionsContainer)
        self.emailOptionsLabel.setGeometry(QtCore.QRect(20, 10, 400, 30))
        self.emailOptionsLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.emailOptionsLabel.setStyleSheet("color: black;")

        self.validateEmailBox = QtWidgets.QCheckBox("Validar formato de correo", self.emailOptionsContainer)
        self.validateEmailBox.setGeometry(QtCore.QRect(20, 50, 250, 30))
        self.validateEmailBox.setStyleSheet("color: black;")

        # Campo de entrada para el valor que se usará si el correo no es válido
        self.invalidEmailValueInput = QtWidgets.QLineEdit(self.emailOptionsContainer)
        self.invalidEmailValueInput.setGeometry(QtCore.QRect(250, 50, 130, 30))
        self.invalidEmailValueInput.setPlaceholderText("Valor para inválido")
        self.invalidEmailValueInput.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.invalidEmailValueInput.setEnabled(False)  # Inicialmente deshabilitado

        self.convertToLowercaseBox = QtWidgets.QCheckBox("Convertir correos a minúsculas", self.emailOptionsContainer)
        self.convertToLowercaseBox.setGeometry(QtCore.QRect(20, 80, 250, 30))
        self.convertToLowercaseBox.setStyleSheet("color: black;")

        self.validateDomainBox = QtWidgets.QCheckBox("Validar dominios permitidos", self.emailOptionsContainer)
        self.validateDomainBox.setGeometry(QtCore.QRect(20, 110, 250, 30))
        self.validateDomainBox.setStyleSheet("color: black;")

        self.allowedDomainInput = QtWidgets.QLineEdit(self.emailOptionsContainer)
        self.allowedDomainInput.setGeometry(QtCore.QRect(20, 140, 200, 30))
        self.allowedDomainInput.setPlaceholderText("Dominios permitidos ejm:@example.com")
        self.allowedDomainInput.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.allowedDomainInput.setEnabled(False)

        self.separatorLabel = QtWidgets.QLabel("Opciones de separadores", parent=self.emailOptionsContainer)
        self.separatorLabel.setGeometry(QtCore.QRect(20, 180, 200, 30))
        self.separatorLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.separatorLabel.setStyleSheet("color: black;")

        self.validateSeparatorBox = QtWidgets.QCheckBox("Validar separadores de correos", self.emailOptionsContainer)
        self.validateSeparatorBox.setGeometry(QtCore.QRect(20, 210, 250, 30))
        self.validateSeparatorBox.setStyleSheet("color: black;")

        self.separatorComboBox = QtWidgets.QComboBox(self.emailOptionsContainer)
        self.separatorComboBox.setGeometry(QtCore.QRect(20, 240, 200, 30))
        self.separatorComboBox.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.separatorComboBox.addItems([
            "Separadores por coma ( , )",
            "Separadores por barra ( / )",
            "Separadores por punto y coma ( ; )",
            "Separador personalizado"
        ])

        self.customSeparatorInput = QtWidgets.QLineEdit(self.emailOptionsContainer)
        self.customSeparatorInput.setGeometry(QtCore.QRect(230, 240, 150, 30))
        self.customSeparatorInput.setPlaceholderText("Ingrese separador")
        self.customSeparatorInput.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.customSeparatorInput.setEnabled(False)

        self.validateDomainBox.stateChanged.connect(self.toggle_domain_input)
        self.validateSeparatorBox.stateChanged.connect(self.toggle_separator_input)
        self.separatorComboBox.currentIndexChanged.connect(self.toggle_custom_separator)
        self.validateEmailBox.stateChanged.connect(self.toggle_invalid_email_input)

        # Conectar validaciones
        self.invalidEmailValueInput.textChanged.connect(self.validate_invalid_email_input)
        self.allowedDomainInput.textChanged.connect(self.validate_allowed_domains)
        self.customSeparatorInput.textChanged.connect(self.validate_custom_separator)

        self.acceptButton = QtWidgets.QPushButton("Aceptar", Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(200, 400, 100, 30))
        self.acceptButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.acceptButton.setStyleSheet("background-color: white; color: black; border-radius: 10px;")
        self.acceptButton.clicked.connect(lambda: self.on_accept(Dialog))

    # Validaciones de los campos
    def validate_invalid_email_input(self):
        value = self.invalidEmailValueInput.text()
        if re.search(r"[\"';]", value):
            self.invalidEmailValueInput.clear()

    def validate_allowed_domains(self):
        domains = self.allowedDomainInput.text()
        if re.search(r"[\"';]", domains):
            self.allowedDomainInput.clear()

    def validate_custom_separator(self):
        separator = self.customSeparatorInput.text()
        if re.search(r"[\"';]", separator):  # No permitir comillas ni punto y coma
            self.customSeparatorInput.clear()

    def toggle_invalid_email_input(self):
        self.invalidEmailValueInput.setEnabled(self.validateEmailBox.isChecked())

    def get_description(self):
        description = self.controller.generate_description()
        return description

    def toggle_domain_input(self):
        self.allowedDomainInput.setEnabled(self.validateDomainBox.isChecked())

    def toggle_separator_input(self):
        is_checked = self.validateSeparatorBox.isChecked()
        self.separatorComboBox.setEnabled(is_checked)
        self.customSeparatorInput.setEnabled(is_checked and self.separatorComboBox.currentText() == "Separador personalizado")

    def toggle_custom_separator(self):
        self.customSeparatorInput.setEnabled(self.separatorComboBox.currentText() == "Separador personalizado")

    def on_accept(self, dialog):

        # Actualizar el controlador con las opciones seleccionadas
        self.controller.set_validate_email_format(self.validateEmailBox.isChecked())
        self.controller.set_convert_to_lowercase(self.convertToLowercaseBox.isChecked())
        self.controller.set_validate_domain(self.validateDomainBox.isChecked())
        self.controller.set_allowed_domains(self.allowedDomainInput.text())
        self.controller.set_validate_separator(self.validateSeparatorBox.isChecked())
        self.controller.set_selected_separator(self.separatorComboBox.currentText())
        self.controller.set_custom_separator(self.customSeparatorInput.text())
        self.controller.set_invalid_email_value(self.invalidEmailValueInput.text() or None)  # Si está vacío, será None (nulo)

        # Guardar y aceptar
        self.controller.accept()
        dialog.accept()

    def on_reject(self):
        self.controller.reject()

    def get_accepted(self):
        return self.controller.is_accepted()
