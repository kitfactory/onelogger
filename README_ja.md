# OneLogger - シンプルで効率的なロギングライブラリ

OneLogger は、環境変数管理ライブラリ [oneenv](https://github.com/kitfactory/oneenv) を利用して、ログ設定を動的に管理できる軽量なロギングライブラリです。  
Python の標準 logging モジュールをベースにし、Python 3.12 までの環境では [picologging](https://github.com/microsoft/picologging) による高速なロギング処理を実現します。  
開発環境、テスト環境、本番環境いずれにおいても柔軟にご利用いただけます。

## 特徴
- **動的な設定管理**: oneenv により、環境変数から簡単にログの設定が可能です。
- **高速なロギング**:
  - Python 3.12 以前では、picologging を利用して高速なログ処理を実現します。
  - Python 3.13 以降では、標準の logging モジュールを使用します。
- **柔軟な出力オプション**: コンソール出力、ファイル出力（ローテーションあり）、またはその両方に対応。
- **カスタムフォーマット**: プレーンテキスト形式および JSON 形式のログ出力が可能です。
- **非同期ロギング**: 必要に応じて非同期ロギングを有効化し、高負荷時のパフォーマンス向上も実現。
- **簡単な統合**: シングルトンパターンによるシンプルな API で、容易にロガーの取得が可能です。

## 対応環境
- **Python 3.11 以降**
  - **Python 3.13 未満**: picologging による高速ロギング
  - **Python 3.13 以降**: 標準の logging モジュールを利用

## インストール手順
1. **リポジトリのクローン**
   ```bash
   git clone <repository-url>
   cd onelogger
   ```

2. **仮想環境の作成と有効化**
   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **依存パッケージのインストール**
   ```bash
   pip install -e .
   ```

## 使い方
OneLogger は以下のように簡単に利用できます:

```python
from onelogger import Logger

# ロガーインスタンスの取得
logger = Logger.get_logger("example_logger")

# 各種ログメッセージの出力
logger.info("これは情報メッセージです。")
logger.error("これはエラーメッセージです。")

try:
    result = 1 / 0
except Exception as e:
    logger.exception("除算処理中に例外が発生しました。")
```

`examples` フォルダ内のサンプルコードで動作を確認できます:
```bash
python examples/example_logger.py
```

## 設定方法
OneLogger は [oneenv](https://github.com/kitfactory/oneenv) を使用して環境変数を簡単に管理できます。  
ライブラリは自動的に `.env.example` テンプレートファイルを生成し、利用可能な全ての設定項目の詳細な説明を提供します。

これにより以下が容易になります：
- 利用可能な全ての設定オプションとその説明の確認
- 各設定項目の目的と有効な値の理解
- テンプレートをコピーして独自の `.env` ファイルを作成

以下は自動生成されるテンプレートの例です：

```ini
# OneEnv により自動生成

# OneLoggerが使用するログレベルを指定します。
# 利用可能な値は DEBUG, INFO, WARNING, ERROR, CRITICAL です。
# 必須項目
LOG_LEVEL=DEBUG

# ログの出力先を指定します。
# 'console' は標準出力、'file' はファイル出力、'both' は両方への出力。
# 必須項目
LOG_OUTPUT=both

# LOG_OUTPUTが'file'または'both'の場合に使用されるログファイルのパス
LOG_FILE_PATH=example.log

# ... (その他の設定項目と説明)
```

OneLogger の設定手順：
1. `.env.example` を `.env` にコピー
2. `.env` 内の値を必要に応じて変更
3. OneLogger 初期化時に自動的にこれらの設定が読み込まれます

## 貢献方法
貢献を歓迎します。Python のベストプラクティスに従い、必要に応じてテストを追加してください。

## ライセンス
本プロジェクトは MIT ライセンスの下で提供されています。

---

OneLogger を活用して、シンプルで柔軟なロギング環境を構築しましょう。 