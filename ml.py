import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from sklearn.ensemble import svm


df = pd.read_excel("logs.xlsx")


def count_remote_addr(remote_addr_list):
    counter_dict = {}
    for addr in remote_addr_list:
        counter_dict[addr] = counter_dict.get(addr, 0) + 1

    return counter_dict


counter_dict = count_remote_addr(df['remote_addr'].values)

x_fake = pd.DataFrame(counter_dict.items(), columns=['remote_addr', 'sum'])
all_data = x_fake.copy()

def plot_anomaly2(data, predicted, ax):
    data2 = data.copy()
    data2['Predicted'] = predicted

    normal = data2.loc[data2['Predicted'] == 1, :]
    anomalies = data2.loc[data2['Predicted'] == -1, :]

    # Make Scatterplot
    column1 = data.columns[0]
    column2 = data.columns[1]

    anomalies.plot.scatter(column1, column2, color='tomato',
                           fontsize=14,  sharex=False, ax=ax)
    normal.plot.scatter(column1, column2, color='grey',
                        fontsize=14,  sharex=False, ax=ax)
#plt.grid(linestyle = '--')

    plt.xlabel(column1, fontsize=14, weight='bold')
    plt.ylabel(column2, fontsize=14, weight='bold')
    return ax


# Create Fake data to classify
# x_fake = pd.DataFrame(np.random.uniform(-5, 19, (35000, 2)),
#                       columns=['Var 1', 'Var 2'])
# Visualize effect of changing Gamma
gammas = [.00005, .005, .01, .025, .05, .1, .3, .6, .9, 2, 5, 10]
fig, axes = plt.subplots(2, 6, figsize=(25, 6), tight_layout=True)
for i, ax in zip(range(len(gammas)), axes.flatten()):
    gamma = gammas[i]
    model = svm.OneClassSVM(kernel='rbf', degree=5, gamma=gamma, coef0=0.0, tol=0.001, nu=0.01,
                            shrinking=True, cache_size=200, verbose=False, max_iter=- 1).fit(all_data)
model_predictions = model.predict(x_fake)
#x_fake['Predictions'] = model_predictions
ax = plot_anomaly2(x_fake, model_predictions, ax)
ax.scatter(all_data.iloc[:, 0], all_data.iloc[:, 1], color='k', s=10)
ax.set_title('Gamma: {}'.format(np.around(gamma, 6)),
             weight='bold', fontsize=14)
