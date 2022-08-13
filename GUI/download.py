import os
import wx
from threading import Thread
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from utils.core import BookInfo, DownloadInfo, get_chapter_content
from utils.config import Config

class DownloadWindow(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "正在下载")

        self.init_UI()

        self.Bind_EVT()

        self.CenterOnParent()

        Thread(target = self.start_download).start()

    def init_UI(self):
        self.panel = wx.Panel(self, -1)

        window_vbox = wx.BoxSizer(wx.VERTICAL)

        self.progress_lab = wx.StaticText(self.panel, -1, "准备开始下载")

        self.progress = wx.Gauge(self.panel, -1, size = self.FromDIP((300, 25)), style = wx.GA_SMOOTH)

        action_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.minimize_btn = wx.Button(self.panel, -1, "最小化", size = self.FromDIP((80, 28)))
        self.cancel_btn = wx.Button(self.panel, -1, "取消", size = self.FromDIP((80, 28)))

        action_hbox.Add(self.minimize_btn, 0, wx.ALL, 10)
        action_hbox.AddStretchSpacer()
        action_hbox.Add(self.cancel_btn, 0, wx.ALL, 10)

        window_vbox.Add(self.progress_lab, 0, wx.EXPAND | wx.ALL, 10)
        window_vbox.Add(self.progress, 0, wx.EXPAND | wx.ALL & (~wx.TOP), 10)
        window_vbox.Add(action_hbox, 0, wx.EXPAND)

        self.panel.SetSizer(window_vbox)

        window_vbox.Fit(self)
    
    def Bind_EVT(self):
        self.minimize_btn.Bind(wx.EVT_BUTTON, self.minimize_btn_EVT)

        self.cancel_btn.Bind(wx.EVT_BUTTON, self.cancel_btn_EVT)

    def start_download(self):
        self.progress.Pulse()

        self.threadpool = ThreadPoolExecutor(max_workers = Config.thread_number)

        DownloadInfo.download_count = len(DownloadInfo.download_chapter_index)
        DownloadInfo.complete_count = 0
        DownloadInfo.error_count = 0
        
        task_list = []

        for index in DownloadInfo.download_chapter_index:
            name = BookInfo.chapter_name_list[index]
            url = BookInfo.chapter_url_list[index]

            task_list.append(self.threadpool.submit(self.download_thread, index, name, url))

        wait(task_list, return_when = ALL_COMPLETED)

        wx.CallAfter(self.download_complete)

    def download_thread(self, index: int, name: str, url: str):
        content = get_chapter_content(url, self.on_error)

        DownloadInfo.content[index] = (name, content)

        DownloadInfo.complete_count += 1

        wx.CallAfter(self.update_progress, name)

    def update_progress(self, name: str):
        progress = int(DownloadInfo.complete_count / DownloadInfo.download_count * 100)

        self.progress.SetValue(progress)

        self.progress_lab.SetLabel("[{}%] 正在下载：{}".format(progress, name))

    def download_complete(self):
        self.save_to_file()

        self.Hide()
        self.RequestUserAttention(wx.USER_ATTENTION_INFO)

        if DownloadInfo.error_count != 0:
            error = "\n\n其中有 {} 个章节下载失败".format(DownloadInfo.error_count)
        else:
            error = ""

        dlg = wx.MessageDialog(self.Parent, '下载完成\n\n小说《{}》下载完成'.format(BookInfo.name) + error, "提示", style = wx.ICON_INFORMATION | wx.YES_NO)
        dlg.SetYesNoLabels("打开所在位置", "确定")

        if dlg.ShowModal() == wx.ID_YES:
            os.startfile(Config.download_path)

        self.Destroy()

    def save_to_file(self):
        self.threadpool.shutdown()

        DownloadInfo.content = dict(sorted(DownloadInfo.content.items(), key = lambda x: x[0]))

        for tuple in DownloadInfo.content.values():
            if Config.add_chapter_title:
                title = tuple[0] + "\n\n"
            else:
                title = ""

            DownloadInfo.file.write(title + tuple[1].getvalue() + "\n\n")

            tuple[1].close()
        
        with open(DownloadInfo.filepath, "w", encoding = "utf-8") as f:
            f.write(DownloadInfo.file.getvalue())
        
        DownloadInfo.content = {}
        
        DownloadInfo.file.close()
        DownloadInfo.file = StringIO()
    
    def minimize_btn_EVT(self, event):
        self.Parent.Iconize()

    def cancel_btn_EVT(self, event):
        dlg = wx.MessageDialog(self, "确认取消下载\n\n是否取消下载小说", "警告", style = wx.ICON_WARNING | wx.YES_NO)

        if dlg.ShowModal() == wx.ID_YES:
            self.threadpool.shutdown(wait = False, cancel_futures = True)

            self.Hide()

    def on_error(self, e):
        DownloadInfo.error_count += 1