import matplotlib.pyplot as plt
from Stad import *
from Network import *

fig, ax = plt.subplots(ncols=3, figsize=(18, 6))
statistic_data = {
            "Score": [],
            "Cars": [],
            "Average score": []
        }

car_amount_list = [50, 200, 500]

for car_amount in car_amount_list:
    city = game.Game(tick_speed=0, tick_cap=5000, stats=True, max_cars=car_amount)
    # Process statistics
    statistic_data_temp = city.get_stats()
    for i in statistic_data_temp:
        statistic_data[i].append(statistic_data_temp[i])


# Render statistics
ax_index = 0  # Bit ugly, but it works
for i in statistic_data:
    for data in statistic_data[i]:
        x, y = data
        ax[ax_index].title.set_text(i)
        ax[ax_index].grid()
        ax[ax_index].plot(x, y)
    ax_index += 1
plt.show()
