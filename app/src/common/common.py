import configparser
import errno
import os
import tkinter as tk
from configparser import SectionProxy

from src.common.definitions import ENCODING_UTF_8


@staticmethod
def read_config(section_name: str) -> SectionProxy:
    """iniファイルから設定を読み込む

    Args:
        section_name (str): 読み込みたいセクション名

    Raises:
        FileNotFoundError: iniファイルが存在しない場合NotFoundを返却します

    Returns:
        SectionProxy: 指定したセクションの値を返却します
    """
    # config.iniが存在しているPATHの構築
    config_file_path = os.path.join(
        os.path.dirname(__file__), "../../", "config", "config.ini"
    )

    # config.iniが存在するか確認
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), config_file_path
        )

    config = configparser.ConfigParser()
    config.read(config_file_path, encoding=ENCODING_UTF_8)

    return config[section_name]


def file_read() -> str | None:
    """
    保存先ディレクトリの指定
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = tk.filedialog.askdirectory(initialdir=current_dir)

    if len(file_path) != 0:
        return file_path
    else:
        # ファイル選択がキャンセルされた場合
        return None


def csv_file_read() -> str | None:
    """
    csv読み込みファイルの指定
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = tk.filedialog.askopenfilename(
        filetypes=[("csvファイル", "*.csv")], initialdir=current_dir
    )

    if len(file_path) != 0:
        return file_path
    else:
        # ファイル選択がキャンセルされた場合
        return None
