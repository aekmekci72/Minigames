from random import randint
import pygame, sys

windowSize = 800

INF = float('inf')

cell = windowSize // 3
center_of_cell = pygame.math.Vector2(cell / 2)
pygame.display.set_caption("Tic Tac Toe")


class Tic_tac_toe:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('images/Neucha-Regular.ttf',cell//3)
        self.setImages()
        self.player = randint(0, 1)
        self.steps = 0

        self.create_board()
        self.create_array()
        self.winner = None
    
    def setImages(self):
        self.board = self.get_scaled_image(path='images/board.jpg', res=[windowSize] * 2)
        self.x = self.get_scaled_image(path='images/x.png', res=[cell] * 2)
        self.o = self.get_scaled_image(path='images/o.png', res=[cell] * 2)

    @staticmethod
    def get_scaled_image(path, res):
        img = pygame.image.load(path)
        return pygame.transform.smoothscale(img, res)

    def create_board(self):
        self.gameboard = [[INF for _ in range(3)] for _ in range(3)]

    def create_array(self):
        self.array = []
        for i in range(3):
            row_indices = [(i, j) for j in range(3)]
            col_indices = [(j, i) for j in range(3)]
            self.array.append(row_indices)
            self.array.append(col_indices)

        diag_indices_1 = [(i, i) for i in range(3)]
        diag_indices_2 = [(i, 2 - i) for i in range(3)]
        self.array.append(diag_indices_1)
        self.array.append(diag_indices_2)
        return self.array
                    
    def run(self):
        self.start()
        self.process()

    def start(self):
        self.game.screen.blit(self.board, (0, 0))
        self.showobj()
        self.showwinner()
    
    def showobj(self):

        for row_index, row in enumerate(self.gameboard):
            for i, obj in enumerate(row):
                if obj == INF:
                    pass
                else:
                    pos = pygame.math.Vector2(i, row_index)*cell
                    if obj:
                        display = self.x
                    else:
                        display = self.o
                    self.game.screen.blit(display, pos)
    
    def showwinner(self):
        if self.winner:
            if self.winner == 'tie':
                label = self.font.render('No winner', True, 'white', 'black')
                self.game.screen.blit(label, (windowSize // 2 - label.get_width() // 2, windowSize // 4))
                label2 = self.font.render('Press space to restart', True, 'white', 'black')
                self.game.screen.blit(label2, (windowSize // 2 - label2.get_width() // 2, windowSize // 2))
            else:
                pygame.draw.line(self.game.screen, 'gold', *self.winner_line, cell // 8)
                label = self.font.render(f'Player "{self.winner}" wins!', True, 'white', 'gold')
                self.game.screen.blit(label, (windowSize // 3 - label.get_width() // 3, windowSize // 4))
                label2 = self.font.render('Press space to restart', True, 'white', 'gold')
                self.game.screen.blit(label2, (windowSize // 2 - label2.get_width() // 2, windowSize // 2))
        else:
            pass


    def process(self):
        cell_processed = pygame.math.Vector2(pygame.mouse.get_pos()) // cell
        column, row = map(int, cell_processed)
        lclick = pygame.mouse.get_pressed()[0]

        if lclick and not self.winner and self.gameboard[row][column] == INF:
            self.gameboard[row][column] = self.player
            self.player = not self.player
            self.steps += 1
            self.is_winner()


    def is_winner(self):
        for i in self.array:
            x=[self.gameboard[i][j] for i, j in i]
            lsum = sum(x)
            if lsum in {0, 3}:
                self.winner = 'XO'[lsum == 0]
                self.winner_line = [pygame.math.Vector2(i[0][::-1]) * cell + center_of_cell,
                                    pygame.math.Vector2(i[2][::-1]) * cell + center_of_cell]
            
        if self.steps == 9 and not self.winner:
            self.winner = 'tie'


class FinalGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([windowSize] * 2)
        
        self.t = Tic_tac_toe(self)

    def run(self):
        while True:
            self.t.run()
            self.check_events()
            pygame.display.update()
            self.clock.tick(60)
    
    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.runAgain()


    def runAgain(self):
        self.t = Tic_tac_toe(self)



game = FinalGame()
game.run()