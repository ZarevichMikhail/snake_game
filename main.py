import pygame as pg
from random import randrange


WINDOW_SIZE = 600
TILE_SIZE = 50 # размер квадратной ячейки
INITIAL_TIME_STEP = 150

# Переменные отвечающие за то, чтобы еда и змейка спавнились в игровом поле
# и их центры находились в квадратных ячейках
RANGE = (TILE_SIZE//2, WINDOW_SIZE - TILE_SIZE//2, TILE_SIZE)
get_random_position = lambda: (randrange(*RANGE), randrange(*RANGE))

# Настройки змейки
snake_head = pg.rect.Rect([0, 0, TILE_SIZE-2, TILE_SIZE-2])
snake_head.center = get_random_position()
length = 1
segments = [snake_head.copy()] # Список, в котором хранятся все части тела змейки
snake_move_dir = (0,0)


time = 0
time_step = INITIAL_TIME_STEP

# Настройки еды
food = snake_head.copy()
food.center = get_random_position()

screen = pg.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
clock = pg.time.Clock()

# Доступные направления движения
possible_move_dirs = {pg.K_w: 1, pg.K_s:1, pg.K_a: 1, pg.K_d: 1}

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        # Движение змейки
        if event.type == pg.KEYDOWN:
            # Если змейка двигается вверх, то она не может изменить напрпавление,
            # чтобы двигаться вниз.
            if event.key == pg.K_w and possible_move_dirs[pg.K_w] == 1:
                snake_move_dir = (0, -TILE_SIZE)
                possible_move_dirs = {pg.K_w: 1, pg.K_s:0, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_s and possible_move_dirs[pg.K_s] == 1:
                snake_move_dir = (0, TILE_SIZE)
                possible_move_dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_a and possible_move_dirs[pg.K_a] == 1:
                snake_move_dir = (-TILE_SIZE, 0)
                possible_move_dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}

            if event.key == pg.K_d and possible_move_dirs[pg.K_d] == 1:
                snake_move_dir = (TILE_SIZE, 0)
                possible_move_dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    screen.fill("black")

    # Draw snake
    #[pg.draw.rect(screen, "green", segment) for segment in segments]
    for segment in segments:
        pg.draw.rect(screen, "green", segment)

    # Draw food
    pg.draw.rect(screen, "red", food)

    # Движение змейки
    # Также скорость можно поменять просто уменьшив clock.tick
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        # move_in_place.
        # Берёт текущие координаты головы и прибавляет к ним координату направления движения
        snake_head.move_ip(snake_move_dir)

        # Мы двигаем голову вперёд, сохраняем её новую позицию в список
        # и удаляем из списка самое старое положение хвоста,
        segments.append(snake_head.copy()) # добавляет элемент в начало списка
        segments = segments[-length:] # убирает последний элемент




    # Взаимодействие змейки и еды
    # Увеличение длины змейки и увеличение скорости движения
    if snake_head.center == food.center:
        food.center = get_random_position()

        # Проверка на то, что еда не появилась в змейке
        i = 0
        while i < len(segments):
            if food.center == segments[i].center:
                food.center = get_random_position()
                i = 0
            else:
                i = i + 1

        length +=1
        time_step = time_step - 5

    # Проверка на то, что змейка не вышла за игровое поле
    # и на коллизию со своим хвостом
    self_collision = pg.Rect.collidelist(snake_head, segments[:-1]) != -1
    if ((snake_head.left < 0 or snake_head.right > WINDOW_SIZE)
            or (snake_head.top < 0 or snake_head.bottom > WINDOW_SIZE)
            or self_collision):
        # Если змейка выходит за игровое поле или ест себя, игра сбрасывается
        # Змейка и еда занимают случайное положение, длина становится 1
        # Сбрасывается скорость движения
        snake_head.center = get_random_position()
        length = 1
        snake_move_dir = (0, 0)
        segments = [snake_head.copy()]
        food.center = get_random_position()

        time_step = INITIAL_TIME_STEP

    pg.display.flip()
    clock.tick(60) # Устанавливаем ФПС на 60 кадров в секунду
