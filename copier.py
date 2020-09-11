"""
                                Copier V0.1a

                                 MIT License

                      Copyright (c) 2020 Marcelo Daros

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
"""

import platform
from threading import *
import os
import fnmatch
import hashlib
import datetime
from xml.dom.minidom import Document
import socket
import wx

# Define notification event for thread completion
EVT_RESULT_ID = 100
EVT_UPDATE_ID = 101

md5 = 1000
xxhash = 1001

ID_COPY = 201
ID_VERIFY = 202
ID_MHL = 203
ID_STOP = 210


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


def EVT_UPDATE(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_UPDATE_ID, func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class UpdateEvent(wx.PyEvent):
    """Simple event to carry updates data."""

    def __init__(self, fname, progress, task):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_UPDATE_ID)
        self.fname = fname
        self.progress = progress
        self.task = task


class CopyThread(Thread):
    def __init__(self, main_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._main_window = main_window
        self.want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        in_folder = self._main_window.in_folder.GetPath()
        out_folder = self._main_window.out_folder.GetPath()

        if os.path.basename(in_folder) != os.path.basename(out_folder):
            out_folder = os.path.join(out_folder, os.path.basename(in_folder))

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        files_count = 0
        for path, dirs, files in os.walk(in_folder):
            if not os.path.exists(os.path.join(out_folder, path.replace(in_folder, "")[1:])):
                os.mkdir(os.path.join(out_folder, path.replace(in_folder, "")[1:]))
            for f in fnmatch.filter(files, '*.*'):
                files_count += 1

        for path, dirs, files in os.walk(in_folder):
            for f in fnmatch.filter(files, '*.*'):
                in_fullname = os.path.abspath(os.path.join(path, f))
                out_fullname = os.path.join(out_folder, in_fullname[len(in_folder) + 1:])

                if os.path.exists(out_fullname):
                    if os.stat(in_fullname).st_size == os.stat(out_fullname).st_size:
                        continue

                total = os.stat(in_fullname).st_size
                progress = 0
                out_file = open(out_fullname, "wb")
                with open(in_fullname, "rb") as in_file:
                    for chunk in iter(lambda: in_file.read(5242880), b""):
                        if self.want_abort:
                            # Use a result of None to acknowledge the abort
                            wx.PostEvent(self._main_window, ResultEvent(None))
                            return

                        out_file.write(chunk)
                        progress += 5242880
                        bar_value = int((progress / total) * 100)
                        wx.PostEvent(self._main_window, UpdateEvent(in_fullname, bar_value, "Copying"))

        errors = self.check_folders(in_folder, out_folder)
        if self.want_abort:
            # Use a result of None to acknowledge the abort
            wx.PostEvent(self._main_window, ResultEvent(None))
            return

        report = ""
        if len(errors) == 0:
            wx.PostEvent(self._main_window, ResultEvent(1))
        else:
            for err in errors:
                report = report + err + "\n"

            if platform != "win32" and platform != "cygwin":
                desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            else:
                desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

            report = report + "\n\nGenerated by Copier v0.1a"
            report_name = "Error_Report" + datetime.datetime.now().strftime("_%Y-%m-%d_%H%M%S") + ".txt"
            report_f = open(os.path.join(desktop, report_name), "w")
            report_f.write(report)
            report_f.close()
            wx.PostEvent(self._main_window, ResultEvent(102))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self.want_abort = 1

    def check_folders(self, in_folder, out_folder):
        hashes = Hashes()

        if self._main_window.rb_md5.GetValue():
            hash_mode = "md5"
        else:
            hash_mode = "xxhash"

        files_in = hashes.hash_files(in_folder, hash_mode, self._main_window, self)
        files_out = hashes.hash_files(out_folder, hash_mode, self._main_window, self)

        errors = []
        for file_in in files_in:
            for file_out in files_out:
                if file_in.file_name.replace(in_folder, "")[1:] == file_out.file_name.replace(out_folder, "")[1:]:
                    if file_in.hash_hex != file_out.hash_hex:
                        errors.append(file_in.file_name.replace(in_folder, "")[1:])
                        continue
                    else:
                        continue

        return errors


class VerifyThread(Thread):
    def __init__(self, main_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._main_window = main_window
        self.want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        in_folder = self._main_window.in_folder.GetPath()
        out_folder = self._main_window.out_folder.GetPath()

        if os.path.basename(in_folder) != os.path.basename(out_folder):
            wx.PostEvent(self._main_window, ResultEvent(101))
            return

        errors = self.check_folders(in_folder, out_folder)
        if self.want_abort:
            # Use a result of None to acknowledge the abort
            wx.PostEvent(self._main_window, ResultEvent(None))
            return

        report = ""
        if len(errors) == 0:
            wx.PostEvent(self._main_window, ResultEvent(2))
        else:
            for err in errors:
                report = report + err + "\n"

            if platform != "win32" and platform != "cygwin":
                desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            else:
                desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

            report = report + "\n\nGenerated by Copier v0.1a"
            report_name = "Error_Report" + datetime.datetime.now().strftime("_%Y-%m-%d_%H%M%S") + ".txt"
            report_f = open(os.path.join(desktop, report_name), "w")
            report_f.write(report)
            report_f.close()
            wx.PostEvent(self._main_window, ResultEvent(103))



    def check_folders(self, in_folder, out_folder):
        hashes = Hashes()

        if self._main_window.rb_md5.GetValue():
            hash_mode = "md5"
        else:
            hash_mode = "xxhash"

        files_in = hashes.hash_files(in_folder, hash_mode, self._main_window, self)
        files_out = hashes.hash_files(out_folder, hash_mode, self._main_window, self)

        errors = []
        for file_in in files_in:
            for file_out in files_out:
                if file_in.file_name.replace(in_folder, "")[1:] == file_out.file_name.replace(out_folder, "")[1:]:
                    if file_in.hash_hex != file_out.hash_hex:
                        errors.append(file_in.file_name.replace(in_folder, "")[1:])
                        continue
                    else:
                        continue

        return errors

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self.want_abort = 1


class MhlThread(Thread):
    def __init__(self, main_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._main_window = main_window
        self.want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        in_folder = self._main_window.in_folder.GetPath()

        if self._main_window.rb_md5.GetValue():
            hash_mode = "md5"
        else:
            hash_mode = "xxhash"

        hashes = Hashes()
        mhl = Mhl()

        start_date = datetime.datetime.now()
        files_list = hashes.hash_files(in_folder, hash_mode, self._main_window, self)
        if self.want_abort:
            # Use a result of None to acknowledge the abort
            wx.PostEvent(self._main_window, ResultEvent(None))
            return

        end_date = datetime.datetime.now()

        creator = MhlUser("Marcelo Daros", "marcelodaros", start_date, end_date)

        mhl.create_mhl(creator, files_list, in_folder)

        wx.PostEvent(self._main_window, ResultEvent(3))

        return

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self.want_abort = 1


# MHL main class, to all MHL file tools
class Mhl:

    def create_mhl(self, user, items, orin_path):
        """Create a MHL file from user info and items. Save MHL to orin_path"""
        # Start a XML document
        mhl = Document()
        # Set root and title for the root
        root = mhl.createElement("hashlist")
        root.setAttribute("version", "1.1")

        # Create user_info element
        user_info = mhl.createElement("creatorinfo")

        # Gets all elements in object user as a dictionary
        user_elements = user.get_all_elements()

        # Creates all elements for Creator Info
        name_t = mhl.createTextNode(user_elements["name"])
        name = mhl.createElement("name")
        name.appendChild(name_t)

        username_t = mhl.createTextNode(user_elements["username"])
        username = mhl.createElement("username")
        username.appendChild(username_t)

        hostname_t = mhl.createTextNode(user_elements["hostname"])
        hostname = mhl.createElement("hostname")
        hostname.appendChild(hostname_t)

        tool_name_t = mhl.createTextNode(user_elements["tool_name"])
        tool_name = mhl.createElement("tool")
        tool_name.appendChild(tool_name_t)

        s_date_t = mhl.createTextNode(user_elements["start_date"])
        s_date = mhl.createElement("startdate")
        s_date.appendChild(s_date_t)

        e_date_t = mhl.createTextNode(user_elements["end_date"])
        e_date = mhl.createElement("finishdate")
        e_date.appendChild(e_date_t)

        # Append them to user_info
        user_info.appendChild(name)
        user_info.appendChild(username)
        user_info.appendChild(hostname)
        user_info.appendChild(tool_name)
        user_info.appendChild(s_date)
        user_info.appendChild(e_date)

        # Append user_info to the root
        root.appendChild(user_info)

        # Loop to get all item
        for item in items:
            # Gets all elements in object item as a dictionary
            item_elements = item.get_all_elements()

            # Creates all elements for hash element
            file_name_t = mhl.createTextNode(item_elements["file_name"].replace(orin_path, "")[1:])
            file_name = mhl.createElement("file")
            file_name.appendChild(file_name_t)

            size_t = mhl.createTextNode(item_elements["file_size"])
            size = mhl.createElement("size")
            size.appendChild(size_t)

            last_mod_date_t = mhl.createTextNode(item_elements["last_mod_date"])
            last_mod_date = mhl.createElement("lastmodificationdate")
            last_mod_date.appendChild(last_mod_date_t)

            hash_type_t = mhl.createTextNode(item_elements["hash_hex"])
            hash_type = mhl.createElement(item_elements["hash_type"])
            hash_type.appendChild(hash_type_t)

            hash_date_t = mhl.createTextNode(item_elements["hash_date"])
            hash_date = mhl.createElement("hashdate")
            hash_date.appendChild(hash_date_t)

            # Creates hash node and append all elements
            hash_node = mhl.createElement("hash")
            hash_node.appendChild(file_name)
            hash_node.appendChild(size)
            hash_node.appendChild(last_mod_date)
            hash_node.appendChild(hash_type)
            hash_node.appendChild(hash_date)

            # Append hash node to root
            root.appendChild(hash_node)

        # Append root to MHL file
        mhl.appendChild(root)

        # Create MHL file name:
        # Name of orin_path folder + date and time
        mhl_filename = os.path.basename(orin_path) + datetime.datetime.now().strftime("_%Y-%m-%d_%H%M%S") + ".mhl"

        # Path to MHL file
        mhl_path = os.path.join(orin_path, mhl_filename)
        # Writes the file
        mhl.writexml(open(mhl_path, "w"),
                     addindent="  ",
                     newl="\n",
                     encoding="UTF-8")

        # Unlink everything to save memory
        mhl.unlink()


# Class to store user info
class MhlUser:

    def __init__(self, name, username, start_date, finish_date):
        self.__name = name
        self.__username = username
        self.__hostname = socket.gethostname()
        self.__tool_name = "Copier v0.1"
        self.__start_date = start_date
        self.__finish_date = finish_date

    def get_all_elements(self):
        """Gets all elements in object and return them as dictionary and all values as strings"""
        elements = {}

        elements["name"] = self.__name
        elements["username"] = self.__username
        elements["hostname"] = self.__hostname
        elements["tool_name"] = self.__tool_name
        elements["start_date"] = self.__start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        elements["end_date"] = self.__finish_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        return elements


class MhlItem:

    def __init__(self, file_name, file_size, last_mod_date, hash_type, hash_hex, hash_date):
        self.__file_name = file_name
        self.__file_size = file_size
        self.__last_mod_date = datetime.datetime.fromtimestamp(last_mod_date)
        self.__hash_type = hash_type
        self.__hash_hex = hash_hex
        self.__hash_date = hash_date

    def get_all_elements(self):
        """Gets all elements in object and return them as dictionary and all values as strings"""
        elements = {"file_name": self.__file_name, "file_size": str(self.__file_size),
                    "last_mod_date": self.__last_mod_date.strftime("%Y-%m-%dT%H:%M:%SZ"), "hash_type": self.__hash_type,
                    "hash_hex": str(self.__hash_hex), "hash_date": self.__hash_date.strftime("%Y-%m-%dT%H:%M:%SZ")}

        return elements

    @property
    def file_name(self):
        """Get filename"""
        return self.__file_name

    @property
    def hash_hex(self):
        """Get Hash"""
        return self.__hash_hex


# Class with all hashes methods
class Hashes:

    def hash(self, fname, mode, main_ui, thread):
        if mode == "md5":
            return self.md5(fname, main_ui, thread)
        else:
            return

    def md5(self, fname, main_ui, thread):
        """Create MD5 Hash"""
        hash_md5 = hashlib.md5()

        # Open file and start reading and hashing in chunks of 5MB
        total = os.stat(fname).st_size
        progress = 0
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(5242880), b""):
                if thread.want_abort:
                    # Use a result of None to acknowledge the abort
                    wx.PostEvent(main_ui, ResultEvent(None))
                    return

                hash_md5.update(chunk)
                progress += 5242880
                bar_value = int((progress / total) * 100)
                wx.PostEvent(main_ui, UpdateEvent(fname, bar_value, "Hashing"))

        # Return hash as hex
        return hash_md5.hexdigest()

    def hash_files(self, orin_path, hash_mode, main_ui, thread):
        """Hashes all the files in orin_path and return a list of MhlItem"""
        items = []

        for path, dirs, files in os.walk(orin_path):
            for f in fnmatch.filter(files, '*.*'):
                fullname = os.path.abspath(os.path.join(path, f))
                wx.PostEvent(main_ui, UpdateEvent(f, 0, "Hashing"))
                file_item = MhlItem(fullname, os.stat(fullname).st_size, os.path.getmtime(path), hash_mode,
                                    self.hash(fullname, hash_mode, main_ui, thread), datetime.datetime.now())
                items.append(file_item)

        return items


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Copier v0.1a", pos=wx.DefaultPosition,
                          size=wx.Size(500, 420), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("imgs/copier_icon.ico"))

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

        self.m_button1 = wx.Button(self, ID_COPY, u"Copy Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button3 = wx.Button(self, ID_VERIFY, u"Verify Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer4.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"MHL Actions", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        self.m_staticText9.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, "Verdana"))

        bSizer4.Add(self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button2 = wx.Button(self, ID_MHL, u"Generate MHL", wx.DefaultPosition, wx.DefaultSize, 0)
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
        self.m_button5.Disable()

        self.pg_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.pg_bar.SetValue(0)
        bSizer1.Add(self.pg_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.copy_thread_start, id=ID_COPY)
        self.m_button3.Bind(wx.EVT_BUTTON, self.verify_thread_start, id=ID_VERIFY)
        self.m_button2.Bind(wx.EVT_BUTTON, self.mhl_thread_start, id=ID_MHL)
        self.m_button5.Bind(wx.EVT_BUTTON, self.cancel_task, id=ID_STOP)

        # Set up event handler for any worker thread results
        EVT_RESULT(self, self.on_result)

        # Set up event handler for updates for Main UI
        EVT_UPDATE(self, self.on_update)

        # No threads at start
        self.thread = None

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def copy_thread_start(self, event):
        if self.in_folder.GetPath() == "" or not os.path.exists(self.in_folder.GetPath()):
            wx.MessageBox("You have to select a valid Source Folder.")
            return None
        elif self.out_folder.GetPath() == "" or not os.path.exists(self.out_folder.GetPath()):
            wx.MessageBox("You have to select a valid Destination Folder.")
            return None
        elif not self.rb_md5.GetValue() and not self.rb_xxhash.GetValue():
            wx.MessageBox("Select a Hash Mode!")
            return None
        elif not self.rb_md5.GetValue() and self.rb_xxhash.GetValue():
            wx.MessageBox("xxHash64 not implemented yet...")
            return None

        if not self.thread:
            self.m_button1.Disable()
            self.m_button2.Disable()
            self.m_button3.Disable()
            self.m_button5.Enable()
            self.in_folder.Disable()
            self.out_folder.Disable()
            self.rb_md5.Disable()
            self.rb_xxhash.Disable()
            self.thread = CopyThread(self)

    def verify_thread_start(self, event):
        if self.in_folder.GetPath() == "" or not os.path.exists(self.in_folder.GetPath()):
            wx.MessageBox("You have to select a valid Source Folder.")
            return None
        elif self.out_folder.GetPath() == "" or not os.path.exists(self.out_folder.GetPath()):
            wx.MessageBox("You have to select a valid Destination Folder.")
            return None
        elif not self.rb_md5.GetValue() and not self.rb_xxhash.GetValue():
            wx.MessageBox("Select a Hash Mode!")
            return None
        elif not self.rb_md5.GetValue() and self.rb_xxhash.GetValue():
            wx.MessageBox("xxHash64 not implemented yet...")
            return None

        if not self.thread:
            self.m_button1.Disable()
            self.m_button2.Disable()
            self.m_button3.Disable()
            self.m_button5.Enable()
            self.in_folder.Disable()
            self.out_folder.Disable()
            self.rb_md5.Disable()
            self.rb_xxhash.Disable()
            self.thread = VerifyThread(self)

    def mhl_thread_start(self, event):
        if self.in_folder.GetPath() == "" or not os.path.exists(self.in_folder.GetPath()):
            wx.MessageBox("You have to select a valid Source Folder.")
            return None
        elif not self.rb_md5.GetValue() and not self.rb_xxhash.GetValue():
            wx.MessageBox("Select a Hash Mode!")
            return None
        elif not self.rb_md5.GetValue() and self.rb_xxhash.GetValue():
            wx.MessageBox("xxHash64 not implemented yet...")
            return None

        if not self.thread:
            self.m_button1.Disable()
            self.m_button2.Disable()
            self.m_button3.Disable()
            self.m_button5.Enable()
            self.in_folder.Disable()
            self.out_folder.Disable()
            self.rb_md5.Disable()
            self.rb_xxhash.Disable()
            self.thread = MhlThread(self)

    def on_result(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            self.SetStatusText("Stopped.")
            self.m_button1.Enable()
            self.m_button2.Enable()
            self.m_button3.Enable()
            self.m_button5.Disable()
            self.in_folder.Enable()
            self.out_folder.Enable()
            self.rb_md5.Enable()
            self.rb_xxhash.Enable()
            self.pg_bar.SetValue(0)
        else:
            if self.rb_md5.GetValue():
                mode = "MD5"
            else:
                mode = "xxHash64"
            # Process results here
            if event.data == 1:
                self.SetStatusText(f"Copy Completed with {mode} checksum!")
                wx.MessageBox(f"Copy Completed with {mode} checksum!")
            elif event.data == 2:
                self.SetStatusText(f"Verification completed with {mode} checksum!")
                wx.MessageBox(f"Verification completed with {mode} checksum!")
            elif event.data == 3:
                self.SetStatusText("MHL Created in Source Folder")
                wx.MessageBox(f"MHL created with {mode} checksum!")
            elif event.data == 101:
                self.SetStatusText("Base folders not the same.")
            elif event.data == 102:
                self.SetStatusText("Error copying files.")
                wx.MessageBox("Error copying files.\nCheck report file in Desktop.")
            elif event.data == 103:
                self.SetStatusText("Error verifying files.")
                wx.MessageBox("Error verifying files.\nCheck report file in Desktop.")
            self.m_button1.Enable()
            self.m_button2.Enable()
            self.m_button3.Enable()
            self.m_button5.Disable()
            self.in_folder.Enable()
            self.out_folder.Enable()
            self.rb_md5.Enable()
            self.rb_xxhash.Enable()
            self.pg_bar.SetValue(0)
        # In either event, the worker is done
        self.thread = None

    def on_update(self, event):
        if event.fname == "":
            self.SetStatusText(f"Start {event.task}")
            self.pg_bar.SetValue(event.progress)
        else:
            self.SetStatusText(f"{event.task} file {event.fname}")
            self.pg_bar.SetValue(event.progress)

    def cancel_task(self, event):
        """Stop any task."""
        # Flag the worker thread to stop if running
        if self.thread:
            self.SetStatusText("Stopping")
            self.thread.abort()


def main():
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()


main()
