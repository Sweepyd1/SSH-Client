import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .BlockWidget import BlockWidget
from .Dialog import AddDialog
from .ErrorWindow import ErrorDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Client")

        self.setFixedSize(900, 900)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F7FA;
            }

            QPushButton#addButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 16px;
                font-weight: 600;
                box-shadow: 0 2px 6px rgba(74, 144, 226, 0.3);
            }

            QPushButton#addButton:hover {
                background-color: #3A7BC8;
            }

            QPushButton#addButton:pressed {
                background-color: #2A6BB4;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        self.add_button = QPushButton("+ Add New SSH Connection")
        self.add_button.setObjectName("addButton")
        self.add_button.setMinimumHeight(50)
        self.add_button.clicked.connect(self.show_add_dialog)
        main_layout.addWidget(self.add_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: #E8ECF1;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #A0AEC0;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #718096;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background:#EFEFEF")

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        self.setup_blocks()

    def show_add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data(check_unique_title=True)

            if data is None:
                return

            dialog.save_data_on_os(data[0], data[1], data[2], data[3])
            self.add_block(data)

    def get_all_configs(self):
        home = Path.home()
        ssh_client_dir = home / ".ssh_client_data"
        ssh_client_dir.mkdir(parents=True, exist_ok=True)
        file_path = ssh_client_dir / "data.json"

        if not file_path.exists() or file_path.stat().st_size == 0:
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения конфигураций: {e}")
            return []

    def setup_blocks(self):
        configs = self.get_all_configs()

        if isinstance(configs, dict):
            configs = [configs]

        for config in configs:
            data_list = [
                config.get("title", ""),
                config.get("address", ""),
                config.get("password", ""),
                config.get("key_path", ""),
            ]
            self.add_block(data_list)

    def add_block(self, data):
        block = BlockWidget(data)

        block.delete_button.clicked.connect(lambda _, b=block: self.delete_block(b))
        block.edit_button.clicked.connect(lambda _, b=block: self.edit_block(b))
        block.run_button.clicked.connect(lambda _, b=block: self.run_block(b))

        self.scroll_layout.addWidget(block)

    def delete_block(self, block):
        block.hide()
        block.deleteLater()

        home = Path.home()
        ssh_client_dir = home / ".ssh_client_data"
        file_path = ssh_client_dir / "data.json"

        if not file_path.exists() or file_path.stat().st_size == 0:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data_list = json.load(f)
                if not isinstance(data_list, list):
                    data_list = []
            except json.JSONDecodeError:
                data_list = []

        target_title = block.data[0]

        new_data_list = [
            item for item in data_list if item.get("title", "") != target_title
        ]

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_data_list, f, ensure_ascii=False, indent=4)

    def edit_block(self, block):
        dialog = AddDialog(self)

        dialog.inputs[0].setText(block.data[0])
        dialog.inputs[1].setText(block.data[1])
        dialog.inputs[2].setText(block.data[2])
        dialog.key_line_edit.setText(block.data[3])

        old_title = block.data[0]

        if dialog.exec() == QDialog.Accepted:
            new_data = dialog.get_data(check_unique_title=False)

            block.data = new_data
            block.title_label.setText(new_data[0])

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

            data_list = [
                item for item in data_list if item.get("title", "") != old_title
            ]

            data_list.append(
                {
                    "title": new_data[0],
                    "address": new_data[1],
                    "password": new_data[2],
                    "key_path": new_data[3],
                }
            )

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)

    def get_terminal(self):
        terminals = [
            "kitty",
            "gnome-terminal",
            "alacritty",
            "konsole",
            "xfce4-terminal",
            "xterm",
        ]
        for term in terminals:
            if shutil.which(term):
                return term

        return None

    def run_block(self, block):
        address = block.data[1]
        password = block.data[2]
        ssh_key = block.data[3]

        platform = sys.platform

        if platform.startswith("linux"):
            if ssh_key:
                ssh_command = f"ssh -i {ssh_key} {address}"
            else:
                ssh_command = f"sshpass -p '{password}' ssh {address}"

            term = self.get_terminal()

            if term == "gnome-terminal":
                cmd = [term, "--", "bash", "-c", f"{ssh_command}; exec bash"]
            elif term in ("konsole", "xfce4-terminal"):
                cmd = [term, "-e", f"bash -c '{ssh_command}; exec bash'"]
            elif term in ("alacritty", "kitty", "xterm"):
                cmd = [term, "-e", "bash", "-c", f"{ssh_command}; exec bash"]
            else:
                cmd = [term, "-e", "bash", "-c", f"{ssh_command}; exec bash"]
            subprocess.Popen(cmd)

        else:
            if platform.startswith("win"):
                putty_path = os.path.join("helpers", "putty.exe")

                if ssh_key:
                    ssh_command = [putty_path, "-ssh", address, "-i", ssh_key]
                else:
                    ssh_command = [putty_path, address, "-pw", password]

                subprocess.Popen(ssh_command)

            else:
                if platform == "darwin":
                    if ssh_key:
                        ssh_command = f'ssh -i "{ssh_key}" {address}'
                    else:
                        ssh_command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {address}"
                    escaped_ssh_command = ssh_command.replace('"', '\\"')
                    applescript = f'tell application "Terminal" to do script "{escaped_ssh_command}"'
                    try:
                        subprocess.Popen(["osascript", "-e", applescript])
                    except Exception as e:
                        print(f"Ошибка при запуске osascript: {e}")
