import tkinter as tk
import tkinter.font as font
import tkinter.scrolledtext
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import datetime
from threading import Timer
import time

"""
1、组件
2、标准属性
3、布局管理
"""
# password = StringVar(); e = ttk.Entry(root, textvariable=password, show='*'); e.pack();
TITLE = "hooTJ"

global timer01
global timer02
global timer03

(entry_width, combobox_width, button_width) = (12, 3, 3)
(ipady, ipadx, padx, pady) = (5, 5, 5, 5)


def unix(frame):
    c1 = ttk.LabelFrame(frame, text="当前时间戳", width=600, height=400)
    c1.pack()
    c2 = ttk.LabelFrame(frame, text="时间戳转换时间", width=600, height=400)
    c2.pack()
    c3 = ttk.LabelFrame(frame, text="时间转时间戳（支持yyyy-MM-dd HH:mm:ss、yyyy-MM-dd HH:mm:ss.SSS）", width=600, height=400)
    c3.pack()

    fn = font.Font(family='Times New Roman', size=10, weight=font.NORMAL)

    ###########################################################################
    create_label(c1, 0, 0, "当前时间", fn)
    ent1_1 = create_entry(c1, 0, 1)
    create_label(c1, 0, 2, "秒", fn)
    ent1_2 = create_entry(c1, 0, 3)
    create_label(c1, 0, 4, "毫秒", fn)
    open_timer([ent1_1, ent1_2])
    btn1_1 = ttk.Button(c1, text="停止", width=button_width, command=lambda: close_timer([timer01, timer02]))
    btn1_1.grid(row=0, column=5, sticky=tk.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
    btn1_2 = ttk.Button(c1, text="开始", width=button_width, command=lambda: open_timer([ent1_1, ent1_2]))
    btn1_2.grid(row=0, column=6, sticky=tk.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
    btn1_1.focus()
    label = create_label(c1, 0, 7, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), fn)
    update_label_show(label)

    ###########################################################################
    create_label(c2, 0, 0, "时间戳", fn)
    ent2_1 = create_entry(c2, 0, 1)
    btn2_1 = ttk.Button(c2, text="转换", width=button_width, command=lambda: transfer_timestamp_date(ent2_1, ent2_2))
    btn2_1.grid(row=0, column=2, sticky=tk.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
    ent2_2 = create_entry(c2, 0, 3, entry_width + 10)

    ###########################################################################
    box3_1_value = tkinter.StringVar()
    create_label(c3, 0, 0, "时间", fn)
    ent3_1 = create_entry(c3, 0, 1, entry_width + 10)
    btn3_1 = ttk.Button(c3, text="转换", width=button_width,
                        command=lambda: transfer_date_timestamp(ent3_1, ent3_2, box3_1_value))
    btn3_1.grid(row=0, column=2, sticky=tk.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
    ent3_2 = create_entry(c3, 0, 3)
    box3_1 = ttk.Combobox(c3, textvariable=box3_1_value, width=combobox_width)
    box3_1.configure(state="readonly")
    box3_1["values"] = ("毫秒", "秒")
    box3_1.grid(row=0, column=4, sticky=tk.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
    box3_1.current(0)  # 默认值中的内容为索引，从0开始
    box3_1.update()


def create_label(parent, row, column, text, fn):
    label = ttk.Label(parent, text=text, font=fn)
    label.grid(row=row, column=column, sticky=tk.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
    return label


def create_entry(parent, row, column, width=None):
    entry = ttk.Entry(parent, width=width if width else entry_width)
    entry.grid(row=row, column=column, sticky=tk.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
    return entry


def fill_text(text, flag):
    text.delete(0, tk.END)
    t = time.time()
    if flag == 1:
        text.insert(tk.END, str(int(t)))
    else:
        text.insert(tk.END, str(int(t * 1000)))
    text.update()

    if flag == 1:
        global timer01
        timer01 = Timer(1.0, fill_text, (text, flag,))
        timer01.setDaemon(True)
        timer01.start()
    else:
        global timer02
        timer02 = Timer(1.0, fill_text, (text, flag,))
        timer02.setDaemon(True)
        timer02.start()


def close_timer(timers=None):
    if timers is None:
        timers = []
    if timers and len(timers) > 0:
        for timer in timers:
            timer.cancel()


def open_timer(texts=None):
    if texts is None:
        texts = []
    if texts and len(texts) > 0:
        for i in range(len(texts)):
            fill_text(texts[i], i + 1)


def update_label_show(label):
    label['text'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    label.update()
    global timer03
    timer03 = Timer(1.0, update_label_show, (label,))
    timer03.setDaemon(True)
    timer03.start()


def transfer_timestamp_date(text1, text2):
    time_str = text1.get()
    if not time_str:
        messagebox.showwarning(TITLE, '请输入时间戳')
        return
    le = len(time_str)
    if le == 0:
        messagebox.showwarning(TITLE, '请输入时间戳')
        return
    text2.delete(0, tk.END)
    if le == 10:
        res = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time_str)))
    elif le == 13:
        res = datetime.fromtimestamp(int(time_str) / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        messagebox.showerror(TITLE, '必须是10或者13位')
        return
    text2.insert(tk.END, res)


def transfer_date_timestamp(text1, text2, box):
    date_str = text1.get()
    if not date_str:
        messagebox.showwarning(TITLE, '请输入时间')
        return
    le = len(date_str)
    if le == 0:
        messagebox.showwarning(TITLE, '请输入时间')
        return
    text2.delete(0, tk.END)

    error = None
    for f in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"]:
        try:
            dt = datetime.strptime(date_str, f)
        except Exception as e:
            error = e
            dt = None
        if dt:
            break
    if not dt:
        messagebox.showerror(TITLE, error)
        return

    t = time.mktime(dt.timetuple())
    if box.get() == '毫秒':
        res = str(int(t * 1000))
    elif box.get() == '秒':
        res = str(int(t))
    else:
        messagebox.showerror(TITLE, '选择合法的转换')
        return
    text2.insert(tk.END, res)


def layout(root_frame, frame, flag):
    content = ttk.LabelFrame(frame, text="内容区域", width=600, height=400)
    content.pack()

    fn = font.Font(family='Times New Roman', size=10, weight=font.NORMAL)

    lab1 = ttk.Label(content, text="输入内容", font=fn)
    lab1.grid(row=0, column=0, sticky=tk.EW)

    # tk.INSERT和tk.END效果一样
    # 插入：t1.insert(tk.END, "哈哈")
    # 获取：t1.get("0.0", tk.END) 表示开始和结束
    # 删除：t1.delete("0.0", tk.END) 表示开始和结束
    t1 = tk.scrolledtext.ScrolledText(content, height=14, wrap=tk.WORD, borderwidth=2, highlightcolor='gray',
                                      highlightthickness=1)
    t1.grid(row=0, column=1, columnspan=5, sticky=tk.EW, ipady=3)

    lab2 = ttk.Label(content, text="输出内容", font=fn)
    lab2.grid(row=1, column=0, sticky=tk.W)

    t2 = tk.scrolledtext.ScrolledText(content, height=14, wrap=tk.WORD, borderwidth=2, highlightcolor='gray',
                                      highlightthickness=1)
    t2.grid(row=1, column=1, columnspan=5, sticky=tk.EW, ipady=3)

    control = ttk.LabelFrame(frame, text="操作区域", width=600, height=400)
    control.pack()

    # cursor光标：arrow、circle、clock、cross、dotbox、exchange、fleur、heart、man、mouse、pirate、plus、shuttle、sizing、spider、spraycan、star、target、tcross、trek、watch
    btn1 = ttk.Button(control, text="清空", width=20, cursor="arrow", command=lambda: clear(t1, t2))
    btn2 = ttk.Button(control, text="执行", width=20, cursor="arrow", command=lambda: execute(t1, t2, flag))
    btn3 = ttk.Button(control, text="粘贴", width=20, cursor="arrow", command=lambda: copy_from(root_frame, t1))
    btn4 = ttk.Button(control, text="复制", width=20, cursor="arrow", command=lambda: copy_to(root_frame, t2))
    btn1.grid(row=1, column=1, sticky=tk.EW, ipady=2)
    btn2.grid(row=1, column=2, sticky=tk.EW, ipady=2)
    btn3.grid(row=1, column=3, sticky=tk.EW, ipady=2)
    btn4.grid(row=1, column=4, sticky=tk.EW, ipady=2)
    # btn2.bind('<Button-1>', func=None)


def clear(t1, t2):
    t1.delete("0.0", tk.END)
    t2.delete("0.0", tk.END)


def text_to_json(v):
    ls = []
    arr = v.split("\n")
    arr1 = arr[0].split("\t")
    for i in range(1, len(arr)):
        arr2 = arr[i].split("\t")
        if len(arr1) != len(arr2):
            continue
        dc = {}
        for j in range(len(arr2)):
            dc[arr1[j]] = arr2[j]
        ls.append(dc)
    return json.dumps(ls, indent=4, ensure_ascii=False)


def transfer(v):
    if v.islower():
        return v.upper()
    else:
        return v.lower()


def execute(t1, t2, flag):
    s = t1.get("0.0", tk.END)
    if not s:
        messagebox.showwarning(TITLE, '请输入内容')
        return
    v = str(s).replace('\r', '').replace('\n', '')
    if v is None or len(v) < 1:
        messagebox.showwarning(TITLE, '请输入内容')
        return
    t2.delete("0.0", tk.END)
    '''
    flag=0 反转
    flag=1 格式化
    flag=2 去格式化
    flag=3 固定格式
    flag=4 大小写
    '''
    try:
        if flag == 0:
            t2.insert(tk.INSERT, reverse(v))
        elif flag == 1:
            t2.insert(tk.INSERT, json.dumps(json.loads(v), indent=4, ensure_ascii=False))
        elif flag == 2:
            t2.insert(tk.INSERT, json.dumps(json.loads(v), ensure_ascii=False))
        elif flag == 3:
            t2.insert(tk.INSERT, text_to_json(str(s)))
        elif flag == 4:
            t2.insert(tk.INSERT, transfer(str(s)))
        else:
            messagebox.showerror(TITLE, '参数不正确')
    except Exception as e:
        messagebox.showerror(TITLE, e)
        return


def reverse(s):
    if (len(s)) < 1:
        return s
    return reverse(s[1:]) + s[0]


def copy_from(root_frame, text):
    s = root_frame.clipboard_get()
    if not s:
        return
    text.insert(tk.END, s)


def copy_to(root_frame, text):
    s = text.get(0.0, tk.END)
    if not s:
        messagebox.showinfo(TITLE, '请先执行再复制')
        return
    v = str(s).replace('\r', '').replace('\n', '')
    if not v or len(v) < 1:
        messagebox.showinfo(TITLE, '请先执行再复制')
        return
    root_frame.clipboard_clear()
    root_frame.clipboard_append(s)
    messagebox.showinfo(TITLE, '复制成功')


class App:
    def __init__(self, r):
        self.root = r
        self.start()

    def start(self):
        # 安装第三方模块（python -m pip install pyperclip），当然也可以直接使用内置的.
        # self.root.clipboard_get()  # 获取剪贴板内容
        # self.root.clipboard_clear()  # 清除剪贴板内容
        # self.root.clipboard_append("aaa")  # 向剪贴板追加内容
        notebook = ttk.Notebook(self.root)
        tabs = ["反转", "格式化", "去格式化", "固定格式", "大小写", "时间戳"]
        for i in range(len(tabs)):
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=tabs[i])
            if i == 5:
                unix(tab)
            else:
                layout(self.root, tab, i)

        notebook.pack(expand=1, fill=tk.BOTH)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)  # 让高宽都固定   root.resizable(width=False, height=False)
    w = root.winfo_screenwidth()  # 获得屏幕宽度   root.winfo_width()
    h = root.winfo_screenheight()  # 获得屏幕高度  root.winfo_height()
    root.geometry("%dx%d+%d+%d" % (700, 500, (w - 700) / 2, (h - 500) / 2))
    root.title(TITLE)
    # root.iconbitmap("icon.ico")
    App(r=root)
    root.mainloop()
