"""
FTC Voronoi Pocketing Tool
==========================
Requirements: pip install pygame numpy ezdxf

WORKFLOW
--------
SCREEN 1 – SETUP
  • Enter plate width & height in mm
  • Choose unit (mm / inches)
  • Press ENTER to continue

SCREEN 2 – PLACE POINTS
  • Left-click  → add screw hole  (cyan ring, auto red halo on stress map)
  • Right-click → add motor mount (yellow ring, larger red halo)
  • Middle-click / DEL → remove nearest point
  • TAB  → toggle point type before placing
  • ENTER → continue to paint

SCREEN 3 – PAINT STRESS
  • 1 → high stress brush (red)
  • 2 → low stress brush  (green)
  • 3 → erase brush       (neutral)
  • +/- → brush size
  • ↑/↓ → seed count
  • [/] → border thickness
  • R   → reset stress map (keeps points)
  • ENTER / SPACE → generate Voronoi

SCREEN 4 – VORONOI RESULT
  • SPACE → regenerate with new random seeds
  • E     → export DXF
  • P     → back to paint
  • Q     → back to setup
"""

import pygame
import numpy as np
from math import sqrt
from random import random, randint
import os, sys

# ── Optional DXF export ───────────────────────────────────────────────────────
try:
    import ezdxf
    HAS_EZDXF = True
except ImportError:
    HAS_EZDXF = False

pygame.init()

# ── Screen ────────────────────────────────────────────────────────────────────
SW, SH = 1100, 760
screen = pygame.display.set_mode((SW, SH), pygame.RESIZABLE)
pygame.display.set_caption("FTC Voronoi Pocketing Tool")
clock = pygame.time.Clock()

# ── Fonts ─────────────────────────────────────────────────────────────────────
try:
    F_MONO_BIG   = pygame.font.SysFont("consolas",   18, bold=True)
    F_MONO_MED   = pygame.font.SysFont("consolas",   14)
    F_MONO_SMALL = pygame.font.SysFont("consolas",   11)
except:
    F_MONO_BIG   = pygame.font.SysFont(None, 18, bold=True)
    F_MONO_MED   = pygame.font.SysFont(None, 14)
    F_MONO_SMALL = pygame.font.SysFont(None, 11)

# ── Palette ───────────────────────────────────────────────────────────────────
C_BG          = ( 12,  14,  18)
C_PANEL       = ( 20,  23,  30)
C_GRID        = ( 32,  36,  44)
C_GRID_MAJOR  = ( 48,  54,  66)
C_ACCENT      = (  0, 200, 160)   # teal
C_ACCENT2     = (255, 180,   0)   # amber – motor
C_SCREW       = ( 80, 200, 255)   # cyan  – screw
C_MOTOR       = (255, 180,   0)   # amber – motor
C_HIGH        = (220,  55,  55)   # red
C_LOW         = ( 55, 200,  80)   # green
C_BORDER      = (  8,   8,  10)
C_TEXT        = (200, 208, 220)
C_DIM         = (100, 110, 125)
C_PLATE_BG    = ( 24,  28,  36)
C_WHITE       = (240, 240, 250)

PANEL_W = 240

# ── App state ─────────────────────────────────────────────────────────────────
SCREEN_SETUP   = "setup"
SCREEN_POINTS  = "points"
SCREEN_PAINT   = "paint"
SCREEN_VORONOI = "voronoi"

app_screen = SCREEN_SETUP

# Setup fields
setup_fields   = {"width": "120", "height": "80", "unit": "mm"}
setup_focus    = "width"   # which field is active
unit_options   = ["mm", "in"]

# Plate geometry (set when entering POINTS screen)
plate_mm_w  = 120.0
plate_mm_h  = 80.0
unit        = "mm"         # display unit

# Pixel dimensions of the plate canvas (computed from plate mm size)
PLATE_X = PANEL_W + 30
PLATE_Y = 40
plate_px_w = 1  # set in init_plate()
plate_px_h = 1

# Stress map (numpy float32, shape [plate_px_h, plate_px_w], values 0..1)
stress_map = None

# Structural points  list of dicts: {x_mm, y_mm, kind}  kind = "screw"|"motor"
struct_points = []
placing_kind  = "screw"

# Symmetry axis (vertical, draggable)
# axis_x_mm: position of symmetry line in mm from left edge
# Points placed left of axis are mirrored to the right and vice-versa
sym_axis_mm      = None   # set in init_plate()
sym_dragging     = False
SYM_DRAG_TOL_PX  = 8     # pixels either side of axis line that count as a grab

# Horizontal symmetry axis
sym_axis_y_mm    = None   # set in init_plate()
sym_y_dragging   = False

# Solid keep-material rectangles  list of {x_mm, y_mm, w_mm, h_mm}
keep_rects   = []
rect_drawing = False          # currently dragging out a new rect
rect_start   = None           # (x_mm, y_mm) of drag start
rect_preview = None           # current drag preview rect dict
rect_mode    = False          # True = rectangle drawing mode active

# Paint settings
brush_mode    = "high"
brush_radius  = 20
num_seeds     = 50
border_thick  = 2

# Voronoi surface
voronoi_surf  = None
status_msg    = ""

# ── Unit helpers ──────────────────────────────────────────────────────────────
def to_display(mm_val):
    if unit == "in":
        return mm_val / 25.4
    return mm_val

def display_suffix():
    return unit

def parse_dimension(s):
    """Parse user input string → mm float. Returns None on error."""
    try:
        v = float(s.replace(",", "."))
        if unit == "in":
            v *= 25.4
        if v <= 0:
            return None
        return v
    except:
        return None

# ── Plate layout ──────────────────────────────────────────────────────────────
def init_plate():
    """Recompute plate pixel size to fit within available canvas."""
    global plate_px_w, plate_px_h, stress_map, struct_points, voronoi_surf

    avail_w = SW - PLATE_X - 30
    avail_h = SH - PLATE_Y - 30

    scale = min(avail_w / plate_mm_w, avail_h / plate_mm_h)
    # cap so it's not absurdly large
    scale = min(scale, 4.0)

    plate_px_w = max(10, int(plate_mm_w * scale))
    plate_px_h = max(10, int(plate_mm_h * scale))

    stress_map = np.full((plate_px_h, plate_px_w), 0.5, dtype=np.float32)
    struct_points = []
    voronoi_surf = None
    global sym_axis_mm, sym_axis_y_mm, keep_rects
    sym_axis_mm   = plate_mm_w / 2.0
    sym_axis_y_mm = plate_mm_h / 2.0
    keep_rects    = []

