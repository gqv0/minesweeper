#import pygame as pg
import random

#hardcoded cus idgaf
board_size = 16
amount_of_mines = 30



class Cell:

    def __init__ (self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.coordinate = ()

class Board:

    def __init__(self, array): # should call make_array() as input -> done in board_setup()
        self.cells = array
        self.size = len(self.cells)

    
    def game_is_won(self) -> bool: # check that we will use for game loop later
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
     
    def get_neighbors(self, cell: Cell): # gets neighbors of specific cell in array
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
    
    def reveal_neighbors(self, cell): # only called from reveal_cell()
        if cell.neighbor_mines != 0:
            return

        for n in self.get_neighbors(cell):
            if n.is_flagged or n.is_revealed:
                continue
            n.is_revealed = True
            if n.neighbor_mines == 0:
                self.reveal_neighbors(n)

    def reveal_cell(self, cell): # returns True if mine is hit, false if it wasnt
        if cell.is_revealed:
            print("Cell is already revealed.") # DEBUG DELETE LATER
            return False
        if cell.is_flagged:
            print("Cell is flagged.") # DEBUG DELETE LATER
            return False
        if cell.is_mine:
            print("Reveal_Cell(): Player hit a mine.") # DEBUG DELETE LATER
            return True
        cell.is_revealed = True
        if cell.neighbor_mines == 0:
            self.reveal_neighbors(cell)
        return False
        

    def toggle_flagged(self, cell): 
        if not cell.is_revealed: # if cell is revealed
            cell.is_flagged = not cell.is_flagged # toggles it

        
    def add_mines(self, mine_n: int, first_clicked): # randomly adds mines in array up to amount_of_mines
        mines_placed = 0
        while mines_placed < mine_n:
            row = random.choice(self.cells)
            col = random.choice(row)
            if col in first_clicked:
                continue
            if not col.is_mine:
                col.is_mine = True
                mines_placed += 1

    def add_neighbors(self): # adds neighbor_mines to cells based on mines
        cells = self.cells
        for row in cells:
            for item in row:
                if item.is_mine:
                    n = self.get_neighbors(item)
                    for b in n:
                        b.neighbor_mines += 1
    
    def print_player_board(self): #prints board that the player will see (revealed)
        player_board = []
        for item in self.cells:
            curr = []
            for n in item:
                if n.is_flagged:
                    curr.append("_") #placeholder 
                if not n.is_revealed:
                    curr.append("-")
                else:
                    curr.append(f"{n.neighbor_mines}")
            player_board.append(curr)
        print(player_board)

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
        print(real_board)


def make_array(n: int): # creates cells and defines their coordinates
    array = []
    for row in range(n):
        current_row = []
        for col in range(n):
            c = Cell()
            c.coordinate = (row, col)
            current_row.append(c)
        array.append(current_row)
    return array


def board_setup(size, mines):
    c = Board(make_array(size))
    return c

# setup first board
is_first_turn = True

# game loop
while True:
        
        curr_board.print_debug_board()
        print("· · ──────────────────────────── ꒰ঌ·✦·໒꒱ ──────────────────────────── · ·") # visual divider cus it's hard to read
        curr_board.print_player_board()
        if curr_board.game_is_won():
            print("You won!")
            curr_board = board_setup(board_size, amount_of_mines) # makes a new random board
            is_first_turn = True
            input("Play again?: ") # doesn't matter what they put
            continue


        # choose cell
        while True:

            # row select
            r = int(input(f"Enter row 1-{len(curr_board.cells)}: "))
            if r > 16 or r < 1:
                            print(f"Please select a number between 1-{len(curr_board.cells)}!")
                            continue
            # col select
            c = int(input(f"Enter column 1-{len(curr_board.cells)}: "))
            if c > 16 or c < 1:
                print(f"Please select a number between 1-{len(curr_board.cells)}!")
                continue
            
            cell = curr_board.cells[r-1][c-1] # -1 to account for python indexing at 0
            break

        if is_first_turn:            
            curr_board = board_setup(board_size, amount_of_mines) # makes an initial board
            # get list of safe blocks
            first_turn_neighbors = curr_board.get_neighbors(cell)
            first_turn_neighbors.append(cell)

            # generate with those safe blocks in mind
            curr_board.add_mines(amount_of_mines, first_turn_neighbors)
            curr_board.add_neighbors()

            # reveal cell
            b = curr_board.reveal_cell(cell)
            is_first_turn = False

        else:
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


        if b: # b holds the value of the previous input (True means mine)
            curr_board.print_debug_board()
            print("Game Over.")
            curr_board = board_setup(board_size, amount_of_mines)
            is_first_turn = True
            input("Play again?: ")
            continue