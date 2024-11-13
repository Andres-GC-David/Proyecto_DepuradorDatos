from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.ruleActionCedulaController import RuleActionCedulaController

class Ui_RuleActionCedulaDialog(object):

    def __init__(self):
        self.controller = RuleActionCedulaController()

    def setupUi(self, Dialog, rule_name):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 500)  
        Dialog.setStyleSheet("background-color: rgb(58, 99, 140);")

        self._create_title(Dialog, rule_name)
        self._create_cedula_options(Dialog)
        self._create_format_validation_section(Dialog)
        self._create_accept_button(Dialog)

        self.validateFormatBox.toggled.connect(self.toggle_format_input)
        self.applyFormatBox.toggled.connect(self.toggle_apply_format_input)

    def _create_title(self, Dialog, rule_name):
        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(30, 20, 450, 40))
        font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("color: white;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setText(f"Configuración de Regla: {rule_name}")

    def _create_cedula_options(self, Dialog):
        self.cedulaOptionsContainer = QtWidgets.QFrame(Dialog)
        self.cedulaOptionsContainer.setGeometry(QtCore.QRect(50, 80, 400, 140))
        self.cedulaOptionsContainer.setStyleSheet("background-color: white; border-radius: 10px;")
        self.cedulaOptionsContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        self.cedulaOptionsLabel = QtWidgets.QLabel("Opciones para la cédula", parent=self.cedulaOptionsContainer)
        self.cedulaOptionsLabel.setGeometry(QtCore.QRect(20, 10, 400, 30))
        self.cedulaOptionsLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.cedulaOptionsLabel.setStyleSheet("color: black;")

        self.radioButtonGroup = QtWidgets.QButtonGroup()

        self.removeHyphenBox = self._add_cedula_option(self.cedulaOptionsContainer, "Eliminar separador '-'", 50, "Quita el guion de las cédulas.", self.radioButtonGroup)
        self.removeZeroBox = self._add_cedula_option(self.cedulaOptionsContainer, "Eliminar separador '0'", 80, "Elimina los ceros que se usan como separadores en la cédula.", self.radioButtonGroup)
        self.removeBothBox = self._add_cedula_option(self.cedulaOptionsContainer, "Eliminar ambos separadores ('-' y '0')", 110, "Remueve tanto los guiones como los ceros en la cédula.", self.radioButtonGroup)

    def _add_cedula_option(self, parent, text, y_position, tooltip, button_group):
        radio_button = QtWidgets.QRadioButton(text, parent)
        radio_button.setGeometry(QtCore.QRect(20, y_position, 350, 30))
        radio_button.setStyleSheet("color: black;")
        radio_button.setToolTip(tooltip)
        button_group.addButton(radio_button)
        return radio_button

    def _create_format_validation_section(self, Dialog):
        self.formatOptionsContainer = QtWidgets.QFrame(Dialog)
        self.formatOptionsContainer.setGeometry(QtCore.QRect(50, 240, 400, 160))  
        self.formatOptionsContainer.setStyleSheet("background-color: rgb(240, 240, 240); border-radius: 10px;")
        self.formatOptionsContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        self.formatOptionsLabel = QtWidgets.QLabel("Validación y formato de cédula", parent=self.formatOptionsContainer)
        self.formatOptionsLabel.setGeometry(QtCore.QRect(20, 10, 400, 30))
        self.formatOptionsLabel.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.formatOptionsLabel.setStyleSheet("color: black;")

        self.validateFormatBox = self._add_format_option(self.formatOptionsContainer, "Validar formato de cédula", 50, "Verifica si la cédula cumple con el formato ingresado.")
        self._add_custom_format_input(self.formatOptionsContainer, 55)

        self.applyFormatBox = self._add_format_option(self.formatOptionsContainer, "Convertir a formato personalizado", 110, "Convierte la cédula al formato definido.")
        self.applyFormatInput = self._add_apply_format_input(self.formatOptionsContainer, 110)

    def _add_format_option(self, parent, text, y_position, tooltip):
        radio_button = QtWidgets.QRadioButton(text, parent)
        radio_button.setGeometry(QtCore.QRect(20, y_position, 350, 30))
        radio_button.setStyleSheet("color: black;")
        radio_button.setToolTip(tooltip)
        self.radioButtonGroup.addButton(radio_button)
        return radio_button

    def _add_custom_format_input(self, parent, y_position):
        self.formatInput = QtWidgets.QLineEdit(parent)
        self.formatInput.setGeometry(QtCore.QRect(280, y_position, 100, 30))
        self.formatInput.setPlaceholderText("Formato")
        self.formatInput.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.formatInput.setToolTip("Ingresa un formato como 9-999-999")
        self.formatInput.setEnabled(False)

        regex = QtCore.QRegularExpression("[9#0\\-()]*")
        validator = QtGui.QRegularExpressionValidator(regex)
        self.formatInput.setValidator(validator)

    def _add_apply_format_input(self, parent, y_position):
        apply_format_input = QtWidgets.QLineEdit(parent)
        apply_format_input.setGeometry(QtCore.QRect(280, y_position, 100, 30))
        apply_format_input.setPlaceholderText("Formato")
        apply_format_input.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        apply_format_input.setToolTip("Ejemplo: 9-999-999")
        apply_format_input.setEnabled(False)

        regex = QtCore.QRegularExpression("[9#0\\-()]*")
        validator = QtGui.QRegularExpressionValidator(regex)
        apply_format_input.setValidator(validator)

        return apply_format_input

    def _create_accept_button(self, Dialog):
        self.acceptButton = QtWidgets.QPushButton("Aceptar", Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(200, 420, 100, 30))
        self.acceptButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.acceptButton.setStyleSheet("background-color: white; color: black; border-radius: 10px;")
        self.acceptButton.clicked.connect(lambda: self.on_accept(Dialog))

    def toggle_format_input(self):
        self.formatInput.setEnabled(self.validateFormatBox.isChecked())

    def toggle_apply_format_input(self):
        self.applyFormatInput.setEnabled(self.applyFormatBox.isChecked())

    def on_accept(self, dialog):
        self.controller.set_remove_hyphen(self.removeHyphenBox.isChecked())
        self.controller.set_remove_zero(self.removeZeroBox.isChecked())
        self.controller.set_remove_both(self.removeBothBox.isChecked())
        self.controller.set_validate_format(self.validateFormatBox.isChecked(), self.formatInput.text())
        self.controller.set_apply_format(self.applyFormatBox.isChecked(), self.applyFormatInput.text())
        self.controller.accept()
        dialog.accept()

    def get_description(self):
        return self.controller.generate_description()

    def on_reject(self):
        self.controller.reject()

    def get_accepted(self):
        return self.controller.is_accepted()
