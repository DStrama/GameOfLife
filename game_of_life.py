import numpy as np
import tkinter as tk
from tkinter import ttk


class GameOfLife:
    def __init__(self, initial_state, width, height):
        self

        self.height = height
        self.width = width
        self.size = np.zeros([height, width])

        if initial_state == 'immutable':
            self.state = np.array([[0, 1, 1, 0],
                                   [1, 0, 0, 1],
                                   [0, 1, 1, 0]])


        elif initial_state == 'glider':
            self.state = np.array([[0, 0, 1, 0],
                                   [0, 0, 0, 1],
                                   [0, 1, 1, 1]])

        elif initial_state == 'oscillator':
            self.state = np.array([[0, 0, 1, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 1, 0]])


        elif initial_state == 'aleatory':
            self.state = np.random.randint(0, 2, (height, width))

        # find overlapping range and then add the arrays using slicing
        # offset
        pos_v, pos_h = 2, 2

        v_range1 = slice(max(0, pos_v), max(min(pos_v + self.state.shape[0], self.size.shape[0]), 0))
        h_range1 = slice(max(0, pos_h), max(min(pos_h + self.state.shape[1], self.size.shape[1]), 0))

        v_range2 = slice(max(0, -pos_v), min(-pos_v + self.size.shape[0], self.state.shape[0]))
        h_range2 = slice(max(0, -pos_h), min(-pos_h + self.size.shape[1], self.state.shape[1]))

        self.size[v_range1, h_range1] += self.state[v_range2, h_range2]

    def next_iteration(self):

        next_iteration = np.zeros([self.height, self.width])

        for i in range(self.height):
            for j in range(self.width):

                neighbours = self.retrive_neighbors(i, j)
                how_many_alive_neighbours = self.count_alive_neighbour(neighbours)

                if self.size[i][j] == 0 and how_many_alive_neighbours == 3:
                    next_iteration[i][j] = 1
                elif how_many_alive_neighbours > 3 and self.size[i][j] == 1:
                    next_iteration[i][j] = 0
                elif how_many_alive_neighbours < 2 and self.size[i][j] == 1:
                    next_iteration[i][j] = 0
                elif self.size[i][j] == 1 and (how_many_alive_neighbours == 3 or how_many_alive_neighbours == 2):
                    next_iteration[i][j] = 1

        self.size = next_iteration

    def retrive_neighbors(self, row, column):

        if row == 0:
            prev_row = self.width - 1
        else:
            prev_row = row - 1

        if row == self.width - 1:
            next_row = 0
        else:
            next_row = row + 1

        if column == 0:
            prev_col = self.height - 1
        else:
            prev_col = column - 1

        if column == self.height - 1:
            next_col = 0
        else:
            next_col = column + 1

        return [self.size[prev_row][prev_col], self.size[prev_row][column], self.size[prev_row][next_col],
                self.size[row][prev_col], self.size[row][next_col],
                self.size[next_row][prev_col], self.size[next_row][column], self.size[next_row][next_col]]

    def count_alive_neighbour(self, neighbours):
        how_many_alive_neighbours = 0
        for neighbour in neighbours:
            if neighbour == 1:
                how_many_alive_neighbours += 1

        return how_many_alive_neighbours

class Gui(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.obj = None
        self.canvas = tk.Canvas(self, width=520, height=1000)
        self.canvas.pack()

        self.label = tk.Label(self, text="Select Rules:")
        self.label.place(x=300, y=5)

        self.combobox_rules = ttk.Combobox(self, values=["immutable", "glider", "oscillator", "manual", "aleatory"],
                                           state="readonly")
        self.combobox_rules.place(x=300, y=30)

        self.button = tk.Button(self, text="Start", command=self.on_button_click)
        self.button.place(x=150, y=100)

        self.label = tk.Label(self, text="Height:")
        self.label.place(x=20, y=70)

        self.entry_height = tk.Entry(self, width=10)
        self.entry_height.place(x=20, y=95)

        self.label = tk.Label(self, text="Width:")
        self.label.place(x=20, y=5)

        self.entry_width = tk.Entry(self, width=10)
        self.entry_width.place(x=20, y=30)

        self.label = tk.Label(self, text="Number of iterations:")
        self.label.place(x=130, y=5)

        self.entry_iteration = tk.Entry(self, width=15)
        self.entry_iteration.place(x=130, y=30)

    def printing(self, achivedgrid, value_x1, value_x2, value_y1, value_y2, width, height):
        x1 = value_x1
        x2 = value_x2
        y1 = value_y1
        y2 = value_y2

        for i in range(height):
            for j in range(width):
                if achivedgrid[i][j] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                x1 = x1 + 5
                x2 = x2 + 5
            y1 = y1 + 5
            y2 = y2 + 5
            x1 = value_x1
            x2 = value_x2

    def how_many_iteration(self, obj, iteration):
        x1 = 20
        x2 = 25
        y1 = 200
        y2 = 205
        z = 0
        for i in range(iteration):
            self.printing(self.obj.size, x1, x2, y1, y2, obj.width, obj.height)
            self.obj.next_iteration()
            x1 += 100
            x2 += 100
            z += 1
            if z == 5:
                y1 += 100
                y2 += 100
                x1 = 20
                x2 = 25
                z = 0

    def on_button_click(self):

        self.obj = GameOfLife(self.combobox_rules.get(), int(self.entry_width.get()), int(self.entry_height.get()))
        self.how_many_iteration(self.obj, int(self.entry_iteration.get()))


gui = Gui()
gui.mainloop()
