import threading
import time
import random
import keyboard

# Настройки
active = False
running = True
current_key = None
lock = threading.Lock()

HOLD_TIME = 2.0
SLEEP_TIME = 30.0
TICK = 0.05


# Воркер
def slave():
    global active, running, current_key
    keys = ['w', 'a', 's', 'd']

    while running:
        if not active:
            time.sleep(TICK)
            continue

        with lock:
            current_key = random.choice(keys)
            keyboard.press(current_key)
            print(f"Зажал: {current_key}")


        held = 0.0
        while held < HOLD_TIME and active and running:
            time.sleep(TICK)
            held += TICK


        with lock:
            if current_key:
                keyboard.release(current_key)
                print(f"Отпустил: {current_key}")
                current_key = None

        if not active or not running:
            continue


        print(f"Сон {SLEEP_TIME} сек...")
        slept = 0.0
        while slept < SLEEP_TIME and active and running:
            time.sleep(TICK)
            slept += TICK



def toggle_on():
    global active
    active = True
    print(">>> ON  (F6)")

def toggle_off():
    global active
    active = False
    print(">>> OFF (F12)")

def stop():
    global running, active
    running = False
    active = False
    print(">>> ВЫХОД (F8)")


# Старт этого дерьма
threading.Thread(target=slave, daemon=True).start()

keyboard.add_hotkey('f6',  toggle_on,  suppress=False)
keyboard.add_hotkey('f12',  toggle_off, suppress=False)
keyboard.add_hotkey('f8', stop,       suppress=False)

print("F6 — старт, F12 — стоп, F8 — выход.")

while running:
    time.sleep(0.1)

with lock:
    if current_key:
        keyboard.release(current_key)
        print(f"Аварийно отпустил: {current_key}")

print("Готово.")