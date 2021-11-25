import pygame
import random
from collections import deque

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
orange = pygame.Color(255, 170, 0)
green = pygame.Color(0, 255, 0)        # my favourite colour
cyan = pygame.Color(0, 255, 255)

# Setting the battleground
pygame.init()
cool_icon = pygame.image.load("snake7.png")
pygame.display.set_caption("SnakeSoul")
pygame.display.set_icon(cool_icon)
background_x = 1600
background_y = 900
background = pygame.display.set_mode((background_x, background_y))
cool_snake = pygame.image.load("fundal8.png")

StillSnaking = 1
step = 1
mode = 1
difficulty = 1
sizes = [0, 100, 50, 25, 10, 5]  # number of pixels of the sides of every square in the grid
speed = 0
MaxSpeed = 10
fps = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240]  # the speeds at which the snake will be moving

INF = 2000000000000000000
inf = 2000000000


def tutorial(k):  # the intro
    background.blit(cool_snake, (400, 500))
    if k == 1:
        style = pygame.font.SysFont("Chiller", 64)
        info = style.render("Hello and welcome to SnakeSoul, an AI that thinks and feels like a snake", True, cyan)
        background.blit(info, (10, 10))
        style = pygame.font.SysFont("Chiller", 50)
        info = style.render("In order to watch the AI master the game of snake, press A", True, cyan)
        background.blit(info, (10, 150))
        info = style.render("If you want to play it yourself, press S", True, cyan)
        background.blit(info, (10, 220))
    elif k == 2:
        style = pygame.font.SysFont("Chiller", 50)
        info = style.render("Choose the difficulty you want:", True, cyan)
        background.blit(info, (10, 10))
        info = style.render("1 - Easy", True, cyan)
        background.blit(info, (10, 70))
        info = style.render("2 - Medium", True, cyan)
        background.blit(info, (10, 130))
        info = style.render("3 - Hard", True, cyan)
        background.blit(info, (10, 190))
        info = style.render("4 - SSSSSSSuper Hard", True, cyan)
        background.blit(info, (10, 250))
        info = style.render("5 - Snakelike", True, cyan)
        background.blit(info, (10, 310))
        style = pygame.font.SysFont("Chiller", 32)
        info = style.render("Press a number from 1 to 5 to choose the desired difficulty", True, cyan)
        background.blit(info, (10, 500))
    elif k == 3:
        style = pygame.font.SysFont("Chiller", 50)
        info = style.render("Before the game starts, here is a quick reminder with the instructions you can use:", True, cyan)
        background.blit(info, (10, 10))
        style = pygame.font.SysFont("Chiller", 50)
        info = style.render("In order to increase or decrease the speed of the snake, press I or D ", True, cyan)
        background.blit(info, (10, 150))
        if mode == 0:
            info = style.render("To move the snake, press any of the UP, DOWN, LEFT, RIGHT keys", True, cyan)
            background.blit(info, (10, 220))
        style = pygame.font.SysFont("Chiller", 50)
        info = style.render("When you feel ready to be amazed, press SPACE", True, cyan)
        background.blit(info, (10, 500))


while StillSnaking and step <= 3:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            StillSnaking = 0
        elif event.type == pygame.KEYDOWN:
            if step == 1:
                if event.key == pygame.K_s:
                    step = 2
                    mode = 0                   # snake mode
                elif event.key == pygame.K_a:
                    step = 2
                    mode = 1                   # AI mode
            elif step == 2:
                if event.key == pygame.K_1:
                    difficulty = 1
                    step = 3
                elif event.key == pygame.K_2:
                    difficulty = 2
                    step = 3
                elif event.key == pygame.K_3:
                    difficulty = 3
                    step = 3
                elif event.key == pygame.K_4:
                    difficulty = 4
                    step = 3
                elif event.key == pygame.K_5:
                    difficulty = 5
                    step = 3
            elif step == 3:
                if event.key == pygame.K_SPACE:
                    step = 4
    background.fill(black)
    if StillSnaking and step <= 3:
        tutorial(step)
    pygame.display.update()

background.fill(black)

yey = 1    # still alive
moves = []

grid_x = background_x // sizes[difficulty]
grid_y = background_y // sizes[difficulty]
grid = [[0 for y in range(grid_y)] for x in range(grid_x)]

