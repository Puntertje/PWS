import matplotlib.pyplot as plt
from tqdm import tqdm
from Stad import *
from Network import *
import time


"""
Variables
"""
# General
AI = False                          # Load the AI
AI_TRAINING = True                  # Train the AI
AUTO = False                        # Let the game run automatically
TICK_CAP = 1000                     # Amount of game ticks per session
car_amount_list = [50, 200, 500]    # Amount of cars in the game session
# Statistics
fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(18, 6))
statistic_data_game = {
            "Score": [],
            "Cars": [],
            "Average score": []
}
# For some weird reason the .copy() method links the two dicts instead of copying.
statistic_data_ai = {
            "Score": [],
            "Cars": [],
            "Average score": []
}

"""
Running the game
"""
if AUTO:
    for car_amount in tqdm(car_amount_list):
        city = game.Game(tick_speed=0, tick_cap=TICK_CAP, stats=True, max_cars=car_amount)
        # Process statistics
        statistic_data_temp = city.get_stats()
        for i in statistic_data_temp:
            statistic_data_game[i].append(statistic_data_temp[i])
if AI:
    for car_amount in car_amount_list:
        city = game.Game(manual=True, stats=True, max_cars=car_amount)
        hanz = hanz_dqn.Brain(city)
        for _ in range(500):
            for _ in range(5):
                if hanz.training:
                    hanz.train()
                else:
                    hanz.test()
        statistic_data_temp = city.get_stats()
        for i in statistic_data_temp:
            statistic_data_ai[i].append(statistic_data_temp[i])

if AI_TRAINING:
    city = game.Game(manual=True, stats=True, max_cars=50)
    hanz = hanz_dqn.Brain(city)
    while True:
        if hanz.training:
            hanz.train()
        else:
            hanz.test()

"""
Statistics
"""
# Render statistics
ax_index = 0  # Bit ugly, but it works
for i in statistic_data_game:
    for data in statistic_data_game[i]:
        x, y = data
        ax[0][ax_index].title.set_text(i)
        ax[0][ax_index].grid()
        ax[0][ax_index].plot(x, y)
    ax_index += 1

ax_index = 0
for i in statistic_data_ai:
    for data in statistic_data_ai[i]:
        x, y = data
        ax[1][ax_index].title.set_text(i)
        ax[1][ax_index].grid()
        ax[1][ax_index].plot(x, y)
    ax_index += 1
plt.show()
time.sleep(5)
