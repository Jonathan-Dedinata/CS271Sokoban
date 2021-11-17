if __name__ == "__main__":
    print("this is game class")
import block

class game:
    player_x = -1
    player_y = -1
    board = {}
    '''board is dict, given (x,y) => block'''

    def hit_wall(self,next_player_x,next_player_y):
        if self.board[(next_player_x, next_player_y)].is_wall:
            return True
        return False

    def






    def __init__(self,max_size,data):
        ''' please load the game to board'''
        print("unfinished")

    def make_move(self, direction):
        next_player_x = -1
        '''d = 1 up, d = 2 down, d = 3 left, d = 4 up'''
        if self.player_x == -1 or self.player_y == -1:
            print("not initialized..... exit")
            exit(1)
        if direction == 1:
            next_player_x = self.player_x
            next_player_y = self.player_y


