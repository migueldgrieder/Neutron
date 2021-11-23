from renderer import Renderer

#class DirectPieceGenerator(renderer), class Position(row, col, floor), class StorePieceGenerator

class DirectPieceGenerator:

    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.current_row = 0
        self.current_col = 0


    def fill_empty(self, columns):
        self.current_col += columns

    def fill_piece(self, columns, offset_x = 0, offset_y = 0):

        for i in reversed(range(columns)):
            self.renderer.render_piece(self.current_row + offset_y, self.current_col + i + offset_x)

        self.current_col += columns

    def next_line(self):
        self.current_row += 1
        self.current_col = 0

    def next_floor(self):
        self.renderer.floor += 1
        self.current_row = 0
        self.current_col = 0

    def reset(self):
        self.renderer.floor = 0
        self.current_row = 0
        self.current_col = 0

class Position: # Uma peca do tabuleiro
    is_focused = False
    def __init__(self, row, col, floor):
        self.row = row
        self.col = col
        self.floor = floor

class StorePieceGenerator:
    pieces = [] #Lista de posicoes de pecas
    current_row = 0
    current_col = 0
    current_floor = 0

    def fill_empty(self, columns):
        self.current_col += columns

    def fill_piece(self, columns, offset_x=0, offset_y=0):

        for i in reversed(range(columns)): # Ira criar todas pecas em loop
            self.pieces.append(
                Position(
                    self.current_row + offset_y,
                    self.current_col + i + offset_x,
                    self.current_floor
                ))

        self.current_col += columns

    def next_line(self):
        self.current_row += 1
        self.current_col = 0

    def next_floor(self):
        self.current_floor += 1
        self.current_row = 0
        self.current_col = 0

    def reset(self):
        self.current_floor = 0
        self.current_row = 0
        self.current_col = 0

    def render_pieces(self, renderer):

        for piece in self.pieces:
            renderer.floor = piece.floor

            color = None

            if piece.is_focused:
                color ='#aeaeae'

            renderer.render_piece(piece.row, piece.col, color=color)

