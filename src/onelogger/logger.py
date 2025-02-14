"""
Core logger implementation
コアロガーの実装
"""

import os
import sys
if sys.version_info >= (3, 13):
    import logging
    from logging import getLogger, StreamHandler, Formatter
    LOGGER_LIB = logging
else:
    import picologging
    from picologging import getLogger, StreamHandler, Formatter
    LOGGER_LIB = picologging
from oneenv import load_dotenv
import json

# ---------------------------------------------------------------------
# PlainFormatter
# ログメッセージ用のプレーンテキストフォーマッター
# ---------------------------------------------------------------------
class PlainFormatter(Formatter):
    """
    Plain text formatter for logging messages.
    ログメッセージ用のプレーンテキストフォーマッター。
    
    Args:
        fmt (str): Format string / フォーマット文字列
        datefmt (str): Date format string / 日付フォーマット文字列
        style (str): Format style, default '%' / フォーマットスタイル（デフォルトは '%'）
        log_stacktrace (bool): Whether to include exception stacktrace / 例外トレースの出力有無
    """
    def __init__(self, fmt=None, datefmt=None, style='%', log_stacktrace=True):
        super().__init__(fmt, datefmt=datefmt, style=style)
        self.log_stacktrace = log_stacktrace

    def formatException(self, ei):
        # If stack trace logging is disabled, return empty string
        # スタックトレースの出力が無効な場合、空文字列を返す
        if not self.log_stacktrace:
            return ""
        return super().formatException(ei)

# ---------------------------------------------------------------------
# JSONFormatter
# ログメッセージ用のJSONフォーマッター
# ---------------------------------------------------------------------
class JSONFormatter(Formatter):
    """
    JSON formatter for logging messages.
    ログメッセージ用のJSONフォーマッター。
    
    Args:
        datefmt (str): Date format string / 日付フォーマット文字列
        log_stacktrace (bool): Whether to include exception stacktrace / 例外トレースの出力有無
    """
    def __init__(self, datefmt=None, log_stacktrace=True):
        # Format string is not used since JSON output is constructed via dict
        # JSON出力は dict で構築するため、fmt は使用しない
        super().__init__(fmt=None, datefmt=datefmt)
        self.log_stacktrace = log_stacktrace

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "logger": record.name,
            "level": record.levelname,
            "message": record.getMessage()
        }
        if record.exc_info and self.log_stacktrace:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# ---------------------------------------------------------------------
