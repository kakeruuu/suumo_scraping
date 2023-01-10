import pandas as pd

from modules.move_csv import move_csv
from process.bot.run import run_bot
from setting import LocalPaths
from utils.df import DataFrames


def browser_control_management(target_info_df: pd.DataFrame, local_dir: LocalPaths):

    header = target_info_df.columns.tolist()
    header.append("エラー内容")
    error_list = DataFrames(header=header)

    
    for row in target_info_df.iterrows():
        # row: tuple[Label, Series] → row[1]はSeriesを指定している
        target = target(row[1].to_dict())
        result = run_bot(target, local_dir.csv_dir)

        target_list = target.output_list()
        target_list.append(result)

        error_list.add_df(target_list)

        if result == "success":
            move_csv(local_dir, target.file_name)

    error_list.commit_df()
    error_list.df.to_csv(local_dir.bot_log_path, encoding="cp932", index=False)
