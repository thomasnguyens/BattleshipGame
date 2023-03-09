'''
PlayerBoard class objects aggregate Ship objects, keep a list of shot locations, and check if the fleet of ships has
been destroyed.
'''
class PlayerBoard:
    def __init__(self, fleet_size):
        self._ship_list = list()
        self._fleet_size = int(fleet_size)
        self._sunk_ships = 0
        self._shot_list = list()

    def get_shot_list(self):
        return self._shot_list

    def add_ship(self, ship):
        if len(self._ship_list) <= self._fleet_size:
            self._ship_list.append(ship)

    def get_ship_list(self):
        return self._ship_list

    def add_shot(self, shot_location):
        self._shot_list.append(shot_location)

    '''Checks if all the players ships have been destroyed. If so, returns true and the game will end.'''
    def is_fleet_destroyed(self):
        destroyed_ships = 0
        for ship in self._ship_list:
            if not ship.get_is_active():
                destroyed_ships += 1
        if destroyed_ships >= self._fleet_size:
            return True
