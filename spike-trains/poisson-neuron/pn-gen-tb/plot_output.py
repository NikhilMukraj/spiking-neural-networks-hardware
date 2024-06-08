import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('output.log')
plt.plot(df['nums'])
plt.show()
