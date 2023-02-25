import os

import pandas as pd


# 最終的にWebページから取得できるようにしたいからとりあえず、CSV保存用フォルダを別途作成する
def list2csv(
    list: list[list], header: list = "", delete_cols: list = ""
) -> pd.DataFrame:
    if header == "":
        df = pd.DataFrame(list)
    else:
        df = pd.DataFrame(list, header)
    # 空白以外の値が入っている列のみ抽出
    df = df.replace("\xa0", "", regex=True)
    df = df.loc[:, (df != "").any(axis=0)]
    # delete_colsはインデックス番号指定で削除できるようにする
    if delete_cols != "":
        df = df.drop(df.columns[delete_cols], axis=1)

    df.to_csv(f"{os.curdir}/src/csv/property_list.csv")
    return df
