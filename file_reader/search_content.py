# -*- coding:utf-8 -*-
import glob
import os
import sys
import string
import mmap
import inspect
import getopt

def searchContent(path, filetype, content):
    needCheckFileType = filetype is not None
    searchstringBytes = content.encode()
    for root, dirs, files in os.walk(path):
        for file in files:
            if not needCheckFileType or file.endswith(filetype):
                fullPath = os.path.join(root, file)
                with open(fullPath, 'rb', 0) as file, \
                    mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                    if s.find(searchstringBytes) != -1:
                        print('Found string in file - ' + fullPath)

def relative_to_caller(*paths):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    return os.path.join(os.path.dirname(mod.__file__), *paths)

def main(argv):
    searchingPath = relative_to_caller('.')
    filetype = None
    content = None
    formattedDes = 'search_content.py -p <seaching-path> -f <file-type> -c <content>'
    try:
        opts, args = getopt.getopt(argv,"hp:f:c:",["seaching-path=","file-type=","content="])
    except getopt.GetoptError:
        print(formattedDes)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(formattedDes)
            sys.exit()
        elif opt in ("-p", "--seaching-path"):
            searchingPath = relative_to_caller(arg)
        elif opt in ("-f", "--file-type"):
            filetype = arg
        elif opt in ("-c", "--content"):
            content = arg
    if content is None:
        print(formattedDes + ', Please provide the content you need to search')
        sys.exit(2)
    searchContent(searchingPath, filetype, content)

if __name__ == '__main__':
    main(sys.argv[1:])

