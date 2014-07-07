#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import wx.html2

news = [("Новость 1", "Текст новости"), ("Новость 2", "Текст новости"), ("Новость 2", "Текст новости")]
html_template = "<h3>%s</h3><p>%s</p>"
html_string = ""


class MyBrowser(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((400, 500))


if __name__ == '__main__':
    app = wx.App()
    dialog = MyBrowser(None, -1)
    dialog.SetTitle('Читалка новостей')
    for pair in news:
        html_string += html_template % pair
    dialog.browser.SetPage(html_string, "")
    dialog.Show()
    app.MainLoop()
