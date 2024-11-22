from PyQt6.QtCore import QThread, pyqtSignal

class ProgressWorker(QThread):
    progress = pyqtSignal(int)  
    finished = pyqtSignal(str)  
    error = pyqtSignal(str)     

    def __init__(self, simulated=True):
        super().__init__()
        self._running = True
        self.simulated = simulated  
        self.real_progress_value = 0  

    def run(self):
        if self.simulated:

            value = 0
            while self._running:
                value += 10
                if value > 100:
                    value = 0
                self.progress.emit(value)
                self.msleep(200)  
        else:
            
            while self._running:
                self.msleep(50) 

    def stop(self):
        self._running = False

    def emit_progress(self, value):

        self.real_progress_value = value
        self.progress.emit(value)

    def emit_finished(self, message="Proceso completado"):

        self.finished.emit(message)
        self.stop()

    def emit_error(self, error_message):

        self.error.emit(error_message)
        self.stop()
