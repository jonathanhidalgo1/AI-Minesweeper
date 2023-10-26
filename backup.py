import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        print(count)
        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"


    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        
    
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0 :
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1
            

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            # self.count = self.count + 1

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=3, width=3):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        
        self.surrounding_cells = set()

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        

        clicked_cell = [cell]
        surrounding_cells = []
        #mark safes
        if count == 0:
            for i in range(clicked_cell[0][0] - 1, clicked_cell[0][0] + 2):
                for j in range(clicked_cell[0][1] - 1, clicked_cell[0][1] + 2):
                    if (i, j) == clicked_cell[0]:
                        continue
                    if i == -1 or j == -1:
                        continue
                    if i >= self.height or j >= self.width:
                        continue
                    if (i,j) in self.safes:
                        continue
                    if (i,j) in self.mines:
                        continue
                    else:
                        self.mark_safe((i,j))
                        # self.surrounding_cells.add((i,j))
                        # surrounding_cells.append((i,j))
        else:
            for i in range(clicked_cell[0][0] - 1, clicked_cell[0][0] + 2):
                for j in range(clicked_cell[0][1] - 1, clicked_cell[0][1] + 2):
                    if (i, j) == clicked_cell[0]:
                        continue
                    if i == -1 or j == -1:
                        continue
                    if i >= self.height or j >= self.width:
                        continue
                    if (i,j) in self.safes:
                        continue
                    if (i,j) in self.mines:
                        continue
                    # if (i,j) in self.surrounding_cells:
                    #     continue
                    else:
                        # self.surrounding_cells.add((i,j))
                        surrounding_cells.append((i,j))
        
                    
        self.knowledge.append(Sentence(surrounding_cells, count))
        
        # mark mines
        mines = []
        for sentence in self.knowledge:
            for cells in sentence.cells:
                if not sentence.known_mines():
                    continue
                if cells in sentence.known_mines():
                    mines.append(cells)
        
        for sentence in self.knowledge:
                if len(sentence.cells) == 1:
                    for cells in sentence.cells:
                        mines.append(cells)    
                
        for mine in mines:
            self.mark_mine(mine)
        
        #mark safes
        safes = []
        for sentence in self.knowledge:
            for cells in sentence.cells:
                if not sentence.known_safes():
                    continue
                if cells in sentence.known_safes():
                    safes.append(cells)
                                    
        for safe in safes:
            self.mark_safe(safe)
        
        
        
        
        knowledge = self.knowledge.copy()
       
        
        # new sentence base on inference
        for sentence in knowledge:
            for sentence2 in reversed(knowledge):
                if sentence.cells == sentence2.cells:
                    continue
                if sentence2.count == 0 and sentence.count == 0:
                    continue
                if len(sentence.cells) == 0 or len(sentence2.cells) == 0:
                    continue
                if len(sentence.cells) == 1 and sentence.count == 1:
                    continue
                if sentence.count > 1:
                    new = list(sentence.cells.difference(sentence2.cells))
                    

                    self.knowledge.append(Sentence(sentence.cells.difference(sentence2.cells), sentence.count - 1))
                    # self.knowledge.append(Sentence(sentence2.cells.difference(sentence.cells), sentence2.count - 1))
                    # print(f'sentence1 = {sentence.cells.difference(sentence2.cells)} count = {sentence.count} sentence2 = {sentence2.cells}')

                        # print(f'sentence1 = {sentence.cells.difference(sentence2.cells)} count = {sentence.count} sentence2 = {sentence2.cells}')
                    # self.knowledge.append(Sentence(sentence.cells.difference(sentence2.cells), sentence.count - 1))
                

        z =[]

        for sentence in self.knowledge:
            if sentence.known_mines() == None:
                continue
            for i in sentence.known_mines():
                z.append(i)
        for i in z:
            self.mark_mine(i)
        

        # print(f'safe cells {self.safes}')
        print(f'mines {self.mines}')

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        if self.safes:
            for safe in self.safes:
                if safe in self.mines:
                    continue
                if safe not in self.moves_made:
                    return safe
        else:
            return None
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        board = set()
        
        for i in range(self.height):
            for j in range(self.width):
                board.add((i,j))
        
        #se nao tiver nada em knolodge pega randomicamente detentro do board
        if not self.knowledge:
             print(f'cells random not knolede {random.choice(tuple(board))}')
             return random.choice(tuple(board))
        else:
            for cells in board:
                if cells in self.mines:
                    continue
                if cells in self.moves_made:
                    continue
                else:
                    return cells
                        
# test = MinesweeperAI()

# test.add_knowledge((0,0),0)
# test.add_knowledge((0,1),1)
# test.add_knowledge((1,0),1)
# test.add_knowledge((1,1),3)
# test.add_knowledge((1,2),2)





# print(test.make_safe_move())

