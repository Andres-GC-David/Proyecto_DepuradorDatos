from PyQt6 import QtCore, QtGui, QtWidgets
from App.Controller.databaseController import DatabaseController
from App.View.databaseManagement import Ui_DataBaseManagementDialog
from App.Controller.query_worker import QueryWorker  # Ya existe
from App.Controller.progressWorker import ProgressWorker  # Importar ProgressWorker
from App.View.loadingDialog import LoadingDialog  # Importar LoadingDialog
from PyQt6.QtCore import Qt

class Ui_Dialog(object):
    def __init__(self, main_window, database_controller):
        # Instanciar el controlador de la base de datos
        self.databaseController = database_controller
        self.main_window = main_window  # Mantener referencia a MainWindow

    def setupUi(self, Dialog):
        self.current_dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(601, 480)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        # Agregar QMenuBar
        self.menuBar = QtWidgets.QMenuBar(Dialog)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 601, 35))  # Ajustar tamaño de la barra
        self.menuBar.setStyleSheet("""
            QMenuBar {
                background-color: rgb(8,172,20);  /* Fondo de la barra de menú */
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
        self.menuBar.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        # Menú de opciones
        self.menuOptions = QtWidgets.QMenu("Opciones", self.menuBar)
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

        # Acción para "Cambiar a Archivos"
        self.actionChangeToFiles = QtGui.QAction("Cambiar a Archivos", self.menuBar)
        self.actionChangeToFiles.triggered.connect(lambda: self.sendToFiles(Dialog))  # Conectar la acción al método correspondiente
        self.menuOptions.addAction(self.actionChangeToFiles)  # Añadir la acción al menú

        # Acción para "Gestionar BD"
        self.actionManageDB = QtGui.QAction("Gestionar BD", self.menuBar)
        self.actionManageDB.triggered.connect(self.open_database_management)  # Conectar la acción al método de gestión de BD
        self.menuOptions.addAction(self.actionManageDB)  # Añadir la acción al menú

        # Añadir el menú de opciones a la barra de menú
        self.menuBar.addMenu(self.menuOptions)

        # Botón aceptar
        self.acceptTableSelectionButton = QtWidgets.QPushButton(parent=Dialog)
        self.acceptTableSelectionButton.setGeometry(QtCore.QRect(210, 420, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.acceptTableSelectionButton.setFont(font)
        self.acceptTableSelectionButton.setStyleSheet("color: rgb(0, 0, 0);\n"
                                                    "background-color: rgb(255, 255, 255);\n"
                                                    "border-radius: 4px;\n")
        self.acceptTableSelectionButton.setObjectName("acceptTableSelectionButton")
        self.acceptTableSelectionButton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Contenedor de selección de bases de datos
        self.databaseSelectionContainer = QtWidgets.QFrame(parent=Dialog)
        self.databaseSelectionContainer.setGeometry(QtCore.QRect(50, 110, 501, 121))
        self.databaseSelectionContainer.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                    "border-radius: 4px;\n")
        self.databaseSelectionContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.databaseSelectionContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.databaseSelectionContainer.setObjectName("databaseSelectionContainer")

        # Etiqueta de selección de bases de datos
        self.databaseSelectionLabel = QtWidgets.QLabel(parent=self.databaseSelectionContainer)
        self.databaseSelectionLabel.setGeometry(QtCore.QRect(20, 40, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.databaseSelectionLabel.setFont(font)
        self.databaseSelectionLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                "background-color: rgb(8,172,20);\n"
                                                "border-radius: 4px;")
        self.databaseSelectionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.databaseSelectionLabel.setObjectName("databaseSelectionLabel")

        # Tabla de opciones de bases de datos
        self.databaseOptionsTable = QtWidgets.QTableWidget(parent=self.databaseSelectionContainer)
        self.databaseOptionsTable.setGeometry(QtCore.QRect(250, 10, 211, 101))
        self.databaseOptionsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.databaseOptionsTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.databaseOptionsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.databaseOptionsTable.setObjectName("databaseOptionsTable")
        self.databaseOptionsTable.setColumnCount(1)
        self.databaseOptionsTable.setRowCount(0)
        self.databaseOptionsTable.setHorizontalHeaderLabels(["Base de Datos"])
        self.databaseOptionsTable.horizontalHeader().setStretchLastSection(True)

        # Contenedor de selección de tablas
        self.tableSelectionContainer = QtWidgets.QFrame(parent=Dialog)
        self.tableSelectionContainer.setGeometry(QtCore.QRect(50, 280, 501, 121))
        self.tableSelectionContainer.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                "border-radius: 4px;\n")
        self.tableSelectionContainer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.tableSelectionContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.tableSelectionContainer.setObjectName("tableSelectionContainer")
        
        self.progress_bar = QtWidgets.QProgressBar(parent=Dialog)
        self.progress_bar.setGeometry(QtCore.QRect(50, 450, 500, 20))  # Ajusta según el diseño
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid black;
                border-radius: 5px;
                background-color: rgb(8,172,20);
                color: white;
            }
            QProgressBar::chunk {
                background-color: rgb(255, 255, 255);
            }
        """)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Oculta inicialmente

        # Etiqueta de selección de tablas
        self.tableSelectionLabel = QtWidgets.QLabel(parent=self.tableSelectionContainer)
        self.tableSelectionLabel.setGeometry(QtCore.QRect(20, 40, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.tableSelectionLabel.setFont(font)
        self.tableSelectionLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "background-color: rgb(8,172,20);\n"
                                            "border-radius: 4px;")
        self.tableSelectionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableSelectionLabel.setObjectName("tableSelectionLabel")

        # Tabla de opciones de tablas
        self.tableOptionTable = QtWidgets.QTableWidget(parent=self.tableSelectionContainer)
        self.tableOptionTable.setGeometry(QtCore.QRect(260, 10, 211, 101))
        self.tableOptionTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableOptionTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableOptionTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableOptionTable.setObjectName("tableOptionTable")
        self.tableOptionTable.setColumnCount(1)
        self.tableOptionTable.setRowCount(0)
        self.tableOptionTable.setHorizontalHeaderLabels(["Tablas"])
        self.tableOptionTable.horizontalHeader().setStretchLastSection(True)

        # Etiqueta de ventana
        self.tableSelectionWindowLabel = QtWidgets.QLabel(parent=Dialog)
        self.tableSelectionWindowLabel.setGeometry(QtCore.QRect(160, 60, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        self.tableSelectionWindowLabel.setFont(font)
        self.tableSelectionWindowLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.tableSelectionWindowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableSelectionWindowLabel.setObjectName("tableSelectionWindowLabel")
        self.retranslateUi(Dialog)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        self.load_databases() 
        self.databaseOptionsTable.itemSelectionChanged.connect(self.load_tables)
        self.acceptTableSelectionButton.clicked.connect(lambda: self.add_table_to_main_window(Dialog))


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Seleccion de Tablas"))
        self.acceptTableSelectionButton.setText(_translate("Dialog", "Aceptar"))
        self.databaseSelectionLabel.setText(_translate("Dialog", "Base de Datos"))
        self.tableSelectionLabel.setText(_translate("Dialog", "Seleccion de Tablas"))
        self.tableSelectionWindowLabel.setText(_translate("Dialog", "Seleccion de Tablas"))
        
    
    def sendToFiles(self, dialog: QtWidgets.QDialog):
        dialog.accept()
        from App.View.seleccionArchivos import Ui_Dialog as FileSelectionDialog
        file_selection_dialog = QtWidgets.QDialog()
        file_selection_dialog_ui = FileSelectionDialog(self.main_window, self.databaseController)
        file_selection_dialog_ui.setupUi(file_selection_dialog)
        file_selection_dialog.exec()

    def load_databases(self):

        databases = self.databaseController.get_databases()
        self.databaseOptionsTable.setRowCount(len(databases))
        for row, database in enumerate(databases):
            self.databaseOptionsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(database))

    def load_tables(self):
        selected_row = self.databaseOptionsTable.currentRow()
        if selected_row != -1:
            selected_database = self.databaseOptionsTable.item(selected_row, 0).text()
            tables = self.databaseController.get_tables(selected_database)  # Obtener tablas

            self.tableOptionTable.setRowCount(len(tables))

            for row, table_name in enumerate(tables):
                self.tableOptionTable.setItem(row, 0, QtWidgets.QTableWidgetItem(table_name))  # Usar nombre completo


                
    def open_database_management(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_DataBaseManagementDialog(self.databaseController)
        self.ui.setupUi(self.dialog)
        self.dialog.exec()

    def add_table_to_main_window(self, Dialog):
        selected_row = self.tableOptionTable.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Por favor, selecciona una tabla.")
            return

        selected_table = self.tableOptionTable.item(selected_row, 0).text()
        selected_database_row = self.databaseOptionsTable.currentRow()
        selected_database = self.databaseOptionsTable.item(selected_database_row, 0).text()

        if selected_table and selected_database:
            try:
                connection_params = self.main_window.connection_params
                if connection_params:
                    self.databaseController.set_credentials(
                        connection_params['username'],
                        connection_params['password'],
                        connection_params['host'],
                        connection_params['port'],
                        connection_params['service_name']
                    )
                    self.databaseController.connect()

                # Mostrar el diálogo de carga
                self.loading_dialog = LoadingDialog(self.main_window)
                self.loading_dialog.show()

                # Iniciar el hilo para la consulta
                self.query_worker = QueryWorker(self.databaseController, selected_database, selected_table)
                self.query_worker.progress.connect(self.loading_dialog.update_progress)
                self.query_worker.finished.connect(self.on_query_finished)
                self.query_worker.error.connect(self.on_query_error)
                self.query_worker.start()

            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error al cargar datos: {str(e)}")


    def on_query_finished(self, result):
        self.loading_dialog.close()  # Cerrar diálogo de carga
        data, column_names = result

        # Cargar datos en la tabla principal
        self.main_window.load_data_in_actual_table(data, column_names)

        # Actualizar tabla resumen
        selected_table = self.tableOptionTable.item(self.tableOptionTable.currentRow(), 0).text()
        self.main_window.summayOfDataTable.setRowCount(0)
        self.main_window.summayOfDataTable.setRowCount(1)
        self.main_window.summayOfDataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Base de Datos"))
        self.main_window.summayOfDataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("Tabla"))
        self.main_window.summayOfDataTable.setItem(0, 2, QtWidgets.QTableWidgetItem(selected_table))

        # Mostrar mensaje de éxito
        QtWidgets.QMessageBox.information(None, "Éxito", "Datos cargados correctamente.")

        # Cerrar el diálogo
        self.current_dialog.close()  # Usamos la referencia correcta




    def on_query_error(self, error_message):
        self.loading_dialog.close()
        QtWidgets.QMessageBox.critical(None, "Error", f"Error al cargar datos: {error_message}")





