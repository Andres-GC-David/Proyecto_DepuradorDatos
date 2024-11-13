from PyQt6 import QtWidgets

class RuleActionCedulaController:
    def __init__(self):
        self.remove_hyphen = False
        self.remove_zero = False
        self.remove_both = False
        self.validate_format = False
        self.format = None
        self.apply_format = False
        self.custom_format = None
        self.accepted = False

    def set_remove_hyphen(self, is_checked):
        self.remove_hyphen = is_checked

    def set_remove_zero(self, is_checked):
        self.remove_zero = is_checked

    def set_remove_both(self, is_checked):
        self.remove_both = is_checked

    def set_validate_format(self, is_checked, format=None):
        self.validate_format = is_checked
        if is_checked:
            self.format = format
        else:
            self.format = None

    def set_apply_format(self, is_checked, custom_format=None):
        self.apply_format = is_checked
        if is_checked:
            self.custom_format = custom_format
        else:
            self.custom_format = None

    def generate_description(self):
        description = []
        if self.remove_both:
            description.append("Eliminar ambos separadores ('-' y '0')")
        else:
            if self.remove_hyphen:
                description.append("Eliminar separador '-' de cédulas")
            if self.remove_zero:
                description.append("Eliminar separador '0' de cédulas")

        if self.validate_format and self.format:
            description.append(f"Validar formato de cédula: {self.format}")
        if self.apply_format and self.custom_format:
            description.append(f"Convertir cédula a formato: {self.custom_format}")
            
        if not description:
            QtWidgets.QMessageBox.warning(None, "Error", "Seleccione al menos una opción de validación.")
            return
        return "; ".join(description) if description else "Sin modificaciones específicas"

    def accept(self):
        self.accepted = True

    def reject(self):
        self.accepted = False

    def is_accepted(self):
        return self.accepted
