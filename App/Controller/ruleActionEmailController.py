from PyQt6 import QtCore, QtGui, QtWidgets
class RuleActionEmailController:
    def __init__(self):
        self.validate_email_format = False
        self.convert_to_lowercase = False
        self.validate_domain = False
        self.allowed_domains = None
        self.validate_separator = False
        self.selected_separator = None
        self.custom_separator = None
        self.invalid_email_value = None 
        self.accepted = False

    def set_validate_email_format(self, value):
        self.validate_email_format = value

    def set_convert_to_lowercase(self, value):
        self.convert_to_lowercase = value

    def set_validate_domain(self, value):
        self.validate_domain = value

    def set_allowed_domains(self, domains):
        self.allowed_domains = domains

    def set_validate_separator(self, value):
        self.validate_separator = value

    def set_selected_separator(self, separator):
        self.selected_separator = separator

    def set_custom_separator(self, separator):
        self.custom_separator = separator
        
    def set_invalid_email_value(self, value):
        self.invalid_email_value = value

    def generate_description(self):
        description = []
        if self.validate_email_format:
            description.append(f"Validar formato de correo (Inválidos como '{self.invalid_email_value or 'null'}')")
        if self.convert_to_lowercase:
            description.append("Convertir correos a minúsculas")
        if self.validate_domain and self.allowed_domains:
            description.append(f"Dominios permitidos: {self.allowed_domains}")
        if self.validate_separator:
            if self.selected_separator == "Separador personalizado" and self.custom_separator:
                description.append(f"Validar correos con separadores personalizados: {self.custom_separator}")
            else:
                description.append(f"Validar correos con {self.selected_separator.lower()}")
                
        if not description:
            QtWidgets.QMessageBox.warning(None, "Error", "Seleccione al menos una opcion de validación.")
            return
        return "; ".join(description) if description else "Sin modificaciones específicas"

    def accept(self):
        self.accepted = True

    def reject(self):
        self.accepted = False

    def is_accepted(self):
        return self.accepted
