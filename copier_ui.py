# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

md5 = 1000
xxhash = 1001
ID_STOP = 1002


###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Copier v0.1a", pos=wx.DefaultPosition,
                          size=wx.Size(500, 420), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(500, 420), wx.Size(500, 420))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel1.SetBackgroundColour(wx.Colour(77, 77, 77))

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_bitmap1 = wx.StaticBitmap(self.m_panel1, wx.ID_ANY,
                                         wx.Bitmap(u"imgs/copier_logo.png", wx.BITMAP_TYPE_ANY), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gSizer1.Add(self.m_bitmap1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Copier", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        self.m_staticText1.SetFont(
            wx.Font(25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Verdana"))
        self.m_staticText1.SetForegroundColour(wx.Colour(255, 255, 255))

        bSizer2.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_staticText2 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"v0.1a", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)

        self.m_staticText2.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))
        self.m_staticText2.SetForegroundColour(wx.Colour(255, 255, 255))

        bSizer2.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        gSizer1.Add(bSizer2, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_panel1.SetSizer(gSizer1)
        self.m_panel1.Layout()
        gSizer1.Fit(self.m_panel1)
        bSizer1.Add(self.m_panel1, 1, wx.EXPAND, 5)

        gSizer3 = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Source Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        self.m_staticText3.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        gSizer3.Add(self.m_staticText3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM | wx.BOTTOM, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Destination Folder", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText4.Wrap(-1)

        self.m_staticText4.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        gSizer3.Add(self.m_staticText4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM | wx.BOTTOM, 5)

        self.in_folder = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                          wx.Size(-1, -1), wx.DIRP_DEFAULT_STYLE)
        self.in_folder.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE))

        gSizer3.Add(self.in_folder, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        self.out_folder = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                           wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        self.out_folder.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE))

        gSizer3.Add(self.out_folder, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        bSizer1.Add(gSizer3, 1, wx.EXPAND, 5)

        gSizer4 = wx.GridSizer(0, 3, 0, 0)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"Folder Actions", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)

        self.m_staticText8.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        bSizer3.Add(self.m_staticText8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Copy Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"Verify Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer4.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"MHL Actions", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        self.m_staticText9.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        bSizer4.Add(self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Generate MHL", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_button2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer4.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"Hash Mode", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        self.m_staticText10.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        bSizer5.Add(self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.rb_md5 = wx.RadioButton(self, md5, u"MD5", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
        self.rb_md5.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        bSizer5.Add(self.rb_md5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.rb_xxhash = wx.RadioButton(self, xxhash, u"xxHash64", wx.DefaultPosition, wx.DefaultSize, 0)
        self.rb_xxhash.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        bSizer5.Add(self.rb_xxhash, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer4.Add(bSizer5, 1, wx.EXPAND, 5)

        bSizer1.Add(gSizer4, 1, wx.EXPAND, 5)

        self.m_button5 = wx.Button(self, ID_STOP, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.pg_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.pg_bar.SetValue(0)
        bSizer1.Add(self.pg_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.copy_thread_start)
        self.m_button3.Bind(wx.EVT_BUTTON, self.verify_thread_start)
        self.m_button2.Bind(wx.EVT_BUTTON, self.mhl_thread_start)
        self.m_button5.Bind(wx.EVT_BUTTON, self.cancel_task)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def copy_thread_start(self, event):
        event.Skip()

    def verify_thread_start(self, event):
        event.Skip()

    def mhl_thread_start(self, event):
        event.Skip()

    def cancel_task(self, event):
        event.Skip()
