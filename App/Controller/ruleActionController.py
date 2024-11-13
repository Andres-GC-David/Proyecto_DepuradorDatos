import re
from PyQt6 import QtCore, QtGui, QtWidgets
class RuleActionController:
    def __init__(self):
        self.phone_length = None
        self.convert_zero = False
        self.custom_null_value = None
        self.null_or_replace = None
        self.replace_value = None
        self.phone_format = None
        self.custom_format = None
        self.accepted = False

    def set_phone_length_validation(self, is_checked, length=None):
        self.phone_length = length if is_checked else None

    def set_convert_zero_to_null(self, is_checked):
        self.convert_zero = is_checked

    def set_custom_null_value(self, is_checked, value=None):
        self.custom_null_value = value if is_checked else None

    def set_null_or_replace(self, action, replace_value=None):
        self.null_or_replace = action
        if action == "Reemplazar con valor personalizado":
            self.replace_value = replace_value 
        else:
            self.replace_value = None


    def set_phone_format(self, apply_format, format_type=None, custom_format=None):
        self.phone_format = format_type if apply_format else None
        self.custom_format = custom_format if format_type == "Formato personalizado" else None

    def generate_description(self):
        description = []
        
        if self.phone_length:
            description.append(f"Validar longitud de los teléfonos (Longitud: {self.phone_length})")
        if self.convert_zero:
            description.append("Convertir a nulo teléfonos con 0 o 00")
        if self.custom_null_value:
            description.append(f"Convertir a nulo si coincide con '{self.custom_null_value}'")
        if self.null_or_replace == "Reemplazar con valor personalizado" and self.replace_value:
            description.append(f"Reemplazar valor con '{self.replace_value}' en vez de nulo")
        if self.phone_format == "Sin separadores":
            description.append("Convertir a formato sin separadores")
        elif self.phone_format == "Formato personalizado" and self.custom_format:
            description.append(f"Convertir a formato personalizado: {self.custom_format}")
        
        if not description:
            QtWidgets.QMessageBox.warning(None, "Error", "Seleccione al menos una opcion de validación.")
            return
        
        return "; ".join(description) if description else "Modificación pendiente"

    def validate_custom_format(self, custom_format):
        return True

    def accept(self):
        self.accepted = True

    def reject(self):
        self.accepted = False

    def is_accepted(self):
        return self.accepted
