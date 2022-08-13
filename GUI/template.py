import wx

from utils.config import Config

class StdWindow(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, -1, title)

        self.SetSize(self.FromDIP(size))
    
        self.panel = wx.Panel(self, -1)

    def show_msg(self, caption, message, style):
        dlg = wx.MessageDialog(self, message, caption, style)
        dlg.ShowModal()

class StdDialog(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title)
    
        self.panel = wx.Panel(self, -1)
    
    def show_msg(self, caption, message, style):
        dlg = wx.MessageDialog(self, message, caption, style)
        dlg.ShowModal()
        
class StdPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
    
    @property
    def ParentWindow(self):
        return self.GetParent().GetParent().GetParent()
    
    @property
    def StatusBar(self):
        return self.GetParent().GetParent().GetParent().status_bar

    def SetPage(self, page: int):
        self.ParentWindow.container.ChangeSelection(page)
    
    def SetTitle(self, name: str):
        self.ParentWindow.SetTitle("{} - {}".format(Config.app_name, name))

    def ClearTitle(self):
        self.ParentWindow.SetTitle(Config.app_name)

    def show_msg(self, caption: str, message: str, style):
        self.ParentWindow.show_msg(caption, message, style)

class RequestError(Exception):
    def __init__(self, error):
        Exception.__init__(self)

        self.error = error
    
    def __str__(self):
        return self.error