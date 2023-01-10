import shutil

from setting import AccountInfoPaths


# クライアントの作成したアカウント情報入力ファイルをローカルにコピー
def copyUserInputsFile():
    account_info = AccountInfoPaths()
    # 共有フォルダ上のファイルをバックグラウンドで開き続けるリスクを回避するため
    shutil.copy(account_info.original_file, account_info.clone_file)


if __name__ == "__main__":
    copyUserInputsFile()
