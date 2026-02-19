import pygame
import sys
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабораторная работа 1")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 200, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255)
]

current_color = BLACK
drawing = False
start_pos = (0, 0)
button = 0

shapes = []

clear_btn = pygame.Rect(WIDTH - 120, 10, 100, 30)

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                screen.fill(WHITE)

                for b, rect, color in shapes:
                    if b == 1:
                        pygame.draw.rect(screen, color, rect, 2)
                    if b == 3:
                        pygame.draw.ellipse(screen, color, rect, 2)

                pygame.display.flip()

                name = f"drawing_{datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(screen, name)


        if event.type == pygame.MOUSEBUTTONDOWN:
            if clear_btn.collidepoint(event.pos):
                shapes.clear()
            elif event.pos[1] <= 50:
                for i, c in enumerate(colors):
                    r = pygame.Rect(10 + i * 50, 5, 40, 40)
                    if r.collidepoint(event.pos):
                        current_color = c
            else:
                drawing = True
                start_pos = event.pos
                button = event.button

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            x1, y1 = start_pos
            x2, y2 = event.pos
            rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2))
            shapes.append((button, rect, current_color))

    for b, rect, color in shapes:
        if b == 1:
            pygame.draw.rect(screen, color, rect, 2)
        if b == 3:
            pygame.draw.ellipse(screen, color, rect, 2)

    if drawing:
        x1, y1 = start_pos
        x2, y2 = pygame.mouse.get_pos()
        rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2))
        if button == 1:
            pygame.draw.rect(screen, current_color, rect, 2)
        if button == 3:
            pygame.draw.ellipse(screen, current_color, rect, 2)

    for i, c in enumerate(colors):
        r = pygame.Rect(10 + i * 50, 5, 40, 40)
        pygame.draw.rect(screen, c, r)
        if c == current_color:
            pygame.draw.rect(screen, BLACK, r, 3)

    pygame.draw.rect(screen, (200,200,200), clear_btn)
    screen.blit(font.render("Очистить", True, BLACK), (clear_btn.x+10, clear_btn.y+7))

    info = [
        "ЛКМ - прямоугольник",
        "ПКМ - эллипс",
        "Выбор цвета - сверху",
        "Очистить - удалить всё",
        "S - сохранить PNG"
    ]

    for i, line in enumerate(info):
        screen.blit(font.render(line, True, BLACK), (10, HEIGHT - 110 + i*20))

    pygame.display.flip()
    clock.tick(60)
