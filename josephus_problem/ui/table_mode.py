import sys

from entity.xlsx_writer import write_to_xlsx
from entity.zip_writer import write_to_zip
from entity.csv_writer import write_to_csv

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView

XLSX_SUFFIX = ".xlsx"
CSV_SUFFIX = ".csv"
ZIP_SUFFIX = ".zip"
WRITER_TYPE_DICT = {
    XLSX_SUFFIX: write_to_xlsx,
    ZIP_SUFFIX: write_to_zip,
    CSV_SUFFIX: write_to_csv
}


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def save_file(self, file_path, file_type, axes):
        write_type = WRITER_TYPE_DICT[file_type]
        write_type(file_path, self._data, axes)
