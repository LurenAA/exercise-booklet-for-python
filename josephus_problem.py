from collections import deque
from abc import ABC, abstractmethod
from zipfile import ZipFile

import pandas

CSV_TEST_FILE = "test.csv"
EXCEL_TEST_FILE = "test.xlsx"
ZIP_TEST_FILE = "test.zip"
CSV_END = "csv"
EXCEL_END = "xlsx"


class FileTypeError(Exception):
    pass


class Student:
    def __init__(self, name, id):
        assert(type(name) == str and type(id) == int)

        self.name = name
        self.id = id

    def __repr__(self):
        return "{%s:%d}" % (self.name, self.id)


class BaseReader(ABC):
    def __init__(self, file, *read_type_setting1, **read_type_setting2):
        # assert(type(file) == str)

        data_frame = self.__readType(
            file, *read_type_setting1, **read_type_setting2)
        self.col_titles = data_frame.columns.array
        self.row_iter = data_frame.itertuples(False)

    def __next__(self):
        row = next(self.row_iter)
        return [getattr(row, index_name) for index_name in self.col_titles]

    def __iter__(self):
        return self

    @abstractmethod
    def __readType(self, file, *read_type_setting1, **read_type_setting2):
        pass


class ExcelReader(BaseReader):
    def _BaseReader__readType(self, file, *excel_setting1, **excel_setting2):
        return pandas.read_excel(file, *excel_setting1, **excel_setting2)


class CSVReader(BaseReader):
    def _BaseReader__readType(self, file, *csv_setting1, **csv_setting2):
        return pandas.read_csv(file, *csv_setting1, **csv_setting2)


class ZipReader:
    def __init__(self, file, *zip_setting, csv_setting={}, excel_setting={}):
        assert(type(csv_setting) ==
               dict and type(excel_setting) == dict)

        self.__file = file
        self.__csv_setting = csv_setting
        self.__excel_setting = excel_setting
        self.__zipfile = ZipFile(self.__file, *zip_setting)
        self.__file_name_iter = iter(self.__zipfile.namelist())
        self.__iter = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.__iter)
        except Exception:
            try:
                file = next(self.__file_name_iter)
            except StopIteration:
                self.__zipfile.close()
                raise StopIteration

            if file.endswith(CSV_END):
                self.__iter = CSVReader(self.__zipfile.open(file),
                                        **(self.__csv_setting))
            elif file.endswith(EXCEL_END):
                self.__iter = ExcelReader(self.__zipfile.open(file),
                                          **(self.__excel_setting))
            else:
                raise FileTypeError

            return next(self.__iter)


class JcSolution:
    def __init__(self, container, start_index, interval):
        self.__result_list = josephus_circle_solution(
            container, start_index, interval)

    def __iter__(self):
        return iter(self.__result_list)

    def __getittem__(self, x):
        return self.__result_list[x]


def josephus_circle_solution(
     container: "iterable", start_index: int, interval: "nonzeno int") -> list:
    assert(0 <= start_index < len(container))
    assert(interval and type(interval) == int)
    assert(container.__iter__ and container.__iter__().__next__
           or container.__next__ or container.__getitem__)

    deque_cp_from_con = deque(container)
    if interval < 0:
        deque_cp_from_con.reverse()
        interval = -interval
    passed_index = start_index - 1
    result_list = list()
    deque_len = len(deque_cp_from_con)

    while deque_len > 1:
        passed_index = (passed_index + interval) % deque_len
        result_list.append(deque_cp_from_con[passed_index])
        # yield deque_cp_from_con[passed_index]
        del deque_cp_from_con[passed_index]
        passed_index -= 1
        deque_len -= 1

    result_list.append(deque_cp_from_con[0])
    # yield deque_cp_from_con[passed_index]
    return result_list


if __name__ == "__main__":
    # reader = CSVReader(CSV_TEST_FILE)
    # reader = ExcelReader(EXCEL_TEST_FILE)
    reader = ZipReader(ZIP_TEST_FILE)
    # for x in reader:
    #     print(x)
    stu_list = [Student(*x) for x in reader]
    # print(stu_list)
    jc_instance = JcSolution(stu_list, 0, 5)
    # print(jc_instance)
    for x in jc_instance:
        print(x)
