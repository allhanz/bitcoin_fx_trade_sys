import os
import sys
import pybrain as brain

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.shortcuts import buildNetwork
#website
#https://wizardforcel.gitbooks.io/python-quant-uqer/content/128.html

HISTORY=10

### 构造BP训练实例
def make_trainer(net, ds, momentum = 0.1, verbose = True, weightdecay = 0.01): # 网络, 训练集, 训练参数
    trainer = BackpropTrainer(net, ds, momentum = momentum, verbose = verbose, weightdecay = weightdecay)
    return trainer


### 开始训练
def start_training(trainer, epochs = 15): # 迭代次数
    trainer.trainEpochs(epochs)

def start_testing(net, dataset):
    return net.activateOnDataset(dataset)

def save_arguments(net):
    NetworkWriter.writeToFile(net, 'huge_data.csv')
    print('Arguments save to file net.csv')

### 建立测试集
def make_testing_data():
    ds = SupervisedDataSet(HISTORY, 1)
    for ticker in universe: # 遍历每支股票
        raw_data = DataAPI.MktEqudGet(ticker=ticker, beginDate=testing_set[0], endDate=testing_set[1], field=[
                'tradeDate', 'closePrice'    # 敏感字段
            ], pandas="1")
        plist = list(raw_data['closePrice'])
        for idx in range(1, len(plist) - HISTORY - 1):
            sample = []
            for i in range(HISTORY):
                sample.append(plist[idx + i - 1] / plist[idx + i] - 1)
            answer = plist[idx + HISTORY - 1] / plist[idx + HISTORY] - 1

            ds.addSample(sample, answer)
    return ds

### 建立数据集
def make_training_data():
    ds = SupervisedDataSet(HISTORY, 1)
    for ticker in universe: # 遍历每支股票
        raw_data = DataAPI.MktEqudGet(ticker=ticker, beginDate=training_set[0], endDate=training_set[1], field=[
                'tradeDate', 'closePrice'    # 敏感字段
            ], pandas="1")
        plist = list(raw_data['closePrice'])
        for idx in range(1, len(plist) - HISTORY - 1):
            sample = []
            for i in range(HISTORY):
                sample.append(plist[idx + i - 1] / plist[idx + i] - 1)
            answer = plist[idx + HISTORY - 1] / plist[idx + HISTORY] - 1

            ds.addSample(sample, answer)
    return ds

"""
training_set = ("20050101", "20130101")       # 训练集（六年）
testing_set  = ("20150101", "20150525")       # 测试集（2015上半年数据）
universe     = ['000001']
                                              # 目标股票池

"""

#=====================================================
#for trading
def initialize(account):                      # 初始化虚拟账户状态
    fnn = NetworkReader.readFrom('net.csv')

def handle_data(account):                     # 每个交易日的买入卖出指令
    hist = account.get_attribute_history('closePrice', 10)
    bucket = []
    for s in account.universe:
        sample = hist[s]
        possibility = fnn.activate(sample)
        bucket.append((possibility, s))

        if possibility < 0 and s in account.valid_secpos:
            order_to(s, 0)

    bucket = sorted(bucket, key=lambda x: x[0], reverse=True)
    print bucket[0][0]

    if bucket[0][0] < 0:
        raise Exception('Network Error')

    for s in bucket[:10]:
        if s[0] > 0.5 and s[1] not in account.valid_secpos:
            order(s[1], 10000 * s[0] * 80000)
#===================================================
def main():
    fnn = buildNetwork(HISTORY, 15, 7, 1)
    training_dataset = make_training_data()
    testing_dataset  = make_testing_data()
    trainer = make_trainer(fnn, training_dataset)
    start_training(trainer, 5)
    save_arguments(fnn)
    print(start_testing(fnn, testing_dataset))

if __name__=="__main__":
    main()