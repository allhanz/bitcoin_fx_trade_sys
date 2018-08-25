import os
import sys
import redis
import mongodb_api
import pickle
import re
import data_process_lib

def mongodb_to_redis():
    print("not finished...")
    
def redis_to_mongodb():
    print("not finished..")

def build_redis_db(db_index):
    if db_index=="" or db_index==None:
        db_index=0
    pool = redis.ConnectionPool(host='localhost', port=6379, db=db_index)
    r = redis.Redis(connection_pool=pool)
    r.scan()
    return r

def set_one_kv(r,kv_data):
    k,v=list(enumerate(kv_data.items()))[0]
    res=r.set(k,v)
    print("res:",res)

def redis_scan(r):
    return scan_match(r,None)
    
def get_one_v(r,key_name):
    res=r.get(key_name)
    print("res:",res)
    return res

def hash_set_multi_kv(r,redis_id,kv_data):
    if redis_id=="" or redis_id==None:
        return
    res=r.hmset(redis_id,kv_data)
    print("res:",res)
    return res

def fx_insert_multi_kv(r,redis_id_prefix,scan_ptn,kv_data):
    if redis_id_prefix=="" or redis_id_prefix==None:
        redis_id_prefix=="fx_price_"
    scan_dict=scan_match(r,scan_ptn)
    print("id_list:",scan_dict["id_list"])
    ptn=re.compile(r".*[0-9]*")
    index_list=[ data_process_lib.parse_int(item) for item in scan_dict["id_list"]]
    max_no=max(index_list)
    redis_id=redis_id_prefix+str(max_no+1)
    res=hash_set_multi_kv(r,redis_id,kv_data)
    print("redis_id:",redis_id)
    return res


def bitcoin_insert_multi_kv(r,redis_id_prefix,scan_ptn,kv_data):
    if redis_id_prefix=="" or redis_id_prefix==None:
        redis_id_prefix=="bitcoin_price_"
    scan_list=scan_match(r,scan_ptn)
    list_len=len(scan_list)
    redis_id=redis_id_prefix+str(list_len+1)
    res=hash_set_multi_kv(r,redis_id,kv_data)
    return res

def change_redis_scan_res_to_dict(scan_tuple):
    if not isinstance(scan_tuple,tuple):
        return 
    if len(scan_tuple)==0:
        return

    scan_dic={
        "db_index":None,
        "id_list":[]
    }
    db_index,id_byte_list=scan_tuple
    id_list=[ i.decode() for i in id_byte_list]
    scan_dic["db_index"]=db_index
    scan_dic["id_list"]=id_list
    return scan_dic

def scan_match(r,ptn_str):
    #match="a*"
    #(0, [b'a', b'another_user'])
    res=r.scan(match=ptn_str)
    res_dict=change_redis_scan_res_to_dict(res)
    return res_dict

def check_redis_id(r,redis_id):
    scan_dict=redis_scan(r)
    if redis_id in scan_dict["id_list"]:
        return True
    else:
        return False

def search_val(r,redis_ptn):
    print("not finished....")

def hash_get_multi_all(r,redis_id):
    flag=check_redis_id(r,redis_id)
    if flag:
        res_all=r.hgetall(redis_id)
        return res_all

def get_fx_all_data(r,scan_ptn):
    info_list=[]
    if scan_ptn=="" or scan_ptn==None:
        scan_ptn="fx_price_*"
    scan_dict=scan_match(r,scan_ptn)
    if len(scan_dict.values()):
        return 

    for id in scan_dict["id_list"]:
        res=hash_get_multi_all(r,id)
        info_list.append(res)
    if len(info_list)>0:
        return info_list

def get_bitcoin_all_data(r,scan_ptn):
    info_list=[]
    if scan_ptn=="" or scan_ptn==None:
        scan_ptn="bitcoin_price_*"
    scan_dict=scan_match(r,scan_ptn)
    if len(scan_dict.values()):
        return 

    for id in scan_dict["id_list"]:
        res=hash_get_multi_all(r,id)
        info_list.append(res)
    if len(info_list)>0:
        return info_list
def delete_data_by_key(r,key_name):
    res=r.delete(key_name)
    return res

def delete_data_by_ptn(r,scan_ptn):
    scan_dict=scan_match(r,scan_ptn)
    for key_id in scan_dict["id_list"]:
        delete_data_by_key(r,key_id)

def build_realtime_db():
    db=build_redis_db(None)
    return db

def main():
    db=build_realtime_db()
    test_dict_list=[
        {"a":2,"b":3},
        {"c":3,"d":8}
    ]
    hash_set_multi_kv(db,"test",test_dict_list)
    set_one_kv(db,{"first":"hello"})
    res_all=hash_get_multi_all(db,"another_u")
    print("res_all:",res_all)
    res_all=redis_scan(db)
    print("res_all:",res_all)

if __name__=="__main__":
    main()