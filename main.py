import tkinter as tk
from random import choice


class Board:
    HEIGHT = 720
    WIDTH = 720

    def __init__(self, n: int, m: int, canvas: tk.Canvas, speed=200):
        self.field_copy = None
        self.__field = None
        self.n = n
        self.m = m
        self.__c = canvas
        self.speed = speed
        print(self.speed)

        self.__cell_width = self.WIDTH / m
        self.__cell_height = self.HEIGHT / n

        self.__field: list[list[(int, int)]]
        self.create_matrix()
        self.draw()

    def draw(self):
        self.__c.delete('all')
        for i in range(self.n):
            for j in range(self.m):
                self.__c.create_polygon(
                    j * self.__cell_width,
                    i * self.__cell_height,

                    (j + 1) * self.__cell_width,
                    i * self.__cell_height,

                    j * self.__cell_width,
                    (i + 1) * self.__cell_height,

                    fill='black' if self.__field[i][j][0] else 'white',
                    # outline='grey'
                )

                self.__c.create_polygon(
                    (j + 1) * self.__cell_width,
                    (i + 1) * self.__cell_height,

                    (j + 1) * self.__cell_width,
                    i * self.__cell_height,

                    j * self.__cell_width,
                    (i + 1) * self.__cell_height,

                    fill='black' if self.__field[i][j][1] else 'white',
                    # outline='black'
                )
        self.step()
        self.__c.after(self.speed, self.draw)

    def step(self):
        self.field_copy = [i.copy() for i in self.__field]

        for i in range(self.n):
            for j in range(self.m):

                # iu, id, jl, rjr
                nns = self.number_of_alive_neighbours(i, j)

                for cell in range(2):
                    nn = nns[cell]
                    if nn not in (3, 4):
                        self.__field[i][j][cell] = 0
                    elif nn == 4:
                        self.__field[i][j][cell] = 1

    def __str__(self):
        return '\n'.join([' '.join(str(i)) for i in self.__field])

    def create_matrix(self):
        self.__field = [[[
            choice([0, 1]), choice([0, 1])
        ] for _ in range(self.m)] for _ in range(self.n)]

    def number_of_alive_neighbours(self, i, j):
        nn_middle = 0
        a, b, c, d = (i - 1) % self.n, (i + 1) % self.n, (j - 1) % self.m, (j + 1) % self.m
        nn_middle += self.field_copy[a][j][1]
        nn_middle += self.field_copy[a][d][0]
        nn_middle += self.__field[a][d][1]
        nn_middle += self.__field[i][d][0]

        nn_middle += self.__field[b][j][0]
        nn_middle += self.__field[b][c][0]
        nn_middle += self.__field[b][c][1]
        nn_middle += self.__field[i][c][1]

        nn_top, nn_bot = nn_middle + self.__field[i][j][1], nn_middle + self.__field[i][j][0]

        nn_top += self.__field[i][c][0]
        nn_top += self.__field[a][c][1]
        nn_top += self.__field[a][j][0]

        nn_bot += self.__field[i][d][1]
        nn_bot += self.__field[b][d][0]
        nn_bot += self.__field[b][j][1]

        return nn_top, nn_bot


root = tk.Tk()
root.geometry('720x720')

canvas = tk.Canvas(root, width=720, height=720)
canvas.pack()

ROWS = int(input('How many rows do you want: '))
COLUMNS = int(input('How many columns do you want: '))
s = int(input('Enter speed of your program (1-9): '))

if type(ROWS) != int or ROWS > 301 or ROWS < 9:
    raise ValueError('ALLOWED VALUE FOR ROWS IS [9-301]')

if type(COLUMNS) != int or COLUMNS > 301 or COLUMNS < 9:
    raise ValueError('ALLOWED VALUE FOR COLUMNS IS [9-301]')

if s not in range(1, 10):
    raise Exception('Speed of the game can assign only integer values from 1 to 9')

game = Board(ROWS, COLUMNS, canvas, speed=(1000 - s*100))

game.step()


root.mainloop()

