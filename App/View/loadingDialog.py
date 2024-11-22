from PyQt6 import QtWidgets, QtCore, QtGui

class LoadingDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Cargando...")
        self.setFixedSize(320, 140)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog |
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False)

        self.setStyleSheet("""
            QDialog {
                background-color: rgb(240, 240, 240);
                border: 1px solid rgb(200, 200, 200);
                border-radius: 8px;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QProgressBar {
                border: 1px solid gray;
                border-radius: 5px;
                text-align: center;
                background: rgb(220, 220, 220);
            }
            QProgressBar::chunk {
                background: rgb(8,172,20);
                width: 10px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QtWidgets.QLabel("Cargando datos, por favor espera...", self)
        self.label.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.cancel_button = QtWidgets.QPushButton("Cancelar", self)
        self.cancel_button.setVisible(False) 
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.center_to_parent(parent)

        self.offset = None

    def center_to_parent(self, parent):
        if parent:
            parent_geometry = parent.geometry()
            self.move(
                parent_geometry.center().x() - self.width() // 2,
                parent_geometry.center().y() - self.height() // 2
            )
        else:
            screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
            self.move(
                screen_geometry.center().x() - self.width() // 2,
                screen_geometry.center().y() - self.height() // 2
            )

    def update_progress(self, value: int, text: str = None):
        self.progress_bar.setValue(value)
        if text:
            self.label.setText(text)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.offset)
            self.offset = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.offset = None
        
    def reset_progress(self):
        self.progress_bar.setValue(0)
