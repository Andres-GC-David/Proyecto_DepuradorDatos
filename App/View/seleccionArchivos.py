import os
import json
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from App.View.manageFileTypesDialog import ManageFileTypesDialog
from App.Controller.databaseController import DatabaseController

class Ui_Dialog(object):
    def __init__(self, main_window, database_controller):
        self.selected_file_path = None
        self.main_window = main_window  
        self.allowed_file_types = self.load_file_types()
        self.database_controller = database_controller
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 300)
        Dialog.setStyleSheet("background-color: rgb(58, 99, 140);")

        # Crear la barra de menú
        self.menuBar = QtWidgets.QMenuBar(Dialog)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 500, 28))  # Ajustar tamaño de la barra
        self.menuBar.setStyleSheet("""
            QMenuBar {
                background-color: rgb(58, 99, 140);  /* Fondo de la barra de menú */
                color: rgb(255, 255, 255);  /* Texto blanco en la barra */
                font-weight: bold;
            }
            QMenuBar::item {
                background-color: transparent;  /* Fondo transparente para ítems */
                color: rgb(255, 255, 255);  /* Texto blanco */
                padding: 6px 20px;
            }
            QMenuBar::item:selected {
                background-color: rgb(255, 255, 255);  /* Hover: fondo blanco */
                color: rgb(0, 0, 0);  /* Hover: texto negro */
            }
        """)

        # Menú de opciones
        self.menuOptions = QtWidgets.QMenu("Opciones", self.menuBar)

        # Aplicar estilo específico al menú "Opciones"
        self.menuOptions.setStyleSheet("""
            QMenu {
                background-color: rgb(255, 255, 255);  /* Fondo blanco */
                color: rgb(0, 0, 0);  /* Texto negro */
            }
            QMenu::item {
                background-color: rgb(255, 255, 255);  /* Fondo blanco en ítems */
                color: rgb(0, 0, 0);  /* Texto negro */
            }
            QMenu::item:selected {
                background-color: rgb(200, 200, 200);  /* Hover: fondo gris claro */
                color: rgb(0, 0, 0);  /* Texto negro */
            }
        """)

        # Añadir acciones a "Opciones"
        self.actionChangeToTable = QtGui.QAction("Cambiar a Base de Datos", self.menuOptions)
        #self.actionManageFileTypes = QtGui.QAction("Gestionar Tipos de Archivos", self.menuOptions)

        # Conectar las acciones
        self.actionChangeToTable.triggered.connect(lambda: self.send_to_table(Dialog))
        #self.actionManageFileTypes.triggered.connect(self.open_manage_file_types_dialog)

        # Añadir las acciones al menú
        self.menuOptions.addAction(self.actionChangeToTable)
        #self.menuOptions.addAction(self.actionManageFileTypes)

        # Añadir el menú a la barra de menú
        self.menuBar.addMenu(self.menuOptions)

        # Etiqueta del título
        self.fileSelectionWindowLabel = QtWidgets.QLabel(Dialog)
        self.fileSelectionWindowLabel.setGeometry(QtCore.QRect(30, 40, 300, 30))  # Ajustado debajo del menú
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        self.fileSelectionWindowLabel.setFont(font)
        self.fileSelectionWindowLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.fileSelectionWindowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fileSelectionWindowLabel.setObjectName("fileSelectionWindowLabel")

        # Contenedor de selección de archivo
        self.fileSelectionContainer = QtWidgets.QFrame(Dialog)
        self.fileSelectionContainer.setGeometry(QtCore.QRect(50, 80, 400, 130))
        self.fileSelectionContainer.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                "border-radius: 10px;\n")
        self.fileSelectionContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.fileSelectionContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.fileSelectionContainer.setObjectName("fileSelectionContainer")

        # Etiqueta de selección de archivo
        self.fileSelectionLabel = QtWidgets.QLabel(parent=self.fileSelectionContainer)
        self.fileSelectionLabel.setGeometry(QtCore.QRect(20, 40, 170, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.fileSelectionLabel.setFont(font)
        self.fileSelectionLabel.setStyleSheet("color: rgb(58, 99, 140);\n"
                                            "background-color: white;\n"
                                            "border-radius: 10px;")
        self.fileSelectionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fileSelectionLabel.setObjectName("fileSelectionLabel")

        # Botón para abrir el explorador de archivos
        self.fileSelectionButton = QtWidgets.QPushButton("Buscar", parent=self.fileSelectionContainer)
        self.fileSelectionButton.setGeometry(QtCore.QRect(200, 40, 170, 41))
        self.fileSelectionButton.setFont(QtGui.QFont("Segoe UI", 12))
        self.fileSelectionButton.setStyleSheet("background-color: rgb(58, 99, 140);\n"
                                            "color: white;\n"
                                            "border-radius: 4px;\n")
        self.fileSelectionButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fileSelectionButton.setObjectName("fileSelectionButton")

        # Label para mostrar el archivo seleccionado
        self.fileSelectedLabel = QtWidgets.QLabel(parent=self.fileSelectionContainer)
        self.fileSelectedLabel.setGeometry(QtCore.QRect(20, 90, 350, 30))
        self.fileSelectedLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.fileSelectedLabel.setStyleSheet("border: 2px solid black;\n"
                                            "background-color: white;\n"
                                            "color: black;\n"
                                            "border-radius: 4px;\n")
        self.fileSelectedLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fileSelectedLabel.setText("")  
        self.fileSelectedLabel.setObjectName("fileSelectedLabel")

        # Botón de aceptar
        self.fileSelectionAcceptButton = QtWidgets.QPushButton(parent=Dialog)
        self.fileSelectionAcceptButton.setGeometry(QtCore.QRect(180, 230, 140, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.fileSelectionAcceptButton.setFont(font)
        self.fileSelectionAcceptButton.setStyleSheet("color: rgb(0, 0, 0);\n"
                                                    "background-color: rgb(255, 255, 255);\n"
                                                    "border-radius: 4px;\n")
        self.fileSelectionAcceptButton.setObjectName("fileSelectionAcceptButton")

        # Conectar el botón aceptar para agregar el archivo a summayOfDataTable
        self.fileSelectionAcceptButton.clicked.connect(lambda: self.add_file_to_main_window(Dialog))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Conectar el botón de selección de archivo al método de selección
        self.fileSelectionButton.clicked.connect(self.open_file_dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Seleccionar Archivo"))
        self.fileSelectionAcceptButton.setText(_translate("Dialog", "Aceptar"))
        self.fileSelectionLabel.setText(_translate("Dialog", "Seleccion Archivo"))
        self.fileSelectionWindowLabel.setText(_translate("Dialog", "Selección de Archivos"))

    def load_file_types(self):
        file_types_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'fileTypes.json')
        if os.path.exists(file_types_path):
            with open(file_types_path, 'r') as file:
                return json.load(file)
        else:
            # Valor por defecto si no se encuentra el archivo
            return [
                {"type": "txt", "filter": "Archivos de texto (*.txt)"},
                {"type": "csv", "filter": "Archivos CSV (*.csv)"},
                {"type": "xlsx", "filter": "Archivos Excel (*.xlsx)"}
            ]
            
    
    def send_to_table(self, dialog: QtWidgets.QDialog):
        # Primero verificamos si existe una conexión activa mediante databaseController
        if self.main_window.database_controller.is_connected():
            # Si la conexión está activa, abrir la ventana de selección de tablas
            dialog.accept()
            from App.View.seleccionTablas import Ui_Dialog as TableSelectionDialog
            table_selection_dialog = QtWidgets.QDialog()
            table_selection_dialog_ui = TableSelectionDialog(self.main_window, self.main_window.database_controller)
            table_selection_dialog_ui.setupUi(table_selection_dialog)
            table_selection_dialog.exec()
        else:
            # Si no hay conexión, abrir la ventana de conexión
            dialog.accept()
            from App.View.connectionDialog import Ui_ConnectionDialog
            connection_dialog = QtWidgets.QDialog()
            connection_dialog_ui = Ui_ConnectionDialog(self.database_controller)
            connection_dialog_ui.setupUi(connection_dialog)
            connection_dialog.exec()
            
            if connection_dialog_ui.connection_successful:
                from App.View.seleccionTablas import Ui_Dialog as TableSelectionDialog
                table_selection_dialog = QtWidgets.QDialog()
                table_selection_dialog_ui = TableSelectionDialog(self.main_window, self.main_window.database_controller)
                table_selection_dialog_ui.setupUi(table_selection_dialog)
                table_selection_dialog.exec()
            
    def add_file_to_main_window(self, dialog: QtWidgets.QDialog):
        if not self.fileSelectedLabel.text():
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Por favor, seleccione un archivo antes de continuar.")
            return
        
        if self.selected_file_path:
            # Detectar el tipo de archivo por su extensión
            file_extension = self.selected_file_path.split('.')[-1].lower()
            file_type = next((ft["type"].upper() for ft in self.allowed_file_types if ft["type"] == file_extension), "Desconocido")

            # Limpiar el contenido actual de summayOfDataTable
            self.main_window.summayOfDataTable.setRowCount(0)

            # Agregar el archivo seleccionado a summayOfDataTable
            self.main_window.summayOfDataTable.setRowCount(1)
            self.main_window.summayOfDataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Archivo"))
            self.main_window.summayOfDataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(file_type))
            self.main_window.summayOfDataTable.setItem(0, 2, QtWidgets.QTableWidgetItem(self.selected_file_path))  # Mostrar la ruta completa del archivo

            # Cargar los datos en la tabla "Esquema Actual"
            self.main_window.load_data_from_file(self.selected_file_path)

        # Cerrar el diálogo
        dialog.close()

    def open_file_dialog(self):
        # Abrir el cuadro de diálogo de archivos, restringido al tipo de archivo seleccionado
        filters = ";;".join([ft["filter"] for ft in self.allowed_file_types])
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Seleccionar Archivo", "", filters)

        if file_path:
            self.selected_file_path = file_path  # Guardar la ruta completa del archivo
            self.fileSelectedLabel.setText(file_path.split("/")[-1])  # Mostrar solo el nombre del archivo
            
            
    def open_manage_file_types_dialog(self):
        manage_file_types_dialog = ManageFileTypesDialog(self.main_window)  # Usar la ventana principal como parent
        manage_file_types_dialog.exec()
        
    


