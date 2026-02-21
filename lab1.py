import pygame
import sys
import math
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабораторная работа 2")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)

colors = [
    BLACK,
    (255, 0, 0),
    (0, 200, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255)
]

current_color = BLACK
shapes = []

drawing = False
start_pos = (0, 0)
button = 0

clear_btn = pygame.Rect(WIDTH - 120, 10, 100, 30)


def get_group_center():
    sel = [s for s in shapes if s["selected"]]

    if not sel:
        return None

    x = sum(s["center"][0] for s in sel) / len(sel)
    y = sum(s["center"][1] for s in sel) / len(sel)

    return [x, y]


def scale_selected(f):
    c = get_group_center()

    if not c:
        return

    for s in shapes:
        if s["selected"]:
            dx = s["center"][0] - c[0]
            dy = s["center"][1] - c[1]

            s["center"][0] = c[0] + dx * f
            s["center"][1] = c[1] + dy * f

            s["width"] *= f
            s["height"] *= f


def rotate_selected(a_deg):
    c = get_group_center()

    if not c:
        return

    a = math.radians(a_deg)

    for s in shapes:
        if s["selected"]:
            dx = s["center"][0] - c[0]
            dy = s["center"][1] - c[1]

            s["center"][0] = c[0] + dx * math.cos(a) - dy * math.sin(a)
            s["center"][1] = c[1] + dx * math.sin(a) + dy * math.cos(a)

            s["angle"] += a_deg


def reflect_vertical():
    c = get_group_center()

    if not c:
        return

    for s in shapes:
        if s["selected"]:
            s["center"][0] = c[0] - (s["center"][0] - c[0])


def draw_shape(surf, s):
    temp = pygame.Surface((s["width"], s["height"]), pygame.SRCALPHA)

    if s["type"] == "rect":
        pygame.draw.rect(temp, s["color"], (0, 0, s["width"], s["height"]), 2)
    else:
        pygame.draw.ellipse(temp, s["color"], (0, 0, s["width"], s["height"]), 2)

    rotated = pygame.transform.rotate(temp, s["angle"])
    r = rotated.get_rect(center=s["center"])

    surf.blit(rotated, r)

    if s.get("selected"):
        pygame.draw.rect(surf, BLUE, r, 2)


def hit_test(pos):
    for s in reversed(shapes):
        rect = pygame.Rect(
            s["center"][0] - s["width"] / 2,
            s["center"][1] - s["height"] / 2,
            s["width"],
            s["height"]
        )

        if rect.collidepoint(pos):
            return s

    return None


while True:

    screen.fill(WHITE)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s:
                surf = pygame.Surface((WIDTH, HEIGHT))
                surf.fill(WHITE)

                for s in shapes:
                    draw_shape(surf, s)

                pygame.image.save(
                    surf,
                    f"drawing_{datetime.now().strftime('%H%M%S')}.png"
                )

            if event.key in [pygame.K_EQUALS, pygame.K_PLUS]:
                scale_selected(1.1)

            if event.key == pygame.K_MINUS:
                scale_selected(0.9)

            if event.key == pygame.K_r:
                reflect_vertical()

        if event.type == pygame.MOUSEWHEEL:
            rotate_selected(event.y * 5)

        if event.type == pygame.MOUSEBUTTONDOWN:

            if clear_btn.collidepoint(event.pos):
                shapes.clear()

            elif event.pos[1] <= 50:
                for i, c in enumerate(colors):
                    rect_color = pygame.Rect(10 + i * 50, 5, 40, 40)

                    if rect_color.collidepoint(event.pos):
                        current_color = c

            else:
                if event.button in [1, 3]:

                    hit = hit_test(event.pos)

                    if hit and event.button == 1:

                        if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            for s in shapes:
                                s["selected"] = False

                        hit["selected"] = not hit["selected"]

                    else:
                        drawing = True
                        start_pos = event.pos
                        button = event.button

        if event.type == pygame.MOUSEBUTTONUP and drawing:

            drawing = False

            x1, y1 = start_pos
            x2, y2 = event.pos

            shapes.append({
                "type": "rect" if button == 1 else "ellipse",
                "center": [(x1 + x2) / 2, (y1 + y2) / 2],
                "width": abs(x1 - x2),
                "height": abs(y1 - y2),
                "angle": 0,
                "color": current_color,
                "selected": False
            })

    for s in shapes:
        draw_shape(screen, s)

    if drawing:

        x1, y1 = start_pos
        x2, y2 = pygame.mouse.get_pos()

        draw_shape(screen, {
            "type": "rect" if button == 1 else "ellipse",
            "center": [(x1 + x2) / 2, (y1 + y2) / 2],
            "width": abs(x1 - x2),
            "height": abs(y1 - y2),
            "angle": 0,
            "color": current_color
        })

    for i, c in enumerate(colors):
        r = pygame.Rect(10 + i * 50, 5, 40, 40)
        pygame.draw.rect(screen, c, r)

        if c == current_color:
            pygame.draw.rect(screen, BLACK, r, 3)

    pygame.draw.rect(screen, (200, 200, 200), clear_btn)
    screen.blit(
        font.render("Очистить", True, BLACK),
        (clear_btn.x + 10, clear_btn.y + 7)
    )

    info = [
        "ЛКМ - прямоугольник/выделение",
        "ПКМ - эллипс",
        "Shift+ЛКМ - множественное выделение",
        "+/- - масштаб",
        "Колесо - поворот",
        "R - отражение",
        "S - сохранить PNG"
    ]

    for i, line in enumerate(info):
        screen.blit(
            font.render(line, True, BLACK),
            (10, HEIGHT - 140 + i * 20)
        )

    pygame.display.flip()
    clock.tick(60)