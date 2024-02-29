import pygame
from random import randint
from random import uniform
from Mouse import Mouse
from MassBody import MassBody
WIDTH = 1000
HEIGHT = 800

# Start Pygame
pygame.init()

# Pygame Display of Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))


mouse = Mouse()

key_was_pressed = False

# SETUP

bodies = []
big_one = MassBody(10000000000000, WIDTH/2, HEIGHT/2, 0, 0)
small_one = MassBody(50000, WIDTH/2 - 300, HEIGHT/2, 0, 1.5)
smaller_one = MassBody(100, WIDTH/2 - 302, HEIGHT/2, 0.1, 1.5)
bodies.extend([big_one, small_one, smaller_one])
n_random_bodies = 200
for n in range(0, n_random_bodies):
    bodies.append(MassBody(uniform(0.1, 10000), uniform(0, WIDTH), uniform(0, HEIGHT), uniform(-4, 4), uniform(-4, 4)))

# Pygame clock for rendering
clock = pygame.time.Clock()
running = True
deletables = []
while running:
    time = clock.get_time()
    rtime = clock.get_rawtime()

    # mouse and keyboard event handling
    mouse.clicked = False
    # mouse position this tick
    mouse.update_position(pygame.mouse.get_pos())

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.press_down()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse.release_up()
    if mouse.clicked:
        print("clicked")

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys:
        if pressed_keys[pygame.K_ESCAPE]:
            running = False
        if pressed_keys[pygame.K_w]:
            pass
        if pressed_keys[pygame.K_a]:
            pass
        if pressed_keys[pygame.K_s]:
            pass
        if pressed_keys[pygame.K_d]:
            pass
        if pressed_keys[pygame.K_i]:
            pass
        if pressed_keys[pygame.K_j]:
            pass
        if pressed_keys[pygame.K_k]:
            pass
        if pressed_keys[pygame.K_l]:
            pass
        if pressed_keys[pygame.K_RETURN]:
            pass
        key_was_pressed = True

    # logic updates
    # calculates positions for this frame
    for body in bodies:
        # update & check for collisions
        # commit new velocities
        if body.update(bodies) is not None:
            deletables.append(body)
    screen.fill((0, 0, 0))
    for body in bodies:
        if body.onscreen_check(WIDTH, HEIGHT):
            body.draw(screen)

    pygame.display.flip()
    # 30 frames per second
    clock.tick(30)

    # Update Game Timers

pygame.quit()

print("calculations per second:", n_random_bodies*n_random_bodies*30)
