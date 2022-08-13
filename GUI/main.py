import wx

from .search import SearchPage
from .loading import LoadingPage
from .detail import DetailPage
from .about import AboutWindow
from .template import StdWindow

from utils.config import Config

class MainWindow(StdWindow):
    def __init__(self):
        StdWindow.__init__(self, None, Config.app_name, (550, 400))

        self.CenterOnScreen()

        self.init_UI()
        self.init_MenuBar()
        self.init_SatusBar()

    def init_UI(self):
        window_vbox = wx.BoxSizer(wx.VERTICAL)

        self.container = wx.Simplebook(self.panel, -1)

        self.SearchPage = SearchPage(self.container)
        self.LoadingPage = LoadingPage(self.container)
        self.DetailPage = DetailPage(self.container)

        self.container.AddPage(self.SearchPage, "Search")
        self.container.AddPage(self.LoadingPage, "Loading")
        self.container.AddPage(self.DetailPage, "Detail")

        window_vbox.Add(self.container, 1, wx.ALL | wx.EXPAND, 10)

        self.panel.SetSizer(window_vbox)
    
    def init_MenuBar(self):
        menu_bar = wx.MenuBar()

        help_menu = wx.Menu()

        help_menu.Append(100, "关于(&A)", " 关于本程序")

        menu_bar.Append(help_menu, "帮助(&H)")

        self.SetMenuBar(menu_bar)

        menu_bar.Bind(wx.EVT_MENU, self.about_menu_EVT, id = 100)

    def init_SatusBar(self):
        self.status_bar = wx.StatusBar(self, -1)
        
        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusWidths([-1, -1])

        self.SetStatusBar(self.status_bar)

        self.status_bar.SetStatusText(" 就绪", 0)
    
    def about_menu_EVT(self, event):
        AboutWindow(self)