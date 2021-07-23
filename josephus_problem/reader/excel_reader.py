from pathlib import Path

from .reader_template import ReaderTemplate

import pandas


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
