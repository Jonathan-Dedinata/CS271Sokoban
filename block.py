if __name__ == "__main__":
    print("this is block class")


class block:
    x = -1
    y = -1
    tag = 0

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        # print("block create at " + str(self.x) + ", " + str(self.y))


    def is_player(self):
        return False

    def is_wall(self):
        return False

    def is_target(self):
        return False

    def is_box(self):
        return False

    def is_score(selfS):
        return False


class player(block):
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.tag = 1
        # print("player create at " + str(self.x) + ", " + str(self.y))

    def is_player(self):
        return True


class wall(block):
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.tag = 2
        # print("wall create at " + str(self.x) + ", " + str(self.y))

    def is_wall(self):
        return True


class target(block):
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.tag = 3
        # print("target create at " + str(self.x) + ", " + str(self.y))

    def is_target(self):
        return True


class box(block):
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.tag = 4
        # print("box create at " + str(self.x) + ", " + str(self.y))

    def is_box(self):
        return True


class score(block):
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.tag = 5
        # print("score create at " + str(self.x) + ", " + str(self.y))

    def is_box(self):
        return True

    def is_target(self):
        return True

    def is_score(self):
        return True
