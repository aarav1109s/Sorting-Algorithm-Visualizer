"""
Sorting Algorithm Visualizer
Sidebar: algorithm selection, speed slider, comparison/access counters.
Red = bars being compared, Green = bars in final sorted position.
"""

import pygame
import random

from algorithms import quicksort, mergesort, heapsort

# --- Constants ---
SIDEBAR_WIDTH = 220
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
CONTENT_LEFT = SIDEBAR_WIDTH
CONTENT_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH
BAR_COUNT = 50
BAR_COLOR = (70, 130, 180)
BAR_OUTLINE = (30, 60, 90)
COMPARE_COLOR = (220, 60, 60)   # Red - being compared
SORTED_COLOR = (60, 180, 80)    # Green - final sorted position
BACKGROUND = (25, 25, 35)
SIDEBAR_BG = (35, 35, 48)
BUTTON_COLOR = (60, 120, 180)
BUTTON_HOVER = (80, 150, 220)
BUTTON_SELECTED = (90, 160, 230)
BUTTON_DISABLED = (80, 80, 90)
BUTTON_TEXT = (255, 255, 255)
TEXT_LABEL = (180, 180, 200)
MARGIN_TOP = 50
MARGIN_SIDES = 30
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 32
BUTTON_MARGIN = 12
SLIDER_WIDTH = 160
SLIDER_HEIGHT = 12
SLIDER_MIN = 1
SLIDER_MAX = 30
SPEED_STEPS_MIN = 1
SPEED_STEPS_MAX = 30


def generate_array(length: int, min_val: int = 10, max_val: int = 400) -> list[int]:
    """Generate a random array of integers for visualization."""
    return [random.randint(min_val, max_val) for _ in range(length)]


def draw_bars(
    surface: pygame.Surface,
    arr: list[int],
    max_val: int,
    compare_indices: list[int] | None = None,
    sorted_indices: list[int] | None = None,
) -> None:
    """Draw the array as vertical bars. Red = comparing, Green = sorted."""
    compare_indices = compare_indices or []
    sorted_indices = sorted_indices or []
    n = len(arr)
    if n == 0:
        return
    bar_area_width = CONTENT_WIDTH - 2 * MARGIN_SIDES
    bar_width = max(2, (bar_area_width / n) - 2)
    gap = 2
    usable_height = WINDOW_HEIGHT - MARGIN_TOP - 40
    compare_set = set(compare_indices)
    sorted_set = set(sorted_indices)
    base_x = CONTENT_LEFT + MARGIN_SIDES

    for i, value in enumerate(arr):
        bar_height = int((value / max_val) * usable_height)
        x = base_x + i * (bar_width + gap)
        y = WINDOW_HEIGHT - 40 - bar_height
        rect = pygame.Rect(x, y, int(bar_width), bar_height)
        if i in sorted_set:
            color = SORTED_COLOR
        elif i in compare_set:
            color = COMPARE_COLOR
        else:
            color = BAR_COLOR
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BAR_OUTLINE, rect, 1)


def draw_button(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    x: float,
    y: float,
    hover: bool,
    selected: bool = False,
    disabled: bool = False,
) -> pygame.Rect:
    """Draw a button and return its rect."""
    rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    if disabled:
        color = BUTTON_DISABLED
    elif selected:
        color = BUTTON_SELECTED
    else:
        color = BUTTON_HOVER if hover else BUTTON_COLOR
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, (100, 160, 220), rect, 2, border_radius=6)
    label = font.render(text, True, BUTTON_TEXT)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)
    return rect


