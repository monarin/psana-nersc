import numpy as np
import matplotlib.pyplot as plt

csv_files = ['fex_pks_det.csv', 
        'fex_pks_ana.csv',
        'fex_pks_tot.csv',
        'fex_pks_pks.csv']
labels = ['det','ana','tot','pks']

data_dict = {}
for i in range(len(labels)):
    _data = np.genfromtxt(csv_files[i], delimiter=',')
    # get rid of the last empty and convert to ms except pks
    if labels[i] != 'pks':
        data_dict[labels[i]] = _data[:_data.shape[0]-1] * 1e3
        print(f'label:{labels[i]} mean:{np.mean(data_dict[labels[i]]):.2f}ms max:{np.max(data_dict[labels[i]]):.2f}ms min:{np.min(data_dict[labels[i]]):.2f}ms sum:{np.sum(data_dict[labels[i]]):.2f}ms #datapts:{_data.shape[0]-1}')
    else:
        data_dict[labels[i]] = _data[:_data.shape[0]-1]
        print(f'label:{labels[i]} mean:{np.mean(data_dict[labels[i]]):.2f} max:{np.max(data_dict[labels[i]]):.2f} min:{np.min(data_dict[labels[i]]):.2f} #datapts:{_data.shape[0]-1}')


plot=True
if plot:
    plt.figure(figsize=(1,2))
    plt.subplot(1,2,1)
    for i in range(len(labels)-2):
        plt.hist(data_dict[labels[i]], label=labels[i])
    plt.xlabel('ms')
    plt.ylabel('#counts')
    plt.legend(loc='best')
    plt.subplot(1,2,2)
    for i in range(len(labels)-2):
        plt.plot(range(data_dict[labels[i]].shape[0]), data_dict[labels[i]], marker='o',linestyle='None',markerfacecolor='None', label=labels[i])
    plt.xlabel('#evt')
    plt.ylabel('ms')
    plt.legend(loc='best')
    plt.show()

    plt.figure(figsize=(1,2))
    plt.subplot(1,2,1)
    plt.plot(data_dict['pks'], data_dict['det'], marker='o',linestyle='None',markerfacecolor='None')
    plt.xlabel('#pks')
    plt.ylabel('det(ms)')
    plt.title('Correlation of #pks and time spent in Det interface')
    plt.subplot(1,2,2)
    plt.plot(data_dict['pks'], data_dict['ana'], marker='o',linestyle='None',markerfacecolor='None')
    plt.xlabel('#pks')
    plt.ylabel('ana(ms)')
    plt.title('Correlation of #pks and peakfinding time')
    plt.show()
