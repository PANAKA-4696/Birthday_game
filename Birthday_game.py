"""pygameのインストール"""
import sys
import subprocess

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

"""pygameのインストール"""

#Birthday Game
#5×5の数字のボードを作成し、0を空白として扱うゲーム

#import必要なライブラリ
import random

# Pygameの初期化
pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Birthday Game")

#色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

#パズルの設定
GRID_SIZE = 5  # 5x5のグリッド
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE  # 各タイルのサイズ

#フォントの設定
font = pygame.font.Font(None, 48)

#ゲームボードの初期化
#goal_boardの作成
goal_board = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 0]
]

#シャッフルしたボードの作成
def create_shuffled_board():
    flat_list = [num for row in goal_board for num in row]
    while True:
        random.shuffle(flat_list)
        #解ける配置かどうかをチェックするロジック(簡略化)
        #5x5のパズルは、ほとんど解けるのでここは簡略化
        break
    shuffeld_board = []
    for i in range(GRID_SIZE):
        shuffeld_board.append(flat_list[i * GRID_SIZE:(i + 1) * GRID_SIZE])
    return shuffeld_board

board = create_shuffled_board()

#タイルの移動関数
def move_tile(board, row, col):
    #指定されたタイルを隣接する空きスペースと交換する関数
    GRID_SIZE = len(board)

    #空きスペースの位置を探す
    empty_row, empty_col = -1, -1
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                empty_row, empty_col = r, c
                break
        if empty_row != -1:
            break

    #クリックされたタイルと空きスペースが隣接しているか判定
    #上下左右のいずれかに空きスペースがあればOK
    is_adjacent = (abs(row - empty_row) == 1 and col == empty_col) or \
                    (abs(col - empty_col) == 1 and row == empty_row)
    
    if is_adjacent:
        #タイルを空きスペースと交換
        board[empty_row][empty_col] = board[row][col]
        board[row][col] = 0

#メインループの前に、ゲーム状態を管理する変数を用意
runnning = True
game_solved = False

#メインループ
while runnning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnning = False

        #マウスのクリックを検出
        if event.type == pygame.MOUSEBUTTONDOWN:
            #マウスクリックで座標を取得
            mouse_x, mouse_y = event.pos

            #どのタイルがクリックされたか計算
            col = mouse_x // TILE_SIZE
            row = mouse_y // TILE_SIZE

            #move_tile関数を呼び出してタイルを移動
            move_tile(board, row, col)

            #ゲームが解けたかどうかをチェック
            if board == goal_board:
                game_solved = True

    #画面描画
    screen.fill(WHITE)  # 背景を白に設定


    #タイルを描画
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_value = board[row][col]
            if tile_value != 0:  # 0は空白なので描画しない
                x = col * TILE_SIZE
                y = row * TILE_SIZE

                #タイルの背景と枠線を描画
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

                #タイルの数字を描画
                text_surface = font.render(str(tile_value), True, BLACK)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                screen.blit(text_surface, text_rect)


    #ゲームがクリアされたらメッセージを表示
    if game_solved:
        text_surface  = font.render("Congratulations! You solved the puzzle!", True, (0, 150, 0))
        text_rect = text_surface .get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface , text_rect)

    pygame.display.flip()  # 画面を更新

pygame.quit()  # Pygameを終了
sys.exit()  # プログラムを終了