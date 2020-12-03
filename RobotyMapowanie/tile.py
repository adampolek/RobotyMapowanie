class Tile:

    def __init__(self):
        self.visited = False
        self.value = 0

    def update_value(self, type):
        if type == '+':
            self.value += 3
        elif type == '-':
            self.value -= 1

        if self.value < 0:
            self.value = 0
        elif self.value > 15:
            self.value = 15

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self):
        return str(self.value)
