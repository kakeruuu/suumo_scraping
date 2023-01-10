import os
import shutil

from setting import LocalPaths


class NoneDownloadCsvFile(Exception):
    pass


def move_csv(tmp_dir: LocalPaths, new_file_name):
    if len(os.listdir(tmp_dir.csv_dir)) == 0:
        raise NoneDownloadCsvFile

    target_file = f"{tmp_dir.csv_dir}\\{os.listdir(tmp_dir.csv_dir)[0]}"
    rename_file = f"{tmp_dir.yesterday_dir}\\{new_file_name}.csv"
    shutil.move(target_file, rename_file)