def draw_slider(
    surface: pygame.Surface,
    font: pygame.font.Font,
    x: float,
    y: float,
    value: float,
    min_val: float,
    max_val: float,
    label: str,
) -> tuple[pygame.Rect, float]:
    """Draw a horizontal slider. Returns (full_slider_rect, value_from_0_to_1)."""
    track_rect = pygame.Rect(x, y, SLIDER_WIDTH, SLIDER_HEIGHT)
    pygame.draw.rect(surface, (60, 60, 75), track_rect, border_radius=4)
    t = (value - min_val) / (max_val - min_val) if max_val > min_val else 0
    t = max(0, min(1, t))
    thumb_x = x + t * (SLIDER_WIDTH - 16) + 8
    thumb_rect = pygame.Rect(thumb_x - 8, y - 2, 16, SLIDER_HEIGHT + 4)
    pygame.draw.rect(surface, BUTTON_COLOR, thumb_rect, border_radius=6)
    label_surf = font.render(label, True, TEXT_LABEL)
    surface.blit(label_surf, (x, y - 22))
    return track_rect, t


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sorting Algorithm Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 24)

    arr = generate_array(BAR_COUNT)
    max_val = max(arr) if arr else 1
    sort_generator = None
    compare_inds: list[int] = []
    sorted_inds: list[int] = []
    comparisons = 0
    accesses = 0
    selected_algorithm = "quicksort"
    steps_per_frame = 8
    slider_dragging = False

    # Sidebar layout
    sx = 14
    sy = 20
    algo_label_y = sy
    qs_rect = ms_rect = hs_rect = None
    sort_rect = None
    reset_rect = None
    slider_rect = None

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        is_sorting = sort_generator is not None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if reset_rect and reset_rect.collidepoint(mouse_pos):
                    sort_generator = None
                    arr = generate_array(BAR_COUNT)
                    max_val = max(arr) if arr else 1
                    compare_inds = []
                    sorted_inds = []
                    comparisons = 0
                    accesses = 0
                elif not is_sorting and sort_rect and sort_rect.collidepoint(mouse_pos):
                    if selected_algorithm == "quicksort":
                        sort_generator = quicksort(arr[:])
                    elif selected_algorithm == "mergesort":
                        sort_generator = mergesort(arr[:])
                    else:
                        sort_generator = heapsort(arr[:])
                    compare_inds = []
                    sorted_inds = []
                    comparisons = 0
                    accesses = 0
                elif not is_sorting and qs_rect and qs_rect.collidepoint(mouse_pos):
                    selected_algorithm = "quicksort"
                elif not is_sorting and ms_rect and ms_rect.collidepoint(mouse_pos):
                    selected_algorithm = "mergesort"
                elif not is_sorting and hs_rect and hs_rect.collidepoint(mouse_pos):
                    selected_algorithm = "heapsort"
                elif slider_rect and slider_rect.collidepoint(mouse_pos):
                    slider_dragging = True
                    rel_x = mouse_pos[0] - slider_rect.x
                    t = max(0, min(1, rel_x / slider_rect.w))
                    steps_per_frame = int(SPEED_STEPS_MIN + t * (SPEED_STEPS_MAX - SPEED_STEPS_MIN))
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slider_dragging = False
            if event.type == pygame.MOUSEMOTION and slider_dragging and slider_rect:
                rel_x = mouse_pos[0] - slider_rect.x
                t = max(0, min(1, rel_x / slider_rect.w))
                steps_per_frame = int(SPEED_STEPS_MIN + t * (SPEED_STEPS_MAX - SPEED_STEPS_MIN))

        if slider_dragging and slider_rect:
            rel_x = mouse_pos[0] - slider_rect.x
            t = max(0, min(1, rel_x / slider_rect.w))
            steps_per_frame = int(SPEED_STEPS_MIN + t * (SPEED_STEPS_MAX - SPEED_STEPS_MIN))

        # Advance sort generator (multiple steps per frame for speed)
        if sort_generator is not None:
            for _ in range(steps_per_frame):
                try:
                    arr, compare_inds, sorted_inds, comparisons, accesses = next(
                        sort_generator
                    )
                    max_val = max(arr) if arr else 1
                except StopIteration:
                    sort_generator = None
                    compare_inds = []
                    break

        screen.fill(BACKGROUND)
        # Sidebar background
        sidebar_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(screen, SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(screen, (60, 60, 80), (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, WINDOW_HEIGHT), 2)

        # Algorithm section
        algo_label = font.render("Algorithm", True, TEXT_LABEL)
        screen.blit(algo_label, (sx, algo_label_y))
        by = algo_label_y + 28
        qs_rect = draw_button(
            screen, font, "QuickSort", sx, by,
            qs_rect.collidepoint(mouse_pos) if qs_rect else False,
            selected=selected_algorithm == "quicksort",
            disabled=is_sorting,
        )
        ms_rect = draw_button(
            screen, font, "MergeSort", sx, by + BUTTON_HEIGHT + 6,
            ms_rect.collidepoint(mouse_pos) if ms_rect else False,
            selected=selected_algorithm == "mergesort",
            disabled=is_sorting,
        )
        hs_rect = draw_button(
            screen, font, "HeapSort", sx, by + 2 * (BUTTON_HEIGHT + 6),
            hs_rect.collidepoint(mouse_pos) if hs_rect else False,
            selected=selected_algorithm == "heapsort",
            disabled=is_sorting,
        )

        # Sort button
        sort_y = by + 3 * (BUTTON_HEIGHT + 6) + 10
        sort_rect = draw_button(
            screen, font, "Sort", sx, sort_y,
            sort_rect.collidepoint(mouse_pos) if sort_rect else False,
            disabled=is_sorting,
        )

        # Speed slider
        slider_y = sort_y + BUTTON_HEIGHT + 24
        slider_rect, _ = draw_slider(
            screen, font_small, sx, slider_y,
            steps_per_frame, SPEED_STEPS_MIN, SPEED_STEPS_MAX, "Speed"
        )
        speed_val = font_small.render(f"{steps_per_frame} steps/frame", True, TEXT_LABEL)
        screen.blit(speed_val, (sx, slider_y + SLIDER_HEIGHT + 4))

        # Counters
        counter_y = slider_y + SLIDER_HEIGHT + 32
        comp_label = font_small.render("Comparisons:", True, TEXT_LABEL)
        screen.blit(comp_label, (sx, counter_y))
        comp_val = font_small.render(str(comparisons), True, (255, 255, 255))
        screen.blit(comp_val, (sx + comp_label.get_rect().width + 8, counter_y))
        acc_label = font_small.render("Array Accesses:", True, TEXT_LABEL)
        screen.blit(acc_label, (sx, counter_y + 22))
        acc_val = font_small.render(str(accesses), True, (255, 255, 255))
        screen.blit(acc_val, (sx + acc_label.get_rect().width + 8, counter_y + 22))

        # Reset button
        reset_rect = draw_button(
            screen, font, "Reset", sx, counter_y + 52,
            reset_rect.collidepoint(mouse_pos) if reset_rect else False,
        )

        draw_bars(screen, arr, max_val, compare_inds, sorted_inds)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
