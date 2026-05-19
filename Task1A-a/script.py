#!/usr/bin/env python3
import cv2
import numpy as np


def analyze_arena(input_image):

    # ==========================================
    # LOAD IMAGE
    # ==========================================

    image = cv2.imread(input_image)

    if image is None:

        print("Error loading image.")
        return {}

    # ==========================================
    # INITIALIZE OUTPUT
    # ==========================================

    result = {

        "arena_size": None,
        "start": None,
        "goal": None,
        "special_cells": {}

    }

    # ==========================================
    # WRITE YOUR LOGIC BELOW
    # ==========================================
    h, w = image.shape[:2]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = max(contours, key=cv2.contourArea)
    x0, y0, aw, ah = cv2.boundingRect(largest)

    edges=cv2.Canny(gray, 50, 150)

    def grid_alignment_score(n, origin, span, axis):
        cell=span/n
        score=0
        for i in range(1,n):
            pos=int(origin + i * cell)
            if axis=='x':
                band=edges[y0:y0 + ah, max(0, pos - 2):min(w, pos + 3)]
            else:
                band =edges[max(0, pos - 2):min(h, pos + 3), x0:x0 + aw]
            score +=int(band.sum())
        return score

    best_size, best_score = 8, -1
    for n in [6, 8, 10, 12]:
        s = grid_alignment_score(n, x0, aw, 'x') + grid_alignment_score(n, y0, ah, 'y')
        if s > best_score:
            best_score, best_size = s, n

    arena_size=best_size
    cell_w=aw/arena_size
    cell_h=ah/arena_size

    result["arena_size"]=arena_size

    color_ranges = {
        "DANGER": [((0,   120,  70), (10,  255, 255)),
                   ((170, 120,  70), (180, 255, 255))],   # red
        "SAFE":   [((36,   60,  60), (85,  255, 255))],   # green
        "REFUEL": [((100,  80,  70), (135, 255, 255))],   # blue
        "SLOW":   [((10,  120, 100), (22,  255, 255))],   # orange
        "START":  [((22,  120, 100), (35,  255, 255))],   # yellow
        "GOAL":   [((80,   80,  80), (100, 255, 255))],   # cyan
    }

    def build_mask(ranges):
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lo, hi in ranges:
            mask |= cv2.inRange(hsv, np.array(lo), np.array(hi))
        return mask

    masks = {label: build_mask(rng) for label, rng in color_ranges.items()}

    pad_r=max(1, int(cell_h * 0.20)) 
    pad_c=max(1, int(cell_w * 0.20))

    for row in range(arena_size):
        for col in range(arena_size):
            # Pixel centre of this cell
            cx=int(x0 + (col + 0.5) * cell_w)
            cy=int(y0 + (row + 0.5) * cell_h)

            y1,y2=max(0, cy - pad_r), min(h, cy + pad_r + 1)
            x1,x2=max(0, cx - pad_c), min(w, cx + pad_c + 1)

            col_letter =chr(ord('A') + col)
            row_number=arena_size -row
            coord = col_letter+str(row_number)

            best_label, best_count = None, 0
            for label, mask in masks.items():
                count = int(mask[y1:y2, x1:x2].sum()) // 255
                if count > best_count:
                    best_count, best_label = count, label

            if best_count == 0:
                continue

            if best_label== "START":
                result["start"]=coord
            elif best_label=="GOAL":
                result["goal"]=coord
            else:
                result["special_cells"][coord]=best_label
  

    '''
    Steps you may follow:

    1. Detect arena size
    2. Divide arena into grid cells
    3. Convert image to HSV 
    4. Detect START cell
    5. Detect GOAL cell
    6. Detect special colored cells
    7. Map cells to arena coordinates
    8. Store outputs in result dictionary

    Color Meaning
    Red : Danger Zone
    Green : Safe Zone
    Blue : Refuel Station
    Orange : Slow Terrain
    Yellow : Start Position
    Cyan : Goal Position
    '''
    # Example:

    # result["arena_size"] = 8
    # result["start"] = "A1"
    # result["goal"] = "H8"

    # result["special_cells"]["B2"] = "DANGER"
    # result["special_cells"]["D5"] = "SAFE"

    # ==========================================
    # SORT SPECIAL CELLS
    # ==========================================

    sorted_cells = dict(

        sorted(

            result["special_cells"].items(),

            key=lambda item: (

                item[0][0],
                int(item[0][1:])

            )
        )
    )

    result["special_cells"] = sorted_cells

    # ==========================================
    # RETURN FINAL OUTPUT
    # ==========================================

    return result