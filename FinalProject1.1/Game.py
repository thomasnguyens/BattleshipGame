'''
Game class objects aggregate PlayerBaord objects. Carry out main game loop and the bulk of the game's functionality.
'''

import json
import random
import pygame
from Ship import Ship
from PlayerBoard import*

BOARD_SPACING = 11
FLEET_SIZE = 5


class Game:
    def __init__(self, width, height):
        pygame.init()
        self._column_width = width / (BOARD_SPACING * 2)
        self._row_height = height / BOARD_SPACING
        self._display = pygame.display.set_mode((width, height))
        self._board_width = width
        self._board_height = height
        self._running = True
        self._player1_board = PlayerBoard(FLEET_SIZE)
        self._player2_board = PlayerBoard(FLEET_SIZE)
        self._grid_surface = pygame.Surface((self._board_width, self._board_height))
        self._background_surface = pygame.Surface((self._board_width, self._board_height))
        self.init_fleet("Fleet Init/fleet1.json", self._player1_board)
        self.init_fleet("Fleet Init/fleet2.json", self._player2_board)

    def run(self):
        player1_winner = False
        player2_winner = False
        while self._running:
            self.create_background()
            self.create_grid()
            self.blit_surfaces()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                    self.user_shot(pygame.mouse.get_pos());
                    self.enemy_shot()
                    if self._player2_board.is_fleet_destroyed():
                        print("Player 1 has won the game.")
                        player1_winner = True
                    elif self._player1_board.is_fleet_destroyed():
                        print("Player 2 has won the game.")
                        player2_winner = True
            self.draw_player_ships()
            self.show_mouse()
            self.draw_shots()
            if player1_winner:
                self.win_message("Player 1")
            elif player2_winner:
                self.win_message("Player 2")
            pygame.display.update()
        pygame.quit()

    '''Takes the mouse position as argument. Adds a shot the user's shot list. Register's a hit if the shot hit the
    opponent's ship(s).'''
    def user_shot(self, location):
        coordinates = list(location)
        coordinates[0] -= self._board_width // 2
        alpha_num_coordinates = self.convert_to_alphanumeric(coordinates)
        if alpha_num_coordinates not in self._player1_board.get_shot_list():
            self._player1_board.add_shot(alpha_num_coordinates)
            self.verify_hit(self._player2_board, alpha_num_coordinates)

    '''Verifies if argument two corresponds to the location of any of argument one's ship locations.'''
    def verify_hit(self, player_board, alpha_num_coord):
        for ship in player_board.get_ship_list():
            if alpha_num_coord in ship.get_grid_coords():
                ship.add_hit()

    '''Register's an enemy shot on the user's territory using random values.'''
    def enemy_shot(self):
        x = random.randint(1, 10)
        y = (random.randint(0, 10) + 65)
        alpha_num_coordinates = (chr(y), x)
        if alpha_num_coordinates not in self._player2_board.get_shot_list():
            self._player2_board.add_shot(alpha_num_coordinates)
            self.verify_hit(self._player1_board, alpha_num_coordinates)

    '''Draws all the shots that have been taken during the game.'''
    def draw_shots(self):
        player_shots_offset = self._board_width / 2 + 1
        enemy_shots_offset = 0
        self.shot_drawing_helper(self._player1_board, self._player2_board, player_shots_offset)
        self.shot_drawing_helper(self._player2_board, self._player1_board, enemy_shots_offset)

    '''Places a graphic in the display for any hits; draws a white square for misses.'''
    def shot_drawing_helper(self, shooter_board, opponent_board, lateral_offset):
        miss_color = (240, 240, 255)
        for shot in shooter_board.get_shot_list():
            coordinates = self.convert_to_XY(shot)
            pygame.draw.rect(self._display, miss_color, (coordinates[0] + lateral_offset, coordinates[1] + 1, self._column_width + 1, self._row_height))
            for ship in opponent_board.get_ship_list():
                if shot in ship.get_grid_coords():
                    img = pygame.image.load('Images/Start Explosion.png')
                    self._display.blit(img, (coordinates[0] + lateral_offset, coordinates[1]), (35, 35, 35, 35))

    '''Draws all the player ship locations in the display.'''
    def draw_player_ships(self):
        ship_color = (50, 50, 50)
        for ship in self._player1_board.get_ship_list():
            point_list = ship.get_grid_coords()
            for point in point_list:
                x = point[1] * self._column_width
                y = (ord(point[0]) - 64) * self._row_height
                pygame.draw.rect(self._display, ship_color,(x, y, self._column_width + 1, self._row_height + 1))

    '''Shows the mouse position in the grid squares during gameplay.'''
    def show_mouse(self):
        mouse_position = pygame.mouse.get_pos()
        quant_coord = self.rectify_values(mouse_position)
        cursor_color = (200, 200, 255)
        pygame.draw.rect(self._display, cursor_color, (quant_coord[0], quant_coord[1], self._column_width, self._row_height))

    '''Takes a location coordinate from anywhere on the playing space and converts it grid coordinates.'''
    def rectify_values(self, location):
        x = location[0]
        y = location[1]
        x_coord = round((x // self._column_width) * self._column_width)
        y_coord = round((y // self._row_height) * self._row_height)
        return x_coord, y_coord

    '''Creates the background water visual.'''
    def create_background(self):
        try:
            background = pygame.image.load("Images/waterTexture.jpg")
            background = pygame.transform.scale(background, (self._board_width, self._board_height))
            self._background_surface.blit(background, (0, 0))
        except IOError:
            print("Image file failed to load.")

    '''Creates the alphanumeric grid pattern and displays it.'''
    def create_grid(self):

        self._grid_surface = pygame.transform.scale(self._grid_surface, (self._board_width, self._board_height))

        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, self._board_height // 20)
        grid_color = (250, 250, 250)

        column_size = (self._board_width / BOARD_SPACING) / 2
        row_height = self._board_height / BOARD_SPACING

        self._grid_surface.fill((0, 0, 0))
        self._grid_surface.set_colorkey((0, 0, 0))

        # Not sure if this does any good.
        self._grid_surface = pygame.transform.scale(self._grid_surface, (self._board_width, self._board_height))

        for i in range(BOARD_SPACING):
            pygame.draw.line(self._grid_surface, grid_color, (column_size * i, 0), (column_size * i, self._board_height))
            pygame.draw.line(self._grid_surface, grid_color, (0, row_height * i), (self._board_width, row_height * i))
            if i > 0:
                letter = chr(64 + i)
                number = str(i)
                letter_text = font.render(letter, False, grid_color)
                number_text = font.render(number, False, grid_color)
                self._grid_surface.blit(letter_text, (column_size / 3, row_height * i + row_height / 3))
                self._grid_surface.blit(number_text, (column_size * i + column_size / 3, row_height / 3))

    '''Blits the relevant surfaces to the display.'''
    def blit_surfaces(self):
        self._background_surface.blit(self._grid_surface, (0, 0))
        self._display.blit(self._background_surface, (0, 0))
        self._display.blit(self._background_surface, (self._board_width / 2, 0))

    '''Reads from JSON files and initializes the player's ship details.'''
    def init_fleet(self, filename, player_board):
        try:
            f = open(filename)

            data = json.load(f)

            for key in data:
                name = key
                size = data[key]["size"]
                start_row = data[key]["start"]
                start_col = data[key]["column"]
                orientation = data[key]["orientation"]
                start_coord = (start_row, start_col)
                if orientation == 'v':
                    alpha_num_list = self.make_ship_locations(start_coord, int(size), 0, 1)
                elif orientation == 'h':
                    alpha_num_list = self.make_ship_locations(start_coord, int(size), 1, 0)
                ship = Ship(name, size)
                ship.add_grid_coordinates(alpha_num_list)
                player_board.add_ship(ship)
        except IOError:
            print("Fleet init file failed to load.")
        f.close()

    '''Receives a (row letter, column number) coordinate. Translates to numerical values that can be shown on the
    playing surface.'''
    def convert_to_XY(self, grid_coordinate):
        letter = grid_coordinate[0].upper()
        number = int(grid_coordinate[1])
        y_coord = (ord(letter) - 64) * self._row_height
        x_coord = number * self._column_width
        return x_coord, y_coord

    '''Takes an (x, y) location and converts it to a grid location - eg. (100, 100) -> ('C', 4)'''
    def convert_to_alphanumeric(self, xy_pair):
        x = int(xy_pair[0] / self._column_width)
        y = chr(int(((xy_pair[1] / self._row_height) + 64))).upper()
        return y, x

    '''Takes in a starting grid coordinate, ship size, and two increment values and creates a list of ship locations.'''
    def make_ship_locations(self, start_grid_coord, size, x_increment, y_increment):

        alpha_num_list = list()

        for i in range(size):
            column = int(start_grid_coord[1]) + (i * x_increment)
            row = chr(ord(start_grid_coord[0]) + (i * y_increment))
            grid_coord = (row, column)
            alpha_num_list.append(grid_coord)
        return alpha_num_list

    '''Checks for incorrect ship coordinates. Not used in current iterations. Consider removing.'''
    def check_ship_overlap(self, ship_list):
        point_list = list()
        for ship in ship_list:
            ship_points = ship.get_location_points()
            for point in ship_points:
                point_list.append(point)

        for x in range(len(point_list)-1):
            for j in range(x+1, len(point_list)):
                if point_list[x] == point_list[j]:
                    print(ship_list)
                    raise Exception ("Duplicate coordinates detected at : ", point_list[x])

    '''Displays a message on the screen when a player has won the game.'''
    def win_message(self, winner):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, self._board_height // 5)
        grid_color = (250, 10, 10)
        text = str(winner) + " has won the game. bye bye."
        full_message = font.render(text, True, grid_color)
        self._display.blit(full_message, (10, self._board_height // 3))

