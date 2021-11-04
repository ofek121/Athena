import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from sklearn.ensemble import IsolationForest
from pyod.models.cblof import CBLOF

df = pd.read_excel("logs.xlsx")


def count_remote_addr(remote_addr_list):
    counter_dict = {}
    for addr in remote_addr_list:
        counter_dict[addr] = counter_dict.get(addr, 0) + 1

    return counter_dict


counter_dict = count_remote_addr(df['remote_addr'].values)

df = pd.DataFrame(counter_dict.items(), columns=['remote_addr', 'sum'])
# print(df['sum'].values)
# print(df['sum'].min(), df['sum'].max())

isolation_forest = IsolationForest(n_estimators=100)
isolation_forest.fit(df['sum'].values.reshape(-1, 1))
xx = np.linspace(df['sum'].min(), df['sum'].max(), len(df)).reshape(-1,1)
anomaly_score = isolation_forest.decision_function(xx)
outlier = isolation_forest.predict(xx)
plt.figure(figsize=(10,4))
plt.plot(xx, anomaly_score, label='anomaly score')
plt.fill_between(xx.T[0], np.min(anomaly_score), np.max(anomaly_score), 
                 where=outlier==-1, color='r', 
                 alpha=.4, label='outlier region')
plt.legend()
plt.ylabel('anomaly score')
plt.xlabel('remote_addr')
plt.show();
