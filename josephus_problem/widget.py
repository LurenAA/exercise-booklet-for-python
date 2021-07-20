from functools import partial
import re
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QApplication,
    QLineEdit,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Signal, Slot, QSize

from josephus_circle import JcSolution
from student import Student
from reader import ZipReader, ExcelReader, CSVReader
from xlsx_writer import write_to_xlsx
from csv_writer import write_to_csv
from zip_writer import write_to_zip

READER_SUFFIX_DIC = {
    ".xlsx": ExcelReader,
    ".csv": CSVReader,
    ".zip": ZipReader
}
FILE_NAME_PATTERN = "*.csv *.xlsx *.zip"
XLSX_SUFFIX = ".xlsx"
CSV_SUFFIX = ".csv"
ZIP_SUFFIX = ".zip"
NAME_PATTERN_DICT = {
    CSV_SUFFIX: "*.csv",
    XLSX_SUFFIX: "*.xlsx",
    ZIP_SUFFIX: "*.zip"
}


class OpenFileWiget(QWidget):
    def __init__(self):
        super().__init__()
        self._file_items_window = FileItemsWindow()
        btn_dialog = QPushButton("打开文件")
        btn_dialog.clicked.connect(self.open_file_dialog)
        # self.line_edit = QPlainTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(btn_dialog)
        # self.layout.addWidget(self.line_edit)
        self.setLayout(layout)

    @Slot()
    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter(FILE_NAME_PATTERN)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec():
            file_name = dialog.selectedFiles()[0]
            self._file_items_window.show()
            # suffix = re.search(r"\.((zip)|(xlsx)|(csv))", file_name)
            # reader = READER_SUFFIX_DIC[suffix.group(0)](file_name)
            reader = READER_SUFFIX_DIC[Path(file_name).suffix](file_name)
            self.hide()
            self._file_items_window.show_table(
                reader.read(),
                reader.axes,
                file_name
            )


class FileItemsWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.resize(280, 230)

    def show_table(self, items, axes, file_name):
        self._file_name = file_name
        self._axes = axes
        self._height = len(items)
        self._width = len(items[0])
        self._table = QTableWidget()
        self._table.setRowCount(len(items))
        self._table.setColumnCount(len(items[0]))
        # self._table.setHorizontalHeaderLabels(["Name", "Id"])
        start_index_label = QLabel()
        start_index_label.setText(f"开始位置的下标：0 <= x < {len(items)}")
        self._start_index_input = QLineEdit()
        jc_interval_label = QLabel()
        jc_interval_label.setText("约瑟夫环间隔：x != 0")
        self._jc_interval = QLineEdit()
        jc_button = QPushButton("显示约瑟夫环结果")
        self._jc_result = QPlainTextEdit()
        save_button = QPushButton("保存数据")

        for i, (name, code) in enumerate(items):
            item_name = QTableWidgetItem(name)
            item_code = QTableWidgetItem(str(code))
            self._table.setItem(i, 0, item_name)
            self._table.setItem(i, 1, item_code)

        jc_button.clicked.connect(self.show_jc_result)
        save_button.clicked.connect(self.open_file_dialog)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self._table)
        self.layout.addWidget(start_index_label)
        self.layout.addWidget(self._start_index_input)
        self.layout.addWidget(jc_interval_label)
        self.layout.addWidget(self._jc_interval)
        self.layout.addWidget(jc_button)
        self.layout.addWidget(save_button)
        self.layout.addWidget(self._jc_result)
        self.setLayout(self.layout)

    @Slot()
    def show_jc_result(self):
        stu_list = [Student(*items) for items in self._get_list()]

        result = [
            x for x in JcSolution(
                stu_list,
                (int(self._start_index_input.text())
                    if self._start_index_input.text() else 0),
                (int(self._jc_interval.text())
                    if self._jc_interval.text() else 1)
            )
        ]
        self._jc_result.setPlainText(str(result))

    @Slot()
    def open_file_dialog(self):
        dialog = QFileDialog()
        pathinfo = Path(self._file_name)
        dialog.setNameFilter(NAME_PATTERN_DICT[pathinfo.suffix])
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec():
            file_name = dialog.selectedFiles()[0]

            if pathinfo.suffix == XLSX_SUFFIX:
                write_to_xlsx(file_name, self._get_list(), self._axes)
            elif pathinfo.suffix == CSV_SUFFIX:
                write_to_csv(file_name, self._get_list(), self._axes)
            else:
                new_pathinfo = Path(file_name)
                nosuffix_file = file_name[:-len(new_pathinfo.suffix)]
                write_to_csv(
                    nosuffix_file,
                    self._get_list(),
                    self._axes
                )
                write_to_zip(file_name, nosuffix_file + CSV_SUFFIX)
                os.remove(nosuffix_file + CSV_SUFFIX)

    def _get_list(self):
        result_list = []

        for x in range(self._height):
            tmp_stu_params = []
            for y in range(self._width):
                value = self._table.item(x, y).text()
                if re.match(r"\A[0-9]+\Z", value):
                    tmp_stu_params.append(int(value))
                else:
                    tmp_stu_params.append(value)
            result_list.append(tmp_stu_params)

        return result_list
