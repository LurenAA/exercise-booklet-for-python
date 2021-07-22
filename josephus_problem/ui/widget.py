from pathlib import Path

from .table_mode import TableModel
from entity.reader import ExcelReader, ZipReader, CSVReader

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QTableView,
    QStackedLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit
)
from PySide6.QtCore import Qt

XLSX_SUFFIX = ".xlsx"
CSV_SUFFIX = ".csv"
ZIP_SUFFIX = ".zip"
OPEN_FILE_BUTTON_TEXT = "选择文件"
FILE_LABEL_TEXT = "文件名："
FILE_NAME_PATTERN = "*.csv *.xlsx *.zip"
ENTER_BUTTON_TEXT = "确认"
FILE_LINE_PLACEHOLDER = "选择或输入文件名"
ERROR_MESSAGE = "文件名不存在或后缀错误"
ERROR_TITLE = "错误"
READER_SUFFIX_DIC = {
    ".xlsx": ExcelReader,
    ".csv": CSVReader,
    ".zip": ZipReader
}
START_INDEX_LABEL = "开始位置下标:"
START_INDEX_CONDITION = "0 <= x < %d"
INTERVAL_LABEL = "间隔："
INTERVAL_CONDITION = "x != 0"
SAVE_BTN_TEXT = "保存"
GEN_BTN_TEXT = "生成"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainwindow_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        file_layout = QHBoxLayout()

        file_label = QLabel()
        file_label.setText(FILE_LABEL_TEXT)
        self._file_line = QLineEdit()
        self._file_line.setPlaceholderText(FILE_LINE_PLACEHOLDER)
        input_layout.addWidget(file_label)
        input_layout.addWidget(self._file_line)

        file_btn = QPushButton(OPEN_FILE_BUTTON_TEXT)
        file_btn.clicked.connect(self._open_file_dialog)
        enter_btn = QPushButton(ENTER_BUTTON_TEXT)
        enter_btn.clicked.connect(self._enter)
        file_layout.addWidget(file_btn)
        file_layout.addWidget(enter_btn)

        mainwindow_layout.addLayout(input_layout)
        mainwindow_layout.addLayout(file_layout)

        self._widget = QWidget()
        self._widget.setLayout(mainwindow_layout)
        self.setCentralWidget(self._widget)

    def _open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter(FILE_NAME_PATTERN)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec():
            self._file_line.setText(dialog.selectedFiles()[0])

    def _enter(self):
        file_name = self._file_line.text()
        pathinfo = Path(file_name)
        if pathinfo.is_file() and pathinfo.suffix in (
            XLSX_SUFFIX,
            CSV_SUFFIX,
            ZIP_SUFFIX,
        ):
            reader_type = READER_SUFFIX_DIC[pathinfo.suffix]
            reader = reader_type(file_name)
            self._widget.close()
            self._widget = QWidget()
            widget_layout = QVBoxLayout()

            items = reader.read()
            self._item_row = len(items)
            self._item_col = len(items[0])
            self._model = TableModel(items)
            self._table = QTableView()
            self._table.setModel(self._model)

            widget_layout.addWidget(self._table)

            start_index_layout = QHBoxLayout()
            start_index_label = QLabel(START_INDEX_LABEL)
            start_index_line = QLineEdit()
            start_index_line.setPlaceholderText(
                START_INDEX_CONDITION % self._item_row
            )
            start_index_layout.addWidget(start_index_label)
            start_index_layout.addWidget(start_index_line)

            widget_layout.addLayout(start_index_layout)

            interval_layout = QHBoxLayout()
            interval_label = QLabel(INTERVAL_LABEL)
            interval_line = QLineEdit()
            interval_line.setPlaceholderText(INTERVAL_CONDITION)
            interval_layout.addWidget(interval_label)
            interval_layout.addWidget(interval_line)

            final_layout = QHBoxLayout()
            save_btn = QPushButton(SAVE_BTN_TEXT)
            gen_btn = QPushButton(GEN_BTN_TEXT)
            final_layout.addWidget(save_btn)
            final_layout.addWidget(gen_btn)

            widget_layout.addLayout(interval_layout)
            widget_layout.addLayout(final_layout)
            self._widget.setLayout(widget_layout)

            self.setCentralWidget(self._widget)
        else:
            err_mes = QMessageBox()
            err_mes.setWindowTitle(ERROR_TITLE)
            err_mes.setText(ERROR_MESSAGE)
            err_mes.exec()
