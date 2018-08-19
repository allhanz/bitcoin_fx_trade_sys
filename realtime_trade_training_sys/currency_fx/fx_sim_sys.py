import os
import sys
import pandas as pd
sys.path.append("../../tools")
import env_settings as env
import trade_algotithms.decision_tree

def fx_data_preprocess():

def trade_method(fx_his_pd):


def main():
    #fx test data file
    file_name=env.usdjpy_test_file
    pd_data=pd.read_csv(file_name,encoding="utf-8",header=None)
    pd_data.columns=env.fx_common_cols
    trade_method(fx_his_pd)

if __name__=="__main__":
    main()