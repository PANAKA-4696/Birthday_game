#Birthday Game
#5×5の数字のボードを作成し、0を空白として扱うゲーム

import pygame
import sys

#ボードの立ち上げ
board = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 0]
]

#goal_boardの作成
goal_board = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 0]
]

#500×500のウィンドウで5×5のボードを表示
TILE_SIZE = 500 // 5 #TILE_SIZEは100
for row in range(5):
    for col in range(5):
        tile_number = board[row][col]
        if tile_number != 0:
            #tile_numberに対応する画像を (col * TILE_SIZE, row * TILE_SIZE) に描画
            pass  # ここに画像描画のコードを追加する必要があります

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

