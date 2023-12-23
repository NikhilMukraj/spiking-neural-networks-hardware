import matplotlib.pyplot as plt


with open('output.log', 'r') as f:
    contents = f.read()

plt.plot([float(i.split(',')[0].strip()) for i in contents.split('\n') if i != ''])
plt.show()
