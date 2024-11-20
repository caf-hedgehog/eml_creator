import tkinter as tk
from distutils.util import strtobool
from functools import partial

import customtkinter as ctk
from customtkinter import CTkEntry, CTkSwitch
from src.common.common import file_read, read_config

FONT_TYPE = "meiryo"


class Application(ctk.CTk):
    def __init__(self):
        self.auto_switch_list: list[CTkSwitch] = []
        self.data_entry_list: list[CTkEntry] = []
        super().__init__()

        print(read_config("GUI_SETTINGS"))

        # フォームの設定
        self.fonts = (FONT_TYPE, 15)
        self.button_fonts = (FONT_TYPE, 13)
        self.title("EMLファイル作成ツール")
        self.geometry("900x550")
        self.resizable(False, False)

        # グリッドの行と列の配置比率を設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # CustomTkinterのフォームデザイン設定
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # サイドバーの配置
        self.sidebar()

        # プログレスバーの配置
        self.progress_bar()

        # メイン画面の配置
        self.manual_property_area()

        # 出力先ディレクトリ指定
        self.export_dir()

    def sidebar(self):
        # フレームの設定
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=10, pady=(10, 0), rowspan=3, sticky="nsw")

        # サイドバーラベル
        _label = ctk.CTkLabel(
            frame,
            text="Options",
            font=self.fonts,
            corner_radius=6,
        )
        _label.grid(row=0, column=0, padx=10, pady=15, sticky="ew")

        # EML自動作成画面遷移ボタン
        option_button_list = ["ヘルプ", "設定"]

        for index, button_name in enumerate(option_button_list, start=1):
            _option_button = ctk.CTkButton(
                frame, text=button_name, font=self.button_fonts
            )
            _option_button.grid(
                row=index, column=0, padx=15, pady=(15, 0), sticky="nsw"
            )

        # ボタン間のスペースを空けるために空のラベルを追加（オプション）
        empty_label = ctk.CTkLabel(frame, text="", font=self.fonts)
        empty_label.grid(row=4, column=0, padx=15, pady=(333, 0), sticky="nsw")

        # EMLファイル出力ボタン
        _exit_button = ctk.CTkButton(frame, text="実行", font=self.button_fonts)
        _exit_button.grid(row=4, column=0, padx=15, pady=(15, 0), sticky="s")

    def progress_bar(self):
        # プログレスバー
        _progress_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        _progress_bar.grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            rowspan=3,
            sticky="ew",
            columnspan=3,
        )

    def set_tab_view(self, frame: ctk.CTkFrame):
        self.tab_view = ctk.CTkSegmentedButton(
            frame,
            values=["手動作成", "自動作成", "CSVインポート"],
            command=None,
            font=self.fonts,
            dynamic_resizing=True,
        )
        self.tab_view.grid(
            row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nwe"
        )

        # デフォルト値をセット
        self.tab_view.set("手動作成")

    def manual_property_area(self):
        # フレームの設定
        _frame = ctk.CTkFrame(self)
        _frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=(10, 0),
            rowspan=2,
            columnspan=2,
            sticky="nswe",
        )

        # タブの設置
        self.set_tab_view(_frame)

        # メールデータ入力ラベル
        _eml_data_label_list = ["From：", "To：", "cc：", "件名：", "本文："]

        for index, eml_data_label in enumerate(_eml_data_label_list, start=1):
            # データラベル
            _data_label = ctk.CTkLabel(_frame, text=eml_data_label, font=self.fonts)
            _data_label.grid(row=index, column=0, padx=15, pady=(10, 0), sticky="e")

            # データエントリー
            _data_entry = ctk.CTkEntry(_frame, placeholder_text="", width=300)
            _data_entry.grid(row=index, column=1, padx=15, pady=(10, 0), sticky="nsw")
            self.data_entry_list.append(_data_entry)

            # 文字列自動生成チェックボックス
            _auto_switch = ctk.CTkSwitch(
                _frame,
                text="auto generate",
                font=self.fonts,
                onvalue="True",
                offvalue="False",
                command=partial(self.toggle_entry, index - 1),
            )
            _auto_switch.grid(row=index, column=2, padx=15, pady=(10, 0), sticky="e")
            self.auto_switch_list.append(_auto_switch)

        # ログ出力ボックス
        _log_box = ctk.CTkTextbox(_frame, font=self.fonts, width=650)
        _log_box.grid(row=6, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="we")
        _log_box.configure(state="disabled")

    def export_dir(self):
        # 出力先ディレクトリ指定
        self.file_path_entry = ctk.CTkEntry(self, placeholder_text=" ./", width=570)
        self.file_path_entry.grid(row=2, column=1, padx=10, pady=(15, 7), sticky="we")

        _file_path_button = ctk.CTkButton(
            self,
            text="開く",
            font=self.button_fonts,
            width=70,
            command=self.explorer_open_button,
        )
        _file_path_button.grid(row=2, column=2, padx=10, pady=(15, 7))

    ############# コールバック関数 ######################

    def toggle_entry(self, index: int):
        """
        自動生成スイッチが推された際に呼び出される
        スイッチがONになるとエントリーが使用不可になる
        """
        if strtobool(self.auto_switch_list[index].get()):
            self.data_entry_list[index].configure(state="disable")
        else:
            self.data_entry_list[index].configure(state="normal")

    def explorer_open_button(self):
        """
        ディレクトリ選択ボタンが押された際にディレクトリ選択ダイアログを表示する
        """
        file_name = file_read()

        if file_name is None:
            return

        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_name)
