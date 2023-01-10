import os
from configparser import ConfigParser
from typing import NamedTuple

from utils.date import SetDate


class Setting:
    def __init__(self) -> None:
        self.set_date = SetDate()
        self.config = ConfigParser()
        self.config.read("./config.ini", "UTF-8")
        self.date_yesterday = self.set_date.trans_dt_yesterday()


setting = Setting()


class LocalPaths(NamedTuple):
    """ローカルパスを管理するクラス"""

    


class RemoteInfoPaths(NamedTuple):
    """ローカル以外のパスを管理するクラス"""

    