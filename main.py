import pygame
import pystray
from PIL import Image
import webbrowser
from datetime import timedelta
from timeit import default_timer
from data.text import Font
import gc

pygame.init()  # Pygame init
display = pygame.display.set_mode((386, 233), pygame.RESIZABLE)  # Pygame window
pygame.display.set_caption("Stopwatch")  # Sets window caption

pil_icon_image = Image.open("data/white_icon.png")  # Icon image for system tray icon
black_icon_image = pygame.image.load("data/icon.png").convert_alpha()  # Icon for window
pygame.display.set_icon(black_icon_image)  # Sets window icon

# Timers
clock = pygame.time.Clock()  # Pygame clock for limiting framerate
start = default_timer()  # Time in seconds
old_time = default_timer() - start  # Time from previous iteration of loop

# Other stuff
timer_font = Font("./data/large_font.png", (250, 250, 250), (1, 0, 0), size=8)  # Font cached at startup
button = pygame.Surface((376, 122))  # Creates the start/stop button
button_state = False  # Boolean button_state, True is PAUSE button state, and False is START button state
duration = 0  # Duration of time that has passed in seconds
total_time = "0" + str(timedelta(seconds=int(duration)))  # Converts duration(time in seconds) to hours, minutes, and seconds


def maximize_window():
    """Maximizes window"""
    global display
    global icon
    display = pygame.display.set_mode((386, 233), pygame.RESIZABLE)  # Re-initializes window so that it's not hidden anymore
    pygame.display.set_icon(black_icon_image)  # Resets window icon
    icon.visible = False
    icon.stop()  # Stops system tray icon


def close():
    """Closes program"""
    global running
    running = False  # Ends main loop
    icon.visible = False
    icon.stop()  # Stops system tray icon


def open_github():
    """Opens the Github page for this project"""
    webbrowser.open('https://github.com/ManPandaMakes/Stopwatch')


def update_button(first_color, second_color, _button_state):
    """Updates button, and changes color depending on if the mouse is hovering over button.
    Returns if the mouse is hovering over button or not"""
    _mouse_hover = False
    # noinspection PyChainedComparisons
    if mouse[0] > 4 and mouse[0] < 381 and mouse[1] > 105 and mouse[1] < 228:
        _mouse_hover = True
        button.fill(first_color)
    else:
        button.fill(second_color)
    return _mouse_hover


# Menu for system tray icon
menu = (pystray.MenuItem('Github', open_github,), pystray.MenuItem('Exit', close), pystray.MenuItem("maximise window", maximize_window, default=True, visible=False))

running = True
while running:

    display.fill((0, 0, 0))
    clock.tick(24)  # Sets the framerate to 24
    mouse = pygame.mouse.get_pos()

    if button_state:
        total_time = str(timedelta(seconds=int(duration)))  # Converts duration(time in seconds) to hours, minutes, and seconds
        # Timedelta turns time in seconds into H/MM/SS, this checks if hours is a single digit(9 or less), and adds a zero to the start if it is
        # Tl;dr turns H/MM/SS to HH/MM/SS
        if total_time[1] == ":":
            total_time = "0" + total_time

        duration += (default_timer() - start) - old_time  # Increases time
        old_time = default_timer() - start  # Old time from last iteration of loop
        mouse_hover = update_button((255, 10, 10), (160, 0, 0), "PAUSE")  # Updates button and returns if the mouse is hovering over button or not
        display.blit(button, (5, 106))  # Blits button
        timer_font.render("PAUSE", display, [(57, 119)])  # Renders "PAUSE" text on button
    else:
        mouse_hover = update_button((10, 138, 10), (0, 128, 0), "START")  # Updates button and returns if the mouse is hovering over button or not
        display.blit(button, (5, 106))  # Blits button
        timer_font.render("START", display, [(57, 119)])  # Renders "START" text on button
    timer_font.render(total_time, display, [(5, 5)])  # Renders time to screen, hours, minutes, and seconds(HH/MM/SS)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            # Changes button to start/pause
            if mouse_hover:
                button_state = not button_state
                # If program was paused, starts time
                if button_state:
                    old_time = default_timer() - start

        # If user clicks close button, minimize to system tray
        if event.type == pygame.QUIT:  # If user clicks the close button:
            screen = pygame.display.set_mode((386, 233), pygame.HIDDEN)  # Hides pygame window
            icon = pystray.Icon("Stopwatch", pil_icon_image, "Stopwatch", menu)  # System tray icon, I have to redeclare it every time because otherwise it'll crash
            icon.run()  # Re-initializes system tray icon

    pygame.display.flip()  # Updates screen
    gc.collect()
