import wx

from utils.core import BookInfo
from utils.config import Config

from .template import StdWindow, StdPage

class PreviewWindow(StdWindow):
    def __init__(self, parent):
        StdWindow.__init__(self, parent, "章节预览", (480, 320))

        self.CenterOnParent()
        self.init_UI()

        self.Bind_EVT()
    
    def init_UI(self):
        window_vbox = wx.BoxSizer(wx.VERTICAL)

        self.container = wx.Simplebook(self.panel, -1)
        
        self.LoadingPage = LoadingPage(self.container)
        self.ReadPage = ReadPage(self.container)

        self.container.AddPage(self.LoadingPage, "Loading")
        self.container.AddPage(self.ReadPage, "Read")

        window_vbox.Add(self.container, 1, wx.ALL | wx.EXPAND, 10)
        
        self.panel.SetSizer(window_vbox)

    def Bind_EVT(self):
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        self.Parent.DetailPage.deselect_item()

        self.Parent.DetailPage.del_preview_window()
        
        self.Destroy()

    def start_loading(self):
        self.SetTitle("章节预览 - 正在加载")

        self.LoadingPage.ai.Start()
        self.container.ChangeSelection(0)

    def stop_loading(self):
        self.SetTitle("章节预览 - {}".format(BookInfo.current_chapter_name))
        self.LoadingPage.ai.Stop()
        self.container.ChangeSelection(1)
    
    @property
    def DetailPage(self):
        return self.Parent.DetailPage

    def set_content(self):
        index = self.DetailPage.index

        if index == 0:
            self.ReadPage.previous_btn.Enable(False)
        else:
            self.ReadPage.previous_btn.Enable(True)

        if index == BookInfo.chapter_count - 1:
            self.ReadPage.next_btn.Enable(False)
        else:
            self.ReadPage.next_btn.Enable(True)

        self.ReadPage.add_chk_EVT(0)

    def previous_chapter(self):
        self.DetailPage.previous_chapter()

    def next_chapter(self):
        self.DetailPage.next_chapter()

class ReadPage(StdPage):
    def __init__(self, parent):
        StdPage.__init__(self, parent)

        self.init_UI()
        self.Bind_EVT()

    def init_UI(self):
        page_vbox = wx.BoxSizer(wx.VERTICAL)

        self.add_chk = wx.CheckBox(self, -1, "自动添加章节标题")
        self.add_chk.SetValue(Config.add_chapter_title)

        self.content_box = wx.TextCtrl(self, -1, style = wx.TE_READONLY | wx.TE_MULTILINE)
        
        action_hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.previous_btn = wx.Button(self, -1, "上一章", size = self.FromDIP((80, 28)))
        self.next_btn = wx.Button(self, -1, "下一章", size = self.FromDIP((80, 28)))

        action_hbox.Add(self.previous_btn)
        action_hbox.AddStretchSpacer()
        action_hbox.Add(self.next_btn)

        page_vbox.Add(self.add_chk, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 10)
        page_vbox.Add(self.content_box, 1, wx.EXPAND)
        page_vbox.Add(action_hbox, 0, wx.EXPAND | wx.TOP, 10)

        self.SetSizer(page_vbox)

    def Bind_EVT(self):
        self.add_chk.Bind(wx.EVT_CHECKBOX, self.add_chk_EVT)

        self.previous_btn.Bind(wx.EVT_BUTTON, self.previous_btn_EVT)
        self.next_btn.Bind(wx.EVT_BUTTON, self.next_btn_EVT)

    def add_chk_EVT(self, event):
        if self.add_chk.GetValue():
            title = BookInfo.current_chapter_name + "\n\n"
        else:
            title = ""

        self.content_box.SetValue(title + BookInfo.current_chapter_content.getvalue())
        
        Config.add_chapter_title = self.add_chk.GetValue()

    def previous_btn_EVT(self, event):
        self.ParentWindow.previous_chapter()

    def next_btn_EVT(self, event):
        self.ParentWindow.next_chapter()

class LoadingPage(StdPage):
    def __init__(self, parent):
        StdPage.__init__(self, parent)

        self.init_UI()

    def init_UI(self):
        page_vbox = wx.BoxSizer(wx.VERTICAL)

        ai_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.ai = wx.ActivityIndicator(self, -1)
        ai_lab = wx.StaticText(self, -1, "正在加载中，请稍候")
        
        ai_hbox.Add(self.ai, 0, wx.ALL, 10)
        ai_hbox.Add(ai_lab, 0, wx.ALL | wx.ALIGN_CENTER, 10)        

        page_vbox.AddStretchSpacer()
        page_vbox.Add(ai_hbox, 0, wx.ALIGN_CENTER)
        page_vbox.AddStretchSpacer()

        self.SetSizer(page_vbox)