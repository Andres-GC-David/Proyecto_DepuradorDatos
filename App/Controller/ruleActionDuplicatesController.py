from PyQt6 import QtWidgets

class RuleActionDuplicatesController:
    def __init__(self):
        self.remove_duplicates_general = False
        self.remove_duplicates_by_columns = False
        self.selected_columns = []
        self.accepted = False

    def set_remove_duplicates_general(self, value):
        self.remove_duplicates_general = value

    def set_remove_duplicates_by_columns(self, value, columns):
        self.remove_duplicates_by_columns = value
        self.selected_columns = columns

    def set_selected_columns(self, columns):
        self.selected_columns = columns

    def generate_description(self):
        description = []
        if self.remove_duplicates_general:
            description.append("Eliminar duplicados generales")
        if self.remove_duplicates_by_columns and self.selected_columns:
            description.append(f"Eliminar duplicados según las columnas: {', '.join(self.selected_columns)}")

        if not description:
            QtWidgets.QMessageBox.warning(None, "Error", "Seleccione al menos una opción de duplicados.")
            return
        return "; ".join(description)

    def accept(self):
        self.accepted = True

    def reject(self):
        self.accepted = False

    def is_accepted(self):
        return self.accepted

    def get_selected_columns(self):
        return self.selected_columns

    def get_duplication_options(self):
        return {
            "remove_general": self.remove_duplicates_general,
            "remove_by_columns": self.remove_duplicates_by_columns,
            "columns": self.selected_columns
        }
