from PyQt6.QtCore import QThread, pyqtSignal

class QueryWorker(QThread):
    progress = pyqtSignal(int)  
    finished = pyqtSignal(tuple)  
    error = pyqtSignal(str)  

    def __init__(self, database_controller, database_name, table_name):
        super().__init__()
        self.database_controller = database_controller
        self.database_name = database_name
        self.table_name = table_name

    def run(self):
        try:
            self.progress.emit(10)  

            self.database_controller.connect()
            self.progress.emit(30)  

            data, column_names = self.database_controller.get_table_data(
                self.database_name,
                self.table_name,
                progress_callback=self.progress.emit 
            )

            self.progress.emit(100)  
            self.finished.emit((data, column_names))
        except Exception as e:
            self.error.emit(str(e))
