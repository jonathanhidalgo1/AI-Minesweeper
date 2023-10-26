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
            print(f'markmine cell{cell} selfcells {self.cells} count {self.count}')
            self.cells.remove(cell)
            self.count = self.count - 1
            

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=4, width=4):

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

        #create sentence
        for i in range(clicked_cell[0][0] - 1, clicked_cell[0][0] + 2):
            for j in range(clicked_cell[0][1] - 1, clicked_cell[0][1] + 2):
                if i == -1 or j == -1:
                    continue
                if (i, j) == clicked_cell[0]:
                    continue
                if i >= self.height or j >= self.width:
                    continue
                if (i,j) in self.safes:
                    continue
                # if (i,j) in self.mines:
                #     continue
                else:
                    surrounding_cells.append((i,j))
        
        
        self.knowledge.append(Sentence(surrounding_cells, count))
        
        
        
        safes = set()
        for i in self.knowledge:
            if i.known_safes() != None:
                if len(i.known_safes()) != 0:
                    for safe in i.known_safes():
                        safes.add(safe)
        for s in safes:
            if s not in self.mines:
                # print(s)
                self.mark_safe(s)
        
        mines = set()
        for i in self.knowledge:
            if i.known_mines() != None:
                if len(i.known_mines()) != 0:
                    for mine in i.known_mines():
                        mines.add(mine)
        for m in mines:
            
            if m not in self.safes:
                # print(m)
                self.mark_mine(m)
  
                        
                    
        copy_knwolede = copy.deepcopy(self.knowledge)
        # new sentence base on inference        
        
        new_sentence = None
        new_count = None
        for sent1 in copy_knwolede:
            # print(sent1.cells)
            for sent2 in copy_knwolede:
                if sent1.cells != sent2.cells:
                    if len(sent1.cells) == 0 or len(sent2.cells) == 0:
                        continue
                    if sent1.cells.issubset(sent2.cells):    
                        # print(f'cell = {cell} sent2 = {sent2.cells} - sent1 = {sent1.cells}')                                     
                        new_sentence = sent2.cells - sent1.cells   
                        new_count = sent2.count - sent1.count     
                        # print(f'sent2 {sent2.cells} sent1 {sent1.cells}')
        # print(cell)
        if new_sentence != None or new_count != None:  
            # print(f'sent {new_sentence} coutn {new_count}')                        
            self.knowledge.append(Sentence(new_sentence, new_count))
            
            # print(new_sentence)
        # print(new_count)
                        
        # for i in self.knowledge:
        #     print(i.known_safes())
        

        
        # for i in self.knowledge:
        #     print(i.known_mines())
        
        
        # for j in self.knowledge:
        #     if len(j.cells) == 0:
        #         continue
        #     else:
        #         print(j)
        
        # print(f"safes {self.safes}")
        print(f"mines {self.mines}")

            
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
                    if safe not in self.moves_made:
                        return safe
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
        # return None
                        
test = MinesweeperAI()

test.add_knowledge((0,0),1)
test.add_knowledge((0,1),1)
test.add_knowledge((0,2),1)
test.add_knowledge((1,1),2)
test.add_knowledge((1,2),2)
test.add_knowledge((2,0),1)
test.add_knowledge((2,1),2)
test.add_knowledge((2,3),2)
test.add_knowledge((3,0),0)
test.add_knowledge((3,1),1)
test.add_knowledge((3,2),2)
# test.add_knowledge((0,3),1)

# print(test.make_safe_move())

