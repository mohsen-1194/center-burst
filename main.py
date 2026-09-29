import math
from dataclasses import dataclass
from random import randint

from PIL import Image, ImageDraw

PAGE_WIDTH = 800
PAGE_HEIGHT = 800
PIXELS = 15
BORDER_START = 0
BORDER_END = PAGE_WIDTH - 1
N_PATHS = 50


@dataclass
class Point:
    x: int
    y: int


CENTER = Point(399, 399)  # it's not precise(off by half a pixel)


def draw_line(
    d: ImageDraw.ImageDraw, last_p: Point, next_p: Point, color: tuple[int, ...]
) -> None:
    d.line([(last_p.x, last_p.y), (next_p.x, next_p.y)], fill=color, width=2)


def is_collide_border(p: Point) -> bool:
    return bool(p.x <= BORDER_START or p.x >= BORDER_END) or bool(
        p.y <= BORDER_START or p.y >= BORDER_END
    )


def is_farther_from_center(lpoint: Point, npoint: Point) -> bool:
    d1 = math.dist((lpoint.x, lpoint.y), (CENTER.x, CENTER.y))
    d2 = math.dist((npoint.x, npoint.y), (CENTER.x, CENTER.y))
    return d2 > d1


def next_point(p: Point) -> Point:
    x = randint((p.x - PIXELS), (p.x + PIXELS))
    y = randint((p.y - PIXELS), (p.y + PIXELS))
    next_p = Point(x, y)
    return next_p


def main():
    page = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color="white")
    draw = ImageDraw.Draw(page)
    draw.point((CENTER.x, CENTER.y), fill="black")

    for _ in range(N_PATHS):
        color = tuple(randint(20, 200) for _ in range(3))
        last_p = Point(CENTER.x, CENTER.y)

        while not is_collide_border(last_p):
            next_p = next_point(last_p)
            result = is_farther_from_center(last_p, next_p)
            if result:
                draw_line(draw, last_p, next_p, color)
                last_p = next_p

    page.save("center-burst.png")


if __name__ == "__main__":
    main()
