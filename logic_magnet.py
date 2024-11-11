import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
from collections import deque

class cell:
    def __init__(self, x, y, color) -> None:
        self.color = color
        self.x = x
        self.y = y

    def __str__(self) -> str:
        if self.color == "red":
            return "🟥"
        elif self.color == "purple":
            return "🟪"
        elif self.color == "gray":
            return "⬛"
        elif self.color == "white":
            return "⚪"
        else:
            return "⬜"

class State:
    def __init__(self, rows, cols, grid) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = grid

    def __str__(self) -> str:
        result = ""
        for row in self.grid:
            for cell in row:
                result += str(cell)
            result += '\n'
        return result

class Play:
    def __init__(self, init_state, whites) -> None:
        self.state = init_state
        self.whites = whites
        self.selected_magnet = None
        self.visited_states = set() 

    def state_key(self):
        return str(self.state)

    def in_grid(self, rowss, colss):
        return 0 <= rowss < self.state.rows and 0 <= colss < self.state.cols

    def can_move(self, x, y):
        if not self.in_grid(x, y):
            return False
        target_cell = self.state.grid[x][y]
        return target_cell.color in ["", "white"]

    def move_magnet(self, start_x, start_y, target_x, target_y):
        if not self.can_move(target_x, target_y):
            print("this wrong")
            return False
        magnet = self.state.grid[start_x][start_y]
        self.state.grid[target_x][target_y] = magnet
        self.state.grid[start_x][start_y] = cell(start_x, start_y, "white" if self.is_white(start_x, start_y) else "")

        if self.state.grid[target_x][target_y].color == "purple":
            self.purpple_magnet(target_x, target_y)
        elif self.state.grid[target_x][target_y].color == "red":
            self.red_magnet(target_x, target_y)

        return True

    def is_white(self, x, y):
        return (x, y) in self.whites

    def red_magnet(self, x, y):
        for rows in range(self.state.rows):
            if rows != x and self.state.grid[rows][y].color in ["gray", "red", "purple"]:
                target_x = rows + 1 if rows < x else rows - 1
                if self.in_grid(target_x, y) and self.state.grid[target_x][y].color in ["", "white"]:
                    self.state.grid[target_x][y] = self.state.grid[rows][y]
                    self.state.grid[rows][y] = cell(rows, y, "white" if self.is_white(rows, y) else "")

        for cols in range(self.state.cols):
            if cols != y and self.state.grid[x][cols].color in ["gray", "red", "purple"]:
                target_y = cols + 1 if cols < y else cols - 1
                if self.in_grid(x, target_y) and self.state.grid[x][target_y].color in ["", "white"]:
                    self.state.grid[x][target_y] = self.state.grid[x][cols]
                    self.state.grid[x][cols] = cell(x, cols, "white" if self.is_white(x, cols) else "")

    def purpple_magnet(self, x, y):
        for rows in range(self.state.rows):
            if rows != x and self.state.grid[rows][y].color in ["gray", "red", "purple"]:
                target_x = rows - 1 if rows < x else rows + 1
                if self.in_grid(target_x, y) and self.state.grid[target_x][y].color in ["", "white"]:
                    self.state.grid[target_x][y] = self.state.grid[rows][y]
                    self.state.grid[rows][y] = cell(rows, y, "white" if self.is_white(rows, y) else "")

        for cols in range(self.state.cols):
            if cols != y and self.state.grid[x][cols].color in ["gray", "red", "purple"]:
                target_y = cols - 1 if cols < y else cols + 1
                if self.in_grid(x, target_y) and self.state.grid[x][target_y].color in ["", "white"]:
                    self.state.grid[x][target_y] = self.state.grid[x][cols]
                    self.state.grid[x][cols] = cell(x, cols, "white" if self.is_white(x, cols) else "")

    def Solved(self):
        for x in range(self.state.rows):
            for y in range(self.state.cols):
                cell = self.state.grid[x][y]
                if cell.color == "white":
                    return False
        else:
            print("yaaaaa you win")
            return True

    def dfs(self):
        stack = [(self.state, [], set())]

        while stack:
            current_state, path, visited = stack.pop()
            self.state = current_state  

            if self.Solved():  
                print("Solution path:")
                for move in path:
                    print(f"Move magnet from ({move[0]}, {move[1]}) to ({move[2]}, {move[3]})")
                    print(self.state) 
                return path  

            for x in range(self.state.rows):
                for y in range(self.state.cols):
                    if self.state.grid[x][y].color in ["red", "purple"]:  
                        for target_x in range(self.state.rows):
                            for target_y in range(self.state.cols):
                                if self.can_move(target_x, target_y):  
                                    new_state = self.copy_state()  
                                    self.move_magnet(x, y, target_x, target_y)

                                    new_path = path + [(x, y, target_x, target_y)]
                                    state_str = str(self.state)
                                    if state_str not in visited:  
                                        visited.add(state_str)
                                        stack.append((self.copy_state(), new_path, visited.copy()))  
                                    self.state = new_state  

        print("No solution found.")
        return None
    

       
    def get_free_moves(self, x, y):
        moves = []
        for i in range(self.state.rows):
            for j in range(self.state.cols):
                if self.state.grid[i][j].color == "white" or self.state.grid[i][j].color == "":
                    moves.append((i, j))
        return moves
    


    def bfs_solve(self):
        queue = deque([(deepcopy(self.state), [])])
        self.visited_states.add(self.state_key())

        while queue:
            current_state, path = queue.popleft()
            self.state = current_state
            if self.Solved():
                return path

            for x in range(self.state.rows):
                for y in range(self.state.cols):
                    cell = current_state.grid[x][y]
                    if cell.color in ["red", "purple"]:
                        possible_moves = self.get_free_moves(x, y)
                        
                        for target_x, target_y in possible_moves:
                            new_state = deepcopy(current_state)
                            new_play = Play(new_state, self.whites)
                            if new_play.move_magnet(x, y, target_x, target_y):
                                new_state_key = new_play.state_key()
                                if new_state_key not in self.visited_states:
                                    self.visited_states.add(new_state_key)
                                    queue.append((new_play.state, path + [(x, y, target_x, target_y)]))
        return None
    


    def copy_state(self):
        new_grid = [[cell(c.x, c.y, c.color) for c in row] for row in self.state.grid]
        return State(self.state.rows, self.state.cols, new_grid)
    

    def play_dfs(self):
        self.dfs()  


    def play_bfs(self):
        solution_path = self.bfs_solve()
        if solution_path:
            print("Solution found:")
            for move in solution_path:
                print(f"Move magnet from ({move[0]}, {move[1]}) to ({move[2]}, {move[3]})")
        else:
            print("No solution found.")



    def play_console(self):
        while True: 
            print("Current Board State:")
            print(self.state)
            start_x, start_y = map(int, input("input (x y) for magnet: ").split())
            target_x, target_y = map(int, input("input(x y) to move: ").split())
            self.move_magnet(start_x, start_y, target_x, target_y)
            if self.Solved() :
                print(self.state)
                break



    def play_gui(self):
        root = tk.Tk()
        root.title("logic magnet")
        cells = [[None for _ in range(self.state.cols)] for _ in range(self.state.rows)]

        def refresh_grid():
            for i in range(self.state.rows):
                for j in range(self.state.cols):
                    cell = self.state.grid[i][j]
                    color = cell.color
                    if color == "red":
                        cells[i][j].config(bg="red")
                    elif color == "purple":
                        cells[i][j].config(bg="purple")
                    elif color == "gray":
                        cells[i][j].config(bg="black")
                    elif color == "white":
                        cells[i][j].config(bg="white")
                    else:
                        cells[i][j].config(bg="gray")

        def cell_clicked(x, y):
            if self.selected_magnet:
                start_x, start_y = self.selected_magnet
                if self.move_magnet(start_x, start_y, x, y):
                    self.selected_magnet = None
                    refresh_grid() 
                    if self.Solved():
                        messagebox.showinfo("Congratulations", "You win!")
                else:
                    messagebox.showerror("Error", "Invalid move")
            else:
                if self.state.grid[x][y].color in ["red", "purple"]:
                    self.selected_magnet = (x, y)

        for i in range(self.state.rows):
            for j in range(self.state.cols):
                cells[i][j] = tk.Button(root, width=4, height=2, command=lambda i=i, j=j: cell_clicked(i, j))
                cells[i][j].grid(row=i, column=j)

        refresh_grid() 
        root.mainloop()


