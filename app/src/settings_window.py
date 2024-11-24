from tkinter import ttk

import customtkinter as ctk

FONT_TYPE = "meiryo"


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.button_fonts = (FONT_TYPE, 13)
        self.title("設定")
        self.geometry("700x500")
        self.resizable(False, False)

        self.setup_form()

    def setup_form(self):
        self.sidebar()

    def sidebar(self):
        """
        サイドバーの設定
        """

        side_frame = ctk.CTkFrame(self)
        side_frame.grid(row=0, column=0, padx=0, pady=(0, 0), rowspan=3, sticky="nsw")

        # サイドバーラベル
        _label = ctk.CTkLabel(
            side_frame,
            text="Settings",
            font=self.fonts,
            corner_radius=6,
        )
        _label.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        # ラベルの下にセパレーター（線）を追加
        separator = ttk.Separator(side_frame, orient="horizontal")
        separator.grid(row=1, column=0, padx=0, pady=(0, 0), sticky="ew")
