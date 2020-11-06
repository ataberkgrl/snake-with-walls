import collections
import time
import pygame


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.body_positions = collections.deque()
        self.body_positions.append((500, 500))
        self.last_position = None
        self.direction = (1, 0)  # DEFAULT RIGHT
        self.length = 1
        self.slow_list = [0.4, 0.1]
        self.slow = 0.4
        self.head = None  # WILL BE INITIALIZED AFTER update_snake() FUNCTION
        self.changing_direction = False
        self.eating_food = False

    def handle_key(self, pressed_key):

        # WITHOUT changing_direction CHECK, PLAYER IS ABLE TO
        # CHANGE ITS DIRECTION 2 TIMES WITH QUICK KEYPRESS BEFORE
        # SNAKE RECT UPDATES, WHICH ALLOWS PLAYER TO TURN BACK
        if not self.changing_direction:
            self.changing_direction = True
            if (pressed_key == pygame.K_LEFT or pressed_key == pygame.K_a) and self.direction != (1, 0):
                self.direction = (-1, 0)  # LEFT
            elif (pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_d) and self.direction != (-1, 0):
                self.direction = (1, 0)  # RIGHT
            elif (pressed_key == pygame.K_UP or pressed_key == pygame.K_w) and self.direction != (0, 1):
                self.direction = (0, -1)  # UP
            elif (pressed_key == pygame.K_DOWN or pressed_key == pygame.K_s) and self.direction != (0, -1):
                self.direction = (0, 1)  # DOWN
            elif pressed_key == pygame.K_SPACE:  # SPEED UP SNAKE
                if self.slow == self.slow_list[0]:
                    self.slow = self.slow_list[1]
                elif self.slow == self.slow_list[1]:
                    self.slow = self.slow_list[0]

    def snake_move(self):
        if not self.eating_food:
            time.sleep(self.slow)
            new_position_x = self.body_positions[self.length - 1][0] + 20 * self.direction[0]
            if new_position_x < 0:  # MOVE FROM BORDER TO BORDER FOR X AXIS
                new_position_x = 600 + new_position_x
            elif new_position_x >= 600:
                new_position_x = new_position_x - 600
            new_position_y = self.body_positions[self.length - 1][1] + 20 * self.direction[1]
            if new_position_y < 0:  # MOVE FROM BORDER TO BORDER FOR Y AXIS
                new_position_y = 600 + new_position_y
            elif new_position_y >= 600:
                new_position_y = new_position_y - 600
            self.body_positions.append((new_position_x, new_position_y))
            self.last_position = self.body_positions.popleft()
        else:
            self.eating_food = False
        self.update_snake()

    def update_snake(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.last_position[0], self.last_position[1], 20, 20))
        for x, y in self.body_positions:
            self.head = pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 20, 20))
        if self.changing_direction:
            self.changing_direction = False

    def check_food(self, food):
        if self.head.colliderect(food):
            return True

    def eats_food(self, food):
        #  ADDS NEW BODY PART TO THE TAIL OF SNAKE AFTER
        #  MOVEMENT WHICH AVOIDS UNEXPECTED COLLISIONS
        if self.check_food(food):
            self.eating_food = True
            new_tail_x = self.body_positions[0][0] - 20 * self.direction[0]
            new_tail_y = self.body_positions[0][1] - 20 * self.direction[1]
            self.body_positions.appendleft((new_tail_x, new_tail_y))
            self.length += 1
            if self.slow > 0.1:
                self.slow_list[0] = self.slow = self.slow - 0.01
                print(f"[LOG] SLOW MULTIPLIER: {self.slow}")
            print(f"[LOG] Eaten food new length: {self.length}")
            return True

    def collides_with_body(self):
        for x, y in list(self.body_positions)[0:self.length - 1]:
            if (x, y) == self.body_positions[self.length - 1]:
                return True
