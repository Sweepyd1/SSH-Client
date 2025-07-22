import json
from pathlib import Path

from PySide6.QtCore import QDir
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from .ErrorWindow import ErrorDialog


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add New Config")
        self.setFixedSize(500, 400)
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

        key_label = QLabel("Key")
        layout.addWidget(key_label)

        key_layout = QHBoxLayout()

        self.key_line_edit = QLineEdit()
        self.key_line_edit.setMinimumHeight(35)
        self.key_line_edit.setReadOnly(False)
        key_layout.addWidget(self.key_line_edit)

        key_button = QPushButton("Select a Key")
        key_button.setMinimumHeight(30)
        key_layout.addWidget(key_button)

        key_button.clicked.connect(self.select_key_file)

        layout.addLayout(key_layout)
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_data_on_os(self, title, address, password, key_path):
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

        new_data = {
            "title": title,
            "address": address,
            "password": password,
            "key_path": key_path,
        }
        data_list.append(new_data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)

    def check_title_exist(self, data):
        home = Path.home()
        ssh_client_dir = home / ".ssh_client_data"
        ssh_client_dir.mkdir(parents=True, exist_ok=True)
        file_path = ssh_client_dir / "data.json"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                configs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            configs = []

        for config in configs:
            if config.get("title") == data[0]:
                error_window = ErrorDialog("A Config with this name already exists")
                error_window.exec()
                raise

    def get_data(self, check_unique_title: bool):
        data = [input_field.text().strip() for input_field in self.inputs]
        title = data[0]
        address = data[1]
        password = data[2]

        ssh_key_path = self.key_line_edit.text().strip()

        if not title or not address:
            error_window = ErrorDialog("Please fill in 'Title' and 'Address'.")
            error_window.exec()

            dialog = AddDialog(self)
            for i, val in enumerate(data):
                dialog.inputs[i].setText(val)
            dialog.key_line_edit.setText(ssh_key_path)
            dialog.exec()

            new_title = dialog.inputs[0].text().strip()
            new_address = dialog.inputs[1].text().strip()
            new_password = dialog.inputs[2].text().strip()
            new_ssh_key_path = dialog.key_line_edit.text().strip()

            if not new_title or not new_address:
                return None

            if not new_password and not new_ssh_key_path:
                error_window = ErrorDialog("Either 'Password' or 'Key' must be filled.")
                error_window.exec()
                return None

            return [new_title, new_address, new_password, new_ssh_key_path]

        if not password and not ssh_key_path:
            error_window = ErrorDialog("Either 'Password' or 'Key' must be filled.")
            error_window.exec()

            dialog = AddDialog(self)
            for i, val in enumerate(data):
                dialog.inputs[i].setText(val)
            dialog.key_line_edit.setText(ssh_key_path)
            dialog.exec()

            new_password = dialog.inputs[2].text().strip()
            new_ssh_key_path = dialog.key_line_edit.text().strip()

            if not new_password and not new_ssh_key_path:
                return None

            return [title, address, new_password, new_ssh_key_path]

        if check_unique_title:
            self.check_title_exist(data=[title])

        return [title, address, password, ssh_key_path]

    def select_key_file(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)

        dialog.setFilter(QDir.AllEntries | QDir.Hidden | QDir.NoDotAndDotDot)

        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            self.key_line_edit.setText(file_path)
