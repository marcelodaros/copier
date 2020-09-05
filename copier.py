#########################################################################################
#########################################################################################
####                                 Copier V0.1                                     ####
####                                                                                 ####
####                                 MIT License                                     ####    
####                                                                                 ####
####                      Copyright (c) 2020 Marcelo Daros                           ####
####                                                                                 ####
####  Permission is hereby granted, free of charge, to any person obtaining a copy   ####
####  of this software and associated documentation files (the "Software"), to deal  ####
####  in the Software without restriction, including without limitation the rights   ####
####  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      ####
####  copies of the Software, and to permit persons to whom the Software is          ####
####  furnished to do so, subject to the following conditions:                       #### 
####                                                                                 ####
####  The above copyright notice and this permission notice shall be included in all ####
####  copies or substantial portions of the Software.                                ####
####                                                                                 ####
####  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     ####
####  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       ####
####  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    ####
####  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         ####
####  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  ####
####  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  ####
####  SOFTWARE.                                                                      ####
#########################################################################################
#########################################################################################

import os
import fnmatch
from mhl_tools import *
import datetime

def main():
    print("#"*10)
    print("#### Copier V0.1 ####")
    print("#"*10)

    orin_path = input("\nFolder de Origem: ")
    dest_path = input("\nFolder de Destino: ")

    hashes = Hashes()
    mhl = Mhl()

    start_date = datetime.datetime.now()

    files_list = hashes.hash_files(orin_path)

    end_date = datetime.datetime.now()

    creator = MhlUser("Marcelo Daros", "marcelodaros", start_date, end_date)
    
    mhl.create_mhl(creator, files_list, orin_path)



main()
