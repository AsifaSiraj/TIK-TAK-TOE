import math
import time

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return len(self.available_moves())

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all(s == letter for s in row):
            return True
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all(s == letter for s in column):
            return True
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0,4,8]]
            diagonal2 = [self.board[i] for i in [2,4,6]]
            if all(s == letter for s in diagonal1) or all(s == letter for s in diagonal2):
                return True
        return False

def minimax(game, player):
    max_player = 'X'
    other_player = 'O' if player == 'X' else 'X'

    if game.current_winner == other_player:
        # Return score based on who won and how many empty squares left
        return {'position': None, 'score': 1 * (game.num_empty_squares() + 1) if other_player == max_player else -1 * (game.num_empty_squares() + 1)}
    elif not game.empty_squares():
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    for possible_move in game.available_moves():
        game.make_move(possible_move, player)
        sim_score = minimax(game, other_player)  # simulate a game after making that move
        game.board[possible_move] = ' '
        game.current_winner = None
        sim_score['position'] = possible_move

        if player == max_player:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score

    return best

def minimax_alpha_beta(game, player, alpha=-math.inf, beta=math.inf):
    max_player = 'X'
    other_player = 'O' if player == 'X' else 'X'

    if game.current_winner == other_player:
        return {'position': None, 'score': 1 * (game.num_empty_squares() + 1) if other_player == max_player else -1 * (game.num_empty_squares() + 1)}
    elif not game.empty_squares():
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    for possible_move in game.available_moves():
        game.make_move(possible_move, player)
        sim_score = minimax_alpha_beta(game, other_player, alpha, beta)
        game.board[possible_move] = ' '
        game.current_winner = None
        sim_score['position'] = possible_move

        if player == max_player:
            if sim_score['score'] > best['score']:
                best = sim_score
            alpha = max(alpha, best['score'])
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
            beta = min(beta, best['score'])

        if beta <= alpha:
            break

    return best

def play_game(algorithm):
    game = TicTacToe()
    game.print_board()

    while game.empty_squares():
        # Human move
        valid_move = False
        while not valid_move:
            try:
                human_move = int(input("Your move (0-8): "))
                if human_move not in game.available_moves():
                    raise ValueError
                valid_move = True
            except ValueError:
                print("Invalid move. Try again.")
        game.make_move(human_move, 'O')
        game.print_board()
        if game.current_winner:
            print("You win!")
            return

        if not game.empty_squares():
            break

        # AI move
        start_time = time.time()
        if algorithm == 'minimax':
            ai_move = minimax(game, 'X')['position']
        else:
            ai_move = minimax_alpha_beta(game, 'X')['position']
        move_time = time.time() - start_time

        game.make_move(ai_move, 'X')
        print(f"AI move ({algorithm}) at position {ai_move} (calculation time: {move_time:.4f} seconds):")
        game.print_board()
        if game.current_winner:
            print("AI wins!")
            return

    print("It's a tie!")

def compare_algorithms():
    test_positions = [
        ['X', 'O', 'X', ' ', 'O', ' ', ' ', ' ', ' '],
        ['X', ' ', 'O', ' ', 'O', ' ', ' ', 'X', ' '],
        [' ', 'X', ' ', 'O', 'O', 'X', ' ', ' ', ' ']
    ]

    print("\nPerformance Comparison:")
    print(f"{'Test #':<7} {'Minimax Time (s)':<20} {'Alpha-Beta Time (s)':<22} {'Speedup':<10}")

    for i, pos in enumerate(test_positions, 1):
        game = TicTacToe()
        game.board = pos.copy()

        start = time.time()
        minimax(game, 'X')
        time_minimax = time.time() - start

        start = time.time()
        minimax_alpha_beta(game, 'X')
        time_ab = time.time() - start

        speedup = time_minimax / time_ab if time_ab > 0 else float('inf')
        print(f"{i:<7} {time_minimax:<20.6f} {time_ab:<22.6f} {speedup:<10.2f}")

if __name__ == "__main__":
    print("=== Tic-Tac-Toe AI: Minimax vs Alpha-Beta Pruning ===")
    while True:
        print("\nMenu:")
        print("1. Play against Minimax AI")
        print("2. Play against Alpha-Beta Pruning AI")
        print("3. Compare performance of Minimax and Alpha-Beta")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            play_game('minimax')
        elif choice == '2':
            play_game('alpha_beta')
        elif choice == '3':
            compare_algorithms()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
