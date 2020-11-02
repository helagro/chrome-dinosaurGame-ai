from PIL import ImageGrab
from neural_network import NN
import time
from pynput.keyboard import Key, Controller
import tweak as m

keyboard = Controller()
nn = NN()
screen_black = True


def is_thing(px):
    return px[0] == 172


def game_running(img):
    return img[m.GAME_OVER_LOCATION[0], m.GAME_OVER_LOCATION[1]][0] != 172


def click(key):
    keyboard.press(key)
    time.sleep(m.JUMP_HOLD_TIME)
    keyboard.release(key)


invalid_values = True
last_pos = m.WATCH_AREA_START + m.SPEED_MEASURE_AREA_STOP
time_checked = 0


def speed_calc(pos_now, last_speed):
    global invalid_values
    global last_pos
    global time_checked

    time_now = time.time()
    speed = last_speed

    if invalid_values:
        invalid_values = False

    else:
        speed = (last_pos - pos_now) / (time_now - time_checked)

    last_pos = pos_now
    time_checked = time_now

    return round(speed)


def found_in_duck_area():
    img = ImageGrab.grab().load()
    for i in range(m.DUCK_AREA_START, m.DUCK_AREA_END, 2):
        if is_thing(img[i, m.LOWER_WATCH_LINE]):
            return True
    return False


def duck_check():
    start_time = time.time()
    time.sleep(0.15)
    while found_in_duck_area():
        if time.time() - start_time > 1:
            return
    keyboard.press(Key.down)
    while not found_in_duck_area():
        if time.time() - start_time > 1:
            break
    keyboard.release(Key.down)


def run():
    global screen_black
    global invalid_values

    start_time = time.time()
    img = ImageGrab.grab().load()

    speed = m.START_SPEED

    while game_running(img):

        # checks lines
        found_at = -1
        for i in range(m.WATCH_AREA_START, m.WATCH_AREA_END, 2):

            if is_thing(img[i, m.LOWER_WATCH_LINE]):
                found_at = 0

                if i > m.WATCH_AREA_START + m.SPEED_MEASURE_AREA_START:
                    if i < m.WATCH_AREA_START + m.SPEED_MEASURE_AREA_STOP:
                        new_speed = speed_calc(i, speed)
                        speed = new_speed if new_speed > speed else speed
                else:
                    invalid_values = True

            elif is_thing(img[i, m.UPPER_WATCH_LINE]):
                found_at = 1

            if found_at != -1:
                if nn.act(i, speed):
                    click(Key.up)
                    duck_check()
                break

        img = ImageGrab.grab().load()
        # screen_black = is_black(img[m.SCREEN_CLR_PLACE, m.SCREEN_CLR_PLACE])

    time.sleep(0.2)
    click(Key.up)
    return time.time() - start_time


def main():
    if input("(l)oad or (n)ew?" ) == "l":
        nn.k = float(input("Enter k value: "))

    while True:
        score = run()
        if score < 4:
            continue
        print("Score: ", score)
        nn.adjust(score)


main()
