"""
Test cases for OneLogger functionality
OneLoggerの機能テスト
"""

import os
import pytest
from onelogger import Logger
import tempfile
import json
import logging
import time

# ---------------------------------------------------------------------
# Fixtures
# テスト用の共通設定
# ---------------------------------------------------------------------
@pytest.fixture
def temp_log_file():
    """
    Create a temporary log file for testing.
    テスト用の一時的なログファイルを作成する。
    """
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_path = f.name
    yield temp_path
    # Shutdown logging to close file handlers before cleanup / クリーンアップ前にファイルハンドラを閉じるため、logging.shutdownを実施
    logging.shutdown()
    if os.path.exists(temp_path):
        # ファイルがロックされる場合があるため、リトライ処理を行う
        for _ in range(10):
            try:
                os.remove(temp_path)
                break
            except PermissionError:
                time.sleep(0.1)

@pytest.fixture
def env_setup(temp_log_file):
    """
    Set up environment variables for testing.
    テスト用の環境変数を設定する。
    """
    original_env = dict(os.environ)
    os.environ.update({
        "LOG_LEVEL": "DEBUG",
        "LOG_OUTPUT": "both",
        "LOG_FILE_PATH": temp_log_file,
        "LOG_FORMAT": "plain",
        "LOG_TIMESTAMP_FORMAT": "%Y-%m-%d %H:%M:%S",
        "LOG_INCLUDE_PID": "true",
        "LOG_INCLUDE_THREAD": "true",
        "LOG_APP_NAME": "TestApp",
        "LOG_STACKTRACE": "true",
        "LOG_ASYNC": "false",
        "LOG_INCLUDE_SOURCE": "true"
    })
    yield
    # Restore original environment / 元の環境変数を復元
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture(autouse=True)
def cleanup_loggers():
    """
    Clean up logger instances after each test.
    各テスト後にロガーインスタンスをクリーンアップする。
    """
    yield
    Logger._instances.clear()
    logging.shutdown()

# ---------------------------------------------------------------------
# Test Cases
# テストケース
# ---------------------------------------------------------------------
def test_logger_singleton():
    """
    Test that logger instances are properly cached (singleton pattern).
    ロガーインスタンスが適切にキャッシュされる（シングルトンパターン）ことをテスト。
    """
    logger1 = Logger.get_logger("test_logger")
    logger2 = Logger.get_logger("test_logger")
    assert logger1 is logger2

def test_logger_different_names():
    """
    Test that different logger names create different instances.
    異なるロガー名で異なるインスタンスが作成されることをテスト。
    """
    logger1 = Logger.get_logger("test_logger1")
    logger2 = Logger.get_logger("test_logger2")
    assert logger1 is not logger2

def test_log_to_file(env_setup, temp_log_file):
    """
    Test logging to a file.
    ファイルへのログ出力をテスト。
    """
    logger = Logger.get_logger("test_file_logger")
    test_message = "Test log message"
    logger.info(test_message)

    # Check if message was written to file / ファイルにメッセージが書き込まれたか確認
    with open(temp_log_file, 'r') as f:
        log_content = f.read()
        assert test_message in log_content
        assert "TestApp" in log_content  # Check if app name is included / アプリ名が含まれているか確認

def test_json_format(env_setup, temp_log_file):
    """
    Test JSON format logging.
    JSON形式のログ出力をテスト。
    """
    os.environ["LOG_FORMAT"] = "json"
    logger = Logger.get_logger("test_json_logger")
    test_message = "Test JSON log"
    logger.info(test_message)

    # Check if valid JSON was written / 有効なJSONが書き込まれたか確認
    with open(temp_log_file, 'r') as f:
        for line in f:
            log_entry = json.loads(line.strip())
            assert log_entry["message"] == test_message
            assert log_entry["level"] == "INFO"
            assert "timestamp" in log_entry

def test_exception_logging(env_setup, temp_log_file):
    """
    Test exception logging functionality.
    例外のログ出力機能をテスト。
    """
    logger = Logger.get_logger("test_exception_logger")
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.error("Error occurred", exc_info=True)

    # Check if exception info is in log / 例外情報がログに含まれているか確認
    with open(temp_log_file, 'r') as f:
        log_content = f.read()
        assert "ValueError" in log_content
        assert "Test exception" in log_content

def test_log_levels(env_setup, temp_log_file):
    """
    Test different log levels.
    異なるログレベルをテスト。
    """
    logger = Logger.get_logger("test_levels_logger")
    
    # Test each level / 各レベルをテスト
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    with open(temp_log_file, 'r') as f:
        log_content = f.read()
        assert "DEBUG" in log_content
        assert "INFO" in log_content
        assert "WARNING" in log_content
        assert "ERROR" in log_content 