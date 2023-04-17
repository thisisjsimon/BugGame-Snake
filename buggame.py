import pygame, sys, random
from pygame.math import Vector2
import json

class BUG:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_bug(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)

            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
            
    def move_bug(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

class Food:
    def __init__(self):
        self.randomize()
    
    def draw_food(self):
        food_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(meal, food_rect)
        #pygame.draw.rect(screen,(126,166,114),food)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        
class MAIN:
    def __init__(self):
        self.bug = BUG()
        self.food = Food()
        self.highscore = self.load_highscore()
        self.show_score = True
        
        self.circuit_board = pygame.image.load('Graphics/circuit_board.jpg').convert_alpha()

    def update(self):
        self.bug.move_bug()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_background()
        self.food.draw_food()
        self.bug.draw_bug()
        self.draw_score()

    def check_collision(self):
        if self.food.pos == self.bug.body[0]:
            self.food.randomize()
            self.bug.add_block()
            self.bug.play_crunch_sound()
        
        for block in self.bug.body[1:]:
            if block == self.food.pos:
                self.food.randomize()

    def check_fail(self):
        if not 0 <= self.bug.body[0].x < cell_number or not 0 <= self.bug.body[0].y < cell_number:
            self.game_over()

        for block in self.bug.body[1:]:
            if block == self.bug.body[0]:
                self.game_over()

    def restart_game(self):
        START()

    def game_over(self):
        game_over_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 100)
        game_over_surface = game_over_font.render('GAME OVER', True, (32, 32, 32))
        game_over_rect = game_over_surface.get_rect(center=(int(cell_size * cell_number / 2), int(cell_size * cell_number / 2) - 30))
        screen.blit(game_over_surface, game_over_rect)
        restart_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        restart_surface = restart_font.render('Press (r) to reboot', True, (32, 32, 32))
        restart_rect = restart_surface.get_rect(center=(int(cell_size * cell_number / 2), int(cell_size * cell_number / 2) + 45))
        screen.blit(restart_surface, restart_rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                        return
                
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def draw_background(self):
        screen.blit(self.circuit_board, (0, 0))

    def draw_score(self):
        if len(self.bug.body) -3 > self.highscore:
            self.highscore = len(self.bug.body) - 3
            self.save_highscore((len(self.bug.body) -3))
        if self.show_score:
            score_text = str(len(self.bug.body) - 3)
        else:
            score_text = str(self.highscore)


        score_surface = game_font.render(score_text,True,(0,0,0))


        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))

        if self.show_score:
            meal_rect = meal.get_rect(midright = (score_rect.left,score_rect.centery))
            bg_rect = pygame.Rect(meal_rect.left,meal_rect.top,meal_rect.width + score_rect.width + 6,meal_rect.height)
        else:
            trophy_rect = trophy.get_rect(midright = (score_rect.left,score_rect.centery))
            bg_rect = pygame.Rect(trophy_rect.left,trophy_rect.top,trophy_rect.width + score_rect.width + 6,trophy_rect.height)

        pygame.draw.rect(screen,(255,255,255),bg_rect)
        screen.blit(score_surface,score_rect)

        if self.show_score:
            screen.blit(meal,meal_rect)
            pygame.draw.rect(screen,(56,74,12),bg_rect,2)
        else:
            screen.blit(trophy,trophy_rect)
            pygame.draw.rect(screen,(56,74,12),bg_rect,2)

        self.bg_rect = bg_rect
        
    def toggle_score_display(self):
        self.show_score = not self.show_score
        
    def load_highscore(self):
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
                return data["highscore"]
        except:
            return 0
        
    def save_highscore(self, new_highscore):
        data = {"highscore": new_highscore}
        with open("highscore.json", "w") as f:
            json.dump(data, f)

pygame.init()
pygame.display.set_caption('BugGame')

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
icon = pygame.image.load('Graphics/head_up.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
meal = pygame.image.load('Graphics/meal.png').convert_alpha()
trophy = pygame.image.load('Graphics/trophy.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

def START():
    main_game = MAIN()
    key_buffer = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SCREEN_UPDATE:
                main_game.update()
            elif event.type == pygame.KEYDOWN:
                if event.key not in key_buffer:
                    key_buffer.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in key_buffer:
                    key_buffer.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if main_game.bg_rect.collidepoint(mouse_pos):
                    main_game.toggle_score_display()

        if pygame.K_UP in key_buffer:
            if main_game.bug.direction.y != 1:
                main_game.bug.direction = Vector2(0, -1)
        if pygame.K_RIGHT in key_buffer:
            if main_game.bug.direction.x != -1:
                main_game.bug.direction = Vector2(1, 0)
        if pygame.K_DOWN in key_buffer:
            if main_game.bug.direction.y != -1:
                main_game.bug.direction = Vector2(0, 1)
        if pygame.K_LEFT in key_buffer:
            if main_game.bug.direction.x != 1:
                main_game.bug.direction = Vector2(-1, 0)

        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)


START()