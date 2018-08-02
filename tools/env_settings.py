import sys
import os

#gmail api_key
auth_root_path="../../auth_info"
gmail_file=auth_root_path+"/gmail_account.xlsx"
api_file=auth_root_path;"/bitflyer_account.xlsx"
quandl_api_file=auth_root_path+"/quandl_account.xlsx"

#data
common_data_root_path="../common_data"

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


currency_list_file="./currency_list.xlsx"
