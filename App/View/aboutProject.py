from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_AboutProject(object):
    def setupUi(self, AboutWindow):
        AboutWindow.setObjectName("AboutWindow")
        AboutWindow.resize(500, 600)  
        AboutWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        AboutWindow.setWindowTitle("Acerca del Proyecto")

        self.centralwidget = QtWidgets.QWidget(AboutWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)


        self.logoLabel = QtWidgets.QLabel(parent=self.centralwidget)
        pixmap = QtGui.QPixmap("App/Images/DepuradorDatosLogo.png") 
        scaled_pixmap = pixmap.scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.logoLabel.setPixmap(scaled_pixmap)
        self.logoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.logoLabel)


        self.titleLabel = QtWidgets.QLabel("Depurador de Datos", parent=self.centralwidget)
        self.titleLabel.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Weight.Bold))
        self.titleLabel.setStyleSheet("color: rgb(8, 172, 20);")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.titleLabel)


        self.separator = QtWidgets.QFrame(parent=self.centralwidget)
        self.separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.main_layout.addWidget(self.separator)


        self.infoLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.infoLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.infoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setText(
            "<b>Desarrollador:</b> Andres David Gutierrez Corales<br>"
            "<b>Nombre:</b> DepuradorDatosApp<br>"
            "<b>Versión:</b> 1.0<br>"
            "<b>Desarrollado en:</b> Python 3.11.3<br>"
            "<b>Fecha de lanzamiento:</b> 21-11-2024<br>"
            "<b>Contacto:</b> <a href='mailto:adavid0902@gmail.com'>adavid0902@gmail.com</a><br>"
        )
        self.infoLabel.setOpenExternalLinks(True)  
        self.main_layout.addWidget(self.infoLabel)


        self.rightsLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.rightsLabel.setFont(QtGui.QFont("Segoe UI", 12))
        self.rightsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rightsLabel.setStyleSheet("color: rgb(120, 120, 120);")
        self.rightsLabel.setWordWrap(True)
        self.rightsLabel.setText(
            "© 2024 Coopeguanacaste R.L.\nTodos los derechos reservados."
        )
        self.main_layout.addWidget(self.rightsLabel)

        # Botón de cierre
        self.closeButton = QtWidgets.QPushButton("Cerrar", parent=self.centralwidget)
        self.closeButton.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(8, 172, 20);
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgb(6, 140, 18);
            }
            QPushButton:pressed {
                background-color: rgb(4, 120, 16);
            }
        """)
        self.closeButton.setFixedSize(100, 40)
        self.closeButton.clicked.connect(AboutWindow.close)
        self.main_layout.addWidget(self.closeButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        AboutWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(AboutWindow)
