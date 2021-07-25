import cmd
from pathlib import Path

from reader.csv_reader import CSVReader
from reader.excel_reader import ExcelReader
from reader.zip_reader import ZipReader
from entity.student import Student
from writer.xlsx_writer import write_to_xlsx
from writer.zip_writer import write_to_zip
from writer.csv_writer import write_to_csv
from jc.josephus_circle import JcSolution

CMD_INTRO = "约瑟夫环命令行应用。输入help或?显示所有命令"
PROMPT = "(jc_shell) "
NO_FILE = "没有选择文件"
XLSX_SUFFIX = ".xlsx"
CSV_SUFFIX = ".csv"
ZIP_SUFFIX = ".zip"
SUFFIX_TUPLE = XLSX_SUFFIX, ZIP_SUFFIX, CSV_SUFFIX
CHOOSE_FILE_SUCCESS = "选择文件成功"
CHOOSE_FILE_FAIL = "文件类型错误"
INPUT_ARG_NUMBER_ERR = "输入参数数量错误"
INPUT_ARG_TYPE_ERR = "输入参数类型错误"
READER_SUFFIX_DIC = {
    ".xlsx": ExcelReader,
    ".csv": CSVReader,
    ".zip": ZipReader
}
SPERATOR = "--------------------------"
CHANGE_SUCCESS = "修改成功"
WRITER_TYPE_DICT = {
    XLSX_SUFFIX: write_to_xlsx,
    ZIP_SUFFIX: write_to_zip,
    CSV_SUFFIX: write_to_csv
}
START_INDEX = "输入开始位置的下标(0 <= X < %d}): "
INTERVAL = "输入间隔(X != 0): "
SAVE_PATH_PROMPT = "输入保存文件位置： "
SAVE_SUCCESS = "保存成功"
FILE_PATH_INPUT = "输入你要操作的文件路径: "
CHOOSE_FILE_HELP = "输入你要操作的文件"
SHOW_FILE_PATH_HELP = "展示你现在当前的文件"
SHOW_FILE_CONTENT_HELP = "展示文件内容"
CHANGE_CONTENT_HELP = "修改数据，按照change_content line attribute value方式进行修改，"
"例如change_content 0 name xxx, 把第0行的name属性改为xxx"
GEN_JC_HELP = "生成约瑟夫环结果"
SAVE_HELP = "保存文件"


class JcShell(cmd.Cmd):
    intro = CMD_INTRO
    prompt = PROMPT

    def __init__(self):
        super().__init__()
        self._file_path = None
        self._stu_list = None

    def do_choose_file(self, arg):
        CHOOSE_FILE_HELP
        file_path = input(FILE_PATH_INPUT)
        pathinfo = Path(file_path)

        if (
            pathinfo.is_file() and
            pathinfo.suffix in SUFFIX_TUPLE
        ):
            self._file_path = file_path
            print(CHOOSE_FILE_SUCCESS)
        else:
            print(CHOOSE_FILE_FAIL)

    def do_show_current_file_path(self, arg):
        SHOW_FILE_PATH_HELP
        if not self._file_path:
            print(NO_FILE)
        else:
            print(f"当前文件为: {self._file_path}")

    def _obtain_stu_list(self):
        if not self._stu_list:
            pathinfo = Path(self._file_path)
            reader_type = READER_SUFFIX_DIC[pathinfo.suffix]
            reader = reader_type(self._file_path)
            raw_data = reader.read()
            self._axes = reader.axes
            self._stu_list = [Student(*item) for item in raw_data]

    def do_show_file_content(self, arg):
        SHOW_FILE_CONTENT_HELP
        if not self._file_path:
            print(NO_FILE)
        else:
            self._obtain_stu_list()
            self._pretty_print(self._stu_list)

    def _pretty_print(self, data_list):
        print(SPERATOR)

        for index, row in enumerate(data_list):
            print(f"|{index}{row}")

        print(SPERATOR)

    def do_change_content(self, arg):
        CHANGE_CONTENT_HELP
        if not self._file_path:
            print(NO_FILE)
            return None

        arg = arg.split()

        if len(arg) != 3:
            print(INPUT_ARG_NUMBER_ERR)
        else:
            index = None
            try:
                index = int(arg[0])
            except Exception:
                print(INPUT_ARG_TYPE_ERR)
                return None

            setattr(self._stu_list[index], arg[1], arg[2])
            print(CHANGE_SUCCESS)

    def do_gen_jc(self, arg):
        GEN_JC_HELP
        if not self._file_path:
            print(NO_FILE)
            return None

        if not self._stu_list:
            self._obtain_stu_list()

        start_index = input(START_INDEX % len(self._stu_list))
        interval = input(INTERVAL)

        try:
            start_index = int(start_index)
            interval = int(interval)
        except Exception:
            print(INPUT_ARG_TYPE_ERR)
            return None

        jc = JcSolution(self._stu_list, start_index, interval)
        self._pretty_print(jc)

    def do_save(self, arg):
        SAVE_HELP
        if not self._file_path:
            print(NO_FILE)
            return None

        if not self._stu_list:
            self._obtain_stu_list()

        save_path = input(SAVE_PATH_PROMPT)
        pathinfo = Path(save_path)

        if not (
            Path(pathinfo.parent).is_dir() and
            pathinfo.suffix in SUFFIX_TUPLE
        ):
            print(CHOOSE_FILE_FAIL)
            return None

        save_type = WRITER_TYPE_DICT[pathinfo.suffix]
        save_type(
            save_path,
            [[stu.name, stu.id] for stu in self._stu_list],
            self._axes
        )
        print(SAVE_SUCCESS)
