from PySide6 import QtCore, QtWidgets


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Ошибка")
        self.setFixedSize(520, 140)
        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
        )

        self.setStyleSheet("""
            QDialog {
                background: #FFFFFF;
                border-radius: 8px;
                border: 1px solid #CCCCCC;
            }

            QLabel {
                color: #333333;
                font-size: 14px;
                font-weight: normal;
                padding: 0 20px;
            }

            QPushButton {
                background-color: transparent;
                color: #005BBB;
                border: 1px solid #005BBB;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 600;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #E6F0FF;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        label = QtWidgets.QLabel(message)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        button = QtWidgets.QPushButton("ОК")
        button.clicked.connect(self.accept)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setFixedHeight(34)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def show_dialog(self):
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        self.exec()
