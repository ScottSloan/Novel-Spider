import wx

from utils.core import BookInfo, DownloadInfo, get_group_list

from .save import SaveDialog
from .template import StdDialog

class OptionDialog(StdDialog):
    def __init__(self, parent):
        StdDialog.__init__(self, parent, "下载选项")
        
        self.init_UI()
        
        self.CenterOnParent()

        self.Bind_EVT()

        self.update_group_list()

    def init_UI(self):
        page_vbox = wx.BoxSizer(wx.VERTICAL)

        download_tip = wx.StaticText(self.panel, -1, "选择要下载的章节")
        
        self.all_rad = wx.RadioButton(self.panel, -1, "全部下载")

        self.select_rad = wx.RadioButton(self.panel, -1, "手动选择")
        self.group_list = wx.CheckListBox(self.panel, -1, size = self.FromDIP((350, 200)))
        
        self.group_list.Enable(False)

        group_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.select_all_chk = wx.CheckBox(self.panel, -1, "全选")
        self.group_chk = wx.CheckBox(self.panel, -1, "将章节分组")

        self.group_lab1 = wx.StaticText(self.panel, -1, "每")
        self.group_box = wx.SpinCtrl(self.panel, -1, size = self.FromDIP((50, 25)), initial = 20, max = 500, min = 1)
        self.group_lab2 = wx.StaticText(self.panel, -1, "章一组")

        self.set_group_hbox_enable(False)
        self.group_box.Enable(False)

        group_hbox.Add(self.select_all_chk, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 10)
        group_hbox.AddStretchSpacer()
        group_hbox.Add(self.group_chk, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 10)
        group_hbox.Add(self.group_lab1, 0, wx.ALIGN_CENTER)
        group_hbox.Add(self.group_box, 0, wx.LEFT | wx.RIGHT, 10)
        group_hbox.Add(self.group_lab2, 0, wx.ALIGN_CENTER | wx.RIGHT, 10)

        self.range_rad = wx.RadioButton(self.panel, -1, "指定范围")
        
        range_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.range_lab1 = wx.StaticText(self.panel, -1, "从第")
        self.range_lab2 = wx.StaticText(self.panel, -1, "章到第")
        self.range_lab3 = wx.StaticText(self.panel, -1, "章")

        self.range_start_box = wx.SpinCtrl(self.panel, -1, size = self.FromDIP((50, 25)), initial = 1, max = BookInfo.chapter_count, min = 1)
        self.range_end_box = wx.SpinCtrl(self.panel, -1, size = self.FromDIP((50, 25)), initial = BookInfo.chapter_count, max = BookInfo.chapter_count, min = 1)

        self.set_range_hbox_enable(False)

        range_hbox.Add(self.range_lab1, 0, wx.ALIGN_CENTER)
        range_hbox.Add(self.range_start_box, 0, wx.LEFT | wx.RIGHT, 10)
        range_hbox.Add(self.range_lab2, 0, wx.ALIGN_CENTER)
        range_hbox.Add(self.range_end_box, 0, wx.LEFT | wx.RIGHT, 10)
        range_hbox.Add(self.range_lab3, 0, wx.ALIGN_CENTER)

        action_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.next_btn = wx.Button(self.panel, -1, "下一步", size = self.FromDIP((90, 28)))

        action_hbox.AddStretchSpacer()
        action_hbox.Add(self.next_btn)

        page_vbox.Add(download_tip, 0, wx.LEFT | wx.TOP, 10)
        page_vbox.Add(self.all_rad, 0, wx.ALL, 10)
        page_vbox.Add(self.select_rad, 0, wx.ALL & (~wx.TOP), 10)
        page_vbox.Add(group_hbox, 0, wx.EXPAND | wx.BOTTOM, 10)
        page_vbox.Add(self.group_list, 0, wx.LEFT | wx.RIGHT, 10)
        page_vbox.Add(self.range_rad, 0, wx.ALL, 10)
        page_vbox.Add(range_hbox, 0, wx.LEFT | wx.RIGHT, 10)
        page_vbox.AddStretchSpacer()
        page_vbox.Add(action_hbox, 0, wx.ALL | wx.EXPAND, 10)

        self.panel.SetSizer(page_vbox)

        page_vbox.Fit(self)

    def Bind_EVT(self):
        self.all_rad.Bind(wx.EVT_RADIOBUTTON, self.all_rad_EVT)

        self.select_rad.Bind(wx.EVT_RADIOBUTTON, self.select_rad_EVT)

        self.range_rad.Bind(wx.EVT_RADIOBUTTON, self.range_rad_EVT)

        self.group_chk.Bind(wx.EVT_CHECKBOX, self.group_chk_EVT)

        self.group_box.Bind(wx.EVT_TEXT, self.group_box_EVT)

        self.next_btn.Bind(wx.EVT_BUTTON, self.next_btn_EVT)

        self.select_all_chk.Bind(wx.EVT_CHECKBOX, self.select_all_EVT)

        self.group_list.Bind(wx.EVT_CHECKLISTBOX, self.group_list_EVT)
        
    def all_rad_EVT(self, event):
        self.group_box.Enable(False)

        self.set_group_hbox_enable(False)

        self.set_range_hbox_enable(False)
    
    def select_rad_EVT(self, event):
        if self.group_chk.GetValue():
            self.group_box.Enable(True)

        self.set_group_hbox_enable(True)

        self.set_range_hbox_enable(False)
    
    def range_rad_EVT(self, event):
        self.group_box.Enable(False)

        self.set_group_hbox_enable(False)

        self.set_range_hbox_enable(True)

    def set_group_hbox_enable(self, state: bool):
        self.select_all_chk.Enable(state)
        self.group_chk.Enable(state)

        self.group_list.Enable(state)

        self.group_lab1.Enable(state)
        self.group_lab2.Enable(state)

    def set_range_hbox_enable(self, state: bool):
        self.range_start_box.Enable(state)
        self.range_end_box.Enable(state)

        self.range_lab1.Enable(state)
        self.range_lab2.Enable(state)
        self.range_lab3.Enable(state)
    
    def group_chk_EVT(self, event):
        self.group_box.Enable(self.group_chk.GetValue())

        self.update_group_list()

    def group_box_EVT(self, event):
        self.update_group_list()

    def update_group_list(self):
        if self.group_chk.GetValue():
            group = self.group_box.GetValue()
        else:
            group = 1

        get_group_list(group)

        self.group_list.Clear()
        self.group_list.Set(DownloadInfo.group_list_str)
    
    def next_btn_EVT(self, event):
        if self.all_rad.GetValue():
            DownloadInfo.download_chapter_index = list(range(BookInfo.chapter_count))

        elif self.select_rad.GetValue():
            self.process_select_group_list()
        
        else:
            start_index = self.range_start_box.GetValue() - 1
            end_index = self.range_end_box.GetValue()

            DownloadInfo.download_chapter_index = list(range(start_index, end_index))
        
        self.Hide()
        
        self.SaveDialog = SaveDialog(self.Parent)
        self.SaveDialog.ShowWindowModal()

        self.Destroy()

    def process_select_group_list(self):
        select_index = self.group_list.GetCheckedItems()

        all_index_list = []

        for index in select_index:
            tuple = DownloadInfo.group_list[index]

            all_index_list.extend(list(range(tuple[0], tuple[1])))

        DownloadInfo.download_chapter_index = all_index_list
    
    def select_all_EVT(self, event):
        if self.select_all_chk.GetValue():
            self.group_list.SetCheckedItems(range(0, self.group_list.GetCount()))
        else:
            self.group_list.SetCheckedItems([])
    
    def group_list_EVT(self, event):
        self.select_all_chk.SetValue(False)