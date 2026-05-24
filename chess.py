import pygame 
import numpy as np
import matplotlib.pyplot


pygame.init()

#Constants
WIDTH = 1400
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 24)

images = {
    "black_king": pygame.image.load("images/black_king.png").convert_alpha(),
    "black_queen": pygame.image.load("images/black_queen.png").convert_alpha(),
    "black_bishop": pygame.image.load("images/black_bishop.png").convert_alpha(),
    "black_knight": pygame.image.load("images/black_knight.png").convert_alpha(),
    "black_pawn": pygame.image.load("images/black_pawn.png").convert_alpha(),
    "black_rook": pygame.image.load("images/black_rook.png").convert_alpha(),
    "white_king": pygame.image.load("images/white_king.png").convert_alpha(),
    "white_queen": pygame.image.load("images/white_queen.png").convert_alpha(),
    "white_bishop": pygame.image.load("images/white_bishop.png").convert_alpha(),
    "white_knight": pygame.image.load("images/white_knight.png").convert_alpha(),
    "white_pawn": pygame.image.load("images/white_pawn.png").convert_alpha(),
    "white_rook": pygame.image.load("images/white_rook.png").convert_alpha()
}


values = {
    "black_queen" : "-9",
    "white_queen" : "9",
    "black_bishop" : "-3",
    "black_knight" : "-3",
    "white_bishop" : "3",
    "white_knight" : "3",
    "white_rook" : "5",
    "black_rook" : "-5",
    "white_pawn" : "1",
    "black_pawn" : "-1"
}


letters = ["a","b","c","d","e","f","g","h"]
numbers = ["8","7","6","5","4","3","2","1"]
board = np.array([
    ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
    ["black_pawn"]*8,
    [""]*8,
    [""]*8,
    [""]*8,
    [""]*8,
    ["white_pawn"]*8,
    ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_bishop", "white_knight", "white_rook"]
], dtype = object)

SQUARE = 90
centerx = (WIDTH-8*SQUARE)//2
centery = (HEIGHT-8*SQUARE)//2
COLOR1 = (240, 200, 180)
MOVE1 = (158, 102, 74)
COLOR2 = (117, 91, 79)
MOVE2 = (54, 32, 22)
SCREEN.fill((25, 21, 38))
black_king_move = False
white_king_move = False
black_rook_move_left = False
white_rook_move_left = False
black_rook_move_right = False
white_rook_move_right = False
turn = True
running = True

for key in images:
    images[key] = pygame.transform.scale(images[key], (SQUARE, SQUARE))

def get_valid_moves(row, col, board, castling = True):
    piece = board[row][col]
    moves = []
    
    if piece == "black_rook" or piece == "white_rook":
        opp = ""
        if piece == "black_rook":
            opp = "white"
        else:
            opp = "black"
        dir = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for dx, dy in dir:
            r = row + dx
            c = col + dy
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "":
                    moves.append((r,c))
                else:
                    if opp in board[r][c]:
                        moves.append((r,c))
                    break
                r += dx
                c += dy
        return moves
    
    elif piece == "black_bishop" or piece == "white_bishop":
        opp = ""
        if piece == "black_bishop":
            opp = "white"
        else:
            opp = "black"
        dir = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in dir:
            r = row + dx
            c = col + dy
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "":
                    moves.append((r,c))
                else:
                    if opp in board[r][c]:
                        moves.append((r,c))
                    break
                r += dx
                c += dy
        return moves
    
    elif piece == "black_knight" or piece == "white_knight":
        opp = ""
        if piece == "black_knight":
            opp = "white"
        else:
            opp = "black"
        dir = [(-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
        for dx, dy in dir:
            r = row + dx
            c = col + dy
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "" or opp in board[r][c]:
                    moves.append((r,c))
        return moves
    
    elif piece == "black_king" or piece == "white_king":
        opp = ""
        if piece == "black_king":
            opp = "white"
        else:
            opp = "black"
        dir = [(-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1), (1, 0), (0, 1), (0, -1)]
        for dx, dy in dir:
            r = row + dx
            c = col + dy
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "" or opp in board[r][c]:
                    moves.append((r,c))
        is_white = False
        if "white" in piece:
            is_white = True 
        if castling:
            king_status = white_king_move if is_white else black_king_move
            lrook_status = white_rook_move_left if is_white else black_rook_move_left
            rrook_status = white_rook_move_right if is_white else black_rook_move_right
            r_idx = 7 if is_white else 0
            if not king_status and not check_king(turn, board):
                if not rrook_status and board[r_idx][5] == "" and board[r_idx][6] == "":
                    if not check_move_checkmate(r_idx, 4, r_idx, 5, board, turn) and not check_move_checkmate(r_idx, 4, r_idx, 6, board, turn):
                        moves.append((r_idx, 6))
                if not lrook_status and board[r_idx][1] == "" and board[r_idx][2] == "" and board[r_idx][3] == "":
                    if not check_move_checkmate(r_idx, 4, r_idx, 3, board, turn) and not check_move_checkmate(r_idx, 4, r_idx, 2, board, turn):
                        moves.append((r_idx, 2))

        return moves
    
    elif piece == "black_queen" or piece == "white_queen":
        opp = ""
        if piece == "black_queen":
            opp = "white"
        else:
            opp = "black"
        dir = [(-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1), (1, 0), (0, 1), (0, -1)]
        for dx, dy in dir:
            r = row + dx
            c = col + dy
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == "":
                    moves.append((r,c))
                else:
                    if opp in board[r][c]:
                        moves.append((r,c))
                    break
                r += dx
                c += dy
        return moves
    
    elif "pawn" in piece:
        is_white = "white" in piece
        dir = -1 if is_white else 1
        sr = 6 if is_white else 1
        opp = "black" if is_white else "white"

        if 0 <= row + dir < 8 and board[row + dir][col] == "":
            moves.append((row + dir, col))
            if row == sr and board[row + 2*dir][col] == "":
                moves.append((row + 2*dir, col))
        for d in [-1, 1]:
            if 0 <= row + dir < 8 and 0 <= col + d < 8:
                if opp in board[row + dir][col + d]:
                    moves.append((row + dir, col + d))
            if en_passant_target == (row, col + d):
                moves.append((row + dir, col + d))    
        return moves
        
    
def check_king(turn, board):
    opp = "black" if turn else "white"
    player = "white_king" if turn else "black_king"
    king_pos = None
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                king_pos = i, j
    for i in range(8):
        for j in range(8):
            if opp in board[i][j]:
                moves = get_valid_moves(i, j, board, False)
                if king_pos in moves:
                    return True
    return False

def check_move_checkmate(sr, sc, er, ec, board, turn):
    new_board = board.copy()
    new_board[er][ec] = new_board[sr][sc]
    new_board[sr][sc] = ""
    if "pawn" in new_board[er][ec] and sc != ec and board[er][ec] == "":
        new_board[sr][ec] = ""
    return check_king(turn, new_board)

def game_over(turn, board):
    has_legal_move = False
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "" and (("white" in piece and turn) or ("black" in piece and not turn)):
                p_moves = get_valid_moves(row, col, board)
                for r, c in p_moves:
                    if not check_move_checkmate(row, col, r, c, board, turn):
                        has_legal_move = True
                        break
            if has_legal_move:
                break
        if has_legal_move:
            break

    if has_legal_move:
        return False
    if check_king(turn, board):
        return "white" if not turn else "black"
    else:
        return "stalemate"
        
en_passant_target = None
moves = []
last_move = (8, 8)
llast_move = (8, 8)
winner = None

while running:
    pygame.draw.rect(SCREEN, (0,0,0), (centerx-5, centery-5, 8*SQUARE+10, 8*SQUARE+10))
    
    board_row, board_col = (8, 8)
    for i in range(8):
        text1 = FONT.render(letters[i], True, (255,255,255))
        SCREEN.blit(text1, (centerx + i*SQUARE + SQUARE//2,centery + 8*SQUARE + 10))
        text2 = FONT.render(numbers[i], True, (255,255,255))
        SCREEN.blit(text2,(centerx - 25,centery + i*SQUARE + SQUARE//2 - 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not winner:
            (mx, my) = event.pos
            col = (mx - centerx)//SQUARE
            row = (my - centery)//SQUARE
            board_row, board_col = col, row

            if 0 <= row < 8 and 0 <= col < 8:
                if board[row][col] != "":
                    if (turn and "white" in board[row][col]) or (not turn and "black" in board[row][col]):
                        last_move = (row, col)
                        uncheck_moves = get_valid_moves(row, col, board)
                        moves = []
                        for r, c in uncheck_moves:
                            if not check_move_checkmate(row, col, r, c, board, turn):
                                moves.append((r, c))

                if (row, col) in moves:
                    x, y = last_move
                    if "pawn" in board[x][y] and col !=y and board[row][col] == "":
                        board[x][col] = ""
                    if "king" in board[x][y] and abs(col-y) == 2:
                        if col == 6:
                            board[row][5] = board[row][7]
                            board[row][7] = ""
                        elif col == 2:
                            board[row][3] = board[row][0]
                            board[row][0] = ""

                    if board[x][y] == "white_king": white_king_move = True
                    if x == 7 and y == 0 : white_rook_move_left = True
                    if x == 7 and y == 7: white_rook_move_right = True
                    if board[x][y] == "black_king": black_king_move = True
                    if x == 0 and y == 0: black_rook_move_left = True
                    if x == 0 and y == 7: black_rook_move_right = True

                    if row == 7 and col == 0: white_rook_move_left = True
                    if row == 7 and col == 7: white_rook_move_right = True
                    if row == 0 and col == 0: black_rook_move_left = True
                    if row == 0 and col == 7: black_rook_move_right = True
                    if "pawn" in board[x][y] and abs(row - x) == 2:
                        en_passant_target = (row, col)
                    else:
                        en_passant_target = None
                    
                    board[row][col] = board[x][y]
                    board[x][y] = ""
                    if "white_pawn" in board[row][col] and row == 0:
                        board[row][col] = "white_queen"
                    elif "black_pawn" in board[row][col] and row == 7:
                        board[row][col] = "black_queen"
                    moves = []
                    llast_move = last_move
                    last_move = (row, col)
                    turn = not turn
                winner = game_over(turn, board)



    for row in range(8):
        y = centery + row*SQUARE
        for col in range(8):
            x = centerx + col*SQUARE
            if (row+col)%2 != 0:
                pygame.draw.rect(SCREEN, COLOR2, (x, y, SQUARE, SQUARE))
            else :
                pygame.draw.rect(SCREEN, COLOR1, (x, y, SQUARE, SQUARE))
            if (row, col) == last_move:
                pygame.draw.rect(SCREEN, (178, 224, 135), (x, y, SQUARE, SQUARE))
            if (row, col) == llast_move:
                pygame.draw.rect(SCREEN, (115, 145, 87), (x, y, SQUARE, SQUARE))
            if board[row][col] != "":
                SCREEN.blit(images[board[row][col]], (x, y))
            if moves is not None and (row, col) in moves:
                COLOR = MOVE1 if (row + col)%2 == 0 else MOVE2
                COLORR = COLOR1 if (row + col)%2 == 0 else COLOR2
                if board[row][col] == "":
                    if board[row][col] != "":
                        SCREEN.blit(images[board[row][col]], (x, y))
                    pygame.draw.circle(SCREEN, COLOR, (x + SQUARE//2, y + SQUARE//2), 10)
                else:
                    pygame.draw.circle(SCREEN, COLOR, (x + SQUARE//2, y + SQUARE//2), SQUARE//2 - 1)
                    pygame.draw.circle(SCREEN, COLORR, (x + SQUARE//2, y + SQUARE//2), SQUARE//2 - 6)
                    if board[row][col] != "":
                        SCREEN.blit(images[board[row][col]], (x, y))
            pygame.draw.line(SCREEN, (0, 0, 0), (centerx, y), (centerx + 8*SQUARE, y), 2)
            pygame.draw.line(SCREEN, (0, 0, 0), (x, centery), (x, centery + 8*SQUARE), 2)
    if winner:
        pygame.draw.rect(SCREEN, (255, 215, 0), (1000, 340, 400, 120), 4, border_radius=15)
        winner_font = pygame.font.SysFont("arial", 48, bold=True)
        text = winner_font.render(f"{winner} Wins!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(1200, 400))
        SCREEN.blit(text, text_rect) 


    pygame.display.flip()
    CLOCK.tick(60)
pygame.quit()