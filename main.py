#!/usr/bin/env python3
"""THE WORLD - front page for Sunday 22 November 2026.

Draws a newspaper front page summing up the day's world news,
using only the Python standard library. No network, no files read,
no timestamps, no randomness: every run writes identical bytes.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import math
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (163, 22, 33)
SEA = (52, 110, 165)
LAND = (46, 125, 50)
GOLD = (201, 162, 39)
GREY = (88, 88, 88)
DARK = (40, 40, 48)
ORANGE = (232, 122, 30)
YELLOW = (250, 204, 60)
WHITE = (255, 255, 255)

# 5x7 bitmap letterforms: 7 rows of 5 characters, '1' = ink.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '\u2022': ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x, y, length, color, thick=1):
        self.fill_rect(x, y, length, thick, color)

    def vline(self, x, y, length, color, thick=1):
        self.fill_rect(x, y, thick, length, color)

    def rect(self, x, y, w, h, color, thick=1):
        self.hline(x, y, w, color, thick)
        self.hline(x, y + h - thick, w, color, thick)
        self.vline(x, y, h, color, thick)
        self.vline(x + w - thick, y, h, color, thick)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill_rect(x0, y0, thick, thick, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.hline(cx - dx, cy + dy, 2 * dx + 1, color)

    def circle_outline(self, cx, cy, r, color, thick=2):
        steps = max(48, r * 4)
        for i in range(steps):
            a = 2.0 * math.pi * i / steps
            x = int(round(cx + r * math.cos(a)))
            y = int(round(cy + r * math.sin(a)))
            self.fill_rect(x, y, thick, thick, color)

    def ellipse_outline(self, cx, cy, rx, ry, color):
        steps = 160
        for i in range(steps):
            a = 2.0 * math.pi * i / steps
            x = int(round(cx + rx * math.cos(a)))
            y = int(round(cy + ry * math.sin(a)))
            self.set(x, y, color)

    def fill_ellipse(self, cx, cy, rx, ry, color):
        for dy in range(-ry, ry + 1):
            t = 1.0 - (dy * dy) / float(ry * ry)
            dx = int(rx * (t ** 0.5)) if t > 0 else 0
            self.hline(cx - dx, cy + dy, 2 * dx + 1, color)


def text_width(text, scale):
    return max(0, len(text) * 6 * scale - scale)


def draw_text(cv, x, y, scale, text, color):
    cx = x
    for ch in text:
        glyph = FONT.get(ch.upper(), FONT[' '])
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == '1':
                    cv.fill_rect(cx + c * scale, y + r * scale,
                                 scale, scale, color)
        cx += 6 * scale
    return cx


def center_text(cv, cx, y, scale, text, color):
    draw_text(cv, cx - text_width(text, scale) // 2, y, scale, text, color)


def right_text(cv, x_right, y, scale, text, color):
    draw_text(cv, x_right - text_width(text, scale), y, scale, text, color)


def wrap(text, max_w, scale):
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(cv, cx, cy, r):
    cv.fill_circle(cx, cy, r, SEA)
    # Land masses, all kept inside the circle.
    cv.fill_circle(cx - 30, cy - 35, 26, LAND)
    cv.fill_circle(cx + 15, cy + 15, 20, LAND)
    cv.fill_circle(cx - 15, cy + 45, 16, LAND)
    cv.fill_circle(cx + 30, cy - 35, 12, LAND)
    cv.fill_circle(cx - 40, cy + 15, 12, LAND)
    cv.fill_ellipse(cx + 2, cy - 52, 22, 10, LAND)
    # Latitude lines and meridian.
    for dy in (-50, -25, 0, 25, 50):
        dx = int((r * r - dy * dy) ** 0.5)
        cv.hline(cx - dx, cy + dy, 2 * dx + 1, WHITE)
    cv.ellipse_outline(cx, cy, 45, r, WHITE)
    cv.vline(cx, cy - r, 2 * r + 1, WHITE)
    cv.circle_outline(cx, cy, r, INK, 3)
    # Small sun above the globe.
    sx, sy = cx + r - 6, cy - r - 4
    cv.fill_circle(sx, sy, 12, GOLD)
    for i in range(8):
        a = 2.0 * math.pi * i / 8.0
        x1 = int(round(sx + 16 * math.cos(a)))
        y1 = int(round(sy + 16 * math.sin(a)))
        x2 = int(round(sx + 24 * math.cos(a)))
        y2 = int(round(sy + 24 * math.sin(a)))
        cv.line(x1, y1, x2, y2, GOLD, 2)


def draw_skyline(cv, x0, y0, x1, y1):
    # Dark skyline silhouettes with lit windows, and a burst above.
    buildings = [
        (0, 62, 34, 96), (36, 40, 30, 118), (68, 78, 36, 80),
        (106, 28, 32, 130), (140, 58, 30, 100), (172, 84, 36, 74),
        (210, 48, 28, 110),
    ]
    for bi, (bx, top, bw, bh) in enumerate(buildings):
        bx += x0
        cv.fill_rect(bx, y0 + top, bw, bh, DARK)
        # Pitched roof on two buildings, antenna on the tallest.
        if bi == 1:
            cv.line(bx, y0 + top, bx + bw // 2, y0 + top - 14, DARK, 3)
            cv.line(bx + bw // 2, y0 + top - 14, bx + bw, y0 + top, DARK, 3)
        if bi == 3:
            cv.vline(bx + bw // 2, y0 + top - 18, 18, DARK, 3)
            cv.fill_circle(bx + bw // 2, y0 + top - 20, 3, RED)
        for wy in range(y0 + top + 10, y0 + top + bh - 8, 16):
            for wx in range(bx + 7, bx + bw - 6, 14):
                if (wx + wy) % 28 == 0:
                    cv.fill_rect(wx, wy, 3, 3, YELLOW)
    # Explosion burst above the skyline.
    bx, by = x0 + 118, y0 + 18
    for i in range(12):
        a = 2.0 * math.pi * i / 12.0
        ln = 34 if i % 2 == 0 else 22
        x2 = int(round(bx + ln * math.cos(a)))
        y2 = int(round(by + ln * math.sin(a)))
        cv.line(bx, by, x2, y2, ORANGE, 3)
    cv.fill_circle(bx, by, 11, RED)
    cv.fill_circle(bx, by, 5, YELLOW)


def draw_front_page(cv):
    cv.fill_rect(0, 0, W, H, PAPER)
    cv.rect(10, 10, W - 20, H - 20, INK, 3)
    cv.rect(18, 18, W - 36, H - 36, INK, 1)

    # Masthead.
    center_text(cv, W // 2, 28, 12, "THE WORLD", INK)
    cv.hline(30, 118, W - 60, INK, 2)
    cv.hline(30, 123, W - 60, INK, 1)

    # Dateline row.
    draw_text(cv, 30, 134, 2, "WORLD EDITION", INK)
    center_text(cv, W // 2, 134, 4, "SUNDAY 22 NOVEMBER 2026", INK)
    right_text(cv, W - 30, 134, 2, "NO. 326", INK)
    cv.hline(30, 170, W - 60, INK, 2)

    # Lead story: COP31.
    draw_text(cv, 30, 182, 2, "CLIMATE SUMMIT - COP31", RED)
    draw_text(cv, 30, 204, 7, "COP31 NEARS", INK)
    draw_text(cv, 30, 258, 7, "FINAL DEAL", INK)
    deck = ("SUMMIT PRESIDENT SAYS TALKS ARE CLOSE TO A FINAL DEAL "
            "AS THE CLIMATE SUMMIT CLOSES.")
    for i, ln in enumerate(wrap(deck, 600, 3)):
        draw_text(cv, 30, 316 + i * 26, 3, ln, INK)
    draw_globe(cv, 830, 285, 98)

    cv.hline(30, 402, W - 60, INK, 2)

    # Second lead: missile strike in Ukraine.
    draw_text(cv, 30, 414, 2, "UKRAINE", RED)
    draw_text(cv, 30, 434, 5, "MISSILE STRIKE HITS", INK)
    draw_text(cv, 30, 472, 5, "ZELENSKYY'S HOMETOWN", INK)
    deck2 = ("A BALLISTIC MISSILE ATTACK ON THE PRESIDENT'S HOMETOWN "
             "IN CENTRAL UKRAINE KILLS 2 AND WOUNDS SCORES.")
    for i, ln in enumerate(wrap(deck2, 720, 2)):
        draw_text(cv, 30, 516 + i * 18, 2, ln, INK)
    draw_skyline(cv, 770, 420, 994, 566)

    cv.hline(30, 580, W - 60, INK, 2)

    # Section header.
    center_text(cv, W // 2, 592, 3, "AROUND THE WORLD", INK)
    cv.hline(30, 602, 320, INK, 1)
    cv.hline(674, 602, 320, INK, 1)

    # Two-column story grid: kicker + one-line headline.
    stories = [
        ("NIGERIA", "BOAT CAPSIZES, 24 DEAD"),
        ("BRAZIL", "STORM TOWN CLEARS RUBBLE"),
        ("PERU", "6.7 QUAKE SHAKES PERU"),
        ("DEFENCE", "PENTAGON CURBS CANADA TIES"),
        ("TRUMP", "TRUMP VOWS 10% CARD CAP"),
        ("FRANCE", "SIXTH WEEKEND OF PROTESTS"),
        ("BELGIUM", "BELGIUM AIR SHUTDOWN LOOMS"),
        ("TECH", "NVIDIA FACES US PROBE"),
        ("ROHINGYA", "GENOCIDE VERDICT HAILED"),
        ("HOUTHIS", "HOUTHI STRIKES HIT RIYADH"),
        ("IRAN", "IRAN HITS THREE TANKERS"),
        ("SOUTH AFRICA", "G20 OPENS IN JOHANNESBURG"),
    ]
    top = 624
    pitch = 48
    for i, (kicker, headline) in enumerate(stories):
        col = i // 6
        row = i % 6
        x = 30 if col == 0 else 524
        y = top + row * pitch
        draw_text(cv, x, y, 2, kicker, RED)
        draw_text(cv, x, y + 16, 3, headline, INK)
    cv.vline(512, top, 6 * pitch - 8, INK, 1)

    # Bottom strip: one-line headlines for the remaining stories.
    cv.hline(30, 922, W - 60, INK, 2)
    tickers = [
        "TAIWAN WARNS CARNEY ON CHINA TIES  \u2022  KIM VISITS FACTORIES AFTER TRUMP SNUB",
        "11 DEAD FROM TAINTED ALCOHOL IN INDIA  \u2022  LEE: SPEED DECISIVE IN AI RACE",
        "PROTESTS HIT META OFFICES IN INDIA  \u2022  WILDBERRIES CEO QUITS AFTER EU SANCTIONS",
        "SENATE DEMOCRATS FACE AN EARLY LEADERSHIP TEST",
    ]
    for i, ln in enumerate(tickers):
        draw_text(cv, 30, 932 + i * 19, 2, ln, INK)


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    data = zlib.compress(bytes(raw), 9)

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        out += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", data)
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    cv = Canvas(W, H, PAPER)
    draw_front_page(cv)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(png_bytes(cv))


if __name__ == "__main__":
    main()
