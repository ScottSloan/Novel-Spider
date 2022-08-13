from threading import Thread
import wx

from utils.core import BookInfo, get_chapter_content
from .template import StdPage, RequestError
from .preview import PreviewWindow
from .option import OptionDialog

class DetailPage(StdPage):
    def __init__(self, parent):
        StdPage.__init__(self, parent)

        self.init_UI()
        self.Bind_EVT()

    def init_UI(self):
        page_vbox = wx.BoxSizer(wx.VERTICAL)

        info_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.info_name_lab = wx.StaticText(self, -1, "书名：null")
        self.info_author_lab = wx.StaticText(self, -1, "作者：null")

        info_hbox.Add(self.info_name_lab, 1, wx.ALL, 10)
        info_hbox.Add(self.info_author_lab, 1, wx.ALL, 10)

        self.chapter_lab = wx.StaticText(self, -1, "章节列表（共 null 章）")
        self.chapter_list = wx.ListBox(self, -1)

        action_hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.back_btn = wx.Button(self, -1, "返回搜索页", size = self.FromDIP((90, 28)))
        self.download_btn = wx.Button(self, -1, "爬取小说", size = self.FromDIP((90, 28)))

        action_hbox.Add(self.back_btn)
        action_hbox.AddStretchSpacer()
        action_hbox.Add(self.download_btn)

        page_vbox.Add(info_hbox, 0, wx.EXPAND)
        page_vbox.Add(self.chapter_lab, 0, wx.ALL & (~wx.BOTTOM), 10)
        page_vbox.Add(self.chapter_list, 1, wx.EXPAND | wx.ALL, 10)
        page_vbox.Add(action_hbox, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        self.SetSizer(page_vbox)

    def Bind_EVT(self):
        self.back_btn.Bind(wx.EVT_BUTTON, self.back_btn_EVT)

        self.download_btn.Bind(wx.EVT_BUTTON, self.download_btn_EVT)
        
        self.chapter_list.Bind(wx.EVT_LISTBOX, self.chapter_list_EVT)

    def init_book_detail(self):
        self.SetTitle(BookInfo.name)

        self.info_name_lab.SetLabel("书名：{}".format(BookInfo.name))
        self.info_author_lab.SetLabel("作者：{}".format(BookInfo.author))

        self.chapter_lab.SetLabel("章节列表（共 {} 章）".format(BookInfo.chapter_count))
        
        self.chapter_list.Clear()
        self.chapter_list.Set(BookInfo.chapter_name_list)
    
    def back_btn_EVT(self, event):
        self.SetPage(0)

        self.ClearTitle()

        if hasattr(self, "preview_window"):
            self.preview_window.Destroy()

            self.del_preview_window()
            
    def download_btn_EVT(self, event):
        self.OptionDialog = OptionDialog(self.ParentWindow)

        self.OptionDialog.ShowWindowModal()
        
    def chapter_list_EVT(self, event):
        self.index = self.chapter_list.GetSelection()

        BookInfo.current_chapter_name = BookInfo.chapter_name_list[self.index]
        BookInfo.current_chapter_url = BookInfo.chapter_url_list[self.index]

        if not hasattr(self, "preview_window"):
            self.preview_window = PreviewWindow(self.ParentWindow)

        self.preview_window.Iconize(False)
        self.preview_window.ReadPage.content_box.SetFocus()

        self.preview_window.start_loading()

        Thread(target = self.preview_chapter_thread).start()

        self.preview_window.Show()
    
    def preview_chapter_thread(self):
        temp = get_chapter_content(BookInfo.current_chapter_url, self.on_preview_error)

        BookInfo.current_chapter_content = temp

        self.preview_window.set_content()

        self.preview_window.stop_loading()
    
    def previous_chapter(self):
        self.chapter_list.SetSelection(self.index - 1)

        self.chapter_list_EVT(0)

    def next_chapter(self):
        self.chapter_list.SetSelection(self.index + 1)

        self.chapter_list_EVT(0)
    
    def deselect_item(self):
        self.chapter_list.Deselect(self.index)
    
    def del_preview_window(self):
        del self.preview_window

    def on_preview_error(self, e):
        self.show_msg("错误", "加载失败\n\n" + e, wx.ICON_ERROR)

        self.preview_window.Destroy()
        self.del_preview_window()

        raise RequestError("加载失败")