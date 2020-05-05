from collections import Counter
import random


class Board:
    def __init__(self):
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    def __str__(self):
        return("\n 7 | 8 | 9     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 4 | 5 | 6     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 1 | 2 | 3     %s | %s | %s" % (self.board[6], self.board[7], self.board[8],
                                                self.board[3], self.board[4], self.board[5],
                                                self.board[0], self.board[1], self.board[2]))

    def valid_move(self, move):
        try:
            move = int(move)
        except ValueError:
            return False
        if 0 <= move <= 8 and self.board[move] == ' ':
            return True
        return False

    def winning(self):
        return ((self.board[0] != ' ' and
                 ((self.board[0] == self.board[1] == self.board[2]) or
                  (self.board[0] == self.board[3] == self.board[6]) or
                  (self.board[0] == self.board[4] == self.board[8])))
                or (self.board[4] != ' ' and
                    ((self.board[1] == self.board[4] == self.board[7]) or
                    (self.board[3] == self.board[4] == self.board[5]) or
                    (self.board[2] == self.board[4] == self.board[6])))
                or (self.board[8] != ' ' and
                    ((self.board[2] == self.board[5] == self.board[8]) or
                    (self.board[6] == self.board[7] == self.board[8]))))

    def draw(self):
        return all((x != ' ' for x in self.board))

    def play_move(self, position, marker):
        self.board[position] = marker

    def board_string(self):
        return ''.join(self.board)


class AIPlayer:
    def __init__(self):
        self.boxes = {}
        self.num_win = 0
        self.num_draw = 0
        self.num_lose = 0

    def start_game(self):
        self.moves_played = []

    def get_move(self, board):
        # Find board in boxes and choose a action
        # If the matchbox is empty, reset match box
        board = board.board_string()
        if board not in self.boxes or len(self.boxes[board]) == 0:
            new_actions = [pos for pos, mark in enumerate(board) if mark == ' ']
            # Early boards start with more actions
            self.boxes[board] = new_actions * ((len(new_actions) + 2) // 2)

        actions = self.boxes[board]
        if len(actions):
            action = random.choice(actions)
            self.moves_played.append((board, action))
        else:
            action = -1
        return action

    def win_game(self):
        # We won, add four actions
        for (board, action) in self.moves_played:
            self.boxes[board].extend([action, action, action, action])
        self.num_win += 1

    def draw_game(self):
        # A draw, add one action
        for (board, action) in self.moves_played:
            self.boxes[board].append(action)
        self.num_draw += 1

    def lose_game(self):
        # Lose, remove two actions
        for (board, action) in self.moves_played:
            self.boxes[board].pop(-1)
            if len(self.boxes[board])>1:
                self.boxes[board].pop(-1)
                self.boxes[board].pop(-1)
        self.num_lose += 1

    def print_stats(self):
        print('Have learnt %d boards' % len(self.boxes))
        print('W/D/L: %d/%d/%d' % (self.num_win, self.num_draw, self.num_lose))

    def print_probability(self, board):
        board = board.board_string()
        try:
            print("Stats for this board: " +
                  str(Counter(self.boxes[board]).most_common()))
        except KeyError:
            print("Never seen this board before.")


class HumanPlayer:
    def __init__(self):
        pass

    def start_game(self):
        print("Get ready!")

    def get_move(self, board):
        while True:
            move = input('Make a move: ')-1
            if board.valid_move(move):
                break
            print("Not a valid move")
        return int(move)

    def win_game(self):
        print("You won!")

    def draw_game(self):
        print("It's a draw.")

    def lose_game(self):
        print("You lose.")

    def print_probability(self, board):
        pass


def play_game(first, second, silent=False):
    first.start_game()
    second.start_game()
    board = Board()

    if not silent:
        print("\n\nStarting a new game!")
        print(board)

    while True:
        if not silent:
            first.print_probability(board)
        move = first.get_move(board)
        if move == -1:
            if not silent:
                print("Player resigns")
            first.lose_game()
            second.win_game()
            break
        board.play_move(move, 'X')
        if not silent:
            print(board)
        if board.winning():
            first.win_game()
            second.lose_game()
            break
        if board.draw():
            first.draw_game()
            second.draw_game()
            break

        if not silent:
            second.print_probability(board)
        move = second.get_move(board)
        if move == -1:
            if not silent:
                print("Player resigns")
            second.lose_game()
            first.win_game()
            break
        board.play_move(move, 'O')
        if not silent:
            print(board)
        if board.winning():
            second.win_game()
            first.lose_game()
            break


if __name__ == '__main__':
    go_first_ai = AIPlayer()
    go_second_ai = AIPlayer()
    human = HumanPlayer()

    d = input('Choose dificulty 1-5: ')+1
    while d not in range(1,7):
        print("Not a valid choice")
        d = input('Choose dificulty 1-5: ')+1
        
    for i in range(10**d):
        play_game(go_first_ai, go_second_ai, silent=True)

    go_first_ai.print_stats()
    go_second_ai.print_stats()

    play_game(go_first_ai, human)
    play_game(human, go_second_ai)
    
x = input('Would you like to play again y/n?: ')

while x == 'y':
    play_game(go_first_ai, human)
    play_game(human, go_second_ai)
    x = input('Would you like to play again y/n?: ')