from PyQt6.QtCore import QThread, pyqtSignal

class DepurationWorker(QThread):
    progress = pyqtSignal(int)  # Señal para actualizar progreso
    finished = pyqtSignal(object)  # Señal para indicar finalización
    error = pyqtSignal(str)  # Señal para manejar errores

    def __init__(self, rule_depuration_controller, df, rules):
        super().__init__()
        self.rule_depuration_controller = rule_depuration_controller
        self.df = df
        self.rules = rules
        self.modified_df = None

    def run(self):
        try:
            total_steps = len(self.rules)  # Por ejemplo, número de reglas
            for i, rule in enumerate(self.rules, start=1):
                # Aplicar cada regla
                self.df = self.rule_depuration_controller.apply_rule(self.df, rule)
                progress = int((i / total_steps) * 100)
                self.progress.emit(progress)  # Emitir progreso
            self.modified_df = self.df
            self.finished.emit(self.modified_df)  # Emitir resultado final
        except Exception as e:
            self.error.emit(str(e))  # Emitir mensaje de error

