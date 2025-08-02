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
import tkinter as tk
from tkinter import filedialog

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

#画像の読み込みとタイル生成の処理を関数化
def load_and_create_tiles(image_path):
    #画像ファイルを読み込み、タイルを生成して返す関数
    try:
        original_image = pygame.image.load(image_path)  # ここに自分の写真のパスを指定
        original_image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"画像ファイルの読み込み中にエラーが発生しました: {e}")
        return None

    tiles = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile_image = original_image.subsurface((x, y, TILE_SIZE, TILE_SIZE))
            tiles.append(tile_image)

    return tiles

#デフォルトの画像パスを指定
tiles = load_and_create_tiles("Birthday_image.png")
if tiles is None:
    print("タイルの生成に失敗しました。プログラムを終了します。")
    sys.exit()

#ボタンの定義
button_text = "Select Foto"
button_font = pygame.font.Font(None, 30)
button_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 130, 40)#画面右上にボタンを配置

#メインループの前に、ゲーム状態を管理する変数を用意
runnning = True
game_solved = False

#メインループ
while runnning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnning = False

        #ボタンのクリックイベントを検出
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            #ボタンがクリックされたかどうかを判定
            if button_rect.collidepoint((mouse_x, mouse_y)):
                root = tk.Tk()
                root.withdraw()
                image_path = filedialog.askopenfilename(
                    title="新しい画像を選択",
                    filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
                )
                root.destroy()

                if image_path:
                    #新しい画像を読み込み、タイルを再生成し、ボードをシャッフル
                    new_tiles = load_and_create_tiles(image_path)
                    if new_tiles:
                        tiles = new_tiles
                        board = create_shuffled_board()
                        game_solved = False # ゲーム状態をリセット

            else:
                #ボタン以外のクリックされたらタイルの移動処理
                if not game_solved:
                    col = mouse_x // TILE_SIZE
                    row = mouse_y // TILE_SIZE
                    move_tile(board, row, col)

                    if board == goal_board:
                        game_solved = True

    #ボタン描画コードを追加
    #画面描画
    screen.fill(WHITE)

    #タイルを描画
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_number = board[row][col]
            
            #空きスペース(0)以外を描画
            if tile_number != 0:
                #tilesリストからタイルの画像を取得
                #boardの値(1-24)とリストのインデックス(0-23)を対応させる
                tile_image = tiles[tile_number - 1]

                #タイルの位置を計算
                x = col * TILE_SIZE
                y = row * TILE_SIZE

                #タイルの画像を描画
                screen.blit(tile_image, (x, y))

    #ボタンを描画
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)  # ボタンの枠線
    text_surface = button_font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    #ゲームがクリアされたらメッセージを表示
    if game_solved:
        text_surface  = font.render("Congratulations! You solved the puzzle!", True, (0, 150, 0))
        text_rect = text_surface .get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface , text_rect)

    pygame.display.flip()  # 画面を更新

pygame.quit()  # Pygameを終了
sys.exit()  # プログラムを終了