import tkinter as tk
from distutils.util import strtobool
from functools import partial
from tkinter import ttk

import customtkinter as ctk
from customtkinter import CTkEntry, CTkFrame, CTkSwitch
from src.common.common import csv_file_read, file_read, read_config
from src.settings_window import ToplevelWindow

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

        # タブ画面の配置
        self.set_tab_view()

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
        _option_button_help = ctk.CTkButton(
            frame, text="ヘルプ", font=self.button_fonts
        )
        _option_button_help.grid(row=1, column=0, padx=15, pady=(15, 0), sticky="nsw")

        _option_button_settings = ctk.CTkButton(
            frame, text="設定", font=self.button_fonts, command=self.open_toplevel
        )
        _option_button_settings.grid(
            row=2, column=0, padx=15, pady=(15, 0), sticky="nsw"
        )

        self.toplevel_window = None

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

    def set_tab_view(self):
        self.tab_view = ctk.CTkSegmentedButton(
            self,
            values=["手動作成", "CSVインポート"],
            command=self.change_tab,
            font=self.fonts,
            dynamic_resizing=True,
        )
        self.tab_view.grid(
            row=0, column=1, columnspan=3, padx=10, pady=10, sticky="nwe"
        )

        # デフォルト値をセット
        self.tab_view.set("手動作成")

        # 各タブの画面を初期化しておく
        self.manual_property_area()
        self.import_property_area()

    def manual_property_area(self) -> CTkFrame:
        # フレームの設定
        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 50),
            rowspan=2,
            columnspan=3,
            sticky="nwes",
        )

        # メールデータ入力ラベル
        _eml_data_label_list = ["From：", "To：", "cc：", "件名：", "本文："]

        for index, eml_data_label in enumerate(_eml_data_label_list, start=1):
            # データラベル
            _data_label = ctk.CTkLabel(
                self.current_frame, text=eml_data_label, font=self.fonts
            )
            _data_label.grid(row=index - 1, column=0, padx=15, pady=(10, 0), sticky="e")

            # データエントリー
            _data_entry = ctk.CTkEntry(
                self.current_frame, placeholder_text="", width=300
            )
            _data_entry.grid(
                row=index - 1, column=1, padx=15, pady=(10, 0), sticky="we"
            )
            self.data_entry_list.append(_data_entry)

            # 文字列自動生成チェックボックス
            _auto_switch = ctk.CTkSwitch(
                self.current_frame,
                text="auto generate",
                font=self.fonts,
                onvalue="True",
                offvalue="False",
                command=partial(self.toggle_entry, index - 1),
            )
            _auto_switch.grid(
                row=index - 1, column=2, padx=15, pady=(10, 0), sticky="w"
            )
            self.auto_switch_list.append(_auto_switch)

        # ログ出力ボックス
        _log_box = ctk.CTkTextbox(self.current_frame, font=self.fonts, width=650)
        _log_box.grid(
            row=5, column=0, columnspan=3, padx=20, pady=(10, 10), sticky="we"
        )
        _log_box.configure(state="disabled")

    def import_property_area(self):
        # フレームの設定
        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 50),
            rowspan=2,
            columnspan=3,
            sticky="we",
        )

        # データラベル
        _data_label = ctk.CTkLabel(
            self.current_frame, text="csv import：", font=self.fonts
        )
        _data_label.grid(row=0, column=0, padx=15, pady=(20, 0), sticky="n")

        # データエントリー
        self.csv_path_entry = ctk.CTkEntry(
            self.current_frame, placeholder_text="", width=350
        )
        self.csv_path_entry.grid(row=0, column=1, padx=15, pady=(20, 20), sticky="we")

        # 文字列自動生成チェックボックス
        _exit_button = ctk.CTkButton(
            self.current_frame,
            text="選択",
            font=self.button_fonts,
            command=self.csv_open_button,
        )
        _exit_button.grid(row=0, column=2, padx=15, pady=(20, 20), sticky="w")

        # ボタン間のスペースを空けるために空のラベルを追加（オプション）
        empty_label = ctk.CTkLabel(self.current_frame, text="", font=self.fonts)
        empty_label.grid(row=1, column=0, padx=15, pady=(84, 0), sticky="nsw")

        # ログ出力ボックス
        _log_box = ctk.CTkTextbox(self.current_frame, font=self.fonts, width=650)
        _log_box.grid(
            row=2, column=0, columnspan=3, padx=20, pady=(15, 15), sticky="we"
        )
        _log_box.configure(state="disabled")

    def export_dir(self):
        # 出力先ディレクトリ指定
        self.file_path_entry = ctk.CTkEntry(self, placeholder_text=" ./", width=570)
        self.file_path_entry.grid(row=2, column=1, padx=10, pady=(15, 6), sticky="swe")

        _file_path_button = ctk.CTkButton(
            self,
            text="開く",
            font=self.button_fonts,
            width=70,
            command=self.explorer_open_button,
        )
        _file_path_button.grid(row=2, column=2, padx=10, pady=(15, 6), sticky="swe")

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

    def csv_open_button(self):
        """
        ファイル選択ボタンが押された際にcsv選択ダイアログを表示する
        """

        file_name = csv_file_read()

        if file_name is None:
            return

        self.csv_path_entry.delete(0, tk.END)
        self.csv_path_entry.insert(0, file_name)

    def change_tab(self, selected_value: str, from_button_callback=None):
        """
        セグメントボタンが選ばれたときに表示を切り替え

        Args:
            selected_value ([type]): [description]
        """

        self.current_frame.grid_forget()

        if selected_value == "手動作成":
            self.manual_property_area()

        if selected_value == "自動作成":
            self.manual_property_area()

        if selected_value == "CSVインポート":
            self.import_property_area()

    def open_toplevel(self):
        """
        設定画面の出現
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)

            # ウィンドウが親ウィンドウの後ろに隠れないように設定
            self.toplevel_window.after(100, self.raise_toplevel_window)
        else:
            self.toplevel_window.focus()

    def raise_toplevel_window(self):
        """
        Toplevelウィンドウを最前面に移動させる
        """
        self.toplevel_window.lift()
        self.toplevel_window.focus_force()
