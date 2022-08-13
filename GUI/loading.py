import wx

from .template import StdPage

class LoadingPage(StdPage):
    def __init__(self, parent):
        StdPage.__init__(self, parent)

        self.init_UI()
        self.Bind_EVT()

    def init_UI(self):
        page_vbox = wx.BoxSizer(wx.VERTICAL)

        ai_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.ai = wx.ActivityIndicator(self, -1)
        ai_lab = wx.StaticText(self, -1, "正在加载中，请稍候")
        
        ai_hbox.Add(self.ai, 0, wx.ALL, 10)
        ai_hbox.Add(ai_lab, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        self.cancel_btn = wx.Button(self, -1, "取消", size = self.FromDIP((80, 28)))

        page_vbox.AddStretchSpacer()
        page_vbox.Add(ai_hbox, 0, wx.ALIGN_CENTER)
        page_vbox.Add(self.cancel_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        page_vbox.AddStretchSpacer()

        self.SetSizer(page_vbox)
    
    def Bind_EVT(self):
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.cancel_btn_EVT)
    
    def cancel_btn_EVT(self, event):
        self.ai.Stop()

        self.SetPage(0)