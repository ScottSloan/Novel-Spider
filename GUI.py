from GUI.main import MainWindow

import wx

if __name__ == "__main__":
    app = wx.App()
        
    main_window = MainWindow()

    main_window.Show()

    app.MainLoop()