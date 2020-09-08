import os
import fnmatch
import hashlib
import datetime
from xml.dom.minidom import Document
import socket
import wx


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

    def hash(self, fname, mode, main_ui):
        if mode == "md5":
            return self.md5(fname, main_ui)
        else:
            return

    def md5(self, fname, main_ui):
        """Create MD5 Hash"""
        hash_md5 = hashlib.md5()

        # Open file and start reading and hashing in chunks of 5MB
        total = os.stat(fname).st_size
        progress = 0
        main_ui.pg_bar.SetValue(0)
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(5242880), b""):
                hash_md5.update(chunk)
                progress += 5242880
                main_ui.pg_bar.SetValue((progress / total) * 100)

        # Return hash as hex
        return hash_md5.hexdigest()

    def hash_files(self, orin_path, hash_mode, main_ui):
        """Hashes all the files in orin_path and return a list of MhlItem"""
        itens = []

        for path, dirs, files in os.walk(orin_path):
            for f in fnmatch.filter(files, '*.*'):
                fullname = os.path.abspath(os.path.join(path, f))
                main_ui.SetStatusText(f"Hashsing {f}")
                file_item = MhlItem(fullname, os.stat(fullname).st_size, os.path.getmtime(path), hash_mode,
                                    self.hash(fullname, hash_mode, main_ui), datetime.datetime.now())
                itens.append(file_item)

        return itens
