from PyQt6 import QtWidgets, QtCore, QtGui
from App.Controller.ruleConfigurationController import RuleConfigurationController
from App.Controller.databaseController import DatabaseController
from App.View.addRule import AddRule  
from App.View.manageRulesDialog import Ui_ManageRulesDialog 
from PyQt6.QtCore import Qt

class RuleConfiguration(object):
    def __init__(self):
        self.controller = RuleConfigurationController()
        self.database_controller = DatabaseController()
        self.non_deletable_rules = [
            "Estandarizacion de Telefonos",
            "Validacion Correos",
            "Estandarizacion de Cedulas",
            "Eliminacion de Duplicados",
        ]

    def setupUi(self, Dialog):
        Dialog.setObjectName("RuleConfigurationDialog")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")
        Dialog.setWindowTitle("Gestión de Reglas de Negocio")

        # Cambiar el título usando geometry
        self.titleLabel = QtWidgets.QLabel("Gestión de Reglas de Negocio", Dialog)
        self.titleLabel.setGeometry(220, 20, 400, 50)
        self.titleLabel.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Weight.Bold))
        self.titleLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # Modificar el botón usando geometry
        self.addRuleButton = QtWidgets.QPushButton("Agregar Regla", Dialog)
        self.addRuleButton.setGeometry(235, 80, 300, 40)
        self.addRuleButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.addRuleButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.addRuleButton.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: rgb(8,172,20);
                border-radius: 10px;
                border: 2px solid rgb(8,172,20);
                padding: 5px 10px;
            }
        """)
        self.addRuleButton.clicked.connect(self.open_add_rule_dialog)

        # Agregar scroll a las reglas dinámicas
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setStyleSheet("background-color: white ;")
        self.scrollArea.setGeometry(20, 140, 760, 400)
        self.scrollArea.setWidgetResizable(True)

        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setGeometry(0, 0, 760, 400)
        
        self.rules_container = QtWidgets.QVBoxLayout(self.scrollWidget)

        self.scrollArea.setWidget(self.scrollWidget)

        self.load_existing_rules()

    def load_existing_rules(self):
        self.clear_layout(self.rules_container)

        rules = self.controller.get_rules()
        burned_rules = [rule for rule in rules if rule['rule'] in self.non_deletable_rules]
        dynamic_rules = [rule for rule in rules if rule['rule'] not in self.non_deletable_rules]

        if burned_rules:
            self.add_section_title("Reglas Generales")
            for rule in burned_rules:
                self.add_rule_item(rule)

        if dynamic_rules:
            self.add_section_title("Reglas Agregadas")
            for rule in dynamic_rules:
                self.add_rule_item(rule)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def add_section_title(self, title):
        section_title = QtWidgets.QLabel(title)
        section_title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        section_title.setStyleSheet("color: rgb(8,172,20);")
        section_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rules_container.addWidget(section_title)

    def add_rule_item(self, rule):
        item_widget = self.create_rule_item(rule)
        self.rules_container.addWidget(item_widget)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.rules_container.addWidget(line)

    def create_rule_item(self, rule):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background-color: white; border-radius: 4px;")
        layout = QtWidgets.QHBoxLayout(widget)

        rule_info = QtWidgets.QVBoxLayout()
        rule_name_label = QtWidgets.QLabel(f"<b>Nombre:</b> {rule['rule']}")
        rule_name_label.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        rule_name_label.setStyleSheet("color: black;")
        rule_description_label = QtWidgets.QLabel(f"<b>Descripción:</b> {rule['description']}")
        rule_description_label.setFont(QtGui.QFont("Segoe UI", 10))
        rule_description_label.setStyleSheet("color: black;")
        rule_info.addWidget(rule_name_label)
        rule_info.addWidget(rule_description_label)

        button_layout = QtWidgets.QHBoxLayout()

        modify_button = self.create_button("Modificar")
        modify_button.clicked.connect(lambda: self.modify_rule(rule))
        button_layout.addWidget(modify_button)

        view_code_button = self.create_button("Ver Código")
        view_code_button.clicked.connect(lambda: self.view_rule_code(rule['rule']))
        button_layout.addWidget(view_code_button)

        if rule['rule'] not in self.non_deletable_rules:
            delete_button = self.create_button("Eliminar", color="red")
            delete_button.clicked.connect(lambda: self.delete_rule(rule['rule']))
            button_layout.addWidget(delete_button)

        layout.addLayout(rule_info)
        layout.addLayout(button_layout)

        return widget


    def create_button(self, text, color="rgb(8,172,20)"):
        button = QtWidgets.QPushButton(text)
        button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        button.setStyleSheet(f"background-color: {color}; color: white;")
        button.setFixedSize(100, 30)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def delete_rule(self, rule_name):
        confirm = QtWidgets.QMessageBox.question(None, "Confirmación", f"¿Está seguro que desea eliminar la regla '{rule_name}'?",
                                                 QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            self.controller.delete_rule(rule_name)
            self.load_existing_rules()

    def modify_rule(self, rule):
        manage_rule_dialog = QtWidgets.QDialog()
        ui = Ui_ManageRulesDialog(controller=self.database_controller, from_rule_configuration=True)  
        ui.setupUi(manage_rule_dialog)
        manage_rule_dialog.exec()  

    def view_rule_code(self, rule_name):
        rule_code = self.controller.get_rule_code(rule_name)
        code_dialog = QtWidgets.QDialog()
        code_dialog.setWindowTitle(f"Código de la regla '{rule_name}'")
        code_dialog.resize(400, 150) 
        layout = QtWidgets.QVBoxLayout(code_dialog)
        
        code_display = QtWidgets.QTextEdit(code_dialog)
        code_display.setPlainText(rule_code)  
        code_display.setReadOnly(True)  
        layout.addWidget(code_display)
        

        code_display.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap) 
        code_display.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        code_display.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        close_button = QtWidgets.QPushButton("Cerrar", code_dialog)
        close_button.clicked.connect(code_dialog.accept)  
        layout.addWidget(close_button)

        code_dialog.exec()


    def open_add_rule_dialog(self, rule=None):
        add_rule_dialog = QtWidgets.QDialog()
        ui = AddRule()  
        ui.setupUi(add_rule_dialog)     
        add_rule_dialog.exec()  
        self.load_existing_rules()

