from datetime import datetime, timedelta


class SetDate:
    def __init__(self) -> None:
        self.dt_now = datetime.now()
        self.dt_yesterday = self.dt_now - timedelta(1)

    def trans_dt_now(self, trans_str: str = "%Y%m%d") -> str:
        """
        trans_str -> default: "%Y%m%d"
        """
        dt_now_str = self.dt_now.strftime(trans_str)
        return dt_now_str

    def trans_dt_yesterday(self, trans_str: str = "%Y%m%d") -> str:
        """
        trans_str -> default: "%Y%m%d"
        """
        dt_yesterday_str = self.dt_yesterday.strftime(trans_str)
        return dt_yesterday_str
