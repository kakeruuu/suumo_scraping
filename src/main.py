import shutil

from log.docorator import create_logging_critical
from modules.check_header import check_header
from process.control_management import browser_control_management
from setting import AccountInfoPaths, LocalPaths


@create_logging_critical
def main():

    tmp_dir = LocalPaths()
    tmp_dir.make_new_dir()

    account_info = AccountInfoPaths()

    account_info_df = pd.read_csv(account_info.clone_csv_file, encoding="cp932")
    account_info_df = account_info_df.where(account_info_df.notnull(), None)

    # 項目列名に変化があった場合エラーが発生
    check_header(account_info_df)

    # スクレイピング処理の実行
    browser_control_management(account_info_df=account_info_df, local_dir=tmp_dir)

    # 取得したレポートと日付フォルダを共有フォルダにコピー
    shutil.copytree(
        tmp_dir.yesterday_dir,
        account_info.insert_dir,
        dirs_exist_ok=True,
    )


if __name__ == "__main__":
    main()
