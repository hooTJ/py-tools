import os.path
import tkinter as tk

from src.app import App

TITLE = "hooTJ"
BASE_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)  # 让高宽都固定   root.resizable(width=False, height=False)
    w = root.winfo_screenwidth()  # 获得屏幕宽度   root.winfo_width()
    h = root.winfo_screenheight()  # 获得屏幕高度  root.winfo_height()
    root.geometry("%dx%d+%d+%d" % (700, 500, (w - 700) / 2, (h - 500) / 2))
    root.title(TITLE)
    # root.iconbitmap(f"{BASE_DIR}/icon.ico")
    app = App(root=root)
    app.start()
    root.mainloop()
