import wx
import wx.adv

from utils.config import Config

class AboutWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)

        info = wx.adv.AboutDialogInfo()
        info.Name = Config.app_name
        info.Version = Config.app_version
        info.Description = "简易的小说爬取工具"
        info.Developers = ["Scott Sloan"]
        info.Copyright = "Copyright (C) 2021-2022 Scott Sloan"
        info.Licence = "MIT License"
        
        info.SetWebSite("https://github.com")

        wx.adv.AboutBox(info)