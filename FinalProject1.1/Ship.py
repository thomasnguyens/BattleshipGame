'''
Ship class objects consist of name, size, grid coordinate locations, active status, and hit count.
'''
class Ship:
    def __init__(self, name, size):
        self._name = name
        self._size = int(size)
        self._hit_count = 0
        self._grid_coords = list()
        self._active = True

    def get_size(self):
        return self._size

    '''
    Register a hit to this ship. Display a message and set active to false if this ship has been sunk.
    '''
    def add_hit(self):
        self._hit_count += 1
        if self._hit_count >= self._size:
            print(self._name, "has been destroyed.")
            self._active = False

    def get_is_active(self):
        return self._active

    def get_name(self):
        return self._name

    def get_hit_count(self):
        return self._hit_count

    '''Adds list of ship grid coordinates - eg. ('B', 4), ('B', 5), etc. - to the grid coords variable.'''
    def add_grid_coordinates(self, grid_coordinates):
        for coordinate in grid_coordinates:
            if coordinate not in self._grid_coords:
                self._grid_coords.append(coordinate)

    def get_grid_coords(self):
        return self._grid_coords

    def __repr__(self):

        grids = ""
        for coord in self._grid_coords:
            grids += str(coord)

        return "{\nname=" + self._name + \
                "isActive=" + str(self._active) + \
               "\nsize=" + str(self._size) + \
               "\nhitcount=" + str(self._hit_count) + \
                "\ngrid_coords" + grids + "\n}\n"
