import pandas as pd
import matplotlib.pyplot as plt
import os
loc_partA=os.path.join(os.getcwd(),'oscilationKp4.txt')
news_A=pd.read_csv(loc_partA)
time=news_A["Time"]
turn=news_A["Turn"]
plt.plot(time,turn)
plt.xlabel("Time")
plt.ylabel("Turn")
plt.title("Oscilation over time")
plt.show()
