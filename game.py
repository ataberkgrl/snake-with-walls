import random
import pygame
import snake


class Game:
    def __init__(self, screen):
        self.score = 0
        self.screen = screen
        self.snake = snake.Snake(self.screen)
        self.food = None
        self.wall_list = None
        self.game_runs = True
        self.start_game()

    def start_game(self):
        self.get_board()
        self.get_walls()
        self.get_new_food()
        while self.game_runs:
            self.key_check()
            self.snake.snake_move()
            if self.collision():
                break
            else:
                pygame.display.update()
            if self.snake.eats_food(self.food):
                self.get_new_food()
                self.score += 10 + self.score / 50
                print(f"{self.score}")

    def get_walls(self):
        wall1 = pygame.draw.rect(self.screen, (255, 0, 0), (140, 120, 320, 20))
        wall2 = pygame.draw.rect(self.screen, (255, 0, 0), (140, 140, 20, 140))
        wall3 = pygame.draw.rect(self.screen, (255, 0, 0), (140, 280, 320, 20))
        wall4 = pygame.draw.rect(self.screen, (255, 0, 0), (440, 300, 20, 140))
        wall5 = pygame.draw.rect(self.screen, (255, 0, 0), (140, 440, 320, 20))
        self.wall_list = [wall1, wall2, wall3, wall4, wall5]

    def get_board(self):
        self.screen.fill((0, 0, 0))
        self.get_walls()

    def get_valid_food_position(self):
        food_pos = (random.randint(0, 29) * 20 + 10, random.randint(0, 29) * 20 + 10)
        while True:
            valid = True
            for x, y in self.snake.body_positions:
                for wall in self.wall_list:
                    if (x, y) == food_pos or wall.collidepoint(food_pos):
                        print("[LOG] INVALID food_pos GENERATING NEW ONE")
                        valid = False
            if valid:
                return food_pos
            else:
                food_pos = (random.randint(0, 29) * 20 + 10, random.randint(0, 29) * 20 + 10)

    def get_new_food(self):
        valid_food_pos = self.get_valid_food_position()
        self.food = pygame.draw.circle(self.screen, (0, 255, 0), valid_food_pos, 10, 0)

    def collision_with_wall(self):
        for wall in self.wall_list:
            if self.snake.head.colliderect(wall):
                return True

    def collision_with_body(self):
        for x, y in list(self.snake.body_positions)[0:self.snake.length - 1]:
            if (x, y) == self.snake.body_positions[self.snake.length - 1]:
                return True

    def collision(self):
        if self.collision_with_body() or self.collision_with_wall():
            return True
        else:
            return False

    def key_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_runs = False
            if event.type == pygame.KEYDOWN:
                self.snake.handle_key(event.key)