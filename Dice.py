import random

class Dice:
    def __init__(self, sides):
        self.sides = sides

    @property
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, value):
        if value < 1:
            raise ValueError("Number of sides must be at least 1")
        self._sides = value

    def roll(self, times):
        total = 0
        rolls = []
        for _ in range(times):
            num = random.randint(1, self.sides)
            total += num
            rolls.append(str(num))
        return total, rolls
