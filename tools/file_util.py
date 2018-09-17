import os
import sys
import pandas as pd
import glob

def check_path(path_name):
    return os.path.exists(path_name)

def get_absolute_path(path_name):
    if check_path(path_name):
        return os.path.abspath(path_name)

def get_specified_ext_file(path_name,ext_name):
    file_list=[]
    if check_path(path_name):
        for r, d, f in os.walk(path_name):
            for file in f:
                file_name,file_ext=os.path.splitext(file)
                if ext_name==file_ext:
                    abs_file=os.path.join(r, file)
                    file_list.append(abs_file)
                    print("file name:",abs_file)

        if len(file_list)>0:
            return file_list
def main():
    #for test
    file_list=get_specified_ext_file("./",".py")
    print("file_list:",file_list)
    print("not tested...")

if __name__=="__main__":
    main()

