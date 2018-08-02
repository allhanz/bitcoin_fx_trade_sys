import pybitflyer
import pandas as pd
import sys
import os
import bitcoin_info_tools


def main():
    api=bitcoin_info_tools.set_api_info()
    print("api:",api)

if __name__=="__main__":
    main()

