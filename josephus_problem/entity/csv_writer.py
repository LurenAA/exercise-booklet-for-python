import csv
import os
from pathlib import Path

CSV_SUFFIX = ".csv"


def write_to_csv(file_path, data_list, axes):
    if Path(file_path).suffix != CSV_SUFFIX:
        file_path += CSV_SUFFIX
    with open(file_path, "w", encoding="utf-8", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(axes)

        for row in data_list:
            csv_writer.writerow(row)


if __name__ == "__main__":
    write_to_csv("test2adasd", [[1,2],[3,4],[5,6]], ["asd", "asd"])