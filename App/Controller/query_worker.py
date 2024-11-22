from PyQt6.QtCore import QThread, pyqtSignal

class QueryWorker(QThread):
    progress = pyqtSignal(int)  # Señal para el progreso
    finished = pyqtSignal(tuple)  # Señal para el resultado exitoso
    error = pyqtSignal(str)  # Señal para errores

    def __init__(self, database_controller, database_name, table_name):
        super().__init__()
        self.database_controller = database_controller
        self.database_name = database_name
        self.table_name = table_name

    def run(self):
        try:
            self.progress.emit(10)  # Indicar inicio

            # Conectar a la base de datos
            self.database_controller.connect()
            self.progress.emit(30)  # Progreso tras conexión

            # Ejecutar consulta para cargar datos
            data, column_names = self.database_controller.get_table_data(
                self.database_name,
                self.table_name,
                progress_callback=self.progress.emit  # Progreso desde el controlador
            )

            self.progress.emit(100)  # Consulta completada
            self.finished.emit((data, column_names))
        except Exception as e:
            self.error.emit(str(e))
