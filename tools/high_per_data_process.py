import os
import sys
import pandas as pd
from hdfs import InsecureClient
import env_settings as env

#hdfs information website
#https://creativedata.atlassian.net/wiki/spaces/SAP/pages/61177860/Python+-+Read+Write+files+from+HDFS
def get_hdfs_server():
    client_hdfs = InsecureClient(env.hdfs_ip_addr)
    return client_hdfs

def write_to_hdfs(client_hdfs,pd_data,file_name):
    full_path=env.fx_hdfs_path+"/"+file_name
    with client_hdfs.write(full_path, encoding = 'utf-8') as writer:
        pd_data.to_csv(writer)

def read_from_hdfs(client_hdfs,file_name):
    # ====== Reading files ======
    with client_hdfs.read(file_name, encoding = 'utf-8') as reader:
        df = pd.read_csv(reader,index_col=0)
        return df
        
def main():

    print("not tested")

if __name__=="__main__":
    main()