from abc import ABC, abstractmethod
from zipfile import ZipFile
from pathlib import Path

import pandas

CSV_END = "csv"
EXCEL_END = "xlsx"
XLSX_SUFFIX = ".xlsx"
CSV_SUFFIX = ".csv"
ZIP_SUFFIX = ".zip"


class ReaderBase(ABC):
    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def read(self, line_num):
        pass

    @abstractmethod
    def readline(self):
        pass


class ReaderTemplate(ReaderBase):
    def _read_type(self, file, cols_list):
        raise NotImplementedError("_read_type must be defined in subclass")

    def __init__(
        self,
        file: "str, bytes, ExcelFile, xlrd.Book, path object,file-like object",
        *,
        cols_list: "list of col index" = None
    ):
        assert (
            isinstance(cols_list, list)
            or cols_list is None
        )

        self._data_frame = self._read_type(
            file,
            cols_list=cols_list
        )

        self._col_titles = self._data_frame.columns.array
        self._row_iter = self._data_frame.itertuples(False)
        # self.axes = list(self._data_frame.axes[1])

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self._row_iter)
        return [getattr(row, title) for title in self._col_titles]

    def readline(self):
        try:
            return self.__next__()
        except StopIteration:
            return []

    def read(self, line_num=-1):
        assert isinstance(line_num, int)

        if line_num < 0:
            return [row for row in self]
        elif line_num == 0:
            return []
        else:
            result_list = []
            for i in range(line_num):
                try:
                    result_list.append(self.__next__())
                except StopIteration():
                    break
            return result_list


class ExcelReader(ReaderTemplate):
    def __init__(
        self,
        file,
        *,
        cols_list=None
    ):
        super().__init__(file, cols_list=cols_list)
        self.axes = list(self._data_frame.axes[1])

    def _read_type(self, file, cols_list):
        return pandas.read_excel(
            file,
            usecols=cols_list)


class CSVReader(ReaderTemplate):
    def __init__(
        self,
        file,
        *,
        cols_list=None
    ):
        super().__init__(file, cols_list=cols_list)
        self.axes = list(self._data_frame.axes[1])

    def _read_type(self, file, cols_list):
        return pandas.read_csv(file, usecols=cols_list)


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

            if file.endswith(CSV_END):
                self._row_iter = CSVReader(
                    self._zipfile.open(file), **(self._csv_setting)
                )
                next_file_flag = False
            elif file.endswith(EXCEL_END):
                self._row_iter = ExcelReader(
                    self._zipfile.open(file), **(self._excel_setting)
                )
                next_file_flag = False
            else:
                continue

        return next(self._row_iter)
