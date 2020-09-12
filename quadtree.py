import random
import pygame
import numpy as np

pygame.init()

WIDTH = 800
HEIGHT = 800

win = pygame.display.set_mode((WIDTH, HEIGHT))

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

win.fill(black)

pygame.display.set_caption("QuadGen")

gameMode = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        # to check if the point lies inside a rectangle object
        return (point.x >= self.x - self.w) and \
               (point.x <= self.x + self.w) and \
               (point.y <= self.y + self.h) and \
               (point.y >= self.y - self.h)


class QuadTree:
    def __init__(self, boundary, n):
        self.boundary = boundary
        self.capacity = n
        self.points = []
        self.divided = False

    def subdivide(self):
        # to access the objects easily this assignment is made
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        # Divide the quad into four if the point is in that domain
        ne = Rectangle(x + w / 2, y - h / 2, w / 2, h / 2)
        self.northeast = QuadTree(ne, self.capacity)
        nw = Rectangle(x - w / 2, y - h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)
        se = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = QuadTree(se, self.capacity)
        sw = Rectangle(x - w / 2, y + h / 2, w / 2, h / 2)
        self.southwest = QuadTree(sw, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        # if the points in a domain is less than the capacity add the point into that domain else subdivide
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True  # append instead of push keyword
        else:
            if not self.divided:
                self.subdivide()

            # Need to change this point - need to refactor
            # Made to factor in the Edge cases
            if self.northeast.insert(point):
                return True
            elif self.northwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True

    def show(self):

        pygame.draw.rect(win, red, (self.boundary.x - self.boundary.w, self.boundary.y - self.boundary.h,
                                    self.boundary.w * 2, self.boundary.h * 2), 1)

        if self.divided:
            # Recursive call to display the rectangles
            self.northeast.show()
            self.northwest.show()
            self.southeast.show()
            self.southwest.show()

        for p in self.points:
            pygame.draw.circle(win, white, (p.x, p.y), 2, 1)

        pygame.display.update()


def main():
    boundary = Rectangle(400, 400, 400, 400)
    qtree = QuadTree(boundary, 1)
    # filename = 'airfoil_2.txt'
    # indata = np.loadtxt(filename, usecols=(0, 1))  # make sure the rest is ignored
    i = 0
    while i < 800:
        p = Point(random.randint(1, 799), random.randint(1, 799))
        # p = Point(int(indata[i][0])*2 - 200, int(indata[i][1])*2-100)
        qtree.insert(p)
        i = i + 1
    qtree.show()
    while i < 1500:
        # To stop pygame from closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 2000
        pygame.display.update()


main()
