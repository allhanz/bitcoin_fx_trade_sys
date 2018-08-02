import tensorflow as tf
import pandas as pd
import os
#设计灵感如下：
#数据收集
#新闻中 敏感信息的抽出
#汇率换算
#各国GDP情况
#各国股市分析情况
#拟合数学算法的研究
#现阶段人工智能算法的设计

from tensorflow.examples.tutorials.mnist import input_data
sess = tf.InteractiveSession()

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
