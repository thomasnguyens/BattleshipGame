'''
This class is not used. It became confusing to attempt to utilize this class rather than lists, tuples, etc.
'''


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_coordinates(self):
        return self._x, self._y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def __repr__(self):
        return str(self._x) + "|" + str(self._y) + "\n"
