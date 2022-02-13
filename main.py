import pygame
import gc
from datetime import timedelta
from timeit import default_timer
from data.text import Font
import wx.adv
import wx

# Pygame init
pygame.init()
screen = pygame.display.set_mode((386, 233))
icon = pygame.image.load("./data/icon.png").convert_alpha()
pygame.display.set_caption("Stopwatch")
pygame.display.set_icon(icon)

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


# Creates a menu for the task bar icon
def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


# Class for the task bar icon
class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.SetIcon(wx.Icon("data/white_icon.png"), "Stopwatch")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.maximize_screen)

    def CreatePopupMenu(self):
        """Creates a popup menu, runs when new TaskBarIcon is created because this is overwriting the CreatePopupMenu method"""
        menu = wx.Menu()
        create_menu_item(menu, 'Exit', self.exit)
        return menu

    # noinspection PyMethodMayBeStatic
    def maximize_screen(self, _event):
        """Maximises screen when user clicks on task bar icon"""
        global screen
        screen = pygame.display.set_mode((386, 233))
        pygame.display.set_icon(icon)

    def exit(self, _event):
        """Closes program"""
        global running
        self.Destroy()
        running = False


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


app = wx.App()  # Wx.App(), this is needed for TaskBarIcon to work
TaskBarIcon()  # Creates a task bar icon
running = True
while running:

    screen.fill((23, 23, 23))
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
        screen.blit(button, (5, 106))  # Blits button
        timer_font.render("PAUSE", screen, [(57, 119)])  # Renders "PAUSE" text on button
    else:
        mouse_hover = update_button((10, 138, 10), (0, 128, 0), "START")  # Updates button and returns if the mouse is hovering over button or not
        screen.blit(button, (5, 106))  # Blits button
        timer_font.render("START", screen, [(57, 119)])  # Renders "START" text on button
    timer_font.render(total_time, screen, [(5, 5)])  # Renders time to screen, hours, minutes, and seconds(HH/MM/SS)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            # Changes button to start/pause
            if mouse_hover:
                button_state = not button_state
                # If program was paused, starts time
                if button_state:
                    old_time = default_timer() - start

        # Minimizes program to system tray(basically just hides the window)
        # Tray icon exists all the time so user can just click tray icon to maximize it or close it
        if event.type == pygame.QUIT:
            screen = pygame.display.set_mode((386, 233), pygame.HIDDEN)

    # Updates screen
    pygame.display.flip()
    clock.tick(24)
    gc.collect()
