import tkinter as tk
from tkinter import messagebox

class cell:
    def __init__(self,x,y ,color) -> None:
        self.color = color
        self.x = x
        self.y = y

    def __str__(self) -> str:
        if self.color =="red" :
            return "🟥"
        elif self.color =="purple" :
            return "🟪"
        elif self.color =="gray" :
            return "⬛"
        elif self.color =="white" :
            return "⚪"
        else:
            return "⬜" 
    

class State : 
    def __init__(self, rows,cols,grid) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = grid

    def __str__(self) -> str:
        result = ""
        for row in self.grid :
            for cell in row :
                result += str(cell)
            result += '\n'
        return result
    
class Play:
    def __init__(self,init_state,whites) -> None:
        self.state = init_state
        self.whites = whites
        self.selected_magnet = None

    
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
        #print(self.whites)
        magnet = self.state.grid[start_x][start_y]
        self.state.grid[target_x][target_y] = magnet
        
        self.state.grid[start_x][start_y] = cell(start_x, start_y, "white" if self.is_white(start_x,start_y)  else "")
        #print(start_x,start_y )
        if self.state.grid[target_x][target_y].color=="purple":
            self.purpple_magnet(target_x,target_y)
        elif self.state.grid[target_x][target_y].color=="red":
            self.red_magnet(target_x,target_y)

        # هون بحال بعد تحرك القطع الحديدية صارت قريبة من مغناطيس ثاني نضمن تأثرها فيه    
        # for x in range(self.state.rows):
        #     for y in range(self.state.cols):
        #         Cell = self.state.grid[x][y]
        #         if Cell.color == "red" and Cell != self.state.grid[start_x][start_y]:
        #             self.red_magnet(x,y)
        #         elif Cell.color == "purple" and Cell != self.state.grid[start_x][start_y]:
        #            self.purpple_magnet(x,y)
        return True    
    

    
    def is_white (self,x,y):
        return (x,y) in self.whites

    
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
            print (" yaaaaa you win")
            return True 

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
                       messagebox.showerror("you win")     
                else:
                    messagebox.showerror("error")
            else:
                if self.state.grid[x][y].color in ["red", "purple"]:
                    self.selected_magnet = (x, y)
                    

        
        for i in range(self.state.rows):
            for j in range(self.state.cols):
                label = tk.Label(root, width=8, height=4, relief="solid")
                label.grid(row=i, column=j)
                label.bind("<Button-1>", lambda e, x=i, y=j: cell_clicked(x, y))
                cells[i][j] = label

        refresh_grid()
        root.mainloop()
        
def main(): 
    init_grid= [["🟪","⬜","⬛","⬜","⬜"],
                ["⬜","⬜","⚪","⬜","⬜"],
                ["⚪","⬜","⬜","⚪","⬛"],
                ["⬜","⬜","⚪","⬜","⬜"],
                ["🟥","⬜","⬛","⬜","⬜"],]

    rows = len(init_grid)
    cols = len(init_grid[0])
    whites = []

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range (rows):
        for j in range (cols):
            if init_grid[i][j] == "🟥":
                cell_color = "red"
            elif init_grid[i][j] == "🟪":
                cell_color = "purple"
            elif init_grid[i][j] == "⬛":
                cell_color = "gray"    
            elif init_grid[i][j] == "⚪":
                cell_color = "white"
                whites.append((i,j))
            else:
                cell_color = ""
        
            grid[i][j] = cell(i,j,cell_color)

    new_state = State(rows,cols,grid)
    play = Play(new_state,whites)
    #print(whites)
    mode = input("choose (console/gui): ").strip().lower()
    if mode == "console":
       play.play_console()
    elif mode == "gui":
         play.play_gui()

if __name__ == "__main__":
    main()