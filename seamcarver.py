#!/usr/bin/env python3

from picture import Picture
from math import sqrt
import sys 

class SeamCarver(Picture):
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        if i < 0 or i > self.width() - 1 or j < 0 or j > self.height() - 1:
            raise IndexError

        i0 = (i - 1 + self.width()) % self.width()
        i2 = (i + 1 + self.width()) % self.width()
        j0 = (j - 1 + self.height()) % self.height()
        j2 = (j + 1 + self.height()) % self.height()
        x_0 = self[i0, j]
        x_2 = self[i2, j]
        y_0 = self[i, j0]
        y_2 = self[i, j2]
        return sqrt(((x_2[0]-x_0[0])**2 + (x_2[1]-x_0[1])**2 + (x_2[2]-x_0[2])**2) + ((y_2[0]-y_0[0])**2 + (y_2[1]-y_0[1])**2 + (y_2[2]-y_0[2])**2))

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''    
        costs = [[0]* (self.height()) for _ in range(self.width())]
        def smallest_triple(i,j):
            '''
            returns either i-1, i, or i+1 whoever is the smallest
            '''
            i0 = max(i-1, 0)
            i2 = min(i+1, self.width()-1)
            mid = costs[i][j]
            left = costs[i0][j]
            right = costs[i2][j]
            if left < mid and left < right:
                return i0
            if mid < left and mid < right:
                return i
            if right < mid and right < left:
                return i2
            return i


        # get the costs
        for j in range(self.height()):
            smallest_cost_i = 0
            smallest_cost = sys.maxsize
            for i in range(self.width()):
                smallest_i = smallest_triple(i, j-1)
                costs[i][j] = self.energy(i, j) + costs[smallest_i][j-1]
                if costs[i][j] < smallest_cost:
                    smallest_cost = costs[i][j]
                    smallest_cost_i = i
        # find the shortest cost path
        # smallest_cost_i now contains the index of the smallest cost in the last row
        # we now iterate upwards
        path = [0] * self.height()
        for j in range(self.height()-1, -1, -1):
            smallest_cost_i = smallest_triple(smallest_cost_i, j)
            path[j] = smallest_cost_i 
        return path
    
    def __transpose(self):
        '''
        Switches x and y values
        '''
        original_values = {}
        original_width = self.width()
        original_height = self.height()
        to_remove = []
        for j in range(self.height()):
            for i in range(self.width()):
                original_values[j,i] = self[i,j]
                if i >= self.height() or j >= self.width():
                    to_remove.append((i,j))
        self._width = original_height
        self._height = original_width
        self.update(original_values)
        for i, j in to_remove:
            del self[i, j]
    
    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        self.__transpose()
        value = self.find_vertical_seam()
        self.__transpose()
        return value
    
    def __seam_check(self, seam: list[int]):
        for i in range(len(seam)-1):
            if abs(seam[i+1] - seam[i]) > 1:
                return False
        return True
    
    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if len(seam) != self.height() or self.width() == 1:
            raise SeamError
        if not self.__seam_check(seam):
            raise SeamError

        self._width += -1
        for j in range(self.height()):
            for i in range(seam[j], self.width()):
                self[i,j] = self[i+1,j]
            del self[self.width(),j]

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        if len(seam) != self.width() or self.height() == 1:
            raise SeamError
        if not self.__seam_check(seam):
            raise SeamError
        self.__transpose()
        self.remove_vertical_seam(seam)
        self.__transpose()

class SeamError(Exception):
    pass
