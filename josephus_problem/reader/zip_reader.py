from zipfile import ZipFile
from pathlib import Path

from .reader_template import ReaderTemplate
from .excel_reader import ExcelReader
from .csv_reader import CSVReader

import pandas

XLSX_SUFFIX = ".xlsx"
CSV_SUFFIX = ".csv"
ZIP_SUFFIX = ".zip"


class ZipReader(ReaderTemplate):
    def __init__(
        self,
        file: "str, bytes, ExcelFile, xlrd.Book, path object,file-like object",
        *,
        csv_setting: dict = {},
        excel_setting: dict = {}
    ):
        assert type(csv_setting) == dict and type(excel_setting) == dict

        self._file = file
        self._csv_setting = csv_setting
        self._excel_setting = excel_setting
        self._zipfile = ZipFile(file)
        self._file_name_iter = iter(self._zipfile.namelist())
        self._row_iter = None

        pathinfo = Path(self._zipfile.namelist()[0])
        with self._zipfile.open(self._zipfile.namelist()[0]) as inner_file:
            if pathinfo.suffix == CSV_SUFFIX:
                data_frame = pandas.read_csv(inner_file)
                self.axes = list(data_frame.axes[1])
            else:
                data_frame = pandas.read_excel(inner_file)
                self.axes = list(data_frame.axes[1])

    def __next__(self):
        if self._row_iter is None:
            next_file_flag = True
        else:
            try:
                return next(self._row_iter)
            except StopIteration:
                next_file_flag = True

        while next_file_flag:
            try:
                file = next(self._file_name_iter)
            except StopIteration:
                self._zipfile.close()
                raise StopIteration

            if file.endswith(CSV_SUFFIX):
                self._row_iter = CSVReader(
                    self._zipfile.open(file), **(self._csv_setting)
                )
                next_file_flag = False
            elif file.endswith(XLSX_SUFFIX):
                self._row_iter = ExcelReader(
                    self._zipfile.open(file), **(self._excel_setting)
                )
                next_file_flag = False
            else:
                continue

        return next(self._row_iter)
