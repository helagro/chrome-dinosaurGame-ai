import numpy as np
import tweak as m
import random
'''
  
'''


class NN:
    k = 0.5
    last_score = 2
    direction = 0.04
    old_adjust_size = 0.04

    def act(self, pos, speed):
        return pos < (speed * self.k)

    def adjust(self, score):

        if score > self.last_score:
            adjust_size = m.ADJUST_FACTOR / score
            adjust_andel = self.old_adjust_size / self.direction

            self.direction = adjust_size / adjust_andel
            self.old_adjust_size = adjust_size
            self.last_score = score
        else:
            self.k -= self.direction
            self.direction = random.uniform(-self.old_adjust_size, self.old_adjust_size)

        self.k += self.direction
        print("k:", self.k, "adjust_size", self.old_adjust_size)

    def __init__(self):
        return




