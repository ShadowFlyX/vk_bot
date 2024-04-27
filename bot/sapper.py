from random import sample

class Sapper:
    
    def __init__(self, width: int, height: int, mines: int):
        self._width = width
        self._height = height
        self._mines = mines


    def create_gamefield(self) -> None:
        if self._mines > self._width * self._height:
            raise ValueError("Count of mines can't be more than size of the gamefield")
        
        mines_positions = set(sample(range(self._width*self._height),self._mines))

        self._field = []

        for i in range(self._width):
            self._field.append([])
            for j in range(self._height):
                if (i * self._width + j) in mines_positions:
                    self._field[i].append(1)
                else:
                    self._field[i].append(0)


    def get_field(self) -> list[list[int]]:
        return self._field

    def get_game_properties(self):
        return self._height, self._width, self._mines


    def open_cell(self, x: int, y: int) -> int:
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            raise IndexError("The indexes of the opened cell cannot go beyond the field")
        return self._field[x][y]

