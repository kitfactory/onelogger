"""
Example usage of OneLogger demonstrating exception logging.
例外ロギングを示すOneLoggerの利用例

This example loads configuration from the .env file located in this folder.
この例では、このフォルダ内にある .env ファイルから設定を読み込みます。
"""

from oneenv import load_dotenv, dotenv_values
import os

# Load .env file from the current directory (examples folder)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
print("Loaded .env values:", dotenv_values(dotenv_path)) 

from onelogger import Logger

# Retrieve a configured logger instance / 設定済みのロガーインスタンスを取得する
logger = Logger.get_logger("example_logger")

# Log an informational message / INFOレベルのメッセージをログに記録する
logger.info("This is an informational message. / これは情報メッセージです。")

try:
    # Example code that raises an exception / 例外を発生させるサンプルコード
    result = 1 / 0
except Exception as e:
    # Log the exception including stack trace / 例外のスタックトレースを含めてログに記録する
    logger.exception("An exception occurred while performing a division. / 除算処理中に例外が発生しました。")

# If asynchronous logging is enabled, remember to shutdown the listener at exit
# 非同期ロギング有効時は、プログラム終了時に shutdown() を呼び出すこと
# For example:
# my_logger = Logger.get_logger("example_logger")
# my_logger.shutdown() 