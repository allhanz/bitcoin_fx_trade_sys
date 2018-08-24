import os
import sys
import redis
import mongodb_api

def mongodb_to_redis():
    print("not finished...")
    
def redis_to_mongodb():
    print("not finished..")

def build_redis_db(db_index):
    if db_index=="" or db_index==None:
        db_index=0
    pool = redis.ConnectionPool(host='localhost', port=6379, db=db_index)
    r = redis.Redis(connection_pool=pool)
    return r

def insert_one_kv(r,kv_data):
    
def get_one_v(r,k_data):
    
def insert_multi_ky(r,kv_list):
    
def fx_realtime_db():
    
def main():
