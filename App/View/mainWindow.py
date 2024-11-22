from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from App.Controller.mainWindowController import MainWindowController
from App.View.addRule import AddRule 
from App.View.ruleConfiguration import RuleConfiguration 
from App.View.aboutProject import Ui_AboutProject 

class Ui_MainWindow(object):
    def __init__(self):
        self.controller = MainWindowController()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1250, 800)  # Tamaño ajustado de la ventana para mantener proporciones
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(8,172,20);")
        MainWindow.setWindowTitle("Depurador de Datos")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Agregar contenedor superior para logo, título y botón de ayuda
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setSpacing(20)

        # Logo
        self.logoLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.logoLabel.setGeometry(QtCore.QRect(0, 0, 250, 70))  # Logo más ancho
        pixmap = QtGui.QPixmap("App/Images/LogoCoope.png")  # Ruta al logo
        scaled_pixmap = pixmap.scaled(250, 70, Qt.AspectRatioMode.KeepAspectRatio)  # Mantener altura
        self.logoLabel.setPixmap(scaled_pixmap)
        self.logoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.header_layout.addWidget(self.logoLabel)

        # Título a la derecha del logo
        self.dataSelectionWindowLabel = QtWidgets.QLabel("Depurador de Datos", parent=self.centralwidget)
        self.dataSelectionWindowLabel.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Weight.Bold))
        self.dataSelectionWindowLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.dataSelectionWindowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.dataSelectionWindowLabel.setContentsMargins(0, 10, 0, 0)  # Bajar un poco el título
        self.header_layout.addWidget(self.dataSelectionWindowLabel)
        
        # Espaciador para centrar el botón de ayuda a la derecha
        self.header_layout.addStretch()

        # Botón circular "?" (blanco con texto negro)
        self.helpButton = QtWidgets.QPushButton("?", parent=self.centralwidget)
        self.helpButton.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Weight.Bold))  # Texto más grande
        self.helpButton.setFixedSize(40, 40)  # Botón más grande
        self.helpButton.setStyleSheet("""
            QPushButton {
                background-color: white;  /* Fondo blanco */
                color: black;             /* Texto negro */
                border-radius: 10%;      /* Hacerlo completamente redondo */
                border: 2px solid black;  /* Borde negro para contraste */
            }
            QPushButton:hover {
                background-color: lightgray;  /* Cambiar a gris claro al pasar el ratón */
            }
            QPushButton:pressed {
                background-color: darkgray;  /* Cambiar a gris oscuro al hacer clic */
            }
        """)
        self.helpButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.header_layout.addWidget(self.helpButton)
        self.helpButton.clicked.connect(self.open_about_project)

        self.main_layout.addLayout(self.header_layout)

        # Contenedor principal para botones y tablas
        self.dataSelectionContainer = QtWidgets.QFrame(parent=self.centralwidget)
        self.dataSelectionContainer.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                "border-radius: 4px;\n")
        self.data_selection_layout = QtWidgets.QHBoxLayout(self.dataSelectionContainer)
        self.data_selection_layout.setSpacing(10)

        self.left_button_layout = QtWidgets.QVBoxLayout()
        self.left_button_layout.setSpacing(10)

        # Botón combinado para selección de tablas y archivos
        self.dataSelectionButton = QtWidgets.QPushButton("Origen de Datos")
        self.setup_button(self.dataSelectionButton)
        self.left_button_layout.addWidget(self.dataSelectionButton)

        # Botón de reglas de negocio
        self.parameterSelectionButton = QtWidgets.QPushButton("Reglas de Negocio")
        self.setup_button(self.parameterSelectionButton)
        self.left_button_layout.addWidget(self.parameterSelectionButton)

        # Botón de aplicar depuración
        self.applyDepurationButton = QtWidgets.QPushButton("Aplicar Depuración")
        self.setup_button(self.applyDepurationButton)
        self.left_button_layout.addWidget(self.applyDepurationButton)
        self.applyDepurationButton.clicked.connect(self.apply_depuration)

        # Botón de descarga
        self.downloadScriptButton = QtWidgets.QPushButton("Descargar")
        self.setup_button(self.downloadScriptButton)
        self.left_button_layout.addWidget(self.downloadScriptButton)
        self.downloadScriptButton.clicked.connect(self.download_data)

        # Botón de configuraciones de regla
        self.ruleConfigurationButton = QtWidgets.QPushButton("Configuraciones de Regla")
        self.setup_button(self.ruleConfigurationButton)
        self.left_button_layout.addWidget(self.ruleConfigurationButton)
        self.ruleConfigurationButton.clicked.connect(self.open_rule_configuration)

        self.data_selection_layout.addLayout(self.left_button_layout)

        self.summary_layout = QtWidgets.QVBoxLayout()

        # Tabla de resumen de datos
        self.summayOfDataTable = QtWidgets.QTableWidget(1, 3, parent=self.dataSelectionContainer)
        self.summayOfDataTable.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.summayOfDataTable.setFixedHeight(70)
        self.summayOfDataTable.setHorizontalHeaderLabels(["Tipo de Archivo", "Tipo de Dato", "Nombre de Archivo"])
        self.summayOfDataTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.summayOfDataTable.horizontalHeader().setStyleSheet("background-color: black; color: white;")
        self.summayOfDataTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.summayOfDataTable.verticalHeader().setVisible(False)
        self.summary_layout.addWidget(self.summayOfDataTable)

        # Tabla de resumen de parámetros
        self.summaryOfParameterTable = QtWidgets.QTableWidget(4, 3, parent=self.dataSelectionContainer)
        self.summaryOfParameterTable.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.summaryOfParameterTable.setFixedHeight(130)
        self.summaryOfParameterTable.setHorizontalHeaderLabels(["Nombre Modificación", "Modificación", "Columna"])
        self.summaryOfParameterTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.summaryOfParameterTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.summaryOfParameterTable.horizontalHeader().setStyleSheet("background-color: black; color: white;")
        self.summaryOfParameterTable.verticalHeader().setVisible(False)
        self.summary_layout.addWidget(self.summaryOfParameterTable)

        self.data_selection_layout.addLayout(self.summary_layout)
        self.main_layout.addWidget(self.dataSelectionContainer)

        self.actual_new_layout = QtWidgets.QHBoxLayout()
        self.actual_new_layout.setSpacing(20)
        self.actual_new_layout.setContentsMargins(0, 20, 0, 0)

        self.actualDataContainer = self.create_data_container("Esquema Actual", 10, 10)
        self.newDataContainer = self.create_data_container("Esquema Modificado", 10, 10)

        self.actual_new_layout.addWidget(self.actualDataContainer)
        self.actual_new_layout.addWidget(self.newDataContainer)

        self.main_layout.addLayout(self.actual_new_layout)
        if self.controller.selected_rules:
            self._restore_selected_rules(self.controller.selected_rules)
            
        self.dataSelectionButton.clicked.connect(self.clear_rules_and_select_tables)


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_button(self, button):
        font = QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold)
        button.setFont(font)
        button.setFixedSize(211, 41)
        button.setStyleSheet("background-color: rgb(8,172,20);\n"
                             "color: rgb(255, 255, 255);\n"
                             "border-radius: 4px;\n")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def _restore_selected_rules(self, selected_rules):
        self.summaryOfParameterTable.setRowCount(len(selected_rules))  # Establecer el número de filas necesarias

        for row, rule in enumerate(selected_rules):
            self.summaryOfParameterTable.setItem(row, 0, QtWidgets.QTableWidgetItem(rule[0]))  # Nombre de la regla
            self.summaryOfParameterTable.setItem(row, 1, QtWidgets.QTableWidgetItem(rule[1]))  # Modificación
            self.summaryOfParameterTable.setItem(row, 2, QtWidgets.QTableWidgetItem(rule[2]))  # Columna
            print(rule[0], rule[1], rule[2], "desde mainWindow")
            
    def clear_rules_and_select_tables(self):
        self.controller.selected_rules = []
        self.summaryOfParameterTable.setRowCount(0)  
        self.summayOfDataTable.setRowCount(0)
        
    def open_about_project(self):
        self.aboutWindow = QtWidgets.QMainWindow()
        self.ui_about = Ui_AboutProject()
        self.ui_about.setupUi(self.aboutWindow)
        self.aboutWindow.show()

    def clear_rules_and_select_files(self):
        self.controller.selected_rules = []
        self.summaryOfParameterTable.setRowCount(0) 

    def create_data_container(self, label_text, rows, cols):
        container = QtWidgets.QFrame()
        container.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                "border-radius: 4px;\n")
        layout = QtWidgets.QVBoxLayout(container)

        label = QtWidgets.QLabel(label_text)
        label.setFont(QtGui.QFont("Segoe UI", 20, QtGui.QFont.Weight.Bold))
        label.setStyleSheet("color: rgb(8,172,20);")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        table = QtWidgets.QTableWidget(rows, cols, parent=container)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        layout.addWidget(table)
        
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)

        return container

    def apply_depuration(self):
        self.controller.apply_depuration(self)

    def download_data(self):
        self.controller.download_data(self)

    def load_data_from_file(self, file_path):
        self.controller.load_data_from_file(self, file_path)

    def load_data_in_actual_table(self, data, column_headers):
        self.controller.load_data_in_actual_table(self, data, column_headers)

    def reset_actual_data_table(self):
        self.controller.reset_actual_data_table(self)
        
    def reset_new_data_table(self):
        self.controller.reset_new_data_table(self)
    
    def open_rule_configuration(self):
        rule_config_window = QtWidgets.QDialog()
        ui = RuleConfiguration()  
        ui.setupUi(rule_config_window)
        rule_config_window.exec()
