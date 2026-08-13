import random

# minesweeper script variables
board_size = 16
amount_of_mines = 40

# change this to True if you want to see the underlying board printed alongside the player's visible board
debug_mode = False

is_first_turn = True


class Cell: # holds information for every cell on the board

    def __init__ (self):
        self.is_mine = False # self explanatory vv
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

class Board: # holds the array of cells and the functions that work on those cells

    def __init__(self, array): # should call make_array() as input -> done in board_setup()
        self.cells = array
        self.size = len(self.cells) # i think this is used like once but i'm not gonna delete it

    def game_is_won(self) -> bool: # returns a bool value whether or not all the non mine cells have been revealed
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
     
    def get_neighbors(self, cell: Cell): # takes in cell and returns the neighbor cells (cell objects)
        x = cell.coordinate 
        size = self.size
        neighbors = []
        new_row_add = x[0] + 1
        new_row_sub = x[0] - 1
        new_col_add = x[1] + 1
        new_col_sub = x[1] - 1

        row_below = new_row_add != size
        row_above = new_row_sub >= 0
        col_right = new_col_add != size
        col_left = new_col_sub >= 0

        # + shaped neighbors
        if col_right:
            neighbors.append(self.cells[x[0]][new_col_add])
        if col_left:
            neighbors.append(self.cells[x[0]][new_col_sub])
        if row_above:
            neighbors.append(self.cells[new_row_sub][x[1]])
        if row_below:
            neighbors.append(self.cells[new_row_add][x[1]])

        # x shaped neighbors

        if row_below:
            if col_left:
                neighbors.append(self.cells[new_row_add][new_col_sub])
            if col_right:
                neighbors.append(self.cells[new_row_add][new_col_add])
        if row_above:
            if col_left:
                neighbors.append(self.cells[new_row_sub][new_col_sub])
            if col_right:
                neighbors.append(self.cells[new_row_sub][new_col_add])
        return neighbors
    
    def reveal_neighbors(self, cell): # takes in a cell and recursively reveals itself and all of it's neighbors, changing state function
        if cell.neighbor_mines != 0:
            return

        for n in self.get_neighbors(cell):
            if n.is_flagged or n.is_revealed:
                continue
            n.is_revealed = True
            if n.neighbor_mines == 0:
                self.reveal_neighbors(n)

    def reveal_cell(self, cell): # takes in a cell and checks if it can be revealed, then attempts to reveal it, returns true if a mine was hit, false if it wasnt
        if cell.is_revealed:
            print("Cell is already revealed.") # DEBUG
            return False
        if cell.is_flagged:
            print("Cell is flagged and cannot be revealed.") # DEBUG
            return False
        if cell.is_mine:
            print("Player hit a mine.") # DEBUG
            return True
        cell.is_revealed = True
        if cell.neighbor_mines == 0:
            self.reveal_neighbors(cell)
        return False
        
    def toggle_flagged(self, cell): # checks if a cell is revealed and toggles is_flagged if it isn't
        if not cell.is_revealed: # if cell is revealed
            cell.is_flagged = not cell.is_flagged # toggles it
      
    def add_mines(self, mine_n: int, first_clicked): # changes mine_n amount of cells to mines in self.cells, also makes sure first_clicked and it's neighbors aren't included (for guaranteed safe first turn)
        mines_placed = 0
        while mines_placed < mine_n:
            row = random.choice(self.cells)
            col = random.choice(row)
            if col in first_clicked:
                continue
            if not col.is_mine:
                col.is_mine = True
                mines_placed += 1

    def add_neighbors(self): # increases int neighbor_mines to cells based on amount of mines in it's neighbors
        cells = self.cells
        for row in cells:
            for item in row:
                if item.is_mine:
                    n = self.get_neighbors(item)
                    for b in n:
                        b.neighbor_mines += 1
    
    def print_player_board(self): #prints board that the player will see (revealed cells only)
        player_board = []
        for item in self.cells:
            curr = []
            for n in item:
                if n.is_flagged:
                    curr.append("!") #placeholder 
                elif not n.is_revealed:
                    curr.append("-")
                else:
                    curr.append(f"{n.neighbor_mines}")
            player_board.append(curr)
            # spacer + column numbers
        print("   ", end="")
        for i in range(1, len(self.cells) + 1):
            print(f"{i:2}", end=" ")
        print()

        # row numbers + the actual board
        for i, row in enumerate(player_board, 1):
            print(f"{i:2}", end=" ")
            for cell in row:
                print(f"{cell:2}", end=" ")
            print()

    def print_debug_board(self): #prints a board with all the locations and values shown
        real_board = []
        for item in self.cells:
            curr = []
            for n in item:
                if n.is_mine:
                    curr.append("*")
                    continue
                if n.is_flagged:
                    curr.append("_")
                if n.neighbor_mines == 0:
                    curr.append("-")
                else:
                    curr.append(f"{n.neighbor_mines}")
            real_board.append(curr)
        for row in real_board:
            print(*row)

