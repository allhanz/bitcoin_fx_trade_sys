import sys
import os

current_file_path=os.path.dirname(os.path.abspath(__file__))

#gmail api_key
auth_root_path=current_file_path+"/../../auth_info"
gmail_file=auth_root_path+"/gmail_account.xlsx"
bitflyer_api_file=auth_root_path+"/bitflyer_account.xlsx"
quandl_api_file=auth_root_path+"/quandl_account.xlsx"

#common data
common_data_root_path=current_file_path+"/../common_data"
#fx data
fx_his_data_root_path=common_data_root_path+"/fx_data"
usdjpy_fx_data_path=fx_his_data_root_path+"/USDJPY/csv_files"
eurjpy_fx_data_path=fx_his_data_root_path+"/EURJPY/csv_files"

chat_msg_data_root_path=common_data_root_path+"/chat_msg_data"
bitflyer_chat_msg_path=chat_msg_data_root_path+"/bitflyer"

currency_daily_data_path=common_data_root_path+"/currency_daily_data"
today_data_path=common_data_root_path+"/today_data"
test_data_path=common_data_root_path+"/test_data"

stock_data_root_path=common_data_root_path+"/stock_data"
oil_data_path=common_data_root_path+"/oil_daily_data"
gold_data_path=common_data_root_path+"/gold_daily_data"

#account
account_balance_data_root_path=common_data_root_path+"/balance_daily"
bitflyer_account_balance_path=account_balance_data_root_path+"/bitflyer"


currency_list_file=current_file_path+"/currency_list.xlsx"

#fx data 
fx_data_root_path=common_data_root_path+"/fx_data"

#the bitcoin price was stored in mongodb database

#webdriver
phantomJS_path="/usr/local/bin/phantomjs" # please set the path
firefox_webdriver_path="/home/hanz/firefox_webdriver/geckodriver"

#hdfs file server
hdfs_database_root_path="/home/hanz/hdfs_data"
fx_hdfs_path=hdfs_database_root_path+"/fx_data"
hdfs_ip_addr="localhost:50070"

#fx test data file
usdjpy_test_file=usdjpy_fx_data_path+"/USDJPY-2018-07.csv"

fx_common_cols=["currency_name","time","price_low","price_high"]

#nlp data
nlp_lib_root_path=common_data_root_path+"/nlp_lib_data"
stopwords_data_path=nlp_lib_root_path+"/stopwords_list"
english_stopword_file=stopwords_data_path+"/english/en_stopwords.csv"
japanese_stopword_file=stopwords_data_path+"/english/jp_stopwords.csv"

nlp_test_file=common_data_root_path+"/nlp_test_words.txt"