dx = [ 0, 1, 0, -1]
dy = [-1, 0, 1,  0]

direction = random.randrange(4)
head_x = random.randrange(grid_x//3, grid_x - grid_x//3)
head_y = random.randrange(grid_y//3, grid_y - grid_y//3)
tail_x = head_x
tail_y = head_y
if not(0 <= tail_x - dx[direction] < grid_x and 0 <= tail_y - dy[direction] < grid_y):
    for wohin in range(4):     # direction in deutsch
        if 0 <= tail_x - dx[wohin] < grid_x and 0 <= tail_y - dy[wohin] < grid_y:
            direction = wohin
            break
tail_x -= dx[direction]
tail_y -= dy[direction]
snake = deque([[head_x, head_y], [tail_x, tail_y]])
grid[head_x][head_y] = 1
grid[tail_x][tail_y] = 1
length = 2
moves += [direction]

free = []

for x in range(grid_x):
    for y in range(grid_y):
        if not(x == head_x and y == head_y) and not(x == tail_x and y == tail_y):
            free += [(x, y)]


food_x, food_y = free[random.randrange(grid_x * grid_y - length)]
last_x = -2
last_y = -2

dif = 0
if grid_x % 2 == 1 and grid_y % 2 == 1:  # edge case
    dif = 1

n = grid_x * grid_y - dif


def draw_snake():  # drawing the snake with a cool visual effect
    changes = []
    if last_x != -2 and last_y != -2:
        pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty] + 1, last_y * sizes[difficulty] + 1, sizes[difficulty] - 2, sizes[difficulty] - 2))
        changes += [pygame.Rect(last_x * sizes[difficulty] + 1, last_y * sizes[difficulty] + 1, sizes[difficulty] - 2, sizes[difficulty] - 2)]
        i = len(snake)-1
        d = -1
        for dd in range(4):
            if snake[i][0] + dx[dd] == last_x and snake[i][1] + dy[dd] == last_y:
                d = dd
                break
        if d == 0:
            pygame.draw.rect(background, black, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, snake[i][1] * sizes[difficulty], sizes[difficulty] - 2, 1))
            pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty] + 1, (last_y + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
            changes += [pygame.Rect(snake[i][0] * sizes[difficulty] + 1, snake[i][1] * sizes[difficulty], sizes[difficulty] - 2, 1)]
            changes += [pygame.Rect(last_x * sizes[difficulty] + 1, (last_y + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1)]
        if d == 1:
            pygame.draw.rect(background, black, pygame.Rect((snake[i][0] + 1) * sizes[difficulty] - 1, snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
            pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty], last_y * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
            changes += [pygame.Rect((snake[i][0] + 1) * sizes[difficulty] - 1, snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
            changes += [pygame.Rect(last_x * sizes[difficulty], last_y * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
        if d == 2:
            pygame.draw.rect(background, black, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, (snake[i][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
            pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty] + 1, last_y * sizes[difficulty], sizes[difficulty] - 2, 1))
            changes += [pygame.Rect(snake[i][0] * sizes[difficulty] + 1, (snake[i][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1)]
            changes += [pygame.Rect(last_x * sizes[difficulty] + 1, last_y * sizes[difficulty], sizes[difficulty] - 2, 1)]
        if d == 3:
            pygame.draw.rect(background, black, pygame.Rect(snake[i][0] * sizes[difficulty], snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
            pygame.draw.rect(background, black, pygame.Rect((last_x + 1) * sizes[difficulty] - 1, last_y * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
            changes += [pygame.Rect(snake[i][0] * sizes[difficulty], snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
            changes += [pygame.Rect((last_x + 1) * sizes[difficulty] - 1, last_y * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
    i = 0
    pygame.draw.rect(background, green, pygame.Rect(snake[i][0]*sizes[difficulty]+1, snake[i][1]*sizes[difficulty]+1, sizes[difficulty]-2, sizes[difficulty]-2))
    changes += [pygame.Rect(snake[i][0]*sizes[difficulty]+1, snake[i][1]*sizes[difficulty]+1, sizes[difficulty]-2, sizes[difficulty]-2)]
    d = -1
    for dd in range(4):
        if snake[i][0] + dx[dd] == snake[i+1][0] and snake[i][1] + dy[dd] == snake[i+1][1]:
            d = dd
            break
    if d == 0:
        pygame.draw.rect(background, green, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, snake[i][1] * sizes[difficulty], sizes[difficulty] - 2, 1))
        pygame.draw.rect(background, green, pygame.Rect(snake[i+1][0] * sizes[difficulty] + 1, (snake[i+1][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
        changes += [pygame.Rect(snake[i][0] * sizes[difficulty] + 1, snake[i][1] * sizes[difficulty], sizes[difficulty] - 2, 1)]
        changes += [pygame.Rect(snake[i+1][0] * sizes[difficulty] + 1, (snake[i+1][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1)]
    if d == 1:
        pygame.draw.rect(background, green, pygame.Rect((snake[i][0]+1) * sizes[difficulty] - 1, snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
        pygame.draw.rect(background, green, pygame.Rect(snake[i+1][0] * sizes[difficulty], snake[i+1][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
        changes += [pygame.Rect((snake[i][0]+1) * sizes[difficulty] - 1, snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
        changes += [pygame.Rect(snake[i+1][0] * sizes[difficulty], snake[i+1][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
    if d == 2:
        pygame.draw.rect(background, green, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, (snake[i][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
        pygame.draw.rect(background, green, pygame.Rect(snake[i+1][0] * sizes[difficulty] + 1, snake[i+1][1] * sizes[difficulty], sizes[difficulty] - 2, 1))
        changes += [pygame.Rect(snake[i][0] * sizes[difficulty] + 1, (snake[i][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1)]
        changes += [pygame.Rect(snake[i+1][0] * sizes[difficulty] + 1, snake[i+1][1] * sizes[difficulty], sizes[difficulty] - 2, 1)]
    if d == 3:
        pygame.draw.rect(background, green, pygame.Rect(snake[i][0] * sizes[difficulty], snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
        pygame.draw.rect(background, green, pygame.Rect((snake[i+1][0] + 1) * sizes[difficulty] - 1, snake[i+1][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
        changes += [pygame.Rect(snake[i][0] * sizes[difficulty], snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
        changes += [pygame.Rect((snake[i+1][0] + 1) * sizes[difficulty] - 1, snake[i+1][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2)]
    pygame.display.update(changes)  # I update only the pixels that changed (for a better performance of the game)


def draw_snake2():  # just for the outro
    if last_x != -2 and last_y != -2:
        pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty] + 1, last_y * sizes[difficulty] + 1, sizes[difficulty] - 2, sizes[difficulty] - 2))
        i = len(snake)-1
        d = -1
        for dd in range(4):
            if snake[i][0] + dx[dd] == last_x and snake[i][1] + dy[dd] == last_y:
                d = dd
                break
        if d == 0:
            pygame.draw.rect(background, black, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, snake[i][1] * sizes[difficulty], sizes[difficulty] - 2, 1))
            pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty] + 1, (last_y + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
        if d == 1:
            pygame.draw.rect(background, black, pygame.Rect((snake[i][0] + 1) * sizes[difficulty] - 1, snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
            pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty], last_y * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
        if d == 2:
            pygame.draw.rect(background, black, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, (snake[i][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
            pygame.draw.rect(background, black, pygame.Rect(last_x * sizes[difficulty] + 1, last_y * sizes[difficulty], sizes[difficulty] - 2, 1))
        if d == 3:
            pygame.draw.rect(background, black, pygame.Rect(snake[i][0] * sizes[difficulty], snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
            pygame.draw.rect(background, black, pygame.Rect((last_x + 1) * sizes[difficulty] - 1, last_y * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
    i = 0
    pygame.draw.rect(background, green, pygame.Rect(snake[i][0]*sizes[difficulty]+1, snake[i][1]*sizes[difficulty]+1, sizes[difficulty]-2, sizes[difficulty]-2))
    d = -1
    for dd in range(4):
        if snake[i][0] + dx[dd] == snake[i+1][0] and snake[i][1] + dy[dd] == snake[i+1][1]:
            d = dd
            break
    if d == 0:
        pygame.draw.rect(background, green, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, snake[i][1] * sizes[difficulty], sizes[difficulty] - 2, 1))
        pygame.draw.rect(background, green, pygame.Rect(snake[i+1][0] * sizes[difficulty] + 1, (snake[i+1][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
    if d == 1:
        pygame.draw.rect(background, green, pygame.Rect((snake[i][0]+1) * sizes[difficulty] - 1, snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
        pygame.draw.rect(background, green, pygame.Rect(snake[i+1][0] * sizes[difficulty], snake[i+1][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
    if d == 2:
        pygame.draw.rect(background, green, pygame.Rect(snake[i][0] * sizes[difficulty] + 1, (snake[i][1] + 1) * sizes[difficulty] - 1, sizes[difficulty] - 2, 1))
        pygame.draw.rect(background, green, pygame.Rect(snake[i+1][0] * sizes[difficulty] + 1, snake[i+1][1] * sizes[difficulty], sizes[difficulty] - 2, 1))
    if d == 3:
        pygame.draw.rect(background, green, pygame.Rect(snake[i][0] * sizes[difficulty], snake[i][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))
        pygame.draw.rect(background, green, pygame.Rect((snake[i+1][0] + 1) * sizes[difficulty] - 1, snake[i+1][1] * sizes[difficulty] + 1, 1, sizes[difficulty] - 2))


def draw_food():  # because I want the code to run very very fast, I'll update again only the changed pixels
    global food_x
    global food_y
    if length != grid_x * grid_y:
        pygame.draw.rect(background, orange, pygame.Rect(food_x * sizes[difficulty]+1, food_y * sizes[difficulty]+1, sizes[difficulty]-2, sizes[difficulty]-2))
        pygame.display.update(pygame.Rect(food_x * sizes[difficulty]+1, food_y * sizes[difficulty]+1, sizes[difficulty]-2, sizes[difficulty]-2))


def woohoo():       # a chi non piace mangiare la pizza (italian for 'who doesn't like to eat pizza')
    global food_x
    global food_y
    global length
    if length != grid_x * grid_y:
        snake.appendleft([food_x, food_y])  # the new head of the snake
        grid[food_x][food_y] = 1
        free.remove((food_x, food_y))
        length += 1  # the snake is getting longer in the game (chubbier in the real world)
        if length != grid_x * grid_y:
            food_x, food_y = free[random.randrange(grid_x * grid_y - length)]  # a random free cell


def move():  # moving the snake, which is stored in a deque (for a better performance of the game)
    global direction
    global yey
    global free
    global food_x
    global food_y
    global last_x
    global last_y
    x = snake[0][0]
    y = snake[0][1]
    x += dx[direction]
    y += dy[direction]
    if x == food_x and y == food_y:
        woohoo()  # if the snake encountered some good food :)
    else:
        if not(0 <= x < grid_x and 0 <= y < grid_y) or (grid[x][y] == 1 and not(x == snake[length-1][0] and y == snake[length-1][1])):  # game over (the snake made an awful move)
            yey = 0  # hello darkness my old friend
        else:
            last_x = snake[length - 1][0]
            last_y = snake[length - 1][1]
            grid[last_x][last_y] = 0
            grid[x][y] = 1
            free += [(last_x, last_y)]
            free.remove((x, y))
            snake.pop()  # the tail of the snake is not there anymore
            snake.appendleft([x, y])  # the snake is now having a new head


hamilton = [[0 for y in range(grid_y)] for x in range(grid_x)]  # the order of every cell in the hamiltonian cycle
maze_x = grid_x//2
maze_y = grid_y//2
maze = [[0 for y in range(maze_y)] for x in range(maze_x)]
v = []
papa = []  # for disjoint set union
dim = []  # for disjoint set union
contour = [[[0 for z in range(2)] for y in range(grid_y)] for x in range(grid_x)]
viz = [[0 for y in range(grid_y)] for x in range(grid_x)]
neighbours = [[] for i in range(maze_x * maze_y)]


def ok(x, y):  # verifies if this cell is a good candidate for the new head of the snake
    safe = 1
    if grid_x % 2 == 1 and grid_y % 2 == 1:  # the edge case needs special attention
        if not(grid[0][2] == 0 and grid[1][2] == 0 and grid[1][1] == 0 and grid[0][1] == 0):
            safe = 0
    if safe == 0:
        return 0
    else:  # the new cell must be between the head and the tail(in the hamiltonian cycle), otherwise there is a small chance that the snake will die(if it will find food in every cell until it moves into its own body and dies or gets trapped)
        head = hamilton[snake[0][0]][snake[0][1]]
        tail = hamilton[snake[length-1][0]][snake[length-1][1]]
        poz = hamilton[x][y]
        if tail <= head:
            if tail < poz <= head:
                return 0
            else:
                return 1
        else:
            if head < poz <= tail:
                return 1
            else:
                return 0


def dist_to_food(x, y):  # i think the name of the function speaks for itself :)
    return (hamilton[food_x][food_y] - hamilton[x][y] + n) % n


def il_capo_di_tutti_capi(x):    # finding the root of a disjoint set (which is a tree btw)
    if x != papa[x]:
        papa[x] = il_capo_di_tutti_capi(papa[x])
    return papa[x]


def join(x, y):     # joining two disjoint sets
    x = il_capo_di_tutti_capi(x)
    y = il_capo_di_tutti_capi(y)
    if dim[x] < dim[y]:
        dim[y] += dim[x]
        papa[x] = y
    else:
        dim[x] += dim[y]
        papa[y] = x


def labyrinth():
    global v
    global papa
    global dim
    # making a maze of a grid with the help of MST(Minimum Spanning Tree) (and Prim's algorithm)
    for i in range(maze_x * maze_y):
        papa += [i]
        dim += [1]
    for i in range(maze_x):
        for j in range(maze_y):
            maze[i][j] = random.randrange(2000000000)  # random values in order to get a random maze
            v += [[maze[i][j], i, j]]
    v.sort()
    for i in range(maze_x * maze_y):
        x = v[i][1]
        y = v[i][2]
        for d in range(4):
            if 0 <= x + dx[d] < maze_x and 0 <= y + dy[d] < maze_y:
                if maze[x + dx[d]][y + dy[d]] <= maze[x][y]:
                    code1 = x * maze_y + y
                    code2 = (x + dx[d]) * maze_y + y + dy[d]
                    if il_capo_di_tutti_capi(code1) != il_capo_di_tutti_capi(code2):
                        join(code1, code2)
                        neighbours[code1] += [code2]
                        neighbours[code2] += [code1]
    # creating the hamiltonian cycle based on the outline of the maze
    for x in range(maze_x):
        for y in range(maze_y):
            code = x * maze_y + y
            d = 0
            if (x + dy[d]) * maze_y + y + dx[d] in neighbours[code]:
                contour[x * 2][y * 2][0] = 0
                contour[x * 2][y * 2 + 1][0] = 0
            else:
                contour[x * 2][y * 2][0] = 1
                contour[x * 2][y * 2 + 1][0] = 3
            d = 1
            if (x + dy[d]) * maze_y + y + dx[d] in neighbours[code]:
                contour[x * 2][y * 2 + 1][1] = 1
                contour[x * 2 + 1][y * 2 + 1][1] = 1
            else:
                contour[x * 2][y * 2 + 1][1] = 2
                contour[x * 2 + 1][y * 2 + 1][1] = 0
            d = 2
            if (x + dy[d]) * maze_y + y + dx[d] in neighbours[code]:
                contour[x * 2 + 1][y * 2][0] = 2
                contour[x * 2 + 1][y * 2 + 1][0] = 2
            else:
                contour[x * 2 + 1][y * 2][0] = 1
                contour[x * 2 + 1][y * 2 + 1][0] = 3
            d = 3
            if (x + dy[d]) * maze_y + y + dx[d] in neighbours[code]:
                contour[x * 2][y * 2][1] = 3
                contour[x * 2 + 1][y * 2][1] = 3
            else:
                contour[x * 2][y * 2][1] = 2
                contour[x * 2 + 1][y * 2][1] = 0
    x = 0
    y = 0
    k = 0
    while k < grid_x * grid_y:
        hamilton[x][y] = k
        viz[x][y] = 1
        for d in contour[x][y]:  # in contour I keep the 2 directions in which the outline of the maze will go from that cell from the grid
            if viz[x + dy[d]][y + dx[d]] == 0:
                x += dy[d]
                y += dx[d]
                break
        k += 1


def hamiltonian_cycle():  # making a hamiltonian cycle of the grid
    if grid_x % 2 == 0 and grid_y % 2 == 0:
        labyrinth()  # this works only if there ar an even number of lines and an even number of columns
    elif grid_x % 2 == 0:
        k = 0
        for i in range(grid_x):
            hamilton[i][0] = k
            k += 1
        for i in range(grid_x - 1, -1, -1):
            if i % 2 == 1:
                for j in range(1, grid_y):
                    hamilton[i][j] = k
                    k += 1
            if i % 2 == 0:
                for j in range(grid_y - 1, 0, -1):
                    hamilton[i][j] = k
                    k += 1
    elif grid_y % 2 == 0:
        k = 0
        for i in range(grid_y):
            hamilton[0][i] = k
            k += 1
        for i in range(grid_y - 1, -1, -1):
            if i % 2 == 1:
                for j in range(1, grid_x):
                    hamilton[j][i] = k
                    k += 1
            if i % 2 == 0:
                for j in range(grid_x - 1, 0, -1):
                    hamilton[j][i] = k
                    k += 1
    else:  # when there are an odd number of lines and an odd number of columns, there is no hamiltonian cycle which covers all the cells from the grid (because a hamiltonian cycle in a grid is always of even length or its length is 1)
        k = 0  # to deal with this case, I will create 2 hamiltonian cycles(which differ by only 1 cell) from which the algorithm will choose depending on the situation
        for i in range(grid_x):
            hamilton[i][0] = k
            k += 1
        for i in range(grid_x - 1, 1, -1):
            if i % 2 == 0:
                for j in range(1, grid_y):
                    hamilton[i][j] = k
                    k += 1
            if i % 2 == 1:
                for j in range(grid_y - 1, 0, -1):
                    hamilton[i][j] = k
                    k += 1
        for j in range(grid_y - 1, 2, -1):
            if j % 2 == 0:
                hamilton[1][j] = k
                k += 1
                hamilton[0][j] = k
                k += 1
            if j % 2 == 1:
                hamilton[0][j] = k
                k += 1
                hamilton[1][j] = k
                k += 1
        hamilton[1][2] = k
        k += 1
        hamilton[0][2] = k
        k += 1
        hamilton[0][1] = k
        k += 1


def think_next_move():  # the hypothalamus of the AI
    global direction
    dist = inf
    best = -1
    for d in range(4):
        if 0 <= snake[0][0] + dx[d] < grid_x and 0 <= snake[0][1] + dy[d] < grid_y:
            x = snake[0][0]
            y = snake[0][1]
            if (hamilton[x][y] + 1) % n == hamilton[x + dx[d]][y + dy[d]]:  # the direction that follows the hamiltonian cycle will always be good
                direction = d
                if not(food_x == -1 and food_y == -1):
                    distance = dist_to_food(x + dx[d], y + dy[d])
                    if distance < dist:
                        dist = distance
                        best = d
            elif not(food_x == -1 and food_y == -1) and (grid[x + dx[d]][y + dy[d]] == 0 or (x + dx[d] == snake[length-1][0] and y + dy[d] == snake[length-1][1])):
                if ok(x + dx[d], y + dy[d]) and (not(hamilton[x + dx[d]][y + dy[d]] == 0) or (x == 0 and y == 0)):
                    distance = dist_to_food(x + dx[d], y + dy[d])
                    if distance < dist:  # trying to make shortcuts in the hamiltonian cycle
                        if length / (grid_x * grid_y) <= 0.5:  # it's not optimal to make shortcuts if length is big
                            dist = distance
                            best = d
    if best != -1:
        direction = best
    if grid_x % 2 == 1 and grid_y % 2 == 1:  # alternating the hamiltonian cycles that the snake will follow (only if it is the case to change the hamiltonian cycle)
        if not(snake[0][0] == 1 and snake[0][1] == 1) and not(snake[0][0] == 0 and snake[0][1] == 2) and not(snake[0][0] == 1 and snake[0][1] == 2):
            if food_x == 1 and food_y == 1:
                hamilton[1][1] = grid_x * grid_y - 3
                hamilton[0][2] = 0
            if food_x == 0 and food_y == 2:
                hamilton[0][2] = grid_x * grid_y - 3
                hamilton[1][1] = 0


if mode == 0:    # snake player
    while StillSnaking and yey:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                StillSnaking = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    speed = max(speed - 1, 0)
                elif event.key == pygame.K_i:
                    speed = min(speed + 1, MaxSpeed)
                elif event.key == pygame.K_UP and moves[len(moves)-1] != 2:
                    moves += [0]
                elif event.key == pygame.K_RIGHT and moves[len(moves)-1] != 3:
                    moves += [1]
                elif event.key == pygame.K_DOWN and moves[len(moves)-1] != 0:
                    moves += [2]
                elif event.key == pygame.K_LEFT and moves[len(moves)-1] != 1:
                    moves += [3]
        if len(moves) >= 2:
            moves.pop(0)                                    # moves was made in order to not miss any keys
            direction = moves[0]                            # that are pressed really fast one after another
        last_x = -2
        last_y = -2
        move()
        draw_snake()
        draw_food()
        if speed < 10:
            pygame.time.Clock().tick(fps[speed])
        if length == grid_x * grid_y:
            break
    if yey == 1:
        style = pygame.font.SysFont("Chiller", 200)
        info = style.render("Congratulations! You won!", True, white)
        background.blit(info, (10, 10))
    else:
        style = pygame.font.SysFont("Chiller", 200)
        info = style.render("You died!", True, white)
        background.blit(info, (10, 10))
    style = pygame.font.SysFont("Chiller", 128)
    info = style.render("SnakeSoul was created and developed by", True, white)
    background.blit(info, (10, 600))
    style = pygame.font.SysFont("Chiller", 128)
    info = style.render("Gheorghe Liviu Armand", True, white)
    background.blit(info, (10, 750))
    pygame.display.update()
    while StillSnaking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                StillSnaking = 0
else:    # snake ai
    hamiltonian_cycle()
    while StillSnaking and yey:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                StillSnaking = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    speed = max(speed - 1, 0)
                elif event.key == pygame.K_i:
                    speed = min(speed + 1, MaxSpeed)

        think_next_move()    # AI

        if length == grid_x * grid_y:
            food_x = -1
            food_y = -1
        last_x = -2
        last_y = -2
        move()
        draw_snake()
        draw_food()
        if speed < 10:
            pygame.time.Clock().tick(fps[speed])
        if length == grid_x * grid_y:
            break
    if grid_x % 2 == 1 and grid_y % 2 == 1:
        style = pygame.font.SysFont("Chiller", 64)
        info = style.render("The AI aced the game!", True, white)
        background.blit(info, (10, 10))
        if background_y <= 700:
            style = pygame.font.SysFont("Chiller", 55)
            info = style.render("SnakeSoul was created and developed by", True, white)
            background.blit(info, (10, 500))
            style = pygame.font.SysFont("Chiller", 55)
            info = style.render("Gheorghe Liviu Armand", True, white)
            background.blit(info, (10, 600))
            pygame.display.update()
        else:
            style = pygame.font.SysFont("Chiller", 55)
            info = style.render("SnakeSoul was created and developed by", True, white)
            background.blit(info, (10, 700))
            style = pygame.font.SysFont("Chiller", 55)
            info = style.render("Gheorghe Liviu Armand", True, white)
            background.blit(info, (10, 800))
            pygame.display.update()
        while StillSnaking:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    StillSnaking = 0
    else:
        while StillSnaking and yey:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    StillSnaking = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        speed = max(speed - 1, 0)
                    elif event.key == pygame.K_i:
                        speed = min(speed + 1, MaxSpeed)

            think_next_move()  # ai

            if length == grid_x * grid_y:
                food_x = -1
                food_y = -1
            last_x = -2
            last_y = -2
            move()
            draw_snake2()
            draw_food()
            style = pygame.font.SysFont("Chiller", 200)
            info = style.render("The AI aced the game!", True, white)
            background.blit(info, (10, 10))
            style = pygame.font.SysFont("Chiller", 128)
            info = style.render("SnakeSoul was created and developed by", True, white)
            background.blit(info, (10, 600))
            style = pygame.font.SysFont("Chiller", 128)
            info = style.render("Gheorghe Liviu Armand", True, white)
            background.blit(info, (10, 750))
            pygame.display.update()
            pygame.display.update()
            if speed < 10:
                pygame.time.Clock().tick(fps[speed])

# Acesta este codul original pentru SnakeSoul, creat de catre Gheorghe Liviu Armand
