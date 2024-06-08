import random

class Grid:
    def __init__(self, rows, cols, n_exits, n_fires, n_civilians, n_frs, t_zr, t_fr, t_v):
        self.rows = rows
        self.cols = cols
        self.n_exits = n_exits
        self.n_fires = n_fires
        self.n_civilians = n_civilians
        self.n_frs = n_frs
        self.t_zr = t_zr
        self.t_fr = t_fr
        self.t_v = t_v
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.__fill_random_cells__(n_fires, 2)
        self.__fill_random_cells_border__(n_exits, 1)
        self.__fill_random_cells__(n_civilians, 3)
        self.__fill_random_cells__(n_frs, 4) 
        
    def __fill_random_cells__(self, count, value):
        if count > self.rows * self.cols:
            raise ValueError("Count exceeds the number of cells in the grid")
        
        all_positions = [(row, col) for row in range(self.rows) for col in range(self.cols)]
        random_positions = random.sample(all_positions, count)
        
        for row, col in random_positions:
            self.set_value(row, col, value)
            
    def __fill_random_cells_border__(self, count, value):
        if count > self.rows * self.cols:
            raise ValueError("Count exceeds the number of cells in the grid")
        
        border_positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if (i == 0 or i ==self.rows-1 or j == 0 or j == self.cols-1):
                    border_positions.append((i, j))
            
        random_positions = random.sample(border_positions, count)
        
        for row, col in random_positions:
            self.set_value(row, col, value)

    def set_value(self, row, col, value):
        self.grid[row][col] = value
    
    def display(self):
        for row in self.grid:
            print(" ".join(map(str, row)))

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.grid)
    
    def gridDeclaration(self):
        grid_str = "{\n"
        last_row_index = len(self.grid) - 1
        for index, row in enumerate(self.grid):
            if index != last_row_index:
                grid_str += "  {" + ", ".join(map(str, row)) + "},\n"
            else:
                grid_str += "  {" + ", ".join(map(str, row)) + "}\n"
        grid_str += "}"
        return grid_str
    
    def generateDeclarations(self):
        prefix = "const int "
        declarations = prefix + "GRID_LENGTH = " + str(self.rows) + ";\n"
        declarations += prefix + "GRID_WIDTH = " + str(self.cols) + ";\n"
        declarations += prefix + "N_EXITS = " + str(self.n_exits) + ";\n"
        declarations += prefix + "N_FIRES = " + str(self.n_fires) + ";\n"
        declarations += prefix + "N_CIVILIANS = " + str(self.n_civilians) + ";\n"
        declarations += prefix + "N_FIRST_RESPONDERS = " + str(self.n_frs) + ";\n"
        declarations += prefix + "T_ZR = " + str(self.t_zr) + ";\n"
        declarations += prefix + "T_FR = " + str(self.t_fr) + ";\n"
        declarations += prefix + "T_V = " + str(self.t_v) + ";\n"
        declarations += "int grid[GRID_LENGTH][GRID_WIDTH] = " + self.gridDeclaration() + "\n"
        print(declarations)
        

grid = Grid(30, 20, 10, 30, 6, 5, 6, 7, 8)
grid.display()
grid.generateDeclarations()