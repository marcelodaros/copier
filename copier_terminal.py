# coding: utf-8
"""
                                Copier V0.2a

                                 MIT License

                      Copyright (c) 2021 Marcelo Daros

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
import os
import fnmatch
import hashlib
import datetime
from xml.dom.minidom import Document
import socket
import colorama
from colorama import Fore, Back, Style

COPY_BUFSIZE = 1024 * 1024 if platform == "win32" or platform == "cygwin" else 64 * 1024
CLEAR_SCREEN = '\033[2J'


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
            fname = item_elements["file_name"].replace(orin_path, "")[1:]
            file_name_t = mhl.createTextNode(fname)
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
        mhl.writexml(open(mhl_path, "w", encoding="utf-8", errors="xmlcharrefreplace"),
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
        elements = {"name": self.__name, "username": self.__username, "hostname": self.__hostname,
                    "tool_name": self.__tool_name, "start_date": self.__start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "end_date": self.__finish_date.strftime("%Y-%m-%dT%H:%M:%SZ")}

        return elements


# Class to create a MHL Item info
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

    def hash(self, fname, mode):
        if mode == "md5":
            return self.md5(fname)
        else:
            return

    def md5(self, fname):
        """Create MD5 Hash"""
        hash_md5 = hashlib.md5()

        # Open file and start reading and hashing in chunks of 5MB
        total = os.stat(fname).st_size
        progress = 0
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(COPY_BUFSIZE), b""):
                hash_md5.update(chunk)
                progress += COPY_BUFSIZE

        # Return hash as hex
        return hash_md5.hexdigest()

    def hash_files(self, orin_path, hash_mode):
        """Hashes all the files in orin_path and return a list of MhlItem"""
        items = []

        for path, dirs, files in os.walk(orin_path):
            for f in fnmatch.filter(files, '*.*'):
                fullname = os.path.abspath(os.path.join(path, f))
                file_item = MhlItem(fullname, os.stat(fullname).st_size, os.path.getmtime(path), hash_mode,
                                    self.hash(fullname, hash_mode), datetime.datetime.now())
                items.append(file_item)

        return items


def copy_files(folder_in, folder_out):
    in_folder = folder_in
    out_folder = folder_out

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
            print("Copiando agora " + in_fullname)
            with open(in_fullname, "rb") as in_file:
                for chunk in iter(lambda: in_file.read(COPY_BUFSIZE), b""):
                    out_file.write(chunk)
                    progress += COPY_BUFSIZE


def check_folders(in_folder, out_folder, mode):
    hashes = Hashes()

    if mode == 1:
        hash_mode = "md5"
    else:
        hash_mode = "xxhash"

    files_in = hashes.hash_files(in_folder, hash_mode)
    files_out = hashes.hash_files(out_folder, hash_mode)

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


def create_mhl(folder_in, hash_m):
    in_folder = folder_in

    if hash_m == 1:
        hash_mode = "md5"
    else:
        hash_mode = "xxhash"

    hashes = Hashes()
    mhl = Mhl()

    start_date = datetime.datetime.now()
    files_list = hashes.hash_files(in_folder, hash_mode)

    end_date = datetime.datetime.now()

    creator = MhlUser("Marcelo Daros", "marcelodaros", start_date, end_date)

    mhl.create_mhl(creator, files_list, in_folder)

    return


def main():
    colorama.init()

    print(CLEAR_SCREEN)
    print(Fore.CYAN)
    print(Style.BRIGHT)
    print("################# Copier v0.2a #################\n")
    print(Style.RESET_ALL)
    print(Fore.RED)
    print(Style.BRIGHT)
    print("Ações:\n1 - Copiar\n2 - Copiar e Verificar\n3 - Verificar\n4 - Gerar MHL\n")
    print(Style.RESET_ALL)
    mode = int(input("Selecione ação: "))

    print("Arraste o folder de origem:")
    in_folder = input()

    print("\nArraste o folder de destino:")
    out_folder = input()

    print("\nSelecione o modo de Hash:\n1 - md5\n2 - xxHash\n")
    hash_mode = int(input("Hash: "))

    copy_files(in_folder, out_folder)
    check_folders(in_folder, out_folder, hash_mode)


main()
