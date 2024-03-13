import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


df = pd.read_csv('output.log')
# spiking is noted right after event occurs
spike_times = [(i[0]-1, df['voltage'][i[0]-1]) for i in df.iterrows() if i[1]['is_spiking'] == 1]

sns.set_theme(style='darkgrid')

plt.plot(df['voltage'])
plt.scatter(*zip(*spike_times))
plt.xlabel('Iteration')
plt.ylabel('Voltage (mV)')
plt.title('Neuron Core Output')
plt.show()
