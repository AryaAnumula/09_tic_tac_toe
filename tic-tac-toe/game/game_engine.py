"""GameEngine: owns board, turn state, round-end logic, and scores."""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell, get_button_action
from game.ai import choose_move


class GameEngine:
    def __init__(self):
        self.x_score = 0
        self.o_score = 0
        self.draws = 0
        self.player_symbol = None
        self.computer_symbol = None
        self.match_started = False
        self.reset_round()

    def reset_round(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = 'X'
        self.round_over = False
        self.winner = None

        if self.match_started and self.player_symbol == 'O':
            self._maybe_take_computer_turn()

    def reset_match(self):
        self.x_score = 0
        self.o_score = 0
        self.draws = 0
        self.player_symbol = None
        self.computer_symbol = None
        self.match_started = False
        self.reset_round()

    def start_match(self, player_symbol):
        self.player_symbol = player_symbol
        self.computer_symbol = 'O' if player_symbol == 'X' else 'X'
        self.match_started = True
        self.reset_round()

    def handle_click(self, pos):
        action = get_button_action(pos)

        if not self.match_started:
            if action in ('X', 'O'):
                self.start_match(action)
            return

        if action == 'round_reset':
            self.reset_round()
            return

        if action == 'match_reset':
            self.reset_match()
            return

        if self.round_over or self.current_player != self.player_symbol:
            return

        cell = board_pos_to_cell(pos)
        if cell is None:
            return

        row, col = cell
        if self.board[row][col] is not None:
            return

        self.board[row][col] = self.current_player
        self.check_round_end()

        if self.round_over:
            return

        self.current_player = self.computer_symbol
        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over or self.current_player != self.computer_symbol:
            return

        move = choose_move(self.board)
        if move is None:
            return

        row, col = move
        self.board[row][col] = self.current_player
        self.check_round_end()

        if self.round_over:
            return

        self.current_player = self.player_symbol

    def handle_keydown(self, key):
        import pygame

        if key == pygame.K_r and self.match_started:
            self.reset_round()
        elif key == pygame.K_m:
            self.reset_match()
        elif not self.match_started:
            if key == pygame.K_x:
                self.start_match('X')
            elif key == pygame.K_o:
                self.start_match('O')

    def check_round_end(self):
        if self.round_over:
            return

        winner = check_winner(self.board)

        if winner:
            self.round_over = True
            self.winner = winner
            if winner == 'X':
                self.x_score += 1
            elif winner == 'O':
                self.o_score += 1
            return

        if is_board_full(self.board):
            self.round_over = True
            self.winner = None
            self.draws += 1

    def draw(self, surface, font):
        from game import renderer

        if not self.match_started:
            renderer.draw_start_screen(surface, font)
            return

        renderer.draw_board(surface, self.board)
        renderer.draw_scoreboard(surface, font, self.x_score, self.o_score, self.draws)

        turn_label = (
            f"Your turn ({self.player_symbol})"
            if self.current_player == self.player_symbol
            else f"Computer's turn ({self.computer_symbol})"
        )
        renderer.draw_text(surface, font, turn_label, (10, 50))

        if self.round_over:
            text = f"{self.winner} wins!" if self.winner else "Draw!"
            renderer.draw_banner(surface, font, text)

        renderer.draw_controls(surface, font)
