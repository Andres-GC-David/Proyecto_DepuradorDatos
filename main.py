from PyQt6 import QtWidgets, QtCore
from App.View.mainWindow import Ui_MainWindow
from App.View.seleccionArchivos import Ui_Dialog as FileSelectionDialog  
from App.View.seleccionTablas import Ui_Dialog as TableSelectionDialog  
from App.View.seleccionReglasDeNegocio import Ui_Dialog as RuleSelectionDialog 
from App.View.seleccionReglasDeNegocioArchivos import Ui_Dialog as RuleSelectionArchivosDialog 
from App.View.connectionDialog import Ui_ConnectionDialog
from PyQt6.QtCore import QTimer

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, database_controller, file_controller):
        super(MainWindow, self).__init__()
        
        self.database_controller = database_controller
        self.file_controller = file_controller
        self.connection_params = None  
        self.is_table_selection = False  
        
        self.setupUi(self)
        
        self.inactivity_timer = QTimer(self)
        #self.inactivity_timer.timeout.connect(self.handle_inactivity)
        self.inactivity_timer.setInterval(25 * 60 * 1000)
        
        #self.reset_inactivity_timer()
        self.installEventFilter(self)
        
        self.dataSelectionButton.clicked.connect(self.openFileSelectionDialog)
        self.parameterSelectionButton.clicked.connect(self.openRuleSelectionDialog)
        self.dataSelectionButton.clicked.connect(self.check_and_clear_parameter_table_and_open_file_selection)
        self.dataSelectionButton.clicked.connect(self.check_and_clear_parameter_table_and_open_table_selection)

    def clear_parameter_table(self):
        self.summaryOfParameterTable.setRowCount(0)

    def is_parameter_table_empty(self):
        return self.summaryOfParameterTable.rowCount() == 0

    def check_and_clear_parameter_table(self):
        if not self.is_parameter_table_empty():
            self.clear_parameter_table()

    def check_and_clear_parameter_table_and_open_file_selection(self):
        self.check_and_clear_parameter_table()

    def check_and_clear_parameter_table_and_open_table_selection(self):
        self.check_and_clear_parameter_table()

    def openFileSelectionDialog(self):
        self.reset_actual_data_table()
        self.reset_new_data_table()
        dialog = QtWidgets.QDialog()
        ui = FileSelectionDialog(self, database_controller) 
        ui.setupUi(dialog)
        dialog.exec()

    def openTableSelectionDialog(self):
        self.reset_actual_data_table()
        self.reset_new_data_table()
        
        if self.database_controller.is_connected():
            self.reset_inactivity_timer()
            self.show_table_selection_dialog()
        else:
            connection_dialog = QtWidgets.QDialog(self)
            connection_ui = Ui_ConnectionDialog(self.database_controller)
            connection_ui.setupUi(connection_dialog)
            connection_ui.successful_connection.connect(self.store_connection_params)
            result = connection_dialog.exec()

            if result == QtWidgets.QDialog.DialogCode.Accepted and connection_ui.connection_successful:
                self.reset_inactivity_timer() 
                self.show_table_selection_dialog()
            else:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("Error")
                msg_box.setText("Por favor, complete la conexion para seguir!")
                msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg_box.exec()
                
    def reset_inactivity_timer(self):
        self.inactivity_timer.stop()  
        self.inactivity_timer.start()  

    def handle_inactivity(self):
        
        if self.database_controller.is_connected():
            self.inactivity_timer.stop() 
            self.database_controller.close_connection()

            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Inactividad")
            msg_box.setText("Has estado inactivo durante 7 minutos. La conexión ha sido cerrada.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg_box.exec()
        else:
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Conexion")
            msg_box.setText("No hay conexión activa cuando se detectó inactividad.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg_box.exec()
                
    def closeEvent(self, event):
        
        if self.database_controller.is_connected():
            self.database_controller.close_connection()
        event.accept()
        
    def event(self, event):
        if event.type() in (QtCore.QEvent.Type.MouseMove, QtCore.QEvent.Type.KeyPress, QtCore.QEvent.Type.MouseButtonPress):
            self.reset_inactivity_timer()  

        return super(MainWindow, self).event(event)
    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.Type.MouseMove, 
                            QtCore.QEvent.Type.KeyPress, 
                            QtCore.QEvent.Type.MouseButtonPress, 
                            QtCore.QEvent.Type.Wheel): 
            self.reset_inactivity_timer()  

        return super(MainWindow, self).eventFilter(obj, event)

    def store_connection_params(self, params):
        self.connection_params = params
        
    def show_table_selection_dialog(self):

        dialog = QtWidgets.QDialog(self)
        ui = TableSelectionDialog(self, self.database_controller)
        ui.setupUi(dialog)
        dialog.exec()  

    def openRuleSelectionDialog(self):
        item = self.summayOfDataTable.item(0, 0)  
        
        if item is None or not item.text():
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Selecciona un archivo o tabla primero!")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return

        file_type = item.text()

        if file_type == "Archivo":
            dialog = QtWidgets.QDialog()
            ui = RuleSelectionArchivosDialog(self, self.file_controller) 
            ui.setupUi(dialog, self.summayOfDataTable)  
            dialog.exec()
            
        elif file_type == "Base de Datos":
            dialog = QtWidgets.QDialog()
            ui = RuleSelectionDialog(self.database_controller, self) 
            ui.setupUi(dialog, self.summayOfDataTable)  
            dialog.exec()
            
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Tipo de archivo seleccionado invalido!")

if __name__ == "__main__":
    import sys
    from App.Controller.databaseController import DatabaseController  
    from App.Controller.fileController import FileController
    
    app = QtWidgets.QApplication(sys.argv)
    
    database_controller = DatabaseController()
    file_controller = FileController()
    window = MainWindow(database_controller, file_controller) 
    window.show()
    
    sys.exit(app.exec())

