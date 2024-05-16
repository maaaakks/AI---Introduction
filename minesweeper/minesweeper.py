import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height, width, mines):

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

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.discard(cell)
            
class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, height, width):

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
        
        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        # mark the cell as safe
        self.mark_safe(cell) 
        
        # add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        
        # For each neighbor of the current cell :
        neighbors = set()
        for x in range(cell[0] - 1, cell[0] + 2):
            for y in range (cell[1] - 1, cell[1] + 2):
                # Filter not current cell + not cell out of the game + not safe cell 
                if (x,y) != cell and 0 <= x < self.width and 0 <= y < self.height and (x,y) not in self.safes:
                    neighbors.add((x,y))   
        # Update knowledge
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

        # Update all sentences with the new knowledge
        for sentence in self.knowledge:
            for cell in sentence.known_safes():
                self.mark_safe(cell)
            for cell in sentence.known_mines():
                self.mark_mine(cell)
                
        # Update all sentence #debug
        for sentence in self.knowledge:
            mines_to_remove = sentence.cells.intersection(self.mines)
            for mine in mines_to_remove:
                sentence.mark_mine(mine)
            if sentence.count == 0:
                for safe_cell in set(sentence.cells):  
                    self.mark_safe(safe_cell)
                    
        # Remove empty sentences from the knowledge base # optimization
        self.knowledge = [sentence for sentence in self.knowledge if len(sentence.cells) > 0]
            
        return(self.mines)
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        '''
        # Create a list of safe and free move based on moves_made and safes move
        self.list_safe = set()
        
        for x in range(self.width):
            for y in range(self.height):
                cell_to_check = (x, y)
                if (x,y) in self.safes and (x,y) not in self.moves_made and (x,y) not in self.list_safe: 
                   self.list_safe.add((x,y))
        '''  
        # Return the first safe move fund
        
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None         
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        '''
        for x in range(self.width):
            for y in range(self.height):
                if (x,y) not in self.moves_made and (x,y):
                   return (x,y)
        return None  
        '''
        available_moves = [cell for cell in self.safes if cell not in self.moves_made]
        
        if len(available_moves) == 0:
            random_move = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            print(random_move)
        else :
            random_move = random.choice(list(available_moves))
            
        return(random_move)

