from kb_poller import KBPoller
import time

running = True

player_x = 10
player_y = 10



x_min = 0
x_max = 100
y_min = 0
y_max = 100

kb_poller = KBPoller()


def scan_keys():
    return kb_poller.pressed


def render_state():
    print("player is at:", player_x, player_y)


def update_state(pressed_key):
    global player_x, player_y, running
    if "a" in pressed_key:
        player_x -= 1
    if "d" in pressed_key:
        player_x += 1
    if "w" in pressed_key:
        player_y -= 1
    if "s" in pressed_key:
        player_y += 1
    if "q" in pressed_key:
        running = False

    if player_x < x_min:
        player_x = x_min
    if player_x > x_max:
        player_x = x_max
    if player_y < y_min:
        player_y = y_min
    if player_y > y_max:
        player_y = y_max


while running:
    # read/check for user actions (input)
    # update game state (physics, AI, etc)
    # render game state (graphics)

    render_state()
    pressed_key = scan_keys()
    update_state(pressed_key)
    time.sleep(0.5)
