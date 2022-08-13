import wx

from threading import Thread

from .template import StdPage, RequestError

from utils.core import SearchResult, Site, BookInfo, search_book, get_book_chapters
from utils.db import load_site_cfg

class SearchPage(StdPage):
    def __init__(self, parent):
        StdPage.__init__(self, parent)
        
        self.init_UI()
        self.Bind_EVT()

        self.init_site_select()
        self.init_result_box()

        self.is_searching = False

    def init_UI(self):
        page_vbox = wx.BoxSizer(wx.VERTICAL)

        search_hbox = wx.BoxSizer(wx.HORIZONTAL)

        search_lab = wx.StaticText(self, -1, "搜索小说")
        self.search_box = wx.TextCtrl(self, -1, style = wx.TE_PROCESS_ENTER)
        self.search_btn = wx.Button(self, -1, "搜索", size = self.FromDIP((70, 28)))
        
        site_lab = wx.StaticText(self, -1, "站点：")
        self.site_select = wx.Choice(self, -1)

        search_hbox.Add(search_lab, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        search_hbox.Add(self.search_box, 1, wx.ALIGN_CENTER | wx.ALL & (~wx.LEFT), 10)
        search_hbox.Add(self.search_btn, 0, wx.ALL, 10)
        search_hbox.AddSpacer(20)
        search_hbox.Add(site_lab, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        search_hbox.Add(self.site_select, 0, wx.ALIGN_CENTER | wx.ALL & (~wx.LEFT), 10)

        self.reslut_box = wx.ListCtrl(self, -1, style = wx.LC_REPORT)

        self.tip_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.ai = wx.ActivityIndicator(self, -1)
        self.ai.Show(False)
        self.tip = wx.StaticText(self, -1, "请开始搜索小说")

        self.tip_hbox.Add(self.ai)
        self.tip_hbox.Add(self.tip, 0, wx.ALIGN_CENTER | wx.LEFT, 10)

        page_vbox.Add(search_hbox, 0, wx.EXPAND)
        page_vbox.Add(self.reslut_box, 1, wx.EXPAND | wx.ALL, 10)
        page_vbox.Add(self.tip_hbox, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        self.SetSizer(page_vbox)

    def Bind_EVT(self):
        self.site_select.Bind(wx.EVT_CHOICE, self.site_select_EVT)

        self.search_box.Bind(wx.EVT_TEXT_ENTER, self.search_btn_EVT)
        self.search_btn.Bind(wx.EVT_BUTTON, self.search_btn_EVT)

        self.reslut_box.Bind(wx.EVT_LIST_ITEM_SELECTED, self.result_box_EVT)

    def init_result_box(self):
        self.reslut_box.ClearAll()

        self.reslut_box.InsertColumn(0, "序号", width = self.FromDIP(35))
        self.reslut_box.InsertColumn(1, "书名", width = self.FromDIP(220))
        self.reslut_box.InsertColumn(2, "作者", width = self.FromDIP(130))
    
    def init_site_select(self):
        load_site_cfg(0)

        self.site_select.Set(Site.site_list)

        self.site_select.SetSelection(0)

    def site_select_EVT(self, event):
        load_site_cfg(self.site_select.GetSelection())
    
    def search_btn_EVT(self, event):
        if self.search_box.GetValue() == "":
            self.show_msg("警告", "搜索关键字不能为空", wx.ICON_WARNING)
            return
        
        if self.is_searching:
            self.show_msg("警告", "请等待搜索结束", wx.ICON_WARNING)
            return

        self.init_result_box()

        Thread(target = self.search_thread).start()
        
        self.tip.SetLabel("正在搜索中，请稍候")
        self.SetTitle("正在搜索")
        self.set_search_status(True)

    def search_thread(self):
        keywords = self.search_box.GetValue()

        search_book(keywords, self.on_search_error)

        for index in range(SearchResult.count):
            self.reslut_box.InsertItem(index, str(index + 1))
            self.reslut_box.SetItem(index, 1, SearchResult.name_list[index])
            self.reslut_box.SetItem(index, 2, SearchResult.author_list[index])
        
        self.tip.SetLabel("共 {} 条搜索结果".format(SearchResult.count))
        self.ClearTitle()

        self.set_search_status(False)

    def set_search_status(self, status: bool):
        self.is_searching = status
        self.search_btn.Enable(not status)
        self.ai.Show(status)
        
        if status: self.ai.Start()
        else: self.ai.Stop()

        self.tip_hbox.Layout()

    def result_box_EVT(self, event):
        self.index = self.reslut_box.GetFocusedItem()

        BookInfo.name = self.reslut_box.GetItemText(self.index, 1)
        BookInfo.author = self.reslut_box.GetItemText(self.index, 2)
        BookInfo.url = SearchResult.url_list[self.index]

        self.ParentWindow.LoadingPage.ai.Start()
        self.SetPage(1)
        self.SetTitle("正在加载")

        Thread(target = self.get_book_detail_thread).start()

    def get_book_detail_thread(self):
        get_book_chapters(BookInfo.url, self.on_load_error)
        
        self.reslut_box.SetItemState(self.index, 0, wx.LIST_STATE_SELECTED)
        
        self.ParentWindow.LoadingPage.ai.Stop()
        self.SetPage(2)

        self.ParentWindow.DetailPage.init_book_detail()

    def on_search_error(self, e: str):
        self.show_msg("错误", "请求失败\n\n" + e, wx.ICON_ERROR)

        self.tip.SetLabel("搜索失败，请重试")
        self.ClearTitle()

        self.set_search_status(False)

        raise RequestError("请求失败")

    def on_load_error(self, e: str):
        self.show_msg("错误", "加载失败\n\n" + e, wx.ICON_ERROR)

        self.reslut_box.SetItemState(self.index, 0, wx.LIST_STATE_SELECTED)

        self.ParentWindow.LoadingPage.ai.Stop()
        self.SetPage(0)
        self.ClearTitle()
        
        raise RequestError("加载失败")
