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

#500×500のウィンドウで5×5のボードを表示
TILE_SIZE = 500 // 5 #TILE_SIZEは100
for row in range(5):
    for col in range(5):
        tile_number = board[row][col]
        if tile_number != 0:
            #tile_numberに対応する画像を (col * TILE_SIZE, row * TILE_SIZE) に描画
            pass  # ここに画像描画のコードを追加する必要があります