import json
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить новый блок")
        self.setFixedSize(400, 300)
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
}

QLineEdit {
    background-color: #F9F9F9;
    border: 1px solid #BBBBBB;
    border-radius: 6px;
    padding: 8px;
    font-size: 14px;
    color: #222222;
}

QPushButton {
    background-color: transparent;
    color: #005BBB;
    border: 1px solid #005BBB;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #E6F0FF;
}

  QPushButton#saveButton:hover {
#                 background-color: #3182CE;
#             }

#             QPushButton#cancelButton {
#                 background-color: #E2E8F0;
#                 color: #4A5568;
#             }

#             QPushButton#cancelButton:hover {
#                 background-color: #CBD5E0;
#             }
}
        """)

        layout = QVBoxLayout()

        self.inputs = []
        for label_text in ["Title Project", "Addres", "Password"]:
            label = QLabel(label_text)
            layout.addWidget(label)

            input_field = QLineEdit()
            input_field.setMinimumHeight(40)
            layout.addWidget(input_field)
            self.inputs.append(input_field)

        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_data_on_os(self, title, address, password):
        home = Path.home()
        ssh_client_dir = home / ".ssh_client_data"
        ssh_client_dir.mkdir(parents=True, exist_ok=True)
        file_path = ssh_client_dir / "data.json"

        if not file_path.exists() or file_path.stat().st_size == 0:
            data_list = []
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data_list = json.load(f)
                    if not isinstance(data_list, list):
                        data_list = []
                except json.JSONDecodeError:
                    data_list = []

        new_data = {"title": title, "address": address, "password": password}
        data_list.append(new_data)

        # Записываем обновлённый список обратно
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)

    def get_data(
        self,
    ):
        return [input_field.text() for input_field in self.inputs]
