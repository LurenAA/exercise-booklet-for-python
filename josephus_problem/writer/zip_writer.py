from zipfile import ZipFile
import os
from pathlib import Path

from .csv_writer import write_to_csv

ZIP_SUFFIX = ".zip"
CSV_SUFFIX = ".csv"


def write_to_zip(file_path, data_list, axes):
    if Path(file_path).suffix != ZIP_SUFFIX:
        file_path += ZIP_SUFFIX
    new_pathinfo = Path(file_path)
    nosuffix_file = file_path[:-len(new_pathinfo.suffix)]
    write_to_csv(
        nosuffix_file,
        data_list,
        axes
    )
    _write_to_zip(file_path, nosuffix_file + CSV_SUFFIX)
    os.remove(nosuffix_file + CSV_SUFFIX)


def _write_to_zip(file_path, *inner_files):
    if Path(file_path).suffix != ZIP_SUFFIX:
        file_path += ZIP_SUFFIX
    zip_obj = ZipFile(file_path, 'w')
    # print(file_path, *inner_files)
    # Add multiple files to the zip
    for file in inner_files:
        parent_dir = str(Path(file).parent)
        zip_obj.write(file, file[len(parent_dir):])
    # close the Zip File
    zip_obj.close()


if __name__ == "__main__":
    write_to_zip("zczx.zip", "C:/Users/xgb/Desktop/"
                 "Exercise Booklet for Python/test.csv")
