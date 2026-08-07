"""Generates a matrix-rain animated GIF for the GitHub profile README."""

import os

import random
from PIL import Image, ImageDraw, ImageFont

W, H = 640, 120
FONT_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_SIZE = 20
CELL_W, CELL_H = 22, 22
COLS = W // CELL_W
ROWS = H // CELL_H
FRAMES = 36
FPS = 12
GREEN = (0, 255, 65)
DIM = (0, 140, 34)
BLACK = (0, 0, 0)

CHARS = "01<>-_\\/[]{}=+*^?#abcdef"

random.seed(42)


class Drop:
    def __init__(self):
        self.reset(True)

    def reset(self, fresh=False):
        self.col = random.randrange(COLS)
        self.speed = random.randint(2, 5)
        self.head = random.randrange(ROWS) if fresh else random.randrange(ROWS + 8)
        self.visible = random.choice([True, True, False])
        self.bright = random.random() < 0.3

    def step(self):
        if random.random() < 0.03:
            self.reset()
            return
        self.head += self.speed / FPS
        if self.head - 6 > ROWS:
            self.reset()


drops = [Drop() for _ in range(COLS * 2)]

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


def frame():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    for drop in drops:
        if not drop.visible:
            continue
        col = drop.col
        for trail in range(7):
            row = int(drop.head - trail)
            if row < 0 or row >= ROWS:
                continue
            ch = random.choice(CHARS)
            if trail == 0:
                color = (255, 255, 255) if drop.bright else GREEN
            else:
                shade = max(0, 40 * (7 - trail))
                color = (0, max(60, 255 - shade), 0)
            x = col * CELL_W + 2
            y = row * CELL_H + 2
            d.text((x, y), ch, fill=color, font=font)
    return img


frames = [frame() for _ in range(FRAMES)]
os.makedirs("assets", exist_ok=True)
frames[0].save(
    "assets/matrix-rain.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1000 // FPS,
    loop=0,
    optimize=True,
)
print(f"OK assets/matrix-rain.gif — {FRAMES} frames, {W}x{H}")
