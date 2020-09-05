import os
import fnmatch
import hashlib
import datetime
from xml.dom.minidom import Document
import socket

class Mhl:

    def create_mhl(self, user, items, orin_path):
        mhl = Document()

        root = mhl.createElement("hashlist")
        root.setAttribute("version", "1.0")

        user_info = mhl.createElement("creatorinfo")
        
        user_elements = user.get_all_elements()

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

        user_info.appendChild(name)
        user_info.appendChild(username)
        user_info.appendChild(hostname)
        user_info.appendChild(tool_name)
        user_info.appendChild(s_date)
        user_info.appendChild(e_date)

        root.appendChild(user_info)

        for item in items:
            item_elements = item.get_all_elements()

            file_name_t = mhl.createTextNode(item_elements["file_name"][len(orin_path):])
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

            hash_node = mhl.createElement("hash")
            hash_node.appendChild(file_name)
            hash_node.appendChild(size)
            hash_node.appendChild(last_mod_date)
            hash_node.appendChild(hash_type)
            hash_node.appendChild(hash_date)

            root.appendChild(hash_node)


        mhl.appendChild(root)

        mhl_filename = orin_path.split("\\")[-2] + datetime.datetime.now().strftime("_%Y-%m-%d_%H%M%S") + ".mhl"

        mhl_path = orin_path + mhl_filename

        mhl.writexml(open(mhl_path, "w"),
                        addindent="  ",
                        newl="\n",
                        encoding="UTF-8")
        
        mhl.unlink()

class MhlUser:

    def __init__(self, name, username, start_date, finish_date):
        self.__name = name
        self.__username = username
        self.__hostname = socket.gethostname()
        self.__tool_name = "Copier v0.1"
        self.__start_date = start_date
        self.__finish_date = finish_date
    
    def get_all_elements(self):
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
    
    def print_item(self):
        print(f"File Name: {self.__file_name}")
        print(f"File Size: {self.__file_size}")
        mod_date = self.__last_mod_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"Mod Date: {mod_date}")
        print(f"Hash Type: {self.__hash_type}")
        print(f"Hash Hex: {self.__hash_hex}")
        hash_date = self.__hash_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"Hash Date: {hash_date}")
    
    def get_all_elements(self):
        elements = {}

        elements["file_name"] = self.__file_name
        elements["file_size"] = str(self.__file_size)
        elements["last_mod_date"] = self.__last_mod_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        elements["hash_type"] = self.__hash_type
        elements["hash_hex"] = str(self.__hash_hex)
        elements["hash_date"] = self.__hash_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        return elements

class Hashes:

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        print(f"Hashing file: {fname}")
        progress = 0
        total_size = os.stat(fname).st_size
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(5242880), b""):
                hash_md5.update(chunk)
                progress += 5242880
                if (progress/total_size) * 100 <= 100:
                    print(f"Progress: {round(((progress/total_size) * 100), 2)}%", end="\r")

        return hash_md5.hexdigest()

    def hash_files(self, orin_path):
        itens = []

        for path,dirs,files in os.walk(orin_path):
            for f in fnmatch.filter(files,'*.*'):
                fullname = os.path.abspath(os.path.join(path,f))
                file_item = MhlItem(fullname, os.stat(fullname).st_size, os.path.getmtime(path), "md5", self.md5(fullname), datetime.datetime.now())
                itens.append(file_item)
        
        return itens
    
