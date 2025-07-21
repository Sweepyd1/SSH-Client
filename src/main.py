import os
import sys

from PySide6.QtGui import (
    QFont,
    QFontDatabase,
)
from PySide6.QtWidgets import QApplication

from ui.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    font_path = os.path.join(
        os.path.dirname(__file__), "fonts", "PressStart2P-Regular.ttf"
    )
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"Ошибка: не удалось загрузить шрифт по пути {font_path}")
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 8)
        app.setFont(font)

    window = MainWindow()

    window.show()
    sys.exit(app.exec())
