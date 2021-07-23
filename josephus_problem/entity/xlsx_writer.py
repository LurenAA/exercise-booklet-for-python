import os
from pathlib import Path

import xlsxwriter

XLSX_SUFFIX = ".xlsx"


def write_to_xlsx(file_path, data_list, axes):
    if Path(file_path).suffix != XLSX_SUFFIX:
        file_path += XLSX_SUFFIX
    with open(file_path, "w") as file:
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()

        for column, value in enumerate(axes):
            worksheet.write(0, column, value)
        row = column = 0

        for row in range(1, len(data_list) + 1):
            for column in range(len(data_list[0])):
                worksheet.write(row, column, data_list[row - 1][column])

        workbook.close()


if __name__ == "__main__":
    write_to_xlsx("test2adasd.xlsx", [[1, 2], [3, 4], [5, 6]], ["asd", "asd"])
