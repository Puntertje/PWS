import matplotlib.pyplot as plt
from Stad import *
from Network import *

city = game.Game(tick_speed=0, tick_cap=500, stats=True)
statistic_data = city.get_stats()

# Render statistics
fig, ax = plt.subplots(ncols=3, figsize=(18, 6))
ax_index = 0    # Bit ugly, but it works
for i in statistic_data:
    x, y = statistic_data[i]
    ax[ax_index].title.set_text(i)
    ax[ax_index].grid()
    ax[ax_index].plot(x, y)
    ax_index += 1
plt.show()
