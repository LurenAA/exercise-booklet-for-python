from ui.widget import MainWindow

import sys

from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cmd":
        pass
    else:
        app = QApplication()
        widget = MainWindow()
        widget.show()
        app.exec()