def make_array(n: int): # creates and array of cells and defines their coordinates
    array = []
    for row in range(n):
        current_row = []
        for col in range(n):
            c = Cell()
            c.coordinate = (row, col)
            current_row.append(c)
        array.append(current_row)
    return array

def board_setup(size): # unnecessary but nice for readability, takes in the size and mines and returns a board with those specs (calls make_array)
    c = Board(make_array(size))
    return c

# setup first board so game loop works
curr_board = board_setup(board_size) # makes an initial board

# game loop
while True:

        if debug_mode == True:
            curr_board.print_debug_board() 

        print("· · ─────────────── ꒰ঌ·✦·໒꒱ ─────────────── · ·") # visual divider cus it's hard to read
        curr_board.print_player_board() 
        if curr_board.game_is_won():
            print("You won!")
            curr_board = board_setup(board_size) # makes a new random board
            is_first_turn = True # resets first turn
            input("Play again?: ") # doesn't matter what they put, you WILL play again.
            continue


        # asks for a cell until one has been picked
        while True:
            
            # row select with checks to make sure it's valid
            r = (input(f"Enter row 1-{len(curr_board.cells)}: "))

            try:
                r = int(r)
            except ValueError:
                print("Please make a valid numerical input.")
                continue
            if r > 16 or r < 1:
                print(f"Please select a number between 1-{len(curr_board.cells)}!")
                continue
            
            # col select with checks to make sure it's valid
            c = (input(f"Enter column 1-{len(curr_board.cells)}: "))
            try:
                c = int(c)
            except ValueError:
                print("Please make a valid numerical input.")
                continue
            if c > 16 or c < 1:
                print(f"Please select a number between 1-{len(curr_board.cells)}!")
                continue
            
            
            cell = curr_board.cells[r-1][c-1] # -1 to account for python indexing at 0
            break

        # if it's the first turn, generate the mines and place neighbor counts on the board
        if is_first_turn:            
            
            # get list of safe blocks
            first_turn_neighbors = curr_board.get_neighbors(cell) # get neighbors
            first_turn_neighbors.append(cell) # add the cell itself

            # generate with those safe blocks in mind
            curr_board.add_mines(amount_of_mines, first_turn_neighbors)
            curr_board.add_neighbors() 

            # reveal that first choice
            b = curr_board.reveal_cell(cell) # <- remember that this returns a bool of whether or not a mine was hit (see reveal_cell)
            is_first_turn = False 

        # game loop if it's not the first turn
        else:
            # checks that make sure that the second input is valid
            while True:
                b = False # need or check later breaks
                choice = input("Type R to Reveal, F to Flag, or X to Cancel: ")
                if choice == "R" or choice == "r":
                    b = curr_board.reveal_cell(cell) 
                    break
                elif choice == "F" or choice == "f":
                    curr_board.toggle_flagged(cell)
                    break
                elif choice == "X" or choice == "x":
                    break
                else:
                    print("Please make a valid input.")

        # if b is false, just reset and ask for another input

        if b: # b holds the value of the previous input (True means mine)
            curr_board.print_debug_board()
            print("Game Over.")
            curr_board = board_setup(board_size)
            is_first_turn = True
            input("Play again?: ") # doesn't matter you WILL PLAY AGAIN!!!
            continue