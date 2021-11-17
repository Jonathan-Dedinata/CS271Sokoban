if __name__ == "__main__":
    print("this is block class")


class block:
    x = -1
    y = -1
    tag = 0

    def __init__(self, _x, _y):
        x = _x
        y = _y
        print("block create at " + self.x + ", " + y)

    def is_player(self):
        return False

    def is_wall(self):
        return False

    def is_target(self):
        return False

    def is_box(self):
        return False


class player(block):
    def __init__(self, _x, _y):
        x = _x
        y = _y
        tag = 1
        print("player create at " + x + ", " + y)

    def is_player(self):
        return True


class wall(block):
    def __init__(self, _x, _y):
        x = _x
        y = _y
        tag = 2
        print("wall create at " + x + ", " + y)

    def is_wall(self):
        return True


class target(block):
    def __init__(self, _x, _y):
        x = _x
        y = _y
        tag = 3
        print("target create at " + x + ", " + y)

    def is_target(self):
        return True


class box(block):
    def __init__(self, _x, _y):
        x = _x
        y = _y
        tag = 4
        print("box create at " + x + ", " + y)

    def is_box(self):
        return True