# OneLogger
# メインロガーのクラス
# ---------------------------------------------------------------------
class OneLogger:
    """
    Main logger class that provides logging functionality.
    ロギング機能を提供するメインロガークラス。
    
    This class retrieves configuration from environment variables using oneenv,
    sets up appropriate handlers (console, file with rotation), applies custom formatting,
    and supports asynchronous logging.
    このクラスは、oneenv を使用して環境変数から設定を取得し、
    コンソールやファイル（ローテーションあり）のハンドラーを設定、カスタムフォーマットを適用し、
    非同期ロギングにも対応します。
    """
    _instances = {}  # Cache for singleton instances / シングルトンインスタンスのキャッシュ

    @classmethod
    def get_logger(cls, name: str):
        """
        Retrieve a configured logger instance. If already created, returns the cached instance.
        設定済みのロガーインスタンスを取得する。既に作成済みの場合、キャッシュされたインスタンスを返す。
        
        Args:
            name (str): Logger name / ロガーの名前
            
        Returns:
            Logger: Configured logger instance / 設定済みロガーインスタンス
        """
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]._logger

    def __init__(self, name: str):
        """
        Initialize logger with given name and configure according to environment variables.
        指定された名前でロガーを初期化し、環境変数に従って設定を行う。
        
        Args:
            name (str): Logger name / ロガーの名前
        """
        # Load environment variables from .env file
        load_dotenv()
        self._logger = getLogger(name)
        # Disable propagation to prevent duplicate logs / ログの重複出力を防止するため伝播を無効にする
        self._logger.propagate = False
        self._configure_logger()

    def _configure_logger(self) -> None:
        """
        Configure logger by setting level, handlers, format and asynchronous options based on environment variables.
        環境変数に基づいてログレベル、ハンドラー、フォーマット、非同期ロギングオプションを設定する。
        
        Environment Variables / 環境変数:
            LOG_LEVEL: Logging level (DEBUG, INFO, etc.) / ログレベル
            LOG_OUTPUT: Output destination (console, file, both) / 出力先
            LOG_FILE_PATH: File path for file output / ファイル出力用ファイルパス
            LOG_FORMAT: Log format (plain, json) / ログフォーマット
            LOG_TIMESTAMP_FORMAT: Timestamp format / タイムスタンプフォーマット
            LOG_ROTATION_TYPE: Rotation type for file output (size, date) / ログローテーションタイプ
            LOG_MAX_FILE_SIZE: Maximum file size in bytes / 最大ファイルサイズ（バイト単位）
            LOG_BACKUP_COUNT: Number of backup files to keep / バックアップファイルの保持数
            LOG_INCLUDE_PID: Include process id in logs (true/false) / プロセスIDの出力有無
            LOG_INCLUDE_THREAD: Include thread id in logs (true/false) / スレッドIDの出力有無
            LOG_APP_NAME: Application name to include / アプリケーション名
            LOG_STACKTRACE: Include exception stacktrace (true/false) / スタックトレースの出力有無
            LOG_ASYNC: Enable asynchronous logging (true/false) / 非同期ロギングの有効化
            LOG_INCLUDE_SOURCE: Include source information (filename and line number) in logs (true/false) / ソース情報の出力有無
        """
        # Clear any existing handlers
        self._logger.handlers = []

        # Retrieve configuration from environment
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_output = os.getenv("LOG_OUTPUT", "console").lower()
        log_format = os.getenv("LOG_FORMAT", "plain").lower()
        log_ts_format = os.getenv("LOG_TIMESTAMP_FORMAT", "%Y-%m-%d %H:%M:%S")
        rotation_type = os.getenv("LOG_ROTATION_TYPE", "size").lower()
        max_file_size = int(os.getenv("LOG_MAX_FILE_SIZE", "10485760"))
        backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))
        log_include_pid = os.getenv("LOG_INCLUDE_PID", "false").lower() == "true"
        log_include_thread = os.getenv("LOG_INCLUDE_THREAD", "false").lower() == "true"
        log_app_name = os.getenv("LOG_APP_NAME", None)
        log_stacktrace = os.getenv("LOG_STACKTRACE", "true").lower() == "true"
        log_async = os.getenv("LOG_ASYNC", "false").lower() == "true"
        log_include_source = os.getenv("LOG_INCLUDE_SOURCE", "false").lower() == "true"

        # Set logger level using picologging's level attributes
        self._logger.setLevel(getattr(LOGGER_LIB, log_level, LOGGER_LIB.INFO))

        # Create formatter based on the chosen log format
        if log_format == "json":
            formatter = JSONFormatter(datefmt=log_ts_format, log_stacktrace=log_stacktrace)
        else:
            # Build a plain format string with optional source info (filename and line) plus optional PID, thread, and application name.
            format_parts = ["%(asctime)s", "%(name)s"]
            if log_include_source:
                format_parts.append("[%(filename)s:%(lineno)d]")
            if log_app_name:
                format_parts.append(f"[{log_app_name}]")
            if log_include_pid:
                format_parts.append("[PID:%(process)d]")
            if log_include_thread:
                format_parts.append("[TID:%(thread)d]")
            format_parts.append("%(levelname)s:")
            format_parts.append("%(message)s")
            plain_format = " ".join(format_parts)
            formatter = PlainFormatter(plain_format, datefmt=log_ts_format, log_stacktrace=log_stacktrace)

        # Prepare handlers list based on output destination
        handlers = []

        # Console output handler
        if log_output in ("console", "both"):
            ch = StreamHandler()
            ch.setFormatter(formatter)
            handlers.append(ch)

        # File output handler with rotation if required
        if log_output in ("file", "both"):
            file_path = os.getenv("LOG_FILE_PATH", "app.log")
            if sys.version_info >= (3, 13):
                from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
            else:
                from picologging.handlers import TimedRotatingFileHandler, RotatingFileHandler
            if rotation_type == "date":
                # Timed rotation (daily) / 日付ベースのローテーション（毎日）
                fh = TimedRotatingFileHandler(file_path, when="midnight")
            else:
                # Size-based rotation / サイズベースのローテーション
                fh = RotatingFileHandler(file_path, maxBytes=max_file_size, backupCount=backup_count)
            fh.setFormatter(formatter)
            handlers.append(fh)

        # If asynchronous logging is enabled, set up QueueHandler and QueueListener
        if log_async:
            import queue
            from logging.handlers import QueueHandler, QueueListener
            log_queue = queue.Queue(-1)
            q_handler = QueueHandler(log_queue)
            self._logger.addHandler(q_handler)
            # Start the listener with the prepared handlers
            self._listener = QueueListener(log_queue, *handlers, respect_handler_level=True)
            self._listener.start()
        else:
            # Synchronous logging: attach handlers directly
            for handler in handlers:
                self._logger.addHandler(handler)

    def shutdown(self) -> None:
        """
        Shutdown any background listener for asynchronous logging.
        非同期ロギング用のバックグラウンドリスナーをシャットダウンする。
        """
        if hasattr(self, "_listener"):
            self._listener.stop()

    def info(self, message: str) -> None:
        """
        Log message at INFO level
        INFOレベルでメッセージをログに記録する

        Args:
            message (str): Message to log
                         ログに記録するメッセージ
        """
        self._logger.info(message)

    def error(self, message: str) -> None:
        """
        Log message at ERROR level
        ERRORレベルでメッセージをログに記録する

        Args:
            message (str): Message to log
                         ログに記録するメッセージ
        """
        self._logger.error(message) 