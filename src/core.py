import base64
import json
import os
import time
import tkinter
from datetime import datetime
from threading import Timer
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.font import Font, NORMAL
from tkinter.scrolledtext import ScrolledText

TITLE = "hooTJ"
entry_width, combobox_width, button_width = (12, 3, 3)
ipady, ipadx, padx, pady = (5, 5, 5, 5)
BASE_DIR = os.path.dirname(__file__)


# tk.INSERT和tk.END效果一样
# 插入：t1.insert(tk.END, "哈哈")
# 获取：t1.get("0.0", tk.END) 表示开始和结束
# 删除：t1.delete("0.0", tk.END) 表示开始和结束

# cursor光标：arrow、circle、clock、cross、dotbox、exchange、fleur、heart、man、mouse、pirate、plus、shuttle、sizing、
# spider、spraycan、star、target、tcross、trek、watch

# 安装第三方模块（python -m pip install pyperclip），当然也可以直接使用内置的.
# self.root.clipboard_get()  # 获取剪贴板内容
# self.root.clipboard_clear()  # 清除剪贴板内容
# self.root.clipboard_append("aaa")  # 向剪贴板追加内容

# password = StringVar(); e = ttk.Entry(root, textvariable=password, show='*'); e.pack();

class TextUtils:
    @staticmethod
    def reverse(text: str) -> str:
        """
        反转
        :param text:
        :return:
        """
        if not text or len(text) < 1:
            return text
        if text.endswith('\n'):
            text = text.rstrip('\n')
        return TextUtils.reverse(text[1:]) + text[0]

    @staticmethod
    def fixed_style_text_to_json(text):
        result_list = []
        items = text.split("\n")
        if len(items) <= 1:
            messagebox.showerror(TITLE, "数据格式不合法")
        keys = items[0].split("\t")
        for i in range(1, len(keys)):
            values = items[i].split("\t")
            if not values or len(keys) != len(values):
                continue
            tmp_dict = {}
            for j in range(len(keys)):
                tmp_dict[keys[j]] = values[j]
            result_list.append(tmp_dict)
        return json.dumps(result_list, indent=4, ensure_ascii=False)

    @staticmethod
    def word_case_toggle(text: str) -> str:
        if text.islower():
            return text.upper()
        else:
            return text.lower()


