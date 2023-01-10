from collections import deque

import pandas as pd


class DataFrames:
    """DataFrameを簡易的なDBに見立てて管理するためのクラス"""

    def __init__(self, header=None) -> None:
        self.df = ""
        self.list: deque = deque()
        self.header = header

    def commit_df(self):
        add_list = list(self.list)
        self.df = pd.DataFrame(data=add_list, columns=self.header)

    def add_df(self, data: list) -> None:
        self.list.append(data)
