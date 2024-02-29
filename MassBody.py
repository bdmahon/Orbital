import pygame
from math import sqrt
G = 6.674e-11
# use smaller dt if doing stepwise calculation(more accurate?)
dt = 1

class MassBody:
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.visual_r = self.get_visual_radius()

    def update(self, bodies):
        # changes velocity by accounting for all other forces
        for body in bodies:
            if body is not self:
                x_diff = self.x - body.x
                y_diff = self.y - body.y
                distance = self.distance_formula(body)
                rDiv = dt / distance ** 3
                self.vx -= x_diff * G * body.mass * rDiv
                self.vy -= y_diff * G * body.mass * rDiv
                # check for collisions?
        xchange = self.vx * dt
        ychange = self.vy * dt
        # print(xchange, ychange)
        self.x += xchange
        self.y += ychange

        return None

    def gravitational_force(self, other_mass):
        force = G * ((self.mass * other_mass.mass)/(self.distance_formula(other_mass)**2))

    def distance_formula(self, other_mass):
        return sqrt(((self.x - other_mass.x)**2 + (self.y - other_mass.y)**2))

    def get_visual_radius(self):
        if 0 < self.mass < 200:
            return 1
        if 200 <= self.mass < 400:
            return 2
        if 400 <= self.mass < 1200:
            return 3
        if 1200 <= self.mass < 3400:
            return 4
        if 3400 <= self.mass < 5500:
            return 5
        if 5500 <= self.mass < 7000:
            return 6
        if 7000 <= self.mass < 1000:
            return 7
        if self.mass >= 1000:
            return 10

    def onscreen_check(self, WIDTH, HEIGHT):
        return (0 < self.x < WIDTH) and (0 < self.y < HEIGHT)

    def draw(self, surface):
        pygame.draw.circle(surface, (180, 180, 180), (self.x, self.y), self.visual_r)
