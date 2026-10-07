"""renderer: all pygame drawing lives here, kept separate from game logic."""

import pygame

WIDTH, HEIGHT = 400, 580
BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_TOP = 100
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)
COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)
COLOR_TEXT = (30, 30, 30)
COLOR_BUTTON = (220, 220, 220)
COLOR_BUTTON_BORDER = (90, 90, 90)

ROUND_RESET_RECT = pygame.Rect(20, 525, 170, 40)
MATCH_RESET_RECT = pygame.Rect(210, 525, 170, 40)
X_CHOICE_RECT = pygame.Rect(70, 220, 100, 60)
O_CHOICE_RECT = pygame.Rect(230, 220, 100, 60)


def board_pos_to_cell(pos):
    x, y = pos
    y -= BOARD_TOP
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return int(row), int(col)


def get_button_action(pos):
    if X_CHOICE_RECT.collidepoint(pos):
        return 'X'
    if O_CHOICE_RECT.collidepoint(pos):
        return 'O'
    if ROUND_RESET_RECT.collidepoint(pos):
        return 'round_reset'
    if MATCH_RESET_RECT.collidepoint(pos):
        return 'match_reset'
    return None


def draw_start_screen(surface, font):
    surface.fill(COLOR_BG)
    title = font.render("Tic-Tac-Toe", True, COLOR_TEXT)
    surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 90)))
    draw_text(surface, font, "Choose your symbol", (surface.get_width() // 2 - 100, 150))

    pygame.draw.rect(surface, COLOR_BUTTON, X_CHOICE_RECT)
    pygame.draw.rect(surface, COLOR_BUTTON_BORDER, X_CHOICE_RECT, 2)
    pygame.draw.rect(surface, COLOR_BUTTON, O_CHOICE_RECT)
    pygame.draw.rect(surface, COLOR_BUTTON_BORDER, O_CHOICE_RECT, 2)

    surface.blit(font.render("Play X", True, COLOR_TEXT),
                  font.render("Play X", True, COLOR_TEXT).get_rect(center=X_CHOICE_RECT.center))
    surface.blit(font.render("Play O", True, COLOR_TEXT),
                  font.render("Play O", True, COLOR_TEXT).get_rect(center=O_CHOICE_RECT.center))

    draw_text(surface, font, "X always starts", (surface.get_width() // 2 - 75, 320))
    draw_text(surface, font, "Press X or O to choose", (surface.get_width() // 2 - 115, 355))


def draw_board(surface, board):
    surface.fill(COLOR_BG)
    for i in range(1, 3):
        pygame.draw.line(surface, COLOR_LINE,
                         (i * CELL_SIZE, BOARD_TOP),
                         (i * CELL_SIZE, BOARD_TOP + BOARD_SIZE), 3)
        pygame.draw.line(surface, COLOR_LINE,
                         (0, BOARD_TOP + i * CELL_SIZE),
                         (BOARD_SIZE, BOARD_TOP + i * CELL_SIZE), 3)

    for r in range(3):
        for c in range(3):
            symbol = board[r][c]
            if symbol is None:
                continue

            center = (c * CELL_SIZE + CELL_SIZE // 2,
                      BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2)

            if symbol == 'X':
                offset = CELL_SIZE // 3
                pygame.draw.line(surface, COLOR_X,
                                 (center[0] - offset, center[1] - offset),
                                 (center[0] + offset, center[1] + offset), 6)
                pygame.draw.line(surface, COLOR_X,
                                 (center[0] + offset, center[1] - offset),
                                 (center[0] - offset, center[1] + offset), 6)
            else:
                pygame.draw.circle(surface, COLOR_O, center, CELL_SIZE // 3, 6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_scoreboard(surface, font, x_score, o_score, draws):
    text = f"X: {x_score}    O: {o_score}    Draws: {draws}"
    surf = font.render(text, True, COLOR_TEXT)
    surface.blit(surf, surf.get_rect(center=(surface.get_width() // 2, 20)))


def draw_banner(surface, font, text):
    surf = font.render(text, True, COLOR_X)
    surface.blit(surf, surf.get_rect(
        center=(surface.get_width() // 2, BOARD_TOP + BOARD_SIZE - 25)))


def draw_controls(surface, font):
    pygame.draw.rect(surface, COLOR_BUTTON, ROUND_RESET_RECT)
    pygame.draw.rect(surface, COLOR_BUTTON_BORDER, ROUND_RESET_RECT, 2)
    pygame.draw.rect(surface, COLOR_BUTTON, MATCH_RESET_RECT)
    pygame.draw.rect(surface, COLOR_BUTTON_BORDER, MATCH_RESET_RECT, 2)

    round_text = font.render("Reset Round", True, COLOR_TEXT)
    match_text = font.render("Reset Match", True, COLOR_TEXT)
    surface.blit(round_text, round_text.get_rect(center=ROUND_RESET_RECT.center))
    surface.blit(match_text, match_text.get_rect(center=MATCH_RESET_RECT.center))
