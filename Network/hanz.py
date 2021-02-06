import tensorflow as tf
import numpy as np

"""
Welcome to Hanz Verkehrsschlager, he doesn't bite except when he does
"""

# Inspired/Stolen from https://github.com/Code-Bullet/Car-QLearning/blob/master/main.py
# Also huge help from sentdex's video series, https://www.youtube.com/c/sentdex
class brain:
    def __init__(self, game):
        self.game = game

