import os
import wx

from .download import DownloadWindow
from .template import StdDialog

from utils.core import DownloadInfo, BookInfo
from utils.config import Config

class SaveDialog(StdDialog):
    def __init__(self, parent):
        StdDialog.__init__(self, parent, "下载选项")

        self.init_UI()
        
        self.CenterOnParent()

        self.Bind_EVT()

        self.init_setting()

    def init_UI(self):
        window_vbox = wx.BoxSizer(wx.VERTICAL)

        filename_hbox = wx.BoxSizer(wx.HORIZONTAL)

        filename_lab = wx.StaticText(self.panel, -1, "文件名   ")
        self.filename_box = wx.TextCtrl(self.panel, -1, size = self.FromDIP((200, 25)))

        filename_hbox.Add(filename_lab, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        filename_hbox.Add(self.filename_box, 0, wx.ALL & (~wx.LEFT), 10)

        filepath_hbox = wx.BoxSizer(wx.HORIZONTAL)

        filepath_lab = wx.StaticText(self.panel, -1, "保存位置")
        self.filepath_box = wx.TextCtrl(self.panel, -1, size = self.FromDIP((200, 25)))
        self.browse_btn = wx.Button(self.panel, -1, "浏览", size = self.FromDIP((60, 25)))

        filepath_hbox.Add(filepath_lab, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        filepath_hbox.Add(self.filepath_box, 10, wx.ALL & (~wx.LEFT), 10)
        filepath_hbox.Add(self.browse_btn, 0, wx.ALL & (~wx.LEFT) | wx.ALIGN_CENTER, 10)

        filetype_hbox = wx.BoxSizer(wx.HORIZONTAL)

        filetype_lab = wx.StaticText(self.panel, -1, "文件格式")
        self.filetype_select = wx.Choice(self.panel, -1, choices = [".txt", ".epub"])

        filetype_hbox.Add(filetype_lab, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        filetype_hbox.Add(self.filetype_select, 0, wx.ALL & (~wx.LEFT), 10)
        
        self.add_chk = wx.CheckBox(self.panel, -1, "自动添加章节标题")

        self.start_btn = wx.Button(self.panel, -1, "开始下载", size = self.FromDIP((100, 35)))

        window_vbox.Add(filename_hbox, 0, wx.EXPAND)
        window_vbox.Add(filepath_hbox, 0, wx.EXPAND)
        window_vbox.Add(filetype_hbox, 0, wx.EXPAND)
        window_vbox.Add(self.add_chk, 0, wx.ALL & (~wx.BOTTOM), 10)
        window_vbox.Add(self.start_btn, 0, wx.ALL | wx.ALIGN_RIGHT, 10)

        self.panel.SetSizer(window_vbox)

        window_vbox.Fit(self)
    
    def Bind_EVT(self):
        self.start_btn.Bind(wx.EVT_BUTTON, self.start_btn_EVT)

        self.browse_btn.Bind(wx.EVT_BUTTON, self.browse_btn_EVT)

    def init_setting(self):
        self.filename_box.SetValue(BookInfo.name)
        self.filepath_box.SetValue(Config.download_path)
        self.filetype_select.SetSelection(DownloadInfo.filetype)

        self.add_chk.SetValue(Config.add_chapter_title)

    def start_btn_EVT(self, event):
        DownloadInfo.filepath = os.path.join(self.filepath_box.GetValue(), self.filename_box.GetValue()) + self.filetype_select.GetStringSelection()
        
        self.Hide()
        
        self.download_window = DownloadWindow(self.Parent)
        self.download_window.ShowWindowModal()

        self.Destroy()

    def browse_btn_EVT(self, event):
        dlg = wx.DirDialog(self, "浏览", defaultPath = self.filepath_box.GetValue())
        
        if dlg.ShowModal() == wx.ID_OK:
            self.filepath_box.SetValue(dlg.GetPath())
