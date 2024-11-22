from PyQt6 import QtWidgets, QtCore
from App.Controller.ruleManegementController import RuleController
from App.Controller.databaseController import DatabaseController

class Ui_ManageRulesDialog(object):
    def __init__(self, controller, main_window=None, is_file=True, database_name=None, from_rule_configuration=False):
        self.controller = DatabaseController()  
        self.main_window = main_window
        self.is_file = is_file  
        self.database_name = database_name
        self.rule_controller = RuleController()  
        self.from_rule_configuration = from_rule_configuration  

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setWindowTitle("Gestionar Reglas")
        Dialog.resize(600, 400)
        Dialog.setStyleSheet("background-color: rgb(8,172,20);")

        self.typeLabel = QtWidgets.QLabel(Dialog)
        self.typeLabel.setText("Tipo de Archivo o Tabla:")
        self.typeLabel.setGeometry(QtCore.QRect(20, 20, 150, 25))
        self.typeLabel.setStyleSheet("color: white;")

        self.typeComboBox = QtWidgets.QComboBox(Dialog)
        self.typeComboBox.setGeometry(QtCore.QRect(180, 20, 200, 25))
        self.typeComboBox.setStyleSheet("background-color: white; color: black")
        
        if self.from_rule_configuration:
            self.load_all_types()
        else:
            self.load_types_based_on_context()  

        self.typeComboBox.currentIndexChanged.connect(self.load_rules_for_file_type)

        self.poolRulesLabel = QtWidgets.QLabel(Dialog)
        self.poolRulesLabel.setText("Reglas Disponibles:")
        self.poolRulesLabel.setGeometry(QtCore.QRect(20, 60, 150, 25))
        self.poolRulesLabel.setStyleSheet("color: white;")

        self.poolRulesList = QtWidgets.QListWidget(Dialog)
        self.poolRulesList.setGeometry(QtCore.QRect(20, 90, 250, 200))
        self.poolRulesList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")

        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setGeometry(QtCore.QRect(280, 140, 40, 30))
        self.addButton.setText("→")
        self.addButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.addButton.clicked.connect(self.add_rule)

        self.removeButton = QtWidgets.QPushButton(Dialog)
        self.removeButton.setGeometry(QtCore.QRect(280, 190, 40, 30))
        self.removeButton.setText("←")
        self.removeButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.removeButton.clicked.connect(self.remove_rule)

        self.appliedRulesLabel = QtWidgets.QLabel(Dialog)
        self.appliedRulesLabel.setText("Reglas Seleccionadas:")
        self.appliedRulesLabel.setGeometry(QtCore.QRect(330, 60, 150, 25))
        self.appliedRulesLabel.setStyleSheet("color: white;")

        self.appliedRulesList = QtWidgets.QListWidget(Dialog)
        self.appliedRulesList.setGeometry(QtCore.QRect(330, 90, 250, 200))
        self.appliedRulesList.setStyleSheet("background-color: white; color: black; border: 1px solid black;")

        self.acceptButton = QtWidgets.QPushButton(Dialog)
        self.acceptButton.setGeometry(QtCore.QRect(250, 320, 100, 30))
        self.acceptButton.setText("Aceptar")
        self.acceptButton.setStyleSheet("background-color: white; color: black; border-radius: 4px;")
        self.acceptButton.clicked.connect(self.accept_changes)

        self.load_all_rules()  
        self.load_rules_for_file_type()  

    def load_all_types(self):
        file_types = ["CSV", "XLSX", "TXT"]
        tables = self.controller.get_all_tables()
        self.typeComboBox.addItems(file_types)
        self.typeComboBox.addItems(tables)

    def load_types_based_on_context(self):
        if self.is_file:
            self.typeComboBox.addItems(["CSV", "XLSX", "TXT"])
        else:
            all_tables = self.controller.get_all_tables()  
            self.typeComboBox.addItems(all_tables)

    def load_all_rules(self):
        self.all_rules = self.rule_controller.get_available_rules()  
        self.poolRulesList.clear()
        self.poolRulesList.addItems(self.all_rules)

    def load_rules_for_file_type(self):
        current_type = self.typeComboBox.currentText()
        if current_type in ["CSV", "XLSX", "TXT"]:
            rules = self.rule_controller.get_rules_for_file_type(current_type)
        else:
            rules = self.controller.get_parameterOptionsWithDescription(current_type)
        
        self.appliedRulesList.clear()
        self.appliedRulesList.addItems([rule['rule'] for rule in rules])

    def add_rule(self):
        selected_rule = self.poolRulesList.currentItem()
        if selected_rule:
            rule_text = selected_rule.text()
            applied_rules = [self.appliedRulesList.item(i).text() for i in range(self.appliedRulesList.count())]
    
            if not self.rule_controller.rule_exists_in_applied(rule_text, applied_rules):
                if self.typeComboBox.currentText() in ["CSV", "XLSX", "TXT"]:
                    self.is_file = True
                else:
                    self.is_file = False
                self.appliedRulesList.addItem(rule_text)
                self.rule_controller.add_rule(self.typeComboBox.currentText(), rule_text, "Descripcion aqui", self.is_file)
                self.rule_controller._save_rules_to_file()  
                self.load_all_rules()  

    def remove_rule(self):
        selected_rule = self.appliedRulesList.currentItem()
        if selected_rule:
            rule_text = selected_rule.text()
            self.appliedRulesList.takeItem(self.appliedRulesList.row(selected_rule))
            self.rule_controller.remove_rule(self.typeComboBox.currentText(), rule_text, self.is_file)
            self.rule_controller._save_rules_to_file() 
            self.load_all_rules()  

    def accept_changes(self):
        selected_rules = [self.appliedRulesList.item(i).text() for i in range(self.appliedRulesList.count())]
        if self.main_window:
            source_type = "file" if self.is_file else "table"
            self.main_window.update_summary_of_options_table(selected_rules, source_type)
        self.Dialog.accept()
