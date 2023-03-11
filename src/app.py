import tkinter
from tkinter import ttk

from .core import CommonLayout, UnixTimeLayout, MavenLayout, Base64Layout, SpeedTestLayout


# 1、组件
# 2、标准属性
# 3、布局管理

class App:
    def __init__(self, root):
        self.root = root

    def start(self):
        notebook = ttk.Notebook(self.root)
        tabs = ["反转", "格式化", "去格式化", "固定格式", "大小写", "时间戳", "仓库导入", "Base64", "测试网速"]
        for i in range(len(tabs)):
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=tabs[i])
            if i == 5:
                UnixTimeLayout(tab_frame).start()
            elif i == 6:
                MavenLayout(tab_frame).start()
            elif i == 7:
                Base64Layout(tab_frame).start()
            elif i == 8:
                SpeedTestLayout(tab_frame).start()
            else:
                CommonLayout(self.root, tab_frame, i).start()
        notebook.pack(expand=1, fill=tkinter.BOTH)