class ComponentUtils:
    @staticmethod
    def create_label(frame, row=None, column=None, text='默认值', fn=None):
        label = ttk.Label(frame, text=text, font=fn)
        if row is not None and column is not None:
            label.grid(row=row, column=column, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        else:
            label.pack()
        return label

    @staticmethod
    def create_entry(frame, row=None, column=None, width=None):
        entry = ttk.Entry(frame, width=width if width else entry_width)
        if row is not None and column is not None:
            entry.grid(row=row, column=column, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        else:
            entry.pack()
        return entry

    @staticmethod
    def create_button(frame, text, width):
        return ttk.Button(frame, text=text, width=width)


class CommonLayout:
    def __init__(self, root: tkinter.Tk, frame: ttk.Frame, index: int):
        """
        :param root:
        :param frame:
        :param index:  0-反转; 1-格式化; 2-去格式化; 3-固定格式; 4-大小写;
        """
        self.root = root
        self.frame = frame
        self.index = index

    def start(self):
        base_font = Font(family='Times New Roman', size=10, weight=NORMAL)
        # 1、内容区域
        content_frame = ttk.LabelFrame(self.frame, text="内容区域", width=600, height=400)
        content_frame.pack()
        # 1.1 输入内容
        scrolled_text_in_label = ttk.Label(content_frame, text="输入内容", font=base_font)
        scrolled_text_in_label.grid(row=0, column=0, sticky=tkinter.EW)
        scrolled_text_in = ScrolledText(content_frame,
                                        height=14,
                                        wrap=tkinter.WORD,
                                        borderwidth=2,
                                        highlightcolor='gray',
                                        highlightthickness=1)
        scrolled_text_in.grid(row=0, column=1, columnspan=5, sticky=tkinter.EW, ipady=3)
        if self.index == 3:
            fixed_content = "a\tb\tc\n1\t2\t3\n4\t5\t6"
            scrolled_text_in.insert(tkinter.INSERT, fixed_content)
        # 1.2 输出内容
        scrolled_text_out_label = ttk.Label(content_frame, text="输出内容", font=base_font)
        scrolled_text_out_label.grid(row=1, column=0, sticky=tkinter.W)
        scrolled_text_out = ScrolledText(content_frame,
                                         height=14,
                                         wrap=tkinter.WORD,
                                         borderwidth=2,
                                         highlightcolor='gray',
                                         highlightthickness=1)
        scrolled_text_out.grid(row=1, column=1, columnspan=5, sticky=tkinter.EW, ipady=3)
        # 2. 操作区域
        control_frame = ttk.LabelFrame(self.frame, text="操作区域", width=600, height=400)
        control_frame.pack()
        # 2.1 按钮事件绑定
        btn_clear = ttk.Button(control_frame, text="清空", width=20, cursor="arrow",
                               command=lambda: self.clear(scrolled_text_in, scrolled_text_out))
        btn_do_execute = ttk.Button(control_frame, text="执行", width=20, cursor="arrow",
                                    command=lambda: self.do_execute(scrolled_text_in, scrolled_text_out))
        btn_paste = ttk.Button(control_frame, text="粘贴", width=20, cursor="arrow",
                               command=lambda: self.paste_from(scrolled_text_in))
        btn_copy = ttk.Button(control_frame, text="复制", width=20, cursor="arrow",
                              command=lambda: self.copy_to(scrolled_text_out))
        # 2.2 按钮布局
        btn_clear.grid(row=1, column=1, sticky=tkinter.EW, ipady=2)
        btn_do_execute.grid(row=1, column=2, sticky=tkinter.EW, ipady=2)
        btn_paste.grid(row=1, column=3, sticky=tkinter.EW, ipady=2)
        btn_copy.grid(row=1, column=4, sticky=tkinter.EW, ipady=2)

    @staticmethod
    def clear(scrolled_text_in, scrolled_text_out):
        """
        操作-清空
        :param scrolled_text_in:
        :param scrolled_text_out:
        :return:
        """
        scrolled_text_in.delete("0.0", tkinter.END)
        scrolled_text_out.delete("0.0", tkinter.END)

    def do_execute(self, scrolled_text_in, scrolled_text_out):
        """
        执行
        :param scrolled_text_in:
        :param scrolled_text_out:
        :return:
        """
        in_content = scrolled_text_in.get("0.0", tkinter.END)
        if not in_content:
            messagebox.showwarning(TITLE, '请输入内容')
            return
        _in_content = str(in_content).replace('\r', '').replace('\n', '')
        if _in_content is None or len(_in_content) < 1:
            messagebox.showwarning(TITLE, '请输入内容')
            return
        scrolled_text_out.delete("0.0", tkinter.END)
        try:
            out_content = ''
            if self.index == 0:
                out_content = TextUtils.reverse(in_content)
            elif self.index == 1:
                out_content = json.dumps(json.loads(_in_content), indent=4, ensure_ascii=False)
            elif self.index == 2:
                out_content = json.dumps(json.loads(_in_content), ensure_ascii=False)
            elif self.index == 3:
                out_content = TextUtils.fixed_style_text_to_json(in_content)
            elif self.index == 4:
                out_content = TextUtils.word_case_toggle(in_content)
            else:
                messagebox.showerror(TITLE, '参数不正确')
            scrolled_text_out.insert(tkinter.INSERT, out_content)
        except Exception as e:
            messagebox.showerror(TITLE, e)
            return

    def paste_from(self, scrolled_text_in):
        """
        操作-粘贴
        :param scrolled_text_in:
        :return:
        """
        content = self.root.clipboard_get()
        if not content:
            messagebox.showinfo(title=TITLE, message="剪切板内容为空")
            return
        scrolled_text_in.insert(tkinter.END, content)

    def copy_to(self, scrolled_text_out):
        """
        操作-复制
        :param scrolled_text_out:
        :return:
        """
        content = scrolled_text_out.get(0.0, tkinter.END)
        if not content:
            messagebox.showinfo(TITLE, '请先执行再复制')
            return
        _content = str(content).replace('\r', '').replace('\n', '')
        if not _content or len(_content) < 1:
            messagebox.showinfo(TITLE, '请先执行再复制')
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(_content)
        messagebox.showinfo(TITLE, '复制成功')


global timer01
global timer02
global timer03


class UnixTimeLayout:
    def __init__(self, frame: ttk.Frame):
        self.frame = frame

    def start(self):
        base_font = Font(family='Times New Roman', size=10, weight=NORMAL)
        # 当前时间戳
        current_time_frame = ttk.LabelFrame(self.frame,
                                            text="当前时间戳",
                                            width=600,
                                            height=400)
        current_time_frame.pack()
        self.current_time(current_time_frame, base_font)
        # 时间戳转换时间
        timestamp_2_time_frame = ttk.LabelFrame(self.frame,
                                                text="时间戳转换时间",
                                                width=600,
                                                height=400)
        timestamp_2_time_frame.pack()
        self.timestamp_2_time(timestamp_2_time_frame, base_font)
        # 时间转时间戳
        time_2_timestamp_frame = ttk.LabelFrame(self.frame,
                                                text="时间转时间戳（支持yyyy-MM-dd HH:mm:ss、yyyy-MM-dd HH:mm:ss.SSS）",
                                                width=600,
                                                height=400)
        time_2_timestamp_frame.pack()
        self.time_2_timestamp(time_2_timestamp_frame, base_font)

    def current_time(self, frame, base_font):
        ComponentUtils.create_label(frame, 0, 0, "当前时间", base_font)
        ent1_1 = ComponentUtils.create_entry(frame, 0, 1)

        ComponentUtils.create_label(frame, 0, 2, "秒", base_font)
        ent1_2 = ComponentUtils.create_entry(frame, 0, 3)

        ComponentUtils.create_label(frame, 0, 4, "毫秒", base_font)
        self.open_timer([ent1_1, ent1_2])

        btn1_1 = ttk.Button(frame, text="停止", width=button_width, command=lambda: self.close_timer([timer01, timer02]))
        btn1_1.grid(row=0, column=5, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        btn1_2 = ttk.Button(frame, text="开始", width=button_width, command=lambda: self.open_timer([ent1_1, ent1_2]))
        btn1_2.grid(row=0, column=6, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        btn1_1.focus()
        label = ComponentUtils.create_label(frame, 0, 7, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), base_font)
        self.update_label_show(label)

    def timestamp_2_time(self, frame, base_font):
        ComponentUtils.create_label(frame, 0, 0, "时间戳", base_font)
        ent2_1 = ComponentUtils.create_entry(frame, 0, 1)
        btn2_1 = ttk.Button(frame, text="转换", width=button_width,
                            command=lambda: self.transfer_timestamp_date(ent2_1, ent2_2))
        btn2_1.grid(row=0, column=2, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        ent2_2 = ComponentUtils.create_entry(frame, 0, 3, entry_width + 10)

    def time_2_timestamp(self, frame, base_font):
        box3_1_value = tkinter.StringVar()
        ComponentUtils.create_label(frame, 0, 0, "时间", base_font)
        ent3_1 = ComponentUtils.create_entry(frame, 0, 1, entry_width + 10)
        btn3_1 = ttk.Button(frame, text="转换", width=button_width,
                            command=lambda: self.transfer_date_timestamp(ent3_1, ent3_2, box3_1_value))
        btn3_1.grid(row=0, column=2, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        ent3_2 = ComponentUtils.create_entry(frame, 0, 3)
        box3_1 = ttk.Combobox(frame, textvariable=box3_1_value, width=combobox_width)
        box3_1.configure(state="readonly")
        box3_1["values"] = ("毫秒", "秒")
        box3_1.grid(row=0, column=4, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        box3_1.current(0)  # 默认值中的内容为索引，从0开始
        box3_1.update()

    @staticmethod
    def fill_text(text, flag):
        text.delete(0, tkinter.END)
        t = time.time()
        if flag == 1:
            text.insert(tkinter.END, str(int(t)))
        else:
            text.insert(tkinter.END, str(int(t * 1000)))
        text.update()

        if flag == 1:
            global timer01
            timer01 = Timer(1.0, UnixTimeLayout.fill_text, (text, flag,))
            timer01.setDaemon(True)
            timer01.start()
        else:
            global timer02
            timer02 = Timer(1.0, UnixTimeLayout.fill_text, (text, flag,))
            timer02.setDaemon(True)
            timer02.start()

    @staticmethod
    def close_timer(timers=None):
        if timers is None:
            timers = []
        if timers and len(timers) > 0:
            for timer in timers:
                timer.cancel()

    @staticmethod
    def open_timer(texts=None):
        if texts is None:
            texts = []
        if texts and len(texts) > 0:
            for i in range(len(texts)):
                UnixTimeLayout.fill_text(texts[i], i + 1)

    @staticmethod
    def update_label_show(label):
        label['text'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        label.update()
        global timer03
        timer03 = Timer(1.0, UnixTimeLayout.update_label_show, (label,))
        timer03.setDaemon(True)
        timer03.start()

    @staticmethod
    def transfer_timestamp_date(text1, text2):
        time_str = text1.get()
        if not time_str:
            messagebox.showwarning(TITLE, '请输入时间戳')
            return
        le = len(time_str)
        if le == 0:
            messagebox.showwarning(TITLE, '请输入时间戳')
            return
        text2.delete(0, tkinter.END)
        if le == 10:
            res = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time_str)))
        elif le == 13:
            res = datetime.fromtimestamp(int(time_str) / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            messagebox.showerror(TITLE, '必须是10或者13位')
            return
        text2.insert(tkinter.END, res)

    @staticmethod
    def transfer_date_timestamp(text1, text2, box):
        date_str = text1.get()
        if not date_str:
            messagebox.showwarning(TITLE, '请输入时间')
            return
        le = len(date_str)
        if le == 0:
            messagebox.showwarning(TITLE, '请输入时间')
            return
        text2.delete(0, tkinter.END)

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
        text2.insert(tkinter.END, res)


class MavenLayout:
    def __init__(self, frame: ttk.Frame):
        self.frame = frame

    def start(self):
        base_font = Font(family='Times New Roman', size=10, weight=NORMAL)

        configure_frame = ttk.LabelFrame(self.frame, text="配置", width=600, height=400)
        configure_frame.pack()
        m2_entry, m2, path_entry, path = self.configure(configure_frame, base_font)

        operation_frame = ttk.LabelFrame(self.frame, text="操作", width=600, height=400)
        operation_frame.pack()
        import_btn, clear_btn = self.operation(operation_frame)

        import_btn.bind('<Button-1>', func=lambda event: self.maven_install(m2, path))
        clear_btn.bind('<Button-1>',
                       func=lambda event: m2_entry.delete(0, tkinter.END) or path_entry.delete(0, tkinter.END))

    @staticmethod
    def configure(frame, base_font) -> (ttk.Entry, tkinter.StringVar, ttk.Entry, tkinter.StringVar):
        ComponentUtils.create_label(frame, 0, 0, "Maven Home", base_font)
        m2_entry = ComponentUtils.create_entry(frame, 0, 1)
        m2 = tkinter.StringVar()
        m2_entry.configure(cnf={"width": 75, "textvariable": m2})

        ComponentUtils.create_label(frame, 1, 0, "Local File", base_font)
        path_entry = ComponentUtils.create_entry(frame, 1, 1)
        path = tkinter.StringVar()
        path_entry.configure(cnf={"width": 75, "textvariable": path})

        return m2_entry, m2, path_entry, path

    @staticmethod
    def operation(frame) -> (ttk.Button, ttk.Button):
        # command=lambda: self.maven_install(m2, path)
        import_btn = ttk.Button(frame,
                                text="导入",
                                width=button_width)
        # command=lambda: m2_entry.delete(0, tk.END) or path_entry.delete(0, tk.END)
        import_btn.grid(row=0, column=1, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)

        clear_btn = ttk.Button(frame,
                               text="清除",
                               width=button_width)
        clear_btn.grid(row=0, column=2, sticky=tkinter.EW, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        return import_btn, clear_btn

    @staticmethod
    def maven_install(m2, path):
        """
        导出方式：
        mvn dependency:copy-dependencies
            -DoutputDirectory=lib/org.springframework.boot
            -DincludeArtifactIds=spring-boot-starter-data-mongodb
        mvn dependency:copy-dependencies
            -DoutputDirectory=lib/org.springframework.data
            -DincludeArtifactIds=spring-data-mongodb,spring-data-commons
        :param m2:
        :param path:
        :return:
        """
        m2_home = "mvn"
        if len(m2.get()) > 0:
            if not os.path.exists(m2.get()):
                messagebox.showerror(TITLE, 'Maven Home路径不存在')
                return
            m2_home = os.path.abspath(os.path.join(m2.get(), "/bin/mvn"))
        if not os.path.exists(path.get()):
            messagebox.showerror(TITLE, 'Local Path路径不存在')
            return
        cmd_template1 = m2_home + " install:install-file " \
                                  "-Dfile={} " \
                                  "-DgroupId={} " \
                                  "-DartifactId={} " \
                                  "-Dversion={} " \
                                  "-DpomFile={} " \
                                  "-Dpackaging={} "
        cmd_template2 = m2_home + " install:install-file " \
                                  "-Dfile={} " \
                                  "-DgroupId={} " \
                                  "-DartifactId={} " \
                                  "-Dversion={} " \
                                  "-Dpackaging={} "
        for r, dirs, files in os.walk(path.get()):
            if r == path.get():
                continue
            for f in files:
                if not f.endswith(".jar") and not f.endswith(".pom"):
                    continue
                file = os.path.join(r, f)
                groupId = os.path.basename(r)
                artifactId = f[0:f.rindex("-")]
                version = f[f.rindex("-") + 1:f.rindex(".")]
                pom = file[0:file.rindex(".") + 1] + "pom"
                if not os.path.exists(pom):
                    pom = ""
                packaging = f[f.rindex(".") + 1:]

                if len(pom) > 0:
                    cmd = cmd_template1.format(file, groupId, artifactId, version, pom, packaging)
                else:
                    cmd = cmd_template2.format(file, groupId, artifactId, version, packaging)
                print(cmd)
                print(os.system(cmd))
        messagebox.showinfo(TITLE, "导入成功")


class Base64Layout:
    def __init__(self, frame: ttk.Frame):
        self.frame = frame
        self.image = None
        self.filename_var = tkinter.StringVar()

    def start(self):
        base_font = Font(family='Times New Roman', size=10, weight=NORMAL)

        content_frame = ttk.LabelFrame(self.frame, text="内容区域", width=600, height=300)
        content_frame.pack()

        transfer_frame = ttk.LabelFrame(self.frame, text="转换区域", width=600, height=50)
        transfer_frame.pack()

        image_frame = ttk.LabelFrame(self.frame, text="图片区域", width=600, height=200)
        image_frame.pack()

        control_frame = ttk.LabelFrame(self.frame, text="操作区域", width=600, height=50)
        control_frame.pack()

        # 1. 内容区域
        code_label = ttk.Label(content_frame, text="Base64编码", font=base_font)
        code_label.grid(row=0, column=0, sticky=tkinter.EW)
        scrolled_text_in = ScrolledText(content_frame, height=8, wrap=tkinter.WORD, borderwidth=2,
                                        highlightcolor='gray',
                                        highlightthickness=1)
        scrolled_text_in.grid(row=1, column=0, columnspan=5, sticky=tkinter.EW, ipady=3)

        # 2. 转换区域
        btn1 = ComponentUtils.create_button(transfer_frame, "正向转换", 8)
        btn1.grid(row=0, column=0, sticky=tkinter.EW, ipady=3)

        btn2 = ComponentUtils.create_button(transfer_frame, "逆向转换", 8)
        btn2.grid(row=0, column=1, sticky=tkinter.EW, ipady=3)

        btn1.bind('<Button-1>', func=lambda event: self.base64_2_image(scrolled_text_in, show_image_canvas))
        btn2.bind('<Button-1>', func=lambda event: self.image_2_base64(scrolled_text_in))

        # 3. 图片区域
        show_image_canvas = tkinter.Canvas(image_frame, width=250, height=170, bg="red", highlightthickness=0)
        show_image_canvas.pack()

        # 4. 操作区域
        btn3 = ComponentUtils.create_button(control_frame, "上传图片", 8)
        btn3.grid(row=0, column=0, sticky=tkinter.EW, ipady=3)

        btn4 = ComponentUtils.create_button(control_frame, "下载图片", 8)
        btn4.grid(row=0, column=2, sticky=tkinter.EW, ipady=3)

        btn3.bind('<Button-1>', func=lambda event: self.select_image(show_image_canvas))
        btn4.bind('<Button-1>', func=lambda event: self.save_image())

    def base64_2_image(self, scrolled_text_in, show_image_canvas):
        in_content = scrolled_text_in.get("0.0", tkinter.END)
        if not in_content:
            messagebox.showerror(TITLE, "暂无内容")
            return
        img_data = base64.b64decode(in_content)
        filename = os.path.join(BASE_DIR, f"{time.time()}.png")
        with open(filename, 'wb') as f:
            f.write(img_data)
        self.show_image(filename, show_image_canvas)

    def image_2_base64(self, scrolled_text_in):
        fn = self.filename_var.get()
        if not fn:
            messagebox.showerror(TITLE, "暂无文件")
            return
        with open(fn, 'rb') as f:
            img_data = base64.b64encode(f.read())
        scrolled_text_in.insert(tkinter.INSERT, img_data)

    def save_image(self):
        from PIL import Image

        fn = self.filename_var.get()
        if not fn:
            messagebox.showerror(TITLE, "暂无文件下载")
            return
        image_open = Image.open(fn)
        image_open.save(os.path.join(BASE_DIR, os.path.basename(fn)))

    def select_image(self, show_image_canvas):
        """
        (1) tkinter.PhotoImage只能显示gif
        (2) from PIL import Image, ImageTk 处理jpg和png
        (3) PIL不支持Python3，需要安装pillow
        """
        filename = askopenfilename()
        if not filename:
            messagebox.showerror(TITLE, "请选择文件")
            return
        self.show_image(filename, show_image_canvas)

    def show_image(self, filename, show_image_canvas):
        """
        PIL(Python Imaging Library)是Python一个强大方便的图像处理库，名气也比较大。不过只支持到Python 2.7。
        Pillow是PIL的一个派生分支，但如今已经发展成为比PIL本身更具活力的图像处理库。pip install Pillow。
        from PIL import ImageTk, Image
        :param filename:
        :param show_image_canvas:
        :return:
        """
        from PIL import Image, ImageTk

        self.filename_var.set(filename)
        image_open = Image.open(filename)
        image = ImageTk.PhotoImage(image_open.resize((250, 170)))
        self.image = image  # 必须持久化，否则当做垃圾被回收
        # image = ImageTk.PhotoImage(image_open)
        # 1. Label显示图片
        # show_image_label = ttk.Label(image_frame, width=10)
        # show_image_label.config(image=image)
        # show_image_label.image = image
        # 2. canvas显示图片
        show_image_canvas.create_image(show_image_canvas.winfo_width() / 2,
                                       show_image_canvas.winfo_height() / 2,
                                       anchor='center', image=self.image)


class SpeedTestLayout:
    def __init__(self, frame):
        self.frame = frame

    def start(self):
        base_font = Font(family='Times New Roman', size=10, weight=NORMAL)

        control_frame = ttk.LabelFrame(self.frame, text="操作区域", width=600, height=50)
        control_frame.pack()

        show_frame = ttk.LabelFrame(self.frame, text="显示区域", width=600, height=300)
        show_frame.pack()
        btn1 = ComponentUtils.create_button(control_frame, "开始测试", 8)
        btn1.pack()
        label = ComponentUtils.create_label(show_frame, text="", fn=base_font)

        btn1.bind('<Button-1>', func=lambda event: label.configure({'text': self.do_test()}))

    @staticmethod
    def do_test():
        try:
            res = SpeedTestLayout.test()
        except RuntimeError as e:
            res = f"测试失败: {e}"
        return res

    @staticmethod
    def test():
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        st.results.share()
        results_dict = st.results.dict()
        download_speed = results_dict['download'] / (10 ** 6)
        upload_speed = results_dict['upload'] / (10 ** 6)
        print(f'下载速度: {download_speed} Mbps')
        print(f'上传速度: {upload_speed} Mbps')
        return f"下载速度: {download_speed} Mbps; 上传速度: {upload_speed} Mbps"
