import os
import sys
import pandas as pd
import mongodb_api
import file_util

#not finshed
def insert_large_data_into_mongodb(collection_obj,csv_file,chunksize):
    
    if not os.path.exists(csv_file):
        return
    for chunk_pd in pd.read_csv(csv_file,chunksize=chunksize):


def main():

if __name__=="__main__":
    main()