from PyQt6.QtCore import QThread, pyqtSignal

class ProgressWorker(QThread):
    progress = pyqtSignal(int)  # Señal para emitir el progreso
    finished = pyqtSignal(str)  # Señal para indicar que el proceso terminó (con algún mensaje opcional)
    error = pyqtSignal(str)     # Señal para manejar errores

    def __init__(self, simulated=True):
        super().__init__()
        self._running = True
        self.simulated = simulated  # Controla si el progreso es simulado o real
        self.real_progress_value = 0  # Para el modo real

    def run(self):
        if self.simulated:
            # Modo simulado: genera progreso automáticamente
            value = 0
            while self._running:
                value += 10
                if value > 100:
                    value = 0
                self.progress.emit(value)
                self.msleep(200)  # Simula el progreso cada 200ms
        else:
            # Modo real: espera a que se emitan señales de progreso
            while self._running:
                self.msleep(50)  # Evita que el hilo consuma demasiados recursos

    def stop(self):
        self._running = False

    def emit_progress(self, value):
        """Emite progreso manualmente en modo real."""
        self.real_progress_value = value
        self.progress.emit(value)

    def emit_finished(self, message="Proceso completado"):
        """Emite la señal de finalización."""
        self.finished.emit(message)
        self.stop()

    def emit_error(self, error_message):
        """Emite la señal de error."""
        self.error.emit(error_message)
        self.stop()
