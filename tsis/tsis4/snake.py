import pygame
import random

WIDTH, HEIGHT = 1520, 840
CELL = 20


class sn:
    def __init__(self, x, y, color):
        self.element = [[x, y]]
        self.dx = CELL
        self.dy = 0
        self.grow = False
        self.color = color

    def draw(self, screen):
        for part in self.element:
            pygame.draw.rect(screen, self.color, (part[0], part[1], CELL, CELL))

    def move(self):
        if self.grow:
            self.element.append([0, 0])
            self.element.append([0, 0])
            self.grow = False

        for i in range(len(self.element) - 1, 0, -1):
            self.element[i][0] = self.element[i - 1][0]
            self.element[i][1] = self.element[i - 1][1]

        self.element[0][0] += self.dx
        self.element[0][1] += self.dy

    def eat(self, x, y):
        head = self.element[0]
        return head[0] == x and head[1] == y

    def self_collision(self):
        head = self.element[0]
        return head in self.element[1:]

    def cut(self, count):
        for _ in range(count):
            if len(self.element) > 1:
                self.element.pop()


class Food:
    def __init__(self, kind="normal"):
        self.kind = kind
        self.weight = 1
        self.x = 0
        self.y = 0
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 7000
        self.gen([], [])

    def gen(self, snake_body, obstacles):
        while True:
            self.x = random.randrange(0, WIDTH, CELL)
            self.y = random.randrange(0, HEIGHT, CELL)

            if [self.x, self.y] not in snake_body and [self.x, self.y] not in obstacles:
                break

        self.spawn_time = pygame.time.get_ticks()

        if self.kind == "normal":
            self.weight = random.choice([1, 2, 3])
        else:
            self.weight = 0

    def expired(self):
        now = pygame.time.get_ticks()
        return now - self.spawn_time > self.life_time

    def draw(self, screen):
        if self.kind == "poison":
            color = (120, 0, 0)
        elif self.weight == 1:
            color = (255, 0, 255)
        elif self.weight == 2:
            color = (255, 200, 0)
        else:
            color = (0, 255, 255)

        pygame.draw.rect(screen, color, (self.x, self.y, CELL, CELL))


class PowerUp:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = random.choice(["speed", "slow", "shield"])
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 8000

    def gen(self, snake_body, obstacles, foods):
        while True:
            self.x = random.randrange(0, WIDTH, CELL)
            self.y = random.randrange(0, HEIGHT, CELL)

            food_positions = []
            for food in foods:
                food_positions.append([food.x, food.y])

            if [self.x, self.y] not in snake_body and [self.x, self.y] not in obstacles and [self.x, self.y] not in food_positions:
                break

        self.type = random.choice(["speed", "slow", "shield"])
        self.spawn_time = pygame.time.get_ticks()

    def expired(self):
        now = pygame.time.get_ticks()
        return now - self.spawn_time > self.life_time

    def draw(self, screen):
        if self.type == "speed":
            color = (0, 0, 255)
        elif self.type == "slow":
            color = (255, 255, 255)
        else:
            color = (0, 255, 0)

        pygame.draw.rect(screen, color, (self.x, self.y, CELL, CELL))