#written by me


import itertools
import random


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
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if len(self.cells) == self.count:
            self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if self.count == 0:
            self.safes.add(cell)
                
    def print_cells(self):
        return self.cells
    
    def print_count(self):
        return self.count


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8, number_of_mines = 8):

        # Set initial height and width
        self.height = height
        self.width = width
        self.number_of_mines = number_of_mines

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

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
            # adding new cell to moves_made
        self.moves_made.add(cell)
        
            # adding new cell to safe
        
        self.safes.add(cell)
        
            # generating a new sentence based on the new information:
            # the cell count tell us how many mines are in the neighbouring cells
            # skipping over cells that are not part of the board
        
        self.new_sentence = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:

                    if cell[0]+i > -1 and cell[0]+i < self.height and cell[1]+j > -1 and cell[1]+j < self.width:
                        if (cell[0]+i, cell[1]+j) not in self.moves_made:
                            self.new_sentence.add((cell[0]+i, cell[1]+j))
                except IndexError:
                    continue
                

        existing = False
        new_sentence = Sentence(self.new_sentence, count)
        for statement in self.knowledge:
            if new_sentence == statement:
                existing = True
                break
        if existing == False:
            self.knowledge.append(new_sentence)

        del existing
        del new_sentence
        
            # removing cell from existing statements, and deleting emtpy statements
        
        for statement in self.knowledge:
            if cell in statement.cells:
                statement.cells.remove(cell)
                
                        
        for statement in self.knowledge:
            if len(statement.cells) == 0:
                self.knowledge.remove(statement)
                
         
                    
            # generating new statements based on subsets:             

            # subsets with 0 and not 0 count:
        permutations = itertools.permutations(self.knowledge, 2)
        perm_cells = set()
        perm_count = int
        for element in permutations:
            if (element[0].count != 0 and element[1].count != 0):

                if element[0].cells.issubset(element[1].cells):
                    perm_cells = perm_cells.union(element[1].cells.difference(element[0].cells))
                    perm_count = element[1].count - element[0].count
                    if perm_cells != set():
                        new_sentence = Sentence(perm_cells, perm_count)
                        existing = False
                        for statement in self.knowledge:
                            if new_sentence == statement:
                                existing = True
                                break
                        if existing == False:
                            self.knowledge.append(new_sentence)
                            del existing
                            del new_sentence
                    perm_cells = set()
                    perm_count = int
                    

        
            # checking all sentences in the knowledge base for any new known mines/safes:
        
        for statement in self.knowledge:
            for element in statement.cells:
                    statement.mark_mine(element)
                    statement.mark_safe(element)
                    
        for statement in self.knowledge:
            for cell in statement.mines:
                self.mines.add(cell)
            for cell in statement.safes:
                self.safes.add(cell)
                
        to_remove_from_safes = set()          
        for i in self.safes:
            if i in self.moves_made:
                to_remove_from_safes.add(i)

                
        for i in to_remove_from_safes:
            self.safes.remove(i)
        
                    
                    
        
        
        if len(self.mines) == 8:
            print("All mines found!!")
            
            
            
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        try:
            while 1:
                move = self.safes.pop()
                if move not in self.moves_made:
                    return move
        except KeyError:
            return None
            

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
            # cleaning up knowledge base
        
        for statement in self.knowledge:
            if len(statement.cells) == 0:
                self.knowledge.remove(statement)
        
            # if knowledge base has no entries, return a random cell        
        
        if len(self.knowledge) == 0:
            random_cells = set()
            for i in range(self.height):
                for j in range(self.width):
                    if ((i,j) not in self.moves_made) and ((i,j) not in self.mines):
                        # if (i,j) not in self.mines:
                        random_cells.add((i,j))
            return random.sample(random_cells, 1)[0]            

            # if knowledge base is know empty, calculate probabilities for best chance for knowledge base
            # and random cell, return the one that has a better chance of not being a mine
                
        else:
            
                # calculating best choice for knowledge base
            
            calculated_chance = 100
            calculated_sentence = object
            for i in self.knowledge:
                if len(i.cells) > 0:
                    if i.count / len(i.cells) < calculated_chance:
                        calculated_chance = (i.count / len(i.cells))
                        calculated_sentence = i
                else:
                    print("no remaining unexplored cells")
                    
                #   calculating random chance (excluding cells used for knowledge based choice)              
                    
            random_chance = 100
            random_cells = set()
            for i in range(self.height):
                for j in range(self.width):
                    if ((i,j) not in self.moves_made) and ((i,j) not in self.mines):
                        random_cells.add((i,j))
            if len(random_cells) > 0:            
                random_chance = (self.number_of_mines-len(self.mines)) / (len(random_cells)-len(calculated_sentence.cells))
            
    
            

            
            
            if len(random_cells) == 0 and len(self.mines) == self.number_of_mines:
                return None
            
            if calculated_chance < random_chance:
                move = random.sample(calculated_sentence.cells, 1)[0]
                return move
            else:
                try:
                    for i in calculated_sentence.cells:
                        random_cells.remove(i)
                    move = random.sample(random_cells, 1)[0]
                    return move
                except AttributeError:
                    move = random.sample(random_cells, 1)[0]
                    return move            
    
                