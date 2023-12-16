import tkinter as tk
from tkinter import YES, BOTH
import random
from collections import deque
from tkinter import messagebox
from queue import PriorityQueue
import time


class MazeApp(tk.Tk):
    class Maze:
        def __init__(self, rows=10, cols=10, canvas=None, switcher=None):
            self.BFStime = None
            self.DFStime = None
            self.AStarTime= None
            self.rectangle_ids = []
            self.rows = rows
            self.cols = cols
            self.maze_map = {}
            self.grid = []
            self.path = {}
            self._cell_width = 50
            self._win = None
            self._canvas = canvas
            self.switcher = switcher

        @property
        def grid(self):
            return self._grid

        @grid.setter
        def grid(self,n):
            self._grid = []
            y = 0
            for n in range(self.cols):
                x = 1
                y = 1 + y
                for m in range(self.rows):
                    self.grid.append((x, y))
                    self.maze_map[x, y] = {'E': 0, 'W': 0, 'N': 0, 'S': 0}
                    x = x + 1

        def OpenEast(self, x, y):
            self.maze_map[x, y]['E'] = 1
            if y + 1 <= self.cols:
                self.maze_map[x, y + 1]['W'] = 1

        def OpenWest(self, x, y):
            self.maze_map[x, y]['W'] = 1
            if y > 1:
                self.maze_map[x, y - 1]['E'] = 1

        def OpenNorth(self, x, y):
            self.maze_map[x, y]['N'] = 1
            if x > 1:
                self.maze_map[x - 1, y]['S'] = 1

        def OpenSouth(self, x, y):
            self.maze_map[x, y]['S'] = 1
            if x + 1 <= self.rows:
                self.maze_map[x + 1, y]['N'] = 1

        def CreateMaze(self, x=1, y=1, pattern=None):

            stack = []
            closed = []

            stack.append((x, y))
            closed.append((x, y))

            while len(stack) > 0:
                cell = []

                if (x, y + 1) not in closed and (x, y + 1) in self.grid:
                    cell.append("E")
                if (x, y - 1) not in closed and (x, y - 1) in self.grid:
                    cell.append("W")
                if (x + 1, y) not in closed and (x + 1, y) in self.grid:
                    cell.append("S")
                if (x - 1, y) not in closed and (x - 1, y) in self.grid:
                    cell.append("N")

                if (len(cell) > 0):
                    current_cell = (random.choice(cell))
                    if current_cell == "E":
                        self.OpenEast(x, y)
                        self.path[x, y + 1] = x, y
                        y = y + 1
                        closed.append((x, y))
                        stack.append((x, y))

                    elif current_cell == "W":
                        self.OpenWest(x, y)
                        self.path[x, y - 1] = x, y
                        y = y - 1
                        closed.append((x, y))
                        stack.append((x, y))

                    elif current_cell == "N":
                        self.OpenNorth(x, y)
                        self.path[(x - 1, y)] = x, y
                        x = x - 1
                        closed.append((x, y))
                        stack.append((x, y))

                    elif current_cell == "S":
                        self.OpenSouth(x, y)
                        self.path[(x + 1, y)] = x, y
                        x = x + 1
                        closed.append((x, y))
                        stack.append((x, y))

                else:

                    x, y = stack.pop()

        def clear_canvas(self):

            # Delete all previously drawn rectangles
            for rectangle_id in self.rectangle_ids:
                self._canvas.delete(rectangle_id)
            # Clear the list of rectangle IDs
            self.rectangle_ids = []
            self._canvas.itemconfig(self.label_id, state='normal')
            self._canvas.itemconfig(self.button3_id, state='normal')
            self._canvas.itemconfig(self.button4_id, state='normal')
            self._canvas.itemconfig(self.button_id, state='normal')
            self._canvas.itemconfig(self.back_button_id, state='hidden')
            self._canvas.itemconfig(self.completion_label_id, state='hidden')
            if self.DFStime is not None:
                label_text = f"It took {self.DFStime:.2f} seconds"
                self.label2 = tk.Label(self._canvas, text=label_text, font=("Arial", 16), wraplength=500, bg='black',
                                       fg='white')
                self.label2_id = self._canvas.create_window(1050, 310, window=self.label2, anchor=tk.NW)

            if self.BFStime is not None:
                label_text = f"It took {self.BFStime:.2f} seconds"
                self.label3 = tk.Label(self._canvas, text=label_text, font=("Arial", 16), wraplength=500, bg='black',
                                       fg='white')
                self.label3_id = self._canvas.create_window(1050, 210, window=self.label3, anchor=tk.NW)

            if self.AStarTime is not None:
                label_text = f"It took {self.AStarTime:.2f} seconds"
                self.label4 = tk.Label(self._canvas, text=label_text, font=("Arial", 16), wraplength=500, bg='black',
                                       fg='white')
                self.label4_id = self._canvas.create_window(1050, 410, window=self.label4, anchor=tk.NW)
            self._canvas.itemconfig(self.label2_id, state='normal')
            self._canvas.itemconfig(self.label3_id, state='normal')
            self._canvas.itemconfig(self.label4_id, state='normal')

        def DFSAnimation(self, cell=None, frontier=None, visited=None, path=None, t1=None):
            if cell is None:
                cell = (self.rows, self.cols)
            if frontier is None:
                frontier = deque()
                frontier.append(cell)
            if visited is None:
                visited = {(self.rows, self.cols)}
            if path is None:
                path = {}
            if t1 is None:
                t1 = time.time()
            space_bw = self._cell_width / 4.75
            self._canvas.itemconfig(self.label_id, state='hidden')
            self._canvas.itemconfig(self.button3_id, state='hidden')
            self._canvas.itemconfig(self.button4_id, state='hidden')
            self._canvas.itemconfig(self.button_id, state='hidden')
            self._canvas.itemconfig(self.label2_id, state='hidden')
            self._canvas.itemconfig(self.label3_id, state='hidden')
            self._canvas.itemconfig(self.label4_id, state='hidden')

            if len(frontier) > 0:
                current_cell = frontier.pop()
                if current_cell != (1, 1):
                    rectangle_id = self._canvas.create_rectangle(
                        (26 + (current_cell[1] - 1) * self._cell_width) + space_bw,
                        (26 + (current_cell[0] - 1) * self._cell_width) + space_bw,
                        (26 + current_cell[1] * self._cell_width) - space_bw,
                        (26 + current_cell[0] * self._cell_width) - space_bw,
                        fill='blue', outline='black', width=2
                    )
                    self.rectangle_ids.append(rectangle_id)
                    # Check neighbors in reverse order to prioritize certain directions
                    directions = ['N', 'E', 'S', 'W']
                    for direction in directions:
                        if self.maze_map[current_cell][direction]:
                            if direction == 'N':
                                next_cell = (current_cell[0] - 1, current_cell[1])
                            elif direction == 'E':
                                next_cell = (current_cell[0], current_cell[1] + 1)
                            elif direction == 'S':
                                next_cell = (current_cell[0] + 1, current_cell[1])
                            elif direction == 'W':
                                next_cell = (current_cell[0], current_cell[1] - 1)
                            # explored frontier and path only appended when not visited
                            if next_cell not in visited:
                                '''rectangle_id = self._canvas.create_rectangle(
                                    (26 + (next_cell[1] - 1) * self._cell_width) + space_bw,
                                    (26 + (next_cell[0] - 1) * self._cell_width) + space_bw,
                                    (26 + next_cell[1] * self._cell_width) - space_bw,
                                    (26 + next_cell[0] * self._cell_width) - space_bw,
                                    fill='blue', outline='black', width=1
                                )
                                self.rectangle_ids.append(rectangle_id)'''
                                path[next_cell] = current_cell
                                frontier.append(next_cell)
                                visited.add(next_cell)

                    self._canvas.after(20, lambda: self.DFSAnimation(cell=cell, frontier=frontier, visited=visited,
                                                                     path=path, t1=t1))
                else:
                    self.animate(DFS=True, path=path, t1=t1)

        def BFSAnimation(self, cell=None, frontier=None, visited=None, path=None, t1=None):
            if cell is None:
                cell = (self.rows, self.cols)
            if frontier is None:
                frontier = deque()
                frontier.append(cell)
            if visited is None:
                visited = {(self.rows, self.cols)}
            if path is None:
                path = {}
            if t1 is None:
                t1 = time.time()
            space_bw = self._cell_width / 4.75
            self._canvas.itemconfig(self.label_id, state='hidden')
            self._canvas.itemconfig(self.button3_id, state='hidden')
            self._canvas.itemconfig(self.button4_id, state='hidden')
            self._canvas.itemconfig(self.button_id, state='hidden')
            self._canvas.itemconfig(self.label2_id, state='hidden')
            self._canvas.itemconfig(self.label3_id, state='hidden')
            self._canvas.itemconfig(self.label4_id, state='hidden')



            if len(frontier) > 0:
                cell = frontier.popleft()
                if cell != (1, 1):
                    rectangle_id = self._canvas.create_rectangle(
                        (26 + (cell[1] - 1) * self._cell_width) + space_bw,
                        (26 + (cell[0] - 1) * self._cell_width) + space_bw,
                        (26 + cell[1] * self._cell_width) - space_bw,
                        (26 + cell[0] * self._cell_width) - space_bw,
                        fill='blue', outline='black', width=2
                    )
                    self.rectangle_ids.append(rectangle_id)

                    if self.maze_map[cell]['W'] and (cell[0], cell[1] - 1) not in visited:
                        nextCell = (cell[0], cell[1] - 1)
                        rectangle_id = self._canvas.create_rectangle(
                            (26 + (nextCell[1] - 1) * self._cell_width) + space_bw,
                            (26 + (nextCell[0] - 1) * self._cell_width) + space_bw,
                            (26 + nextCell[1] * self._cell_width) - space_bw,
                            (26 + nextCell[0] * self._cell_width) - space_bw,
                            fill='white', outline='black', width=1
                        )
                        self.rectangle_ids.append(rectangle_id)
                        path[nextCell] = cell
                        frontier.append(nextCell)
                        visited.add(nextCell)
                    if self.maze_map[cell]['S'] and (cell[0] + 1, cell[1]) not in visited:
                        nextCell = (cell[0] + 1, cell[1])
                        rectangle_id = self._canvas.create_rectangle(
                            (26 + (nextCell[1] - 1) * self._cell_width) + space_bw,
                            (26 + (nextCell[0] - 1) * self._cell_width) + space_bw,
                            (26 + nextCell[1] * self._cell_width) - space_bw,
                            (26 + nextCell[0] * self._cell_width) - space_bw,
                            fill='white', outline='black', width=1
                        )
                        self.rectangle_ids.append(rectangle_id)
                        path[nextCell] = cell
                        frontier.append(nextCell)
                        visited.add(nextCell)
                    if self.maze_map[cell]['E'] and (cell[0], cell[1] + 1) not in visited:
                        nextCell = (cell[0], cell[1] + 1)
                        rectangle_id = self._canvas.create_rectangle(
                            (26 + (nextCell[1] - 1) * self._cell_width) + space_bw,
                            (26 + (nextCell[0] - 1) * self._cell_width) + space_bw,
                            (26 + nextCell[1] * self._cell_width) - space_bw,
                            (26 + nextCell[0] * self._cell_width) - space_bw,
                            fill='white', outline='black', width=1
                        )
                        self.rectangle_ids.append(rectangle_id)
                        path[nextCell] = cell
                        frontier.append(nextCell)
                        visited.add(nextCell)
                    if self.maze_map[cell]['N'] and (cell[0] - 1, cell[1]) not in visited:
                        nextCell = (cell[0] - 1, cell[1])
                        rectangle_id = self._canvas.create_rectangle(
                            (26 + (nextCell[1] - 1) * self._cell_width) + space_bw,
                            (26 + (nextCell[0] - 1) * self._cell_width) + space_bw,
                            (26 + nextCell[1] * self._cell_width) - space_bw,
                            (26 + nextCell[0] * self._cell_width) - space_bw,
                            fill='white', outline='black', width=1
                        )
                        self.rectangle_ids.append(rectangle_id)
                        path[nextCell] = cell
                        frontier.append(nextCell)
                        visited.add(nextCell)

                    self._canvas.after(20, lambda: self.BFSAnimation(cell=cell, frontier=frontier, visited=visited,
                                                                     path=path, t1=t1))
                else:
                    self.animate(BFS=True, path=path, t1=t1)


        def aStarSekci(self, path=None, t1=None ,start=None, g_score = None, f_score = None, open = None):
            space_bw = self._cell_width / 4.75
            self._canvas.itemconfig(self.label_id, state='hidden')
            self._canvas.itemconfig(self.button3_id, state='hidden')
            self._canvas.itemconfig(self.button4_id, state='hidden')
            self._canvas.itemconfig(self.button_id, state='hidden')
            self._canvas.itemconfig(self.label2_id, state='hidden')
            self._canvas.itemconfig(self.label3_id, state='hidden')
            self._canvas.itemconfig(self.label4_id, state='hidden')
            if path is None:
                path = {}
            if t1 is None:
                t1 = time.time()
            if start is None:
                start = (self.rows, self.cols)
            if g_score is None:
                g_score = {cell: float('inf') for cell in self.grid}
                g_score[start] = 0
            if f_score is None:
                f_score = {cell: float('inf') for cell in self.grid}
                f_score[start] = abs(start[0]-1)+abs(start[1]-1)
            if open is None:
                open = PriorityQueue()
                open.put((f_score[start], f_score[start], start))

            if not open.empty():
                current_cell = open.get()[2]
                if current_cell != (1, 1):
                    directions = ['N', 'E', 'S', 'W']
                    for direction in directions:
                        if self.maze_map[current_cell][direction]:
                            if direction == 'N':
                                next_cell = (current_cell[0] - 1, current_cell[1])
                            if direction == 'E':
                                next_cell = (current_cell[0], current_cell[1] + 1)
                            if direction == 'S':
                                next_cell = (current_cell[0] + 1, current_cell[1])
                            if direction == 'W':
                                next_cell = (current_cell[0], current_cell[1] - 1)
                            temp_g_score = g_score[current_cell] + 1
                            temp_f_score = temp_g_score + self.h(next_cell, (1, 1))
                            if temp_f_score < f_score[next_cell]:
                                g_score[next_cell] = temp_g_score
                                f_score[next_cell] = temp_f_score
                                open.put((temp_f_score, self.h(next_cell, (1, 1)), next_cell))
                                path[next_cell] = current_cell
                                rectangle_id=self._canvas.create_rectangle(
                                    (26 + (current_cell[1] - 1) * self._cell_width) + space_bw,
                                    (26 + (current_cell[0] - 1) * self._cell_width) + space_bw,
                                    (26 + current_cell[1] * self._cell_width) - space_bw,
                                    (26 + current_cell[0] * self._cell_width) - space_bw,
                                    fill='blue', outline='black', width=2
                                )
                                self.rectangle_ids.append(rectangle_id)
                    self._canvas.after(20, lambda: self.aStarSekci(path=path, t1=t1,start=start,g_score=g_score,f_score=f_score,open=open))
                else:
                    self.animate(AStar=True,path=path,t1=t1)


        def h(self,cell1,cell2):
            x1,y1=cell1
            x2,y2=cell2
            return abs(x1-x2) + abs(y1-y2)

        def animate(self, cell=None, fwdPath=None, BFS=False, DFS=False, path=None, t1=None, AStar=False):
            space_bw = self._cell_width / 4.75
            if cell is None:
                cell = (1, 1)
            if fwdPath is None:
                fwdPath = {}

            if cell == (self.rows, self.cols):
                rectangle_id = self._canvas.create_rectangle(
                    (26 + (cell[1] - 1) * self._cell_width) + space_bw,
                    (26 + (cell[0] - 1) * self._cell_width) + space_bw,
                    (26 + cell[1] * self._cell_width) - space_bw,
                    (26 + cell[0] * self._cell_width) - space_bw,
                    fill='red', outline='black', width=1
                )
                self.rectangle_ids.append(rectangle_id)
                if (BFS == True):
                    t2 = time.time()
                    self.BFStime = t2 - t1
                    label_text = f"Breadth First Search completed. Time taken for completion was {self.BFStime:.2f} s "
                    self.completion_label = tk.Label(
                        self._canvas,
                        text=label_text,
                        font=("Arial", 20),
                        wraplength=500,
                        bg='black',
                        fg='white'
                    )
                    self.completion_label_id = self._canvas.create_window(
                        920, 100, window=self.completion_label, anchor=tk.NW
                    )
                    # Show back button
                    self.back_button = tk.Button(
                        self._canvas,
                        text="Back",
                        font=('Arial', 20),
                        bg="red",
                        fg='white',
                        command=self.clear_canvas
                    )
                    self.back_button_id = self._canvas.create_window(
                        1100, 200, window=self.back_button, anchor=tk.NW
                    )
                if (DFS == True):
                    t2 = time.time()
                    self.DFStime = t2 - t1
                    label_text = f"Depth First Search completed. Time taken for completion was {self.DFStime:.2f} s "
                    self.completion_label = tk.Label(
                        self._canvas,
                        text=label_text,
                        font=("Arial", 20),
                        wraplength=500,
                        bg='black',
                        fg='white'
                    )
                    self.completion_label_id = self._canvas.create_window(
                        920, 100, window=self.completion_label, anchor=tk.NW
                    )
                    # Show back button
                    self.back_button = tk.Button(
                        self._canvas,
                        text="Back",
                        font=('Arial', 16),
                        bg="red",
                        fg='white',
                        command=self.clear_canvas
                    )

                    self.back_button_id = self._canvas.create_window(
                        1100, 200, window=self.back_button, anchor=tk.NW
                    )

                if(AStar==True):
                    t2 = time.time()
                    self.AStarTime = t2 - t1
                    label_text = f"A Star algorithm completed. Time taken for completion was {self.AStarTime:.2f} s "
                    self.completion_label = tk.Label(
                        self._canvas,
                        text=label_text,
                        font=("Arial", 20),
                        wraplength=500,
                        bg='black',
                        fg='white'
                    )
                    self.completion_label_id = self._canvas.create_window(
                        920, 100, window=self.completion_label, anchor=tk.NW
                    )
                    # Show back button
                    self.back_button = tk.Button(
                        self._canvas,
                        text="Back",
                        font=('Arial', 16),
                        bg="red",
                        fg='white',
                        command=self.clear_canvas
                    )

                    self.back_button_id = self._canvas.create_window(
                        1100, 200, window=self.back_button, anchor=tk.NW
                    )

                return

            fwdPath[path[cell]] = cell
            nextCell = path[cell]

            rectangle_id = self._canvas.create_rectangle(
                (26 + (cell[1] - 1) * self._cell_width) + space_bw,
                (26 + (cell[0] - 1) * self._cell_width) + space_bw,
                (26 + cell[1] * self._cell_width) - space_bw,
                (26 + cell[0] * self._cell_width) - space_bw,
                fill='red', outline='black', width=1
            )
            self.rectangle_ids.append(rectangle_id)
            # Schedule the next iteration after 100 milliseconds
            if (BFS == True):
                self._canvas.after(20, lambda: self.animate(cell=nextCell, fwdPath=fwdPath, BFS=True, path=path, t1=t1))
            if (DFS == True):
                self._canvas.after(20, lambda: self.animate(cell=nextCell, fwdPath=fwdPath, DFS=True, path=path, t1=t1))
            if (AStar == True):
                self._canvas.after(20, lambda: self.animate(cell=nextCell, fwdPath=fwdPath, AStar=True, path=path, t1=t1))

        def drawMaze(self):

            cell = (self.rows, self.cols)
            frontier = deque()
            frontier.append(cell)
            self.animation_in_progress = False
            self.completion_label_id = None
            self.back_button_id = None
            self.label2_id = None
            self.label3_id = None
            self.label4_id = None


            def switchin():
                self._canvas.pack_forget()
                self.switcher()

            self._LabWidth = 26  # Space from the top for Labels

            scr_width = 1536
            scr_height = 864
            width_to_include_label = 890
            self._canvas = tk.Canvas(width=scr_width, height=scr_height, bg='black')  # 0,0 is top left corner
            self._canvas.pack(expand=YES, fill=BOTH)
            # Some calculations for calculating the width of the maze cell
            k = 3.25
            if self.rows >= 95 and self.cols >= 95:
                k = 0
            elif self.rows >= 80 and self.cols >= 80:
                k = 1
            elif self.rows >= 70 and self.cols >= 70:
                k = 1.5
            elif self.rows >= 50 and self.cols >= 50:
                k = 2
            elif self.rows >= 35 and self.cols >= 35:
                k = 2.5
            elif self.rows >= 22 and self.cols >= 22:
                k = 3
            self._cell_width = round(min(((scr_height - self.rows - k * self._LabWidth) / (self.rows)),
                                         ((width_to_include_label - self.cols - k * self._LabWidth) / (self.cols)), 90),
                                     3)

            # Creating Maze lines



            if self.grid is not None:
                for cell in self.grid:
                    x, y = cell
                    w = self._cell_width
                    x = x * w - w + self._LabWidth
                    y = y * w - w + self._LabWidth
                    if self.maze_map[cell]['E'] == False:
                        l = self._canvas.create_line(y + w, x, y + w, x + w, width=2, fill='white', tag='line')
                    if self.maze_map[cell]['W'] == False:
                        l = self._canvas.create_line(y, x, y, x + w, width=2, fill='white', tag='line')
                    if self.maze_map[cell]['N'] == False:
                        l = self._canvas.create_line(y, x, y + w, x, width=2, fill='white', tag='line')
                    if self.maze_map[cell]['S'] == False:
                        l = self._canvas.create_line(y, x + w, y + w, x + w, width=2, fill='white', tag='line')

                start_cell = (1, 1)
                self._canvas.create_rectangle(
                    (26 + (start_cell[1] - 1) * self._cell_width),
                    (26 + (start_cell[0] - 1) * self._cell_width),
                    (26 + start_cell[1] * self._cell_width),
                    (26 + start_cell[0] * self._cell_width),
                    fill='yellow', outline='black', width=2
                )
                self._canvas.create_text(
                    (26 + (start_cell[1] - 0.5) * self._cell_width),
                    (26 + (start_cell[0] - 0.5) * self._cell_width),
                    text="End", fill='black'
                )
                start_cell = (self.rows, self.cols)
                self._canvas.create_rectangle(
                    (26 + (start_cell[1] - 1) * self._cell_width),
                    (26 + (start_cell[0] - 1) * self._cell_width),
                    (26 + start_cell[1] * self._cell_width),
                    (26 + start_cell[0] * self._cell_width),
                    fill='green', outline='black', width=2
                )
                self._canvas.create_text(
                    (26 + (start_cell[1] - 0.5) * self._cell_width),
                    (26 + (start_cell[0] - 0.5) * self._cell_width),
                    text="Start", fill='white'
                )

                self.label = tk.Label(self._canvas, text="Which algorithm would you like to solve the maze with",
                                      font=("Arial", 20), wraplength=500, bg='black', fg='white')
                self.label_id = self._canvas.create_window(900, 50, window=self.label, anchor=tk.NW)

                self.button = tk.Button(self._canvas, text="Breadth First Search", font=('Arial', 20), bg="red",
                                        fg='white', command=self.BFSAnimation)
                self.button_id = self._canvas.create_window(1018, 150, window=self.button, anchor=tk.NW)

                self.button2 = tk.Button(self._canvas, text="Back To Home", font=('Arial', 16), bg="gray", fg='white',
                                         command=switchin)
                self.button2_id = self._canvas.create_window(1063, 650, window=self.button2, anchor=tk.NW)

                self.button3 = tk.Button(self._canvas, text="Depth First Search", font=('Arial', 20), bg="red",
                                         fg='white', command=self.DFSAnimation)
                self.button3_id = self._canvas.create_window(1028, 250, window=self.button3, anchor=tk.NW)

                self.button4 = tk.Button(self._canvas, text="A-Star Search  ", font=('Arial', 20), bg="red",
                                       fg='white', command=self.aStarSekci)
                self.button4_id = self._canvas.create_window(1048, 350, window=self.button4, anchor=tk.NW)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Maze Solver')
        scr_width = self.winfo_screenwidth()
        scr_height = self.winfo_screenheight()
        self.geometry(f"{scr_width}x{scr_height}+0+0")

    def startScreen(self):

        # Starting screen components
        self.start_frame = tk.Frame(self)
        self.start_frame.pack(expand=YES, fill=BOTH)
        self.start_frame.configure(bg='#5d08cc')  #3b0680# Replace 'your_desired_color' with the color you want

        fire_emoji = "\U0001F525"
        self.label = tk.Label(self.start_frame, text=f"{fire_emoji} MAZE SOLVER{fire_emoji}", font=("Arial", 50), bg='#5d08cc',
                              fg='#ffffff')
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.label_rows = tk.Label(self.start_frame, text='Enter Rows:', font=('Arial', 16, 'bold'), bg='#5d08cc', fg='#2e2328')
        self.label_rows.place(relx=0.4, rely=0.5, anchor='center', y=-60)

        self.entry_rows = tk.Entry(self.start_frame, width=20, font=('Arial', 14), justify="center", bg='#8932fa', fg='#2e2328', borderwidth=0, highlightthickness=0)
        self.entry_rows.place(relx=0.57, rely=0.46, anchor='center', y=-30)

        self.label_cols = tk.Label(self.start_frame, text='Enter Columns:', font=('Arial', 16, 'bold'), bg='#5d08cc', fg='#2e2328')
        self.label_cols.place(relx=0.4, rely=0.54, anchor='center', y=0)

        self.entry_cols = tk.Entry(self.start_frame, width=20, font=('Arial', 14, 'normal'), justify="center", bg='#8932fa', fg='#2e2328', borderwidth=0, highlightthickness=0)
        self.entry_cols.place(relx=0.57, rely=0.5, anchor='center', y=30)

        self.generate_button = tk.Button(self.start_frame, text='Generate Maze', font=('Arial', 12, 'bold'), command=self.generate_maze, borderwidth=0, highlightthickness=0, bg='#8932fa', fg='#2e2328')
        self.generate_button.place(relx=0.5, rely=0.57, anchor='center', y=60)

        self.maze_frame = tk.Frame(self)

        self.maze_canvas = tk.Canvas(self.maze_frame, bg='black')
        self.maze_canvas.pack(expand=YES, fill=BOTH)

        self.maze = None

    def changeScreen(self):
        self.start_frame.pack(expand=YES, fill=BOTH)

    def generate_maze(self):
        try:
            rows = int(self.entry_rows.get())
            cols = int(self.entry_cols.get())

            if self.maze:
                self.maze_frame.pack_forget()

            self.start_frame.pack_forget()

            self.maze = self.Maze(rows=rows, cols=cols, canvas=self.maze_canvas, switcher=self.changeScreen)
            self.maze.CreateMaze()
            self.maze.drawMaze()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers for rows and columns.")


if __name__ == "__main__":
    app = MazeApp()
    app.startScreen()
    app.mainloop()
