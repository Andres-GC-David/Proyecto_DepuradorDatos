from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.databaseController import DatabaseController
import re

class Ui_ConnectionDialog(QtCore.QObject):
    successful_connection = QtCore.pyqtSignal(dict)  

    def __init__(self, database_controller):
        super().__init__()
        self.database_controller = database_controller  
        self.connection_successful = False  
        self.local_username = None  
        self.local_password = None
        self.local_host = None
        self.local_port = None
        self.local_service_name = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setStyleSheet("background-color: rgb(58, 99, 140);")

        self.connectionLabel = QtWidgets.QLabel(Dialog)
        self.connectionLabel.setGeometry(QtCore.QRect(50, 20, 300, 30))
        self.connectionLabel.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.connectionLabel.setStyleSheet("color: white;")
        self.connectionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.connectionLabel.setText("Ingrese los datos de conexión")

        self.usernameInput = self.create_input(Dialog, 60, "Usuario")
        self.usernameInput.setStyleSheet("background-color: white; color: black;")
        self.passwordInput = self.create_input(Dialog, 100, "Contraseña", is_password=True)
        self.passwordInput.setStyleSheet("background-color: white; color: black;")
        self.hostInput = self.create_input(Dialog, 140, "Host")
        self.hostInput.setStyleSheet("background-color: white; color: black;")
        self.portInput = self.create_input(Dialog, 180, "Puerto")
        self.portInput.setStyleSheet("background-color: white; color: black;")
        self.serviceNameInput = self.create_input(Dialog, 220, "Service Name") 
        self.serviceNameInput.setStyleSheet("background-color: white; color: black;")

        self.connectButton = QtWidgets.QPushButton(Dialog)
        self.connectButton.setGeometry(QtCore.QRect(150, 260, 100, 30))
        self.connectButton.setText("Conectar")
        self.connectButton.setStyleSheet("background-color: white; color: black;")
        self.connectButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.connectButton.clicked.connect(lambda: self.connect(Dialog))

    def create_input(self, Dialog, y, placeholder, is_password=False):
        label = QtWidgets.QLabel(Dialog)
        label.setGeometry(QtCore.QRect(30, y, 80, 20))
        label.setText(f"{placeholder}:")
        label.setStyleSheet("color: white;")

        input_field = QtWidgets.QLineEdit(Dialog)
        input_field.setGeometry(QtCore.QRect(120, y, 200, 25))
        input_field.setPlaceholderText(placeholder)
        if is_password:
            input_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        return input_field

    def connect(self, Dialog):
        # Obtener valores de los campos de texto
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        host = self.hostInput.text()
        port = self.portInput.text()
        service_name = self.serviceNameInput.text()  

        # Validar campos antes de intentar conectar
        if not self.validate_inputs(username, password, host, port, service_name):
            return

        self.local_username = username
        self.local_password = password
        self.local_host = host
        self.local_port = port
        self.local_service_name = service_name

        try:
            # Intentar establecer la conexión
            self.database_controller.set_credentials(username, password, host, port, service_name)
            connection = self.database_controller.get_connection()  

            if connection:
                self.connection_successful = True  
                self.successful_connection.emit({
                    'username': username,
                    'password': password,
                    'host': host,
                    'port': port,
                    'service_name': service_name
                })
                Dialog.accept()  
            else:
                self.connection_successful = False
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Error al conectar: {str(e)}")
            self.connection_successful = False

    def validate_inputs(self, username, password, host, port, service_name):
        if not all([username, password, host, port, service_name]):
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Por favor, complete todos los campos.")
            return False

        if not re.match(r'^[\w.]+$', username):
            QtWidgets.QMessageBox.warning(None, "Advertencia", "El usuario contiene caracteres inválidos.")
            return False

        if not re.match(r'^[\w.]+$', service_name):
            QtWidgets.QMessageBox.warning(None, "Advertencia", "El nombre del servicio contiene caracteres inválidos.")
            return False

        if not self.is_valid_host(host):
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Por favor, ingrese un host válido (dirección IP o hostname).")
            return False

        if not port.isdigit() or not (1 <= int(port) <= 65535):
            QtWidgets.QMessageBox.warning(None, "Advertencia", "El puerto debe ser un número entre 1 y 65535.")
            return False

        if any(char in password for char in ["'", '"', ";", "--"]):
            QtWidgets.QMessageBox.warning(None, "Advertencia", "La contraseña contiene caracteres peligrosos.")
            return False

        return True

    def is_valid_host(self, host):
        ipv4_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
        if ipv4_pattern.match(host):
            octets = host.split('.')
            if all(0 <= int(octet) <= 255 for octet in octets):
                return True

        ipv6_pattern = re.compile(r'^([\da-fA-F]{1,4}:){7}[\da-fA-F]{1,4}$')
        if ipv6_pattern.match(host):
            return True

        hostname_pattern = re.compile(r'^[a-zA-Z0-9.-]+$')
        if hostname_pattern.match(host):
            return True

        return False
