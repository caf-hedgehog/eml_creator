# main.py
import os
import sys

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


from src.gui import Application

if __name__ == "__main__":

    app = Application()
    app.mainloop()
