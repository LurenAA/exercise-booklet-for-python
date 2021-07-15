import unittest

from josephus_circle import JcSolution
from student import Student
from reader import ZipReader, ExcelReader, CSVReader

CSV_TEST_FILE = "test.csv"
EXCEL_TEST_FILE = "test.xlsx"
ZIP_TEST_FILE = "test.zip"


class ReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.readers = [
            CSVReader(CSV_TEST_FILE, cols_list=[0, 1]),
            ExcelReader(EXCEL_TEST_FILE),
            ZipReader(ZIP_TEST_FILE,
                      csv_setting={"cols_list": [0, 1]},
                      excel_setting={"sheet_name": "Sheet1"})
        ]

    def test_init(self):
        self.assertIsInstance(CSVReader(CSV_TEST_FILE), CSVReader)
        self.assertIsInstance(CSVReader(
            CSV_TEST_FILE, cols_list=[0, 1]),
            CSVReader
        )
        with self.assertRaises(AssertionError):
            CSVReader(CSV_TEST_FILE, sheet_name=[])
        self.assertIsInstance(ExcelReader(EXCEL_TEST_FILE), ExcelReader)
        self.assertIsInstance(ExcelReader(
            EXCEL_TEST_FILE, cols_list=[0, 1]), ExcelReader)

    def test_read(self):
        for reader in self.readers:
            result_list = reader.read(-1)
            self.assertGreater(len(result_list), 0)
            self.assertIsInstance(result_list, list)
            self.assertIsInstance(result_list[0], list)
            for row in result_list:
                self.assertIsInstance(row[0], str)
                self.assertIsInstance(row[1], int)

    def test_readline(self):
        for reader in self.readers:
            result = True
            while result:
                result = reader.readline()
                self.assertIsInstance(result, list)
                if result:
                    self.assertEqual(len(result), 2)
                    self.assertIsInstance(result[0], str)
                    self.assertIsInstance(result[1], int)

    def test_iterable(self):
        for reader in self.readers:
            for row in reader:
                self.assertIsInstance(row[0], str)
                self.assertIsInstance(row[1], int)


class JcSolutionTestCase(unittest.TestCase):
    def test_init(self):
        self.assertRaises(AssertionError, JcSolution, -1, 0, 5)
        self.assertRaises(AssertionError, JcSolution, [], 1, 4)
        reader = ExcelReader(EXCEL_TEST_FILE)
        stu_list = [Student(*x) for x in reader]
        self.assertIsInstance(
            JcSolution(stu_list, 0, 5),
            JcSolution)

    def setUp(self):
        reader = ExcelReader(EXCEL_TEST_FILE)
        stu_list = [Student(*x) for x in reader]
        self.jc_instance = JcSolution(stu_list, 0, 5)

    def test_iterable(self):
        for i in range(2):
            jc_iter = iter(self.jc_instance)
            for id in (5, 4, 6, 2, 3, 1):
                self.assertEqual(next(jc_iter).id, id)


class StudentTestCase(unittest.TestCase):
    def test_init(self):
        self.assertRaises(AssertionError, Student, 1, 3)
        self.assertRaises(AssertionError, Student, "asdas", "asd")
        self.assertIsInstance(Student("xgb", 12), Student)

    def test_repr(self):
        self.assertTrue(str(Student("xgb", 12)).startswith('{xgb'))


if __name__ == "__main__":
    unittest.main()
