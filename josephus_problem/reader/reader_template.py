from entity.reader_base import ReaderBase


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
