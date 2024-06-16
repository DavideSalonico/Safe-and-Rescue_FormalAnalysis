import math
import random


class Grid:
    def __init__(self, rows, cols, n_exits, n_fires, n_civilians, n_frs, t_zr, t_fr, t_v, n_drones, n_v):
        self.rows = rows
        self.cols = cols
        self.n_exits = n_exits
        self.n_fires = n_fires
        self.n_civilians = n_civilians
        self.n_frs = n_frs
        self.t_zr = t_zr
        self.t_fr = t_fr
        self.t_v = t_v
        self.n_drones = n_drones
        self.n_v = n_v
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        #self.__fill_random_cells__(n_fires, 2)
        self.__fill_random_cells_cluster__(n_fires, 2)
        self.__fill_random_cells_border__(n_exits, 1)
        self.__fill_random_cells__(n_civilians, 3)
        self.__fill_random_cells__(n_frs, 4)
        self.trajectories = self.__build_drone_trajectories__()
        self.traj_lengths = [len(traj) for traj in self.trajectories]
        self.max_traj = max(self.traj_lengths)
        
    def get_value(self, row, col):
        return self.grid[row][col]
            
    def __fill_random_cells__(self, count, value):
        if count > self.rows * self.cols:
            raise ValueError("Count exceeds the number of cells in the grid")
        
        all_positions = [(row, col) for row in range(self.rows) for col in range(self.cols)]
        random_positions = random.sample(all_positions, count)
        
        for row, col in random_positions:
            self.set_value(row, col, value)
            
    def __fill_random_cells_cluster__(self, count, value):
        tmp_fires = 0
        # Calculate the dimensions of each cluster based on the given percentage
        cluster_rows = max(1, int(self.rows * 0.2))
        cluster_cols = max(1, int(self.cols * 0.2))

        # Calculate the number of clusters needed to cover the grid
        n_clusters_row = self.rows // cluster_rows + (1 if self.rows % cluster_rows > 0 else 0)
        n_clusters_col = self.cols // cluster_cols + (1 if self.cols % cluster_cols > 0 else 0)

        # Ensure count does not exceed the total number of cells
        if count > self.rows * self.cols:
            raise ValueError("Count exceeds the number of cells in the grid")
        
        # Calculate the total number of clusters
        total_clusters = n_clusters_row * n_clusters_col

        # Determine the number of clusters to fill based on the fill_cluster_percentage
        clusters_to_fill = math.ceil(count / (cluster_rows * cluster_cols))
        print("Clusters to fill: " + str(clusters_to_fill))

        # Randomly select clusters to fill
        all_clusters = [(r, c) for r in range(n_clusters_row) for c in range(n_clusters_col)]
        selected_clusters = random.sample(all_clusters, clusters_to_fill)

        # Fill cells in the selected clusters
        for cluster_row, cluster_col in selected_clusters:
            # Calculate the start and end positions of the current cluster
            start_row = cluster_row * cluster_rows
            end_row = min((cluster_row + 1) * cluster_rows, self.rows)
            start_col = cluster_col * cluster_cols
            end_col = min((cluster_col + 1) * cluster_cols, self.cols)

            # Generate all positions within the current cluster
            cluster_positions = [(row, col) for row in range(start_row, end_row) for col in range(start_col, end_col)]

            # Fill the selected positions with the given value
            for row, col in cluster_positions:
                self.set_value(row, col, value)
                tmp_fires += 1
              
        assert tmp_fires >= count
        
        cells_with_value_2 = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.get_value(row, col) == 2:  # Assuming get_value is a method to get the value of a cell
                    cells_with_value_2.append((row, col))
                          
        cells_to_restore = random.sample(cells_with_value_2, tmp_fires - count)
        for row, col in cells_to_restore:
            self.set_value(row, col, 0)

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
            
    def __build_drone_trajectories__(self):
        trajectories = []
        for i in range(self.n_drones):
            print("Calculating trajectory for drone " + str(i))
            drone_trajectory = []
            for c in range(self.cols):
                drone_trajectory.append((i * self.rows // self.n_drones, c))
                print(drone_trajectory)
            trajectories.append(drone_trajectory)
        return trajectories
    
    def dist(self, src, dst):
        return abs(src[0] - dst[0]) + abs(src[1] - dst[1])
            

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
    
    def droneDeclaration(self):
        drone_str = "{\n"
        last_drone_index = len(self.trajectories) - 1
        for index, drone_trajectory in enumerate(self.trajectories):
            # Ensure all trajectories are of length self.max_traj
            adjusted_trajectory = drone_trajectory + [("OUT_OF_MAP",)] * (self.max_traj - self.traj_lengths[index])
            
            # Convert each position in the trajectory to string, handling OUT_OF_MAP separately
            adjusted_trajectory_str = []
            for position in adjusted_trajectory:
                if position == ("OUT_OF_MAP",):
                    adjusted_trajectory_str.append("OUT_OF_MAP")
                else:
                    adjusted_trajectory_str.append("{" + ", ".join(map(str, position)) + "}")
            
            # Join the trajectory into a string
            if index != last_drone_index:
                drone_str += "  {" + ", ".join(adjusted_trajectory_str) + "},\n"
            else:
                drone_str += "  {" + ", ".join(adjusted_trajectory_str) + "}\n"
        drone_str += "}"
        return drone_str
    
    def displayDrones(self):
        for drone_trajectory in self.trajectories:
            print(" ".join(map(str, drone_trajectory)))
    
    def generateDeclarations(self):
        prefix = "const int "
        declarations = "typedef struct { int r; int c; } pos_t;\n"
        declarations += prefix + "GRID_LENGTH = " + str(self.rows) + ";\n"
        declarations += prefix + "GRID_HEIGHT = " + str(self.cols) + ";\n"
        declarations += prefix + "N_EXITS = " + str(self.n_exits) + ";\n"
        declarations += prefix + "N_FIRES = " + str(self.n_fires) + ";\n"
        declarations += prefix + "N_CIVILIANS = " + str(self.n_civilians) + ";\n"
        declarations += prefix + "N_FIRST_RESPONDERS = " + str(self.n_frs) + ";\n"
        declarations += prefix + "N_DRONES = " + str(self.n_drones) + ";\n"
        declarations += prefix + "T_ZR = " + str(self.t_zr) + ";" + "                      // Time that a Zero Responder needs to help someone\n"
        declarations += prefix + "T_FR = " + str(self.t_fr) + ";" + "                      // Time that a First Responder needs to help someone\n"
        declarations += prefix + "T_V = " + str(self.t_v) + ";" + "                       // Time before a civilian is supposed to die\n"
        declarations += prefix + "N_V = " + str(self.n_v) + ";" + "                       // Drones' visibility range\n"
        declarations += prefix + "MAX_TRAJ = " + str(self.max_traj) + ";" + "                   // Max trajectory length\n"
        declarations += "\n// Grid layout\n\n"
        declarations += "const pos_t OUT_OF_MAP = { -1, -1 };\n"
        declarations += "int grid[GRID_LENGTH][GRID_WIDTH] = " + self.gridDeclaration() + "\n"
        declarations += "\n// Global arrays\n\n"
        declarations += "int drone_trajectories[N_DRONES][MAX_TRAJ] = " + self.droneDeclaration() + "\n"
        declarations += "int drone_traj_lengths[N_DRONES] = {" + ", ".join(map(str, self.traj_lengths)) + "};\n"
        print(declarations)
        

grid = Grid(rows=30, cols=20, n_exits=10, n_fires=30, n_civilians=6, n_frs=5, t_zr=6, t_fr=7, t_v=8, n_drones=3, n_v=2)
#grid.display()
#grid.displayDrones()
grid.generateDeclarations()

"""
    def __fill_cluster_cells__(self, count, value, cluster_size=3):
        if count > self.rows * self.cols:
            raise ValueError("Count exceeds the number of cells in the grid")
        
        # Calculate the number of clusters along rows and columns
        clusters_rows = (self.rows + cluster_size - 1) // cluster_size
        clusters_cols = (self.cols + cluster_size - 1) // cluster_size
        
        # Create a list of all clusters
        all_clusters = [(cluster_row, cluster_col) for cluster_row in range(clusters_rows) for cluster_col in range(clusters_cols)]
        
        # Determine the number of clusters to select based on the count and cluster size
        clusters_to_select = min(len(all_clusters), max(1, count // (cluster_size**2)))
        
        # Randomly select clusters
        selected_clusters = random.sample(all_clusters, clusters_to_select)
        
        for cluster_row, cluster_col in selected_clusters:
            # Calculate the actual number of rows and cols in the cluster (for edge cases)
            actual_cluster_rows = min(cluster_size, self.rows - cluster_row * cluster_size)
            actual_cluster_cols = min(cluster_size, self.cols - cluster_col * cluster_size)
            
        # Calculate the number of cells to fill in each selected cluster
        cells_to_fill_per_cluster = min(actual_cluster_rows * actual_cluster_cols, max(1, count // clusters_to_select))
        
        # Generate all positions within the cluster
        cluster_positions = [(cluster_row * cluster_size + row_offset, cluster_col * cluster_size + col_offset) 
                             for row_offset in range(actual_cluster_rows) 
                             for col_offset in range(actual_cluster_cols)]
        
        # Randomly select positions within the cluster to fill
        selected_positions = random.sample(cluster_positions, cells_to_fill_per_cluster)
        
        for row, col in selected_positions:
            self.set_value(row, col, value)
    """
    
    #TODO: Implement a function to fill cells in clusters
    #      - Take a percentage of total cells
    #      - Take a fraction of the dimemsions