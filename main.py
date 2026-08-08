import random

WIDTH = 800
HEIGHT = 800

GRAVITY = 0.5
JUMP_SPEED = -13
MOVE_SPEED = 5

PLATFORM_IMAGES = ["ground_grass", "ground_sand", "ground_stone", "ground_wood", "ground_cake"]
PLATFORM_MARGIN_X = 100

MIN_GAP = 50
MAX_GAP = 90

bunny = Actor("bunny")

platforms = []
traps = []
game_over = False

def generate_platforms(anchor_x=None):
    platforms.clear()
    traps.clear()
    y = HEIGHT - 60
    x = anchor_x if anchor_x is not None else random.randint(PLATFORM_MARGIN_X, WIDTH - PLATFORM_MARGIN_X)

    while y > 0:
        platform = Actor(random.choice(PLATFORM_IMAGES))
        platform.pos = (x, y)
        platforms.append(platform)
        y -= random.randint(MIN_GAP, MAX_GAP)
        x = random.randint(PLATFORM_MARGIN_X, WIDTH - PLATFORM_MARGIN_X)

    if len(platforms) > 1:
        num_traps = random.randint(1, min(3, len(platforms) - 1))
        trap_platforms = random.sample(platforms[1:], num_traps)
        for platform in trap_platforms:
            trap = Actor("spikes")
            trap.x = platform.x
            trap.bottom = platform.top
            traps.append(trap)

generate_platforms()

vx = 0
vy = 0

def reset_bunny():
    global vx, vy, game_over
    game_over = False
    generate_platforms()
    first_platform = platforms[0]
    bunny.x = first_platform.x
    bunny.bottom = first_platform.top - 60
    vx = 0
    vy = 0

reset_bunny()

def update():
    global vx, vy, game_over

    if game_over:
        if keyboard.space:
            reset_bunny()
        return

    if keyboard.left:
        vx = -MOVE_SPEED
    elif keyboard.right:
        vx = MOVE_SPEED
    else:
        vx = 0

    prev_bottom = bunny.bottom

    vy += GRAVITY
    bunny.y += vy
    bunny.x += vx

    if bunny.x < 0:
        bunny.x = WIDTH
    elif bunny.x > WIDTH:
        bunny.x = 0

    if vy > 0:
        for platform in platforms:
            if prev_bottom <= platform.top <= bunny.bottom and platform.left < bunny.x < platform.right:
                vy = JUMP_SPEED
                break

    for trap in traps:
        if bunny.colliderect(trap):
            game_over = True
            return

    if bunny.bottom < 0:
        generate_platforms(anchor_x=bunny.x)
        safety_platform = platforms[0]
        bunny.x = safety_platform.x
        bunny.bottom = safety_platform.top
        vy = JUMP_SPEED

    if bunny.top > HEIGHT:
        reset_bunny()

def draw():
    screen.fill((70, 130, 227))
    for platform in platforms:
        platform.draw()
    for trap in traps:
        trap.draw()
    bunny.draw()

    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 30), fontsize=64, color="#4817bd")
        screen.draw.text("Ви зачепили ловушку!", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=32, color="white")
        screen.draw.text("Натисніть SPACE, щоб почати знову", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=24, color="yellow")