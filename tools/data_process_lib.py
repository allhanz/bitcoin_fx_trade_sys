# for data processing lib
import os
import sys
import pandas as pd
import numpy as np
import string

def get_digit_str(str_data):
    #keep the "." string data
    digit_str=""
    for i in str_data:
        if i!=".":
            if i.isdigit():
                digit_str=digit_str+i
        else:
            digit_str=digit_str+i
    return digit_str

def parse_int(str_data):
    digit_str=get_digit_str(str_data)
    return int(digit_str.strip(string.ascii_letters))

def main():
    str_data="asdnsc234.5,56/.?"
    int_data=parse_int(str_data)
    print(int_data)
    
if __name__=="__main__":
    main()

