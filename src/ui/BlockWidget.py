from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class BlockWidget(QFrame):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setStyleSheet("""
BlockWidget {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 12px;
    border: 1px solid #E2E8F0;
}

QLabel {
    color: #222222;
    font-size: 14px;

}

QLabel#title {
    font-size: 16px;
    font-weight: 600;
    color: #111111;
}

QPushButton {
    background-color: transparent;
    color: #005BBB;
    border: 1px solid #005BBB;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #E6F0FF;
}

QPushButton#runButton {
    border-color: #2A9D8F;
    color: #2A9D8F;
}

QPushButton#runButton:hover {
    background-color: #D1F2EB;
}

QPushButton#deleteButton {
    border-color: #E63946;
    color: #E63946;
}

QPushButton#deleteButton:hover {
    background-color: #FAD4D8;
}

        """)

        self.setMaximumHeight(100)

        main_layout = QHBoxLayout()

        data_layout = QVBoxLayout()
        self.title_label = QLabel(data[0])
        self.title_label.setObjectName("title")
        data_layout.addWidget(self.title_label)

        main_layout.addLayout(data_layout, 70)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignTop)

        self.run_button = QPushButton("Run")
        self.run_button.setObjectName("runButton")
        self.run_button.setMinimumHeight(30)

        button_layout.addWidget(self.run_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setMinimumHeight(30)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.setMinimumHeight(30)
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout, 30)

        self.setLayout(main_layout)
