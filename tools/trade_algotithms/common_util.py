import os
import sys
sys.path.append(os.path.abspath("../"))
from sklearn.cross_validation import train_test_split
import redis_datatabase_api
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot

def mkdirs(folderpath):
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

def data_preprocess(array_X,array_Y,test_size):
    (X_train, X_test, y_train, y_test)= train_test_split( array_X, array_Y, test_size = test_size, random_state = 100)
    return (X_train, X_test, y_train, y_test)

def load_realtime_data(scan_ptn):
    if scan_ptn=="" or scan_ptn==None:
        scan_ptn="bitflyer_bitcoin_price_[0-9]*"
    r=redis_datatabase_api.build_redis_db(None)
    db_data=redis_datatabase_api.get_all_data_by_ptn(r,scan_ptn)
    return db_data

def bitflyer_data_preprocess(pd_data,target_cols_list):
    if target_cols_list==None:
        target_cols_list=["buy_price","date","sell_price","time"]
    data_copy=pd_data.copy()
    map_fuc=lambda x: x.replace(",","")
    for item in target_cols_list:
        if item in pd_data.columns:
            data_copy[item]=data_copy[item].map(map_fuc)
            #data_copy[item]= map(lambda x: x.replace(" ",""),data_copy[item])
    return data_copy[target_cols_list].astype(np.float32)
    '''
    target_data=pd_data[target_cols].values
    for i in range(target_data.shape[0]):
        for j in range(target_data.shape[1]):
            target_data[i][j]=target_data[i][j].replace(",","")

    target_data=target_data.T
    #target_data=target_data.replace(",","")
    return target_data.astype(np.float32)
    '''
# normalize the dataset
def data_normalize(ndarray_data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(ndarray_data)
    return dataset

def plot_each_col_data(array_data):
    # plot each column
    i=1
    pyplot.figure()
    for group in range(array_data.shape[0]):
        pyplot.subplot(array_data.shape[0], 1, i)
        pyplot.plot(array_data[group,:])
        #pyplot.title(dataset.columns[group], y=0.5, loc='right')
        i += 1
    pyplot.show()

# convert an array of values into a dataset matrix
# for lstm model input dataset
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        xset = []
        for j in range(dataset.shape[1]):
            a = dataset[i:(i+look_back), j]
            xset.append(a)
        dataY.append(dataset[i + look_back, 0])      
        dataX.append(xset)
    return np.array(dataX), np.array(dataY)


    '''
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)
    '''
def main():
    scan_ptn="bitflyer_bitcoin_price_[0-9]*"
    db_data=load_realtime_data(scan_ptn)
    print("length of db_data:",len(db_data))
    print("db_data head:",db_data.head())

    values=bitflyer_data_preprocess(db_data,None)
    print("shape of values:",values.shape)
    print("data:",values)
    nor_data=data_normalize(values)
    plot_each_col_data(nor_data)

if __name__=="__main__":
    main()