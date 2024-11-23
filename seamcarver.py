#!/usr/bin/env python3

from picture import Picture
from math import sqrt

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        # apparently (based on my guess), self[i,j] returns a tuple (r,g,b) for pixel [i,j]
        x_0 = self[i-1,j] if (i-1, j) in self else (0,0,0)
        x_2 = self[i+1,j] if (i+1, j) in self else (0,0,0)
        y_0 = self[i, j-1] if (i, j-1) in self else (0,0,0)
        y_2 = self[i, j+1] if (i, j+1) in self else (0,0,0)
        xcdiff =  (x_2[0]-x_0[0])**2 + (x_2[1]-x_0[1])**2 + (x_2[2]-x_0[2])**2
        ycdiff =  (y_2[0]-y_0[0])**2 + (y_2[1]-y_0[1])**2 + (y_2[2]-y_0[2])**2
        return sqrt(xcdiff + ycdiff)

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''    
        # +1 is a neat little trick
        energies = [[0]* (self.width()) for _ in range(self.height())]
        
        def smallest_triple(i,j):
            '''
            returns either i-1, i, or i+1 whoever is the smallest
            '''

            mid = energies[i, j] if (i, j) in energies else 0
            left = energies[i-1, j] if (i-1, j) in energies else mid + 1
            right = energies[i+1, j] if (i+1, j) in energies else mid + 1
            if left < mid and left < right:
                return i-1
            if mid < left and mid < right:
                return i
            if right < mid and right < left:
                return i+1
            return i

        
        # get the energies
        
        for j in range(self.height()):
            for i in range(self.width()):
                smallest_i = smallest_triple(i, j-1)
                energies[i,j] = self.energy(i, j) + energies[smallest_i, j-1]
                # no need to worry for first row case because [0-1] = [height+1] = 0
        
        # find the shortest cost path
        # smallest_i now contains the index of the most recent path
        # we now iterate upwards
        path = [energies[i,j]]
        for j in range(self.height()-1, -1):
            smallest_i = smallest_triple(smallest_i, j)
            path.append(energies[smallest_i, j])
        
        return path
    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
