import pygame
import numpy as np
from random import uniform
from Mouse import Mouse
from MassBody import MassBody

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------
WIDTH = 1000
HEIGHT = 800
G = 6.674e-11
dt = 1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

mouse = Mouse()
clock = pygame.time.Clock()

# ----------------------------------------------------
# Initialize Bodies
# ----------------------------------------------------
bodies = []

big_one = MassBody(10000000000000, WIDTH/2, HEIGHT/2, 0, 0)
small_one = MassBody(50000, WIDTH/2 - 300, HEIGHT/2, 0, 1.5)
smaller_one = MassBody(100, WIDTH/2 - 302, HEIGHT/2, 0.1, 1.5)
bodies.extend([big_one, small_one, smaller_one])

n_random_bodies = 1000
for n in range(n_random_bodies):
    bodies.append(MassBody(
        uniform(0.1, 10000),
        uniform(0, WIDTH/4),
        uniform(0, HEIGHT),
        uniform(-4, 1),
        uniform(-4, 1)
    ))

# ----------------------------------------------------
# Convert Bodies → NumPy Arrays (physics storage)
# ----------------------------------------------------
N = len(bodies)

masses = np.array([b.mass for b in bodies], dtype=float)
x = np.array([b.x for b in bodies], dtype=float)
y = np.array([b.y for b in bodies], dtype=float)
vx = np.array([b.vx for b in bodies], dtype=float)
vy = np.array([b.vy for b in bodies], dtype=float)

running = True

# ----------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------
while running:

    # --- EVENT HANDLING ---
    mouse.clicked = False
    mouse.update_position(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.press_down()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse.release_up()

    # --- EXIT ON ESC ---
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        running = False

    # ----------------------------------------------------
    # VECTORIZED GRAVITY PHYSICS
    # ----------------------------------------------------

    # Pairwise differences (NxN matrices)
    dx = x[:, None] - x[None, :]
    dy = y[:, None] - y[None, :]

    # Square distance + epsilon (no divide by zero)
    dist_sq = dx * dx + dy * dy + 1e-6
    dist = np.sqrt(dist_sq)

    # 1/r^3 (with diagonal zeroed)
    inv_r3 = 1.0 / (dist_sq * dist)
    np.fill_diagonal(inv_r3, 0)

    # Force components (vectorized)
    # masses[None, :] broadcasts each mass across the row
    Fx = -G * dx * inv_r3 * masses[None, :]
    Fy = -G * dy * inv_r3 * masses[None, :]

    # Total accelerations per body
    ax = np.sum(Fx, axis=1)
    ay = np.sum(Fy, axis=1)

    # Update velocity
    vx += ax * dt
    vy += ay * dt

    # Update position
    x += vx * dt
    y += vy * dt

    # ----------------------------------------------------
    # Write updated positions back into MassBody objects
    # ----------------------------------------------------
    for i, b in enumerate(bodies):
        b.x = x[i]
        b.y = y[i]
        b.vx = vx[i]
        b.vy = vy[i]

    # ----------------------------------------------------
    # DRAW
    # ----------------------------------------------------
    screen.fill((0, 0, 0))

    for b in bodies:
        if 0 < b.x < WIDTH and 0 < b.y < HEIGHT:
            b.draw(screen)

    pygame.display.flip()
    clock.tick(30)  # 30 FPS target

pygame.quit()
