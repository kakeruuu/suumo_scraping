import sys

import pandas as pd

from log.logging import get_my_logger


class NotCorrectHeaderError(Exception):
    pass


def check_header(target_info_df: pd):
    correct_header = ()
    current_header = target_info_df.columns.tolist()

    
    # 存在しなかった場合、その時点でエラーを出力後、強制終了。
    try:
        for h in current_header:
            if h not in correct_header:
                raise NotCorrectHeaderError("入力項目列名がツール作成時と異なっている可能性があります。")

    except NotCorrectHeaderError as e:
        logger = get_my_logger(__name__)
        logger.info("The specified element may not exist.")
        logger.exception("The detailed error message -", exc_info=e)
        sys.exit(0)
