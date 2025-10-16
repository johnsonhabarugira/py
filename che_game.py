import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
BROWN = (181, 136, 99)
BEIGE = (240, 217, 181)
HIGHLIGHT = (0, 255, 0, 100)

# Load images with safe fallbacks when files are missing
pieces = {}
piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
for color in ['w', 'b']:
    for piece in piece_names:
        key = color + piece
        path = os.path.join('images', f'{color}_{piece}.png')
        try:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
            else:
                raise FileNotFoundError(path)
        except Exception:
            # Create a simple placeholder surface: a circle + letter
            img = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            img.fill((0, 0, 0, 0))
            circle_color = (245, 245, 245) if color == 'w' else (30, 30, 30)
            pygame.draw.circle(img, circle_color, (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//3)
            # draw a letter for piece
            try:
                font = pygame.font.SysFont(None, max(12, SQUARE_SIZE//4))
                letter = piece[0].upper()
                text_color = (0,0,0) if color == 'w' else (255,255,255)
                txt = font.render(letter, True, text_color)
                txt_rect = txt.get_rect(center=(SQUARE_SIZE//2, SQUARE_SIZE//2))
                img.blit(txt, txt_rect)
            except Exception:
                pass
        pieces[key] = img

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

def draw_board(selected_square=None):
    for row in range(ROWS):
        for col in range(COLS):
            color = BEIGE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if selected_square == (row, col):
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(120)
                s.fill(HIGHLIGHT)
                screen.blit(s, (col*SQUARE_SIZE, row*SQUARE_SIZE))


def compute_possible_moves(board, selected_piece, selected_square, turn):
    """Return a list of (r,c, capture_bool) squares that are valid moves for selected_piece."""
    moves = []
    if not selected_piece or not selected_square:
        return moves
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) == selected_square:
                continue
            try:
                if is_valid_move(selected_piece, selected_square, (r, c), board, turn):
                    capture = board[r][c] != "--"
                    moves.append((r, c, capture))
            except Exception:
                continue
    return moves

def draw_pieces(board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                screen.blit(pieces[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))


def choose_promotion(color):
    """Display an on-screen modal to choose promotion piece for `color` ('w' or 'b').
    Returns one of: 'queen', 'rook', 'bishop', 'knight'. Blocks until a choice is made.
    """
    options = ['queen', 'rook', 'bishop', 'knight']
    box_w = SQUARE_SIZE * 1.6
    box_h = SQUARE_SIZE * 1.6
    gap = 12
    total_w = box_w * len(options) + gap * (len(options) - 1)
    start_x = (WIDTH - total_w) // 2
    y = (HEIGHT - box_h) // 2
    option_rects = [pygame.Rect(start_x + i*(box_w+gap), y, box_w, box_h) for i in range(len(options))]
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    font = pygame.font.SysFont(None, max(14, SQUARE_SIZE//4))
    clock = pygame.time.Clock()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mx, my):
                        return options[i]
            if ev.type == pygame.KEYDOWN:
                # allow quick keys: q, r, b, n
                if ev.key == pygame.K_q:
                    return 'queen'
                if ev.key == pygame.K_r:
                    return 'rook'
                if ev.key == pygame.K_b:
                    return 'bishop'
                if ev.key == pygame.K_n:
                    return 'knight'

        # draw modal
        draw_board()
        draw_pieces(board_placeholder())
        screen.blit(overlay, (0, 0))

        for i, opt in enumerate(options):
            rect = option_rects[i]
            pygame.draw.rect(screen, (220, 220, 220), rect, border_radius=6)
            pygame.draw.rect(screen, (10, 10, 10), rect, 2, border_radius=6)
            # draw piece image if available
            key = color + opt
            img = pieces.get(key)
            if img:
                # scale to fit inside rect
                iw = int(rect.width * 0.8)
                ih = int(rect.height * 0.8)
                im = pygame.transform.smoothscale(img, (iw, ih))
                screen.blit(im, (rect.x + (rect.width - iw)//2, rect.y + (rect.height - ih)//2))
            else:
                txt = font.render(opt[0].upper(), True, (0,0,0))
                screen.blit(txt, (rect.x + rect.width//2 - txt.get_width()//2, rect.y + rect.height//2 - txt.get_height()//2))

        pygame.display.flip()
        clock.tick(30)


def board_placeholder():
    """Return a simple empty board for drawing underneath modals (keeps current pieces visible).
    This function reads the current screen buffer from the board variable in main via a simple approach: it
    constructs an empty board surface using the current global `pieces` state and default empty board layout.
    """
    # We'll return the current board if available in globals; otherwise an empty board
    return globals().get('current_board', [["--"]*8 for _ in range(8)])

def is_valid_move(piece, start, end, board, turn):
    s_row, s_col = start
    e_row, e_col = end
    target = board[e_row][e_col]

    # Can't capture own pieces
    if target != "--" and target[0] == piece[0]:
        return False

    kind = piece[1:]  # pawn, rook, etc
    direction = 1 if piece[0] == 'w' else -1

    # Pawn moves
    if kind == "pawn":
        if s_col == e_col and target == "--":
            if e_row - s_row == -direction:
                return True
            if (s_row == 6 and piece[0] == 'w') or (s_row == 1 and piece[0] == 'b'):
                if e_row - s_row == -2*direction and board[s_row - direction][s_col] == "--":
                    return True
        elif abs(s_col - e_col) == 1 and e_row - s_row == -direction and target != "--":
            return True
        return False
    # Rook moves
    elif kind == "rook":
        if s_row == e_row or s_col == e_col:
            # Check path is clear
            step_row = 0 if s_row == e_row else (1 if e_row > s_row else -1)
            step_col = 0 if s_col == e_col else (1 if e_col > s_col else -1)
            r, c = s_row + step_row, s_col + step_col
            while (r, c) != (e_row, e_col):
                if board[r][c] != "--":
                    return False
                r += step_row
                c += step_col
            return True
        return False
    # Knight moves
    elif kind == "knight":
        return (abs(s_row - e_row), abs(s_col - e_col)) in [(2,1), (1,2)]
    # Bishop moves
    elif kind == "bishop":
        if abs(s_row - e_row) == abs(s_col - e_col):
            step_row = 1 if e_row > s_row else -1
            step_col = 1 if e_col > s_col else -1
            r, c = s_row + step_row, s_col + step_col
            while (r, c) != (e_row, e_col):
                if board[r][c] != "--":
                    return False
                r += step_row
                c += step_col
            return True
        return False
    # Queen moves
    elif kind == "queen":
        # Combine rook and bishop
        return is_valid_move(piece[0]+"rook", start, end, board, turn) or is_valid_move(piece[0]+"bishop", start, end, board, turn)
    # King moves
    elif kind == "king":
        return max(abs(s_row - e_row), abs(s_col - e_col)) == 1
    return False

def main():
    clock = pygame.time.Clock()
    
    # Initial board setup
    board = [
        ["brook","bknight","bbishop","bqueen","bking","bbishop","bknight","brook"],
        ["bpawn"]*8,
        ["--"]*8,
        ["--"]*8,
        ["--"]*8,
        ["--"]*8,
        ["wpawn"]*8,
        ["wrook","wknight","wbishop","wqueen","wking","wbishop","wknight","wrook"]
    ]
    
    selected_piece = None
    selected_square = None
    turn = 'w'  # White starts
    
    running = True
    while running:
        # expose board to modal helper so promotion UI can draw current pieces
        globals()['current_board'] = board
        draw_board(selected_square)
        draw_pieces(board)
        # draw possible-move markers when a piece is selected
        possible = compute_possible_moves(board, selected_piece, selected_square, turn)
        for (r, c, capture) in possible:
            center = (c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2)
            if capture:
                # red semi-transparent circle for captures
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(s, (200, 50, 50, 180), (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//3)
                screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            else:
                # small green dot for normal moves
                pygame.draw.circle(screen, (0, 180, 0), center, max(4, SQUARE_SIZE//12))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                piece = board[row][col]
                
                if selected_piece:
                    if is_valid_move(selected_piece, selected_square, (row, col), board, turn):
                        board[row][col] = selected_piece
                        # Remove piece from its original square
                        s_row, s_col = selected_square
                        board[s_row][s_col] = "--"
                        # Handle pawn promotion when reaching the end rank
                        color = selected_piece[0]
                        kind = selected_piece[1:]
                        if kind == 'pawn':
                            # white promotes on row 0, black on row 7
                            if (color == 'w' and row == 0) or (color == 'b' and row == 7):
                                promoted = choose_promotion(color)
                                board[row][col] = color + promoted
                        selected_piece = None
                        selected_square = None
                        # Switch turn
                        turn = 'b' if turn == 'w' else 'w'
                    else:
                        # Invalid move, deselect
                        selected_piece = None
                        selected_square = None
                elif piece != "--" and piece[0] == turn:
                    selected_piece = piece
                    selected_square = (row, col)
        
        clock.tick(60)

if __name__ == "__main__":
    main()
