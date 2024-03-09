import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('output.log')
spike_times = [(i[0]-1, df['voltage'][i[0]-1]) for i in df.iterrows() if i[1]['is_spiking'] == 1]

plt.plot(df['voltage'])
plt.scatter(*zip(*spike_times))
plt.show()