def mm_to_px(x_mm, y_mm):
    """Convert mm coords (relative to plate origin) → screen pixel coords."""
    px = PLATE_X + int(x_mm / plate_mm_w * plate_px_w)
    py = PLATE_Y + int(y_mm / plate_mm_h * plate_px_h)
    return px, py

def px_to_mm(sx, sy):
    """Screen pixel → plate mm coords. Returns None if outside plate."""
    lx = sx - PLATE_X
    ly = sy - PLATE_Y
    if 0 <= lx <= plate_px_w and 0 <= ly <= plate_px_h:
        return lx / plate_px_w * plate_mm_w, ly / plate_px_h * plate_mm_h
    return None

def px_to_local(sx, sy):
    """Screen pixel → plate-local pixel coords."""
    lx = sx - PLATE_X
    ly = sy - PLATE_Y
    if 0 <= lx < plate_px_w and 0 <= ly < plate_px_h:
        return lx, ly
    return None

def plate_rect():
    return pygame.Rect(PLATE_X, PLATE_Y, plate_px_w, plate_px_h)

# ── Stress helpers ────────────────────────────────────────────────────────────
def _paint_circle_raw(cx, cy, r, mode):
    """Paint a single circle onto the stress map (no symmetry)."""
    y0 = max(0, cy - r);  y1 = min(plate_px_h, cy + r + 1)
    x0 = max(0, cx - r);  x1 = min(plate_px_w, cx + r + 1)
    ys, xs = np.ogrid[y0:y1, x0:x1]
    mask = (xs - cx)**2 + (ys - cy)**2 <= r**2
    if mode == "high":
        stress_map[y0:y1, x0:x1][mask] = np.minimum(
            stress_map[y0:y1, x0:x1][mask] + 0.2, 1.0)
    elif mode == "low":
        stress_map[y0:y1, x0:x1][mask] = np.maximum(
            stress_map[y0:y1, x0:x1][mask] - 0.2, 0.0)
    else:
        stress_map[y0:y1, x0:x1][mask] = 0.5

def paint_stress_circle(cx_local, cy_local, radius_px, mode):
    """Paint stress circle mirrored across vertical axis only."""
    _paint_circle_raw(cx_local, cy_local, radius_px, mode)
    axis_px = int(sym_axis_mm / plate_mm_w * plate_px_w)
    mx = 2 * axis_px - cx_local
    if 0 <= mx < plate_px_w:
        _paint_circle_raw(mx, cy_local, radius_px, mode)

