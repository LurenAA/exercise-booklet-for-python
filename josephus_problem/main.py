from widget import OpenFileWiget

import sys

from PySide6.QtWidgets import QApplication

CSV_TEST_FILE = "test.csv"
EXCEL_TEST_FILE = "test.xlsx"
ZIP_TEST_FILE = "test.zip"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cmd":
        pass
    else:
        app = QApplication()
        widget = OpenFileWiget()
        widget.show()
        app.exec()