def main():
    # init_grid = [
    #     ["⬜", "⬜", "⬜"],
    #     ["⚪", "⬛", "⚪"],
    #     ["🟪", "⬜", "⬜"],
    # ]

    init_grid = [
        ["⬛", "⬜", "⬛", "⬜", "⬜"],
        ["⬜", "⬜", "⚪", "⬜", "⬜"],
        ["⚪", "⬜", "⬜", "⚪", "⬛"],
        ["⬜", "⬜", "⚪", "⬜", "⬜"],
        ["🟥", "⬜", "⬛", "⬜", "⬜"],
    ]

    rows = len(init_grid)
    cols = len(init_grid[0])
    whites = []

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            if init_grid[i][j] == "🟥":
                cell_color = "red"
            elif init_grid[i][j] == "🟪":
                cell_color = "purple"
            elif init_grid[i][j] == "⬛":
                cell_color = "gray"    
            elif init_grid[i][j] == "⚪":
                cell_color = "white"
                whites.append((i, j))
            else:
                cell_color = ""
            grid[i][j] = cell(i, j, cell_color)

    new_state = State(rows, cols, grid)
    play = Play(new_state, whites)

    mode = input("Choose mode (console/gui/dfs/bfs): ").strip().lower()
    if mode == "console":
       play.play_console()
    elif mode == "gui":
        play.play_gui()
    elif mode == "dfs":
        play.play_dfs()
    elif mode == "bfs":
        play.play_bfs()
    

if __name__ == "__main__":
    main()