def apply_point_halo(pt):
    """Auto-paint a red halo around a structural point."""
    scale = plate_px_w / plate_mm_w
    lx = int(pt["x_mm"] / plate_mm_w * plate_px_w)
    ly = int(pt["y_mm"] / plate_mm_h * plate_px_h)
    r  = int(12 * scale) if pt["kind"] == "motor" else int(7 * scale)
    r  = max(6, min(r, plate_px_w // 4))
    # First stamp full red
    paint_stress_circle(lx, ly, r, "high")
    # Guaranteed center solid
    yr = max(0, ly-2); yx = min(plate_px_h, ly+3)
    xr = max(0, lx-2); xx = min(plate_px_w, lx+3)
    stress_map[yr:yx, xr:xx] = 1.0

def reset_stress_with_halos():
    """Reset stress to neutral then re-apply all point halos."""
    stress_map[:] = 0.5
    for pt in struct_points:
        apply_point_halo(pt)

def stress_color(v):
    """Stress float 0..1 → RGB. Green=low, grey=neutral, red=high."""
    if v <= 0.5:
        t = v * 2
        return (
            int(C_LOW[0]*(1-t) + 70*t),
            int(C_LOW[1]*(1-t) + 70*t),
            int(C_LOW[2]*(1-t) + 70*t),
        )
    else:
        t = (v - 0.5) * 2
        return (
            int(70*(1-t) + C_HIGH[0]*t),
            int(70*(1-t) + C_HIGH[1]*t),
            int(70*(1-t) + C_HIGH[2]*t),
        )

# ── Grid drawing ──────────────────────────────────────────────────────────────
def draw_grid():
    """Draw engineering-style grid over the plate."""
    # Choose a nice grid spacing in mm
    for mm_step, col in [(10, C_GRID_MAJOR), (5, C_GRID)]:
        x = 0.0
        while x <= plate_mm_w:
            sx, _ = mm_to_px(x, 0)
            pygame.draw.line(screen, col, (sx, PLATE_Y), (sx, PLATE_Y + plate_px_h), 1)
            x += mm_step
        y = 0.0
        while y <= plate_mm_h:
            _, sy = mm_to_px(0, y)
            pygame.draw.line(screen, col, (PLATE_X, sy), (PLATE_X + plate_px_w, sy), 1)
            y += mm_step

def draw_rulers():
    """Dimension rulers along plate edges."""
    # Bottom ruler
    y_ruler = PLATE_Y + plate_px_h + 6
    pygame.draw.line(screen, C_DIM, (PLATE_X, y_ruler), (PLATE_X + plate_px_w, y_ruler), 1)
    pygame.draw.line(screen, C_DIM, (PLATE_X, y_ruler-3), (PLATE_X, y_ruler+3), 1)
    pygame.draw.line(screen, C_DIM, (PLATE_X+plate_px_w, y_ruler-3), (PLATE_X+plate_px_w, y_ruler+3), 1)
    label = f"{to_display(plate_mm_w):.1f} {display_suffix()}"
    ts = F_MONO_SMALL.render(label, True, C_DIM)
    screen.blit(ts, (PLATE_X + plate_px_w//2 - ts.get_width()//2, y_ruler + 4))

    # Right ruler
    x_ruler = PLATE_X + plate_px_w + 6
    pygame.draw.line(screen, C_DIM, (x_ruler, PLATE_Y), (x_ruler, PLATE_Y + plate_px_h), 1)
    pygame.draw.line(screen, C_DIM, (x_ruler-3, PLATE_Y), (x_ruler+3, PLATE_Y), 1)
    pygame.draw.line(screen, C_DIM, (x_ruler-3, PLATE_Y+plate_px_h), (x_ruler+3, PLATE_Y+plate_px_h), 1)
    label2 = f"{to_display(plate_mm_h):.1f} {display_suffix()}"
    ts2 = F_MONO_SMALL.render(label2, True, C_DIM)
    # Rotated
    ts2r = pygame.transform.rotate(ts2, 90)
    screen.blit(ts2r, (x_ruler + 4, PLATE_Y + plate_px_h//2 - ts2r.get_height()//2))

# ── Structural points drawing ─────────────────────────────────────────────────
def _draw_dashed_vline(x, y0, y1, col, dash=6):
    y = y0
    while y < y1:
        pygame.draw.line(screen, col, (x, y), (x, min(y+dash, y1)), 1)
        y += dash * 2

def _draw_dashed_hline(y, x0, x1, col, dash=6):
    x = x0
    while x < x1:
        pygame.draw.line(screen, col, (x, y), (min(x+dash, x1), y), 1)
        x += dash * 2

def draw_symmetry_axis():
    """Draw both draggable symmetry axes and keep-rect overlays."""
    col = (80, 160, 255)

    # Vertical axis (left↔right)
    axis_px, _ = mm_to_px(sym_axis_mm, 0)
    _draw_dashed_vline(axis_px, PLATE_Y, PLATE_Y + plate_px_h, col)
    pygame.draw.polygon(screen, col, [
        (axis_px, PLATE_Y - 2),
        (axis_px - 6, PLATE_Y - 10),
        (axis_px + 6, PLATE_Y - 10)])
    pygame.draw.polygon(screen, col, [
        (axis_px, PLATE_Y + plate_px_h + 2),
        (axis_px - 6, PLATE_Y + plate_px_h + 10),
        (axis_px + 6, PLATE_Y + plate_px_h + 10)])
    lbl = F_MONO_SMALL.render(f"X {to_display(sym_axis_mm):.1f}{display_suffix()}", True, col)
    screen.blit(lbl, (axis_px + 8, PLATE_Y + 4))

    # Horizontal axis (top↔bottom)
    _, axis_py = mm_to_px(0, sym_axis_y_mm)
    _draw_dashed_hline(axis_py, PLATE_X, PLATE_X + plate_px_w, col)
    pygame.draw.polygon(screen, col, [
        (PLATE_X - 2,  axis_py),
        (PLATE_X - 10, axis_py - 6),
        (PLATE_X - 10, axis_py + 6)])
    pygame.draw.polygon(screen, col, [
        (PLATE_X + plate_px_w + 2,  axis_py),
        (PLATE_X + plate_px_w + 10, axis_py - 6),
        (PLATE_X + plate_px_w + 10, axis_py + 6)])
    lbl2 = F_MONO_SMALL.render(f"Y {to_display(sym_axis_y_mm):.1f}{display_suffix()}", True, col)
    screen.blit(lbl2, (PLATE_X + 4, axis_py + 4))

    # Keep-rects
    C_KEEP = (255, 220, 80)
    all_rects = list(keep_rects)
    if rect_preview:
        all_rects.append(rect_preview)
    for kr in all_rects:
        for rx, ry, rw, rh in _keep_rect_quads(kr):
            sx, sy = mm_to_px(rx, ry)
            ex, ey = mm_to_px(rx + rw, ry + rh)
            r = pygame.Rect(sx, sy, ex-sx, ey-sy)
            s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill((255, 220, 80, 50))
            screen.blit(s, r.topleft)
            pygame.draw.rect(screen, C_KEEP, r, 1)

def _keep_rect_quads(kr):
    """Return list of (x_mm,y_mm,w_mm,h_mm) for the rect + its left/right mirror."""
    x, y, w, h = kr["x_mm"], kr["y_mm"], kr["w_mm"], kr["h_mm"]
    mx = 2 * sym_axis_mm - (x + w)
    return [
        (x,  y, w, h),   # original
        (mx, y, w, h),   # x-mirror
    ]

def draw_struct_points():
    for pt in struct_points:
        sx, sy = mm_to_px(pt["x_mm"], pt["y_mm"])
        col  = C_SCREW if pt["kind"] == "screw" else C_MOTOR
        r    = 5 if pt["kind"] == "screw" else 8
        pygame.draw.circle(screen, col, (sx, sy), r, 2)
        pygame.draw.circle(screen, col, (sx, sy), 2)
        label = "S" if pt["kind"] == "screw" else "M"
        ts = F_MONO_SMALL.render(label, True, col)
        screen.blit(ts, (sx + r + 2, sy - ts.get_height()//2))

# ── Panel drawing helpers ─────────────────────────────────────────────────────
_panel_y = 0

def panel_start():
    global _panel_y
    _panel_y = 16

def panel_line(txt, col=None, font=None, indent=0):
    global _panel_y
    col  = col  if col  is not None else C_TEXT
    font = font if font is not None else F_MONO_MED
    surf = font.render(txt, True, col)
    screen.blit(surf, (14 + indent, _panel_y))
    _panel_y += surf.get_height() + 5

def panel_gap(px=8):
    global _panel_y
    _panel_y += px

def panel_divider():
    global _panel_y
    pygame.draw.line(screen, C_GRID_MAJOR, (10, _panel_y), (PANEL_W-10, _panel_y), 1)
    _panel_y += 10

def panel_key(key, desc, val=None, col=None):
    global _panel_y
    col_k = col if col else C_ACCENT
    col_d = C_DIM
    col_v = C_TEXT
    ksurf = F_MONO_SMALL.render(f"[{key}]", True, col_k)
    dsurf = F_MONO_SMALL.render(f" {desc}", True, col_d)
    screen.blit(ksurf, (14, _panel_y))
    screen.blit(dsurf, (14 + ksurf.get_width(), _panel_y))
    if val is not None:
        vsurf = F_MONO_SMALL.render(str(val), True, col_v)
        screen.blit(vsurf, (PANEL_W - vsurf.get_width() - 10, _panel_y))
    _panel_y += dsurf.get_height() + 4

# ── SCREEN: SETUP ─────────────────────────────────────────────────────────────
setup_error = ""

def draw_setup():
    screen.fill(C_BG)
    pygame.draw.rect(screen, C_PANEL, (0, 0, SW, SH))

    # Title
    t = F_MONO_BIG.render("FTC VORONOI POCKETING TOOL", True, C_ACCENT)
    screen.blit(t, (SW//2 - t.get_width()//2, 60))
    t2 = F_MONO_MED.render("Lightweight aluminium plates via stress-weighted Voronoi pocketing", True, C_DIM)
    screen.blit(t2, (SW//2 - t2.get_width()//2, 90))

    pygame.draw.line(screen, C_ACCENT, (SW//2-300, 115), (SW//2+300, 115), 1)

    # Form box
    box_w, box_h = 480, 320
    bx = SW//2 - box_w//2
    by = 140
    pygame.draw.rect(screen, (18, 21, 28), (bx, by, box_w, box_h), border_radius=4)
    pygame.draw.rect(screen, C_GRID_MAJOR, (bx, by, box_w, box_h), 1, border_radius=4)

    y = by + 28

    def field(label, key, hint=""):
        nonlocal y
        active = (setup_focus == key)
        lsurf = F_MONO_MED.render(label, True, C_ACCENT if active else C_DIM)
        screen.blit(lsurf, (bx + 30, y))
        y += lsurf.get_height() + 6

        fw, fh = 200, 32
        fx = bx + 30
        fcol = C_ACCENT if active else C_GRID_MAJOR
        pygame.draw.rect(screen, (25, 29, 38), (fx, y, fw, fh))
        pygame.draw.rect(screen, fcol, (fx, y, fw, fh), 1)
        val = setup_fields[key]
        cursor = "|" if active and (pygame.time.get_ticks()//500)%2==0 else ""
        vsurf = F_MONO_MED.render(val + cursor, True, C_WHITE)
        screen.blit(vsurf, (fx + 8, y + 7))
        if hint:
            hsurf = F_MONO_SMALL.render(hint, True, C_DIM)
            screen.blit(hsurf, (fx + fw + 12, y + 8))
        y += fh + 18

    field("PLATE WIDTH", "width",  f"({display_suffix()})")
    field("PLATE HEIGHT", "height", f"({display_suffix()})")

    # Unit selector
    lsurf = F_MONO_MED.render("UNIT", True, C_DIM)
    screen.blit(lsurf, (bx + 30, y))
    y += lsurf.get_height() + 6
    for i, u in enumerate(unit_options):
        ux = bx + 30 + i * 90
        active = (setup_fields["unit"] == u)
        pygame.draw.rect(screen, C_ACCENT if active else (25,29,38), (ux, y, 75, 30))
        pygame.draw.rect(screen, C_ACCENT if active else C_GRID_MAJOR, (ux, y, 75, 30), 1)
        ucolor = C_BG if active else C_TEXT
        usurf = F_MONO_MED.render(u, True, ucolor)
        screen.blit(usurf, (ux + 75//2 - usurf.get_width()//2, y + 7))
    y += 50

    # Error
    if setup_error:
        esurf = F_MONO_MED.render(setup_error, True, C_HIGH)
        screen.blit(esurf, (bx + 30, y))

    # Enter to continue
    y = by + box_h - 40
    esurf = F_MONO_MED.render("ENTER  →  continue", True, C_ACCENT)
    screen.blit(esurf, (bx + box_w//2 - esurf.get_width()//2, y))


def handle_setup_key(event):
    global setup_focus, setup_error, app_screen, plate_mm_w, plate_mm_h, unit
    if event.key == pygame.K_TAB:
        order = ["width", "height"]
        idx = order.index(setup_focus) if setup_focus in order else 0
        setup_focus = order[(idx+1) % len(order)]
    elif event.key == pygame.K_RETURN:
        # Validate
        u = setup_fields["unit"]
        old_unit = unit
        unit = u
        w = parse_dimension(setup_fields["width"])
        h = parse_dimension(setup_fields["height"])
        if w is None or h is None:
            setup_error = "Invalid dimensions."
            unit = old_unit
            return
        if w > 500 or h > 500:
            setup_error = "Max 500mm / ~20in per side."
            unit = old_unit
            return
        plate_mm_w = w
        plate_mm_h = h
        setup_error = ""
        init_plate()
        app_screen = SCREEN_POINTS
    elif event.key == pygame.K_BACKSPACE:
        if setup_focus in setup_fields:
            setup_fields[setup_focus] = setup_fields[setup_focus][:-1]
    elif event.key == pygame.K_1 and setup_focus == "unit":
        setup_fields["unit"] = "mm"
    elif event.key == pygame.K_2 and setup_focus == "unit":
        setup_fields["unit"] = "in"
    else:
        ch = event.unicode
        if ch and setup_focus in ("width","height"):
            if ch in "0123456789.,":
                setup_fields[setup_focus] += ch

def handle_setup_click(pos):
    global setup_focus
    bx = SW//2 - 480//2
    by = 140

    # Width field  (y position matches draw_setup field() layout)
    # field() renders: label (~20px) + gap 6 + input box 32px
    # width field starts at by+28, label height ~20, so input at by+28+26=by+54
    width_rect  = pygame.Rect(bx + 30, by + 54,  200, 32)
    # height field: width block = label(20)+6 + box(32)+18 = 76px after by+28=104
    height_rect = pygame.Rect(bx + 30, by + 130, 200, 32)

    if width_rect.collidepoint(pos):
        setup_focus = "width"
    elif height_rect.collidepoint(pos):
        setup_focus = "height"

    # Unit buttons
    for i, u in enumerate(unit_options):
        ux = bx + 30 + i * 90
        uy = by + 230
        r = pygame.Rect(ux, uy, 75, 30)
        if r.collidepoint(pos):
            setup_fields["unit"] = u


# ── SCREEN: PLACE POINTS ──────────────────────────────────────────────────────
def draw_points_screen():
    screen.fill(C_BG)
    pygame.draw.rect(screen, C_PLATE_BG, plate_rect())
    draw_grid()
    draw_symmetry_axis()
    draw_rulers()
    draw_struct_points()
    pygame.draw.rect(screen, C_ACCENT, plate_rect(), 1)

    # Crosshair at mouse if inside plate
    mx, my = pygame.mouse.get_pos()
    pt = px_to_mm(mx, my)
    if pt:
        pygame.draw.line(screen, (40,50,60), (PLATE_X, my), (PLATE_X+plate_px_w, my), 1)
        pygame.draw.line(screen, (40,50,60), (mx, PLATE_Y), (mx, PLATE_Y+plate_px_h), 1)
        col = C_SCREW if placing_kind=="screw" else C_MOTOR
        r = 5 if placing_kind=="screw" else 8
        pygame.draw.circle(screen, col, (mx, my), r, 1)
        coord = f"{to_display(pt[0]):.1f}, {to_display(pt[1]):.1f} {display_suffix()}"
        cs = F_MONO_SMALL.render(coord, True, C_DIM)
        screen.blit(cs, (mx+10, my-18))

    # Panel
    pygame.draw.rect(screen, C_PANEL, (0, 0, PANEL_W, SH))
    pygame.draw.line(screen, C_ACCENT, (PANEL_W, 0), (PANEL_W, SH), 1)
    panel_start()
    panel_line("PLACE POINTS", C_ACCENT, F_MONO_BIG)
    panel_divider()
    mode_col = C_SCREW if placing_kind=="screw" else C_MOTOR
    panel_line(f"Mode: {'SCREW' if placing_kind=='screw' else 'MOTOR'}", mode_col)
    panel_gap()
    panel_key("TAB",   "toggle type")
    panel_key("LMB",   "place point")
    panel_key("RMB",   "remove nearest")
    panel_key("DEL",   "remove nearest")
    panel_divider()
    panel_line("SCREW", C_SCREW)
    panel_line(" cyan ring · small halo", C_DIM, F_MONO_SMALL)
    panel_gap(4)
    panel_line("MOTOR", C_MOTOR)
    panel_line(" amber ring · large halo", C_DIM, F_MONO_SMALL)
    panel_divider()
    panel_line(f"Points: {len(struct_points)}", C_TEXT)
    panel_divider()
    panel_divider()
    rect_col = C_ACCENT if rect_mode else C_DIM
    panel_line(f"Rect mode: {'ON' if rect_mode else 'OFF'}", rect_col)
    panel_key("R",     "toggle rect mode")
    panel_key("RMB",   "delete rect (rect mode)")
    panel_divider()
    panel_key("ENTER", "next: paint stress", col=C_ACCENT)
    panel_key("Q",     "back to setup")

    # Point list
    panel_gap(6)
    panel_line("Placed points:", C_DIM, F_MONO_SMALL)
    for i, pt in enumerate(struct_points[-8:]):  # show last 8
        tag = "S" if pt["kind"]=="screw" else "M"
        col = C_SCREW if pt["kind"]=="screw" else C_MOTOR
        panel_line(f" {tag} {to_display(pt['x_mm']):.1f},{to_display(pt['y_mm']):.1f}", col, F_MONO_SMALL)


def mirror_x_mm(x_mm):
    """Mirror an x coordinate (mm) across the vertical symmetry axis."""
    return 2 * sym_axis_mm - x_mm

def mirror_y_mm(y_mm):
    """Mirror a y coordinate (mm) across the horizontal symmetry axis."""
    return 2 * sym_axis_y_mm - y_mm

def _place_mirrored_points(x_mm, y_mm, kind):
    """Place a point + its left/right mirror only."""
    struct_points.append({"x_mm": x_mm, "y_mm": y_mm, "kind": kind})
    apply_point_halo(struct_points[-1])
    mx = mirror_x_mm(x_mm)
    if abs(mx - x_mm) > 0.5 and 0 <= mx <= plate_mm_w:
        struct_points.append({"x_mm": mx, "y_mm": y_mm, "kind": kind})
        apply_point_halo(struct_points[-1])

def handle_points_click(pos, button):
    global app_screen, rect_drawing, rect_start, rect_preview
    pt = px_to_mm(*pos)
    if pt is None:
        return
    if rect_mode:
        if button == 1:
            rect_drawing = True
            rect_start   = pt
        elif button == 3:
            # Remove nearest keep-rect
            if keep_rects:
                mx_s, my_s = pos
                best = min(range(len(keep_rects)), key=lambda i: (
                    mm_to_px(keep_rects[i]["x_mm"] + keep_rects[i]["w_mm"]/2,
                             keep_rects[i]["y_mm"] + keep_rects[i]["h_mm"]/2)[0] - mx_s)**2 + (
                    mm_to_px(keep_rects[i]["x_mm"] + keep_rects[i]["w_mm"]/2,
                             keep_rects[i]["y_mm"] + keep_rects[i]["h_mm"]/2)[1] - my_s)**2)
                keep_rects.pop(best)
                reset_stress_with_halos()
    else:
        if button == 1:
            x_mm, y_mm = pt
            _place_mirrored_points(x_mm, y_mm, placing_kind)
        elif button == 3:
            remove_nearest_point(pos)

def remove_nearest_point(pos):
    if not struct_points:
        return
    best = None
    best_d = 1e9
    for i, pt in enumerate(struct_points):
        sx, sy = mm_to_px(pt["x_mm"], pt["y_mm"])
        d = (sx-pos[0])**2 + (sy-pos[1])**2
        if d < best_d:
            best_d = d
            best = i
    if best is not None and best_d < 40**2:
        struct_points.pop(best)
        reset_stress_with_halos()


# ── SCREEN: PAINT STRESS ──────────────────────────────────────────────────────
painting = False
sym_dragging = False

def draw_stress_map_surf():
    """Draw stress map onto screen using block rendering."""
    block = max(1, min(3, plate_px_w // 200 + 1))
    for py in range(0, plate_px_h, block):
        for px in range(0, plate_px_w, block):
            v = float(stress_map[py, px])
            col = stress_color(v)
            pygame.draw.rect(screen, col,
                (PLATE_X + px, PLATE_Y + py, block, block))

def draw_paint_screen():
    screen.fill(C_BG)
    draw_stress_map_surf()
    draw_grid()
    draw_symmetry_axis()
    draw_struct_points()
    pygame.draw.rect(screen, C_ACCENT, plate_rect(), 1)
    draw_rulers()

    # Brush preview
    mx, my = pygame.mouse.get_pos()
    if plate_rect().collidepoint(mx, my):
        bcol = C_HIGH if brush_mode=="high" else (C_LOW if brush_mode=="low" else C_DIM)
        pygame.draw.circle(screen, bcol, (mx, my), brush_radius, 1)

    # Panel
    pygame.draw.rect(screen, C_PANEL, (0, 0, PANEL_W, SH))
    pygame.draw.line(screen, C_ACCENT, (PANEL_W, 0), (PANEL_W, SH), 1)
    panel_start()
    panel_line("PAINT STRESS", C_ACCENT, F_MONO_BIG)
    panel_divider()

    bmode_col = C_HIGH if brush_mode=="high" else (C_LOW if brush_mode=="low" else C_DIM)
    panel_line(f"Brush: {brush_mode.upper()}", bmode_col)
    panel_gap(4)
    panel_key("1", "high stress", "RED")
    panel_key("2", "low stress",  "GRN")
    panel_key("3", "erase",       "---")
    panel_divider()
    panel_key("+/-", "brush size",  f"{brush_radius}px")
    panel_key("↑/↓", "seed count",  num_seeds)
    panel_key("[/]", "border px",   border_thick)
    panel_divider()
    panel_key("R",     "reset map")
    panel_key("SPACE", "generate →", col=C_ACCENT)
    panel_key("P",     "back to points")
    panel_key("Q",     "back to setup")

    # Stress legend
    panel_divider()
    panel_line("STRESS LEGEND", C_DIM, F_MONO_SMALL)
    panel_line("  RED   = keep material", C_HIGH, F_MONO_SMALL)
    panel_line("  GREEN = pocket here",   C_LOW,  F_MONO_SMALL)
    panel_line("  GREY  = neutral",       C_DIM,  F_MONO_SMALL)


# ── Two-tone colours for Voronoi result ──────────────────────────────────────
C_MATERIAL = (160, 165, 175)   # aluminium grey – solid walls / kept material
C_POCKET   = ( 30,  35,  45)   # dark recess    – pocketed area

# Edge margin kept solid around the plate perimeter (mm)
EDGE_MARGIN_MM = 4.0

# ── SCREEN: VORONOI ───────────────────────────────────────────────────────────
def generate_voronoi():
    global voronoi_surf, status_msg
    status_msg = "Generating..."
    pygame.display.flip()

    scale = plate_px_w / plate_mm_w   # px per mm

    # ── Solid mask: True = keep material, no pocketing ───────────────────────
    solid = np.zeros((plate_px_h, plate_px_w), dtype=bool)

    # 1. Edge margin
    em = max(1, int(EDGE_MARGIN_MM * scale))
    solid[:em,  :]  = True
    solid[-em:, :]  = True
    solid[:,  :em]  = True
    solid[:, -em:]  = True

    # 2. Keep-rects (all 4 mirrored quadrants)
    for kr in keep_rects:
        for rx, ry, rw, rh in _keep_rect_quads(kr):
            x0p = max(0, int(rx / plate_mm_w * plate_px_w))
            y0p = max(0, int(ry / plate_mm_h * plate_px_h))
            x1p = min(plate_px_w, int((rx+rw) / plate_mm_w * plate_px_w))
            y1p = min(plate_px_h, int((ry+rh) / plate_mm_h * plate_px_h))
            solid[y0p:y1p, x0p:x1p] = True

    # 3. Exclusion discs around structural points
    ys_grid, xs_grid = np.ogrid[0:plate_px_h, 0:plate_px_w]
    for pt in struct_points:
        cx = int(pt["x_mm"] / plate_mm_w * plate_px_w)
        cy = int(pt["y_mm"] / plate_mm_h * plate_px_h)
        r_mm = 7.0 if pt["kind"] == "motor" else 4.0
        r_px = max(6, int(r_mm * scale))
        solid[(xs_grid - cx)**2 + (ys_grid - cy)**2 <= r_px**2] = True

    # Symmetry axis in pixels
    axis_px = int(sym_axis_mm / plate_mm_w * plate_px_w)

    def mirror_seed(px, py):
        """Mirror a seed pixel across the axis. Returns None if out of bounds."""
        mx = 2 * axis_px - px
        if 0 <= mx < plate_px_w:
            return (mx, py)
        return None

    def add_seed(px, py):
        """Add a seed and its mirror. Skip if in solid zone."""
        nonlocal placed
        if solid[py, px]:
            return
        seeds.append((px, py))
        placed += 1
        m = mirror_seed(px, py)
        # Only add mirror if it differs and is not in solid zone
        if m and m != (px, py) and not solid[m[1], m[0]]:
            seeds.append(m)
            placed += 1

    # ── Force seeds at structural points so walls radiate from them ──────────
    seeds = []
    placed = 0
    # Only process points on the left of (or on) the axis to avoid doubling
    seen_pairs = set()
    for pt in struct_points:
        cx = int(pt["x_mm"] / plate_mm_w * plate_px_w)
        cy = int(pt["y_mm"] / plate_mm_h * plate_px_h)
        # Deduplicate mirrored pairs — only process the left-side point
        mirror_cx = 2 * axis_px - cx
        key = (min(cx, mirror_cx), cy)
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        add_seed(cx, cy)
        # Spoke ring
        r_mm   = 7.0 if pt["kind"] == "motor" else 4.0
        r_px   = max(6, int(r_mm * scale)) + border_thick + 2
        spokes = 8 if pt["kind"] == "motor" else 6
        for i in range(spokes):
            angle = 2 * np.pi * i / spokes
            sx = int(cx + r_px * np.cos(angle))
            sy = int(cy + r_px * np.sin(angle))
            if 0 <= sx < plate_px_w and 0 <= sy < plate_px_h:
                add_seed(sx, sy)

    # ── Weighted random seed placement (left half only, mirrored) ────────────
    attempts = num_seeds * 150
    while placed < num_seeds and attempts > 0:
        attempts -= 1
        # Only sample from left half (up to and including axis)
        px = randint(0, axis_px)
        py = randint(0, plate_px_h - 1)
        if solid[py, px]:
            continue
        v = float(stress_map[py, px])
        if random() < (0.05 + 0.95 * v):
            add_seed(px, py)

    if not seeds:
        status_msg = "No seeds placed — try more seeds or less solid area."
        return

    pts = np.array([[s[0], s[1]] for s in seeds], dtype=np.float32)

    xs = np.arange(plate_px_w, dtype=np.float32)
    ys = np.arange(plate_px_h, dtype=np.float32)
    gx, gy = np.meshgrid(xs, ys)

    dx = gx[:, :, None] - pts[:, 0]
    dy = gy[:, :, None] - pts[:, 1]
    dist2 = dx**2 + dy**2
    nearest = np.argmin(dist2, axis=2)

    # Uniform-width borders via neighbour ownership check
    is_border = np.zeros((plate_px_h, plate_px_w), dtype=bool)
    bt = border_thick
    for ddx in range(-bt, bt+1):
        for ddy in range(-bt, bt+1):
            if ddx == 0 and ddy == 0:
                continue
            shifted = np.roll(np.roll(nearest, ddy, axis=0), ddx, axis=1)
            is_border |= (shifted != nearest)

    # ── Assemble colour grid ──────────────────────────────────────────────────
    # Start with pocket colour everywhere
    color_grid = np.full((plate_px_h, plate_px_w, 3), C_POCKET, dtype=np.uint8)
    # Voronoi walls → material colour
    color_grid[is_border] = C_MATERIAL
    # Solid zones override everything → material colour
    color_grid[solid] = C_MATERIAL

    surf = pygame.surfarray.make_surface(color_grid.transpose(1, 0, 2))

    # Structural point markers on top
    for pt in struct_points:
        sx = int(pt["x_mm"] / plate_mm_w * plate_px_w)
        sy = int(pt["y_mm"] / plate_mm_h * plate_px_h)
        col = C_SCREW if pt["kind"] == "screw" else C_MOTOR
        r   = 5 if pt["kind"] == "screw" else 8
        pygame.draw.circle(surf, col, (sx, sy), r, 2)
        pygame.draw.circle(surf, col, (sx, sy), 2)

    voronoi_surf = surf
    status_msg = f"Generated · {len(seeds)} seeds  ·  edge margin {EDGE_MARGIN_MM}mm"


def draw_voronoi_screen():
    screen.fill(C_BG)
    if voronoi_surf:
        screen.blit(voronoi_surf, (PLATE_X, PLATE_Y))
    else:
        pygame.draw.rect(screen, C_PLATE_BG, plate_rect())
    pygame.draw.rect(screen, C_ACCENT, plate_rect(), 1)
    draw_rulers()

    pygame.draw.rect(screen, C_PANEL, (0, 0, PANEL_W, SH))
    pygame.draw.line(screen, C_ACCENT, (PANEL_W, 0), (PANEL_W, SH), 1)
    panel_start()
    panel_line("VORONOI RESULT", C_ACCENT, F_MONO_BIG)
    panel_divider()
    panel_line(status_msg, C_DIM, F_MONO_SMALL)
    panel_gap(4)
    panel_key("SPACE", "regenerate")
    panel_key("E",     "export DXF" + ("" if HAS_EZDXF else " (needs ezdxf)"))
    panel_divider()
    panel_key("P", "back to paint")
    panel_key("Q", "back to setup")
    panel_divider()
    panel_line("LEGEND", C_DIM, F_MONO_SMALL)
    panel_line("  Dark cells  = pockets",    C_DIM,      F_MONO_SMALL)
    panel_line("  Grey areas  = material",   C_MATERIAL, F_MONO_SMALL)
    panel_line("  Cyan  ●  = screw",         C_SCREW, F_MONO_SMALL)
    panel_line("  Amber ●  = motor",         C_MOTOR, F_MONO_SMALL)

    panel_divider()
    wall_pct = 0
    if voronoi_surf:
        # Quick estimate: border pixels / total pixels
        bt = border_thick
        total = plate_px_w * plate_px_h
        # recompute is_border count from saved surf is expensive; skip
        pass
    panel_line(f"Seeds:  {num_seeds}", C_TEXT, F_MONO_SMALL)
    panel_line(f"Border: {border_thick}px", C_TEXT, F_MONO_SMALL)
    panel_line(f"Plate:  {to_display(plate_mm_w):.1f}×{to_display(plate_mm_h):.1f}{display_suffix()}", C_TEXT, F_MONO_SMALL)


# ── DXF EXPORT ────────────────────────────────────────────────────────────────
def export_dxf():
    global status_msg
    if not HAS_EZDXF:
        status_msg = "ezdxf not installed. Run: pip install ezdxf"
        return

    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    doc.layers.new("PLATE_OUTLINE", dxfattribs={"color": 7})
    doc.layers.new("VORONOI_CELLS", dxfattribs={"color": 3})
    doc.layers.new("SCREW_HOLES",   dxfattribs={"color": 4})
    doc.layers.new("MOTOR_MOUNTS",  dxfattribs={"color": 2})

    # Plate outline
    msp.add_lwpolyline(
        [(0,0),(plate_mm_w,0),(plate_mm_w,plate_mm_h),(0,plate_mm_h),(0,0)],
        dxfattribs={"layer":"PLATE_OUTLINE"}
    )

    # Structural point circles
    for pt in struct_points:
        r = 1.5 if pt["kind"]=="screw" else 3.0
        layer = "SCREW_HOLES" if pt["kind"]=="screw" else "MOTOR_MOUNTS"
        msp.add_circle(
            (pt["x_mm"], plate_mm_h - pt["y_mm"]),  # flip Y for DXF
            r,
            dxfattribs={"layer": layer}
        )

    # Voronoi borders as polylines (trace border pixels)
    # Simple approach: export border pixel positions as small squares
    if voronoi_surf:
        # Recompute border from stress map + seeds
        # (voronoi_surf doesn't store seed data, recompute nearest for export)
        # For now, export a note; full contour tracing is complex
        msp.add_text(
            "Voronoi border geometry — see PNG for visual reference",
            dxfattribs={"layer":"VORONOI_CELLS","height":2}
        ).set_placement((2, -6))

    path = os.path.join(os.path.expanduser("~"), "voronoi_pocketing.dxf")
    doc.saveas(path)
    status_msg = f"DXF saved → {path}"


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
init_plate()

def update_sym_axis(mouse_x):
    global sym_axis_mm
    local_x = mouse_x - PLATE_X
    sym_axis_mm = max(1.0, min(plate_mm_w - 1.0,
                               local_x / plate_px_w * plate_mm_w))

def update_sym_axis_y(mouse_y):
    global sym_axis_y_mm
    local_y = mouse_y - PLATE_Y
    sym_axis_y_mm = max(1.0, min(plate_mm_h - 1.0,
                                 local_y / plate_px_h * plate_mm_h))

while True:
    SW, SH = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            SW, SH = event.w, event.h
            if app_screen != SCREEN_SETUP:
                init_plate()

        elif event.type == pygame.KEYDOWN:
            k = event.key

            # ── Setup ──
            if app_screen == SCREEN_SETUP:
                handle_setup_key(event)

            # ── Points ──
            elif app_screen == SCREEN_POINTS:
                if k == pygame.K_RETURN:
                    app_screen = SCREEN_PAINT
                elif k == pygame.K_TAB:
                    placing_kind = "motor" if placing_kind=="screw" else "screw"
                elif k in (pygame.K_DELETE, pygame.K_BACKSPACE):
                    remove_nearest_point(pygame.mouse.get_pos())
                elif k == pygame.K_r:
                    rect_mode = not rect_mode
                elif k == pygame.K_q:
                    app_screen = SCREEN_SETUP

            # ── Paint ──
            elif app_screen == SCREEN_PAINT:
                if k in (pygame.K_SPACE, pygame.K_RETURN):
                    app_screen = SCREEN_VORONOI
                    generate_voronoi()
                elif k == pygame.K_1:
                    brush_mode = "high"
                elif k == pygame.K_2:
                    brush_mode = "low"
                elif k == pygame.K_3:
                    brush_mode = "erase"
                elif k in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    brush_radius = min(100, brush_radius + 3)
                elif k in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    brush_radius = max(4, brush_radius - 3)
                elif k == pygame.K_UP:
                    num_seeds = min(400, num_seeds + 5)
                elif k == pygame.K_DOWN:
                    num_seeds = max(5, num_seeds - 5)
                elif k == pygame.K_LEFTBRACKET:
                    border_thick = max(0, border_thick - 1)
                elif k == pygame.K_RIGHTBRACKET:
                    border_thick = min(8, border_thick + 1)
                elif k == pygame.K_r:
                    reset_stress_with_halos()
                elif k == pygame.K_p:
                    app_screen = SCREEN_POINTS
                elif k == pygame.K_q:
                    app_screen = SCREEN_SETUP

            # ── Voronoi ──
            elif app_screen == SCREEN_VORONOI:
                if k == pygame.K_SPACE:
                    generate_voronoi()
                elif k == pygame.K_e:
                    export_dxf()
                elif k == pygame.K_p:
                    app_screen = SCREEN_PAINT
                elif k == pygame.K_q:
                    app_screen = SCREEN_SETUP

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if app_screen == SCREEN_SETUP:
                handle_setup_click(pos)
            elif app_screen in (SCREEN_POINTS, SCREEN_PAINT):
                axis_sx, _  = mm_to_px(sym_axis_mm, 0)
                _, axis_sy  = mm_to_px(0, sym_axis_y_mm)
                near_vaxis  = abs(pos[0] - axis_sx) <= SYM_DRAG_TOL_PX and plate_rect().collidepoint(pos)
                near_haxis  = abs(pos[1] - axis_sy) <= SYM_DRAG_TOL_PX and plate_rect().collidepoint(pos)
                if near_vaxis:
                    sym_dragging = True
                elif near_haxis:
                    sym_y_dragging = True
                elif app_screen == SCREEN_POINTS:
                    handle_points_click(pos, event.button)
                elif app_screen == SCREEN_PAINT and event.button == 1:
                    painting = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                painting = False
                sym_dragging = False
                sym_y_dragging = False
                if rect_drawing and rect_preview:
                    keep_rects.append(rect_preview)
                    reset_stress_with_halos()
                rect_drawing = False
                rect_preview = None

    # Continuous paint while mouse held
    if painting and app_screen == SCREEN_PAINT:
        lp = px_to_local(*pygame.mouse.get_pos())
        if lp:
            paint_stress_circle(lp[0], lp[1], brush_radius, brush_mode)

    # Drag symmetry axes
    if sym_dragging:
        update_sym_axis(pygame.mouse.get_pos()[0])
    if sym_y_dragging:
        update_sym_axis_y(pygame.mouse.get_pos()[1])

    # Update rect preview while dragging
    if rect_drawing and rect_start:
        cur = px_to_mm(*pygame.mouse.get_pos())
        if cur:
            x0 = min(rect_start[0], cur[0])
            y0 = min(rect_start[1], cur[1])
            w  = abs(cur[0] - rect_start[0])
            h  = abs(cur[1] - rect_start[1])
            rect_preview = {"x_mm": x0, "y_mm": y0, "w_mm": max(w, 0.5), "h_mm": max(h, 0.5)}

    # ── Draw current screen ──
    if app_screen == SCREEN_SETUP:
        draw_setup()
    elif app_screen == SCREEN_POINTS:
        draw_points_screen()
    elif app_screen == SCREEN_PAINT:
        draw_paint_screen()
    elif app_screen == SCREEN_VORONOI:
        draw_voronoi_screen()

    pygame.display.flip()
    clock.tick(60)