import pdb
from configparser import ConfigParser

from process.accounts import Account
from process.bot.run import run_bot

# テスト参考
# https://www.magata.net/memo/index.php?pytest%C6%FE%CC%E7
if __name__ == "__main__":
    config = ConfigParser()
    config.read("./config.ini", encoding="utf-8")
    test_account_items = config.items("Test")
    test_account_dict = dict(test_account_items)

    account = Account(test_account_dict)
    success = run_bot(account, test_account_dict["DEFAULT_DOWNLOAD_DIR_PATH"])
