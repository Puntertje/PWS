import matplotlib.pyplot as plt
from Stad import *
from Network import *

city = game.Game(tick_speed=0, tick_cap=50, stats=True)
statistic_data = city.get_stats()

for i in statistic_data:
    fig, ax = plt.subplots()
    x, y = statistic_data[i]
    ax.title.set_text(i)
    ax.grid()
    ax.plot(x, y)

plt.show()
