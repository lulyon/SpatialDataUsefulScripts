#! /usr/bin/python
# filename: mif2shp.py
# date: 2012-12-03
# author: luliang@ict.ac.cn

import os
import time
import re
import sys

def searchOption(mystr, filename):
    lines  = open(filename, "r").readlines()
    for line in lines:
        if re.search(mystr, line):
            info = str(line).split();
            count = int(info[1])
            if(count > 0):
                return 1
    return 0


def transform(directory):
    assert os.path.exists(directory)
    
    now = time.localtime(time.time())
    postfix = time.strftime("%y%m%d%H%M", now)
    
    if os.path.isfile(directory):
        filename = directory + "_" + postfix
        os.system("cp -f " + directory + " " + filename)
        return None
    
    stack = [directory]
    
    rootdir = directory + "_" + postfix
    if not os.path.exists(rootdir):
        os.mkdir(rootdir);
    
    stack2 = [rootdir]
    
    options = (" LINE ", " POINT ", " POLY ", " TEXT ")
    
    while stack:
        directory = stack.pop()
        directory2 = stack2.pop()
        
        for filename in os.listdir(directory):
            fullname = os.path.join(directory, filename)
            fullname2 = os.path.join(directory2, filename)
            
            if os.path.isdir(fullname) and not os.path.islink(fullname):
                stack.append(fullname)
                stack2.append(fullname2)
                if not os.path.exists(fullname2):
                    os.mkdir(fullname2)
                
            if os.path.isfile(fullname):
                # os.system("cp -f " + fullname + " " + fullname2)
                combname = os.path.splitext(fullname)
                combname2 = os.path.splitext(fullname2)
                
                if(combname[1] == ".mif"):
                    tempfilename = combname[0] + ".temp"
                    os.system("avmifshp.exe INFO " + combname[0] + " " + tempfilename)
                                            
                    for option in options:
                        if(searchOption(option, tempfilename) != 0):
                            if os.path.exists(combname2[0] + ".shp"):
                                newstr = str(option).replace(" ", "_")
                                os.system("avmifshp.exe " + option + " " + combname[0] + " " + combname2[0] + newstr)
                            os.system("avmifshp.exe " + option + " " + combname[0] + " " + combname2[0])
                    
                    if os.path.exists(tempfilename):
                        os.remove(tempfilename)       
    
    return None

if __name__ == "__main__":
    print "Script name: ", sys.argv[0]
    if len(sys.argv) < 1:
        print "Please input Fold path."
        return None
    print "Path: ", sys.argv[1]
    transform(sys.argv[1])
    print "Done."

