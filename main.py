import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys, pygame
pygame.init()
import numpy
rng = numpy.random.default_rng()

screen_size = screen_width, screen_height = 640, 480
FPS = 30

class Size:
    small = 0
    big = 1

class Color:
    red = 0
    green = 1
    blue = 2

class Shape:
    triangle = 0
    rectangle = 1
    circle = 2

    __create_key = object()

    @classmethod
    def create(cls, pos, speed, shape, color: int, size: int):
        return Shape(cls.__create_key, pos, speed, shape, color, size)
    @classmethod
    def create_triangle(cls, pos, speed, color: int, size: int):
        return Shape(cls.__create_key, pos, speed, Shape.triangle, color, size)
    @classmethod
    def create_rectangle(cls, pos, speed, color: int, size: int):
        return Shape(cls.__create_key, pos, speed, Shape.rectangle, color, size)
    @classmethod
    def create_circle(cls, pos, speed, color: int, size: int):
        return Shape(cls.__create_key, pos, speed, Shape.circle, color, size)

    def __init__(self, create_key, pos, speed, shape: str, color: int, size: int):
        assert(create_key == Shape.__create_key), \
            "Shape objects must be created using Shape.create, Shape.create_triangle, Shape.create_rectangle, or Shape.create_circle"

        self.size = size
        self.__size = 24
        if (self.size == Size.small):
            self.__size = 18
        elif (self.size == Size.big):
            self.__size = 30
        self.__rect = pygame.Rect(pos, (self.__size, self.__size))

        self.shape = shape
        self.speed = speed

        self.color = color
        self.__color = (0, 0, 0)
        if (self.color == Color.red):
            self.__color = (255, 0, 0)
        elif (self.color == Color.green):
            self.__color = (0, 255, 0)
        elif (self.color == Color.blue):
            self.__color = (0, 0, 255)

    def draw(self, screen):
        rect = self.__rect
        if (self.shape == Shape.triangle):
            pygame.draw.polygon(screen, self.__color, (rect.midtop, rect.bottomleft, rect.bottomright))
        elif (self.shape == Shape.rectangle):
            pygame.draw.rect(screen, self.__color, rect)
        elif (self.shape == Shape.circle):
            pygame.draw.circle(screen, self.__color, rect.center, self.__size / 2)

    def move(self):
        self.__rect.move_ip(self.speed)
        if self.__rect.left < 0 or self.__rect.right > screen_width:
            self.speed[0] = -self.speed[0]
        if self.__rect.top < 0 or self.__rect.bottom > screen_height:
            self.speed[1] = -self.speed[1]

def main():
    white = 255, 255, 255
    
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Phocushapes')
    font = pygame.font.Font(None, 25)
    
    clock = pygame.time.Clock()
    score = 0
    max_view_time = 5 * FPS
    view_time = max_view_time - 1 * FPS
    shape_count = 5
    viewing_shapes = False
    in_menu = True
    question = "What?"
    options = ["Yes", "No", "What?", "Yes"]
    correct_option = 0
    click_pos = None
    shapes = []
    shape_counts = [0] * 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                click_pos = pygame.mouse.get_pos()
        
        screen.fill(white)
        text_surface = font.render(str(score), True, (0, 0, 0))
        screen.blit(text_surface, (screen_width//2 - text_surface.get_rect().centerx, 0))
        if viewing_shapes:
            for shape in shapes:
                shape.move()
                shape.draw(screen)
            view_time += 1
            if (view_time >= max_view_time):
                view_time = 0
                viewing_shapes = False
                shape_right = random.randint(0, 2)
                question = f'How many {(["triangles", "rectangles", "circles"])[shape_right]} were there?'
                options = [""] * 4
                correct_option = random.randint(0, 3)
                correct = shape_counts[shape_right]
                for i in range(4):
                    if (i != correct_option):
                        if (random.randint(0, 1) == 0):
                            options[i] = str(correct - i - 1)
                        else:
                            options[i] = str(correct + i + 1)
                    else:
                        options[i] = str(correct)
        else:
            if in_menu:
                viewing_shapes = True
                in_menu = False
                view_time = 0
                shape_count = 5
                score = 0
                shapes = []
                shape_counts = [0] * 3
                for i in range(0, shape_count):
                    pos = [random.randint(0, screen_width - 30), random.randint(0, screen_height - 30)]
                    speed = rng.normal(0, 3, 2)
                    shape = random.randint(0, 2)
                    color = random.randint(0, 2)
                    size = random.randint(0, 1)
                    shape_counts[shape] += 1
                    shapes.append(Shape.create(pos, speed, shape, color, size))
            else:
                text_surface = font.render(question, True, (0, 0, 0))
                screen.blit(text_surface, (screen_width//2 - text_surface.get_rect().centerx, screen_height // 3.5))
                for i, option in enumerate(options):
                    text_surface = font.render(option, True, (0, 0, 0))
                    rect = pygame.Rect((screen_width // 2 - 50, screen_height * 2 // 3.5 + i * 35 - 5), (100, 30))
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                    screen.blit(text_surface, (screen_width // 2 - text_surface.get_rect().centerx, screen_height * 2 // 3.5 + i * 35))


                    if (click_pos is not None):
                        if rect.collidepoint(click_pos):
                            if (i == correct_option):
                                score += 1
                                shapes = []
                                shape_counts = [0] * 3
                                for i in range(0, shape_count):
                                    pos = [random.randint(0, screen_width - 30), random.randint(0, screen_height - 30)]
                                    speed = rng.normal(0, 3, 2)
                                    shape = random.randint(0, 2)
                                    color = random.randint(0, 2)
                                    size = random.randint(0, 1)
                                    shape_counts[shape] += 1
                                    shapes.append(Shape.create(pos, speed, shape, color, size))
                                shape_count += 2
                                viewing_shapes = True
                            else:
                                in_menu = True

        pygame.display.flip()
        click_pos = None
        clock.tick(FPS)

if __name__ == "__main__":
    main()
