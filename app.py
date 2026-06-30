import customtkinter as ctk
import threading
import time
import random
import keyboard
from pynput.mouse import Controller, Button
from tkinter import Canvas

# ---------------- UI SETUP ----------------
ctk.set_appearance_mode("Dark")

app = ctk.CTk()
app.title("Rain Clicker")
app.geometry("520x380")
app.resizable(False, False)

mouse = Controller()

# ---------------- STATE ----------------
running = False
cps = 10

toggle_key = "f6"
click_button = "left"

capture_mode = None  # None | "toggle" | "click"

rain_drops = []

# ---------------- CLICKER ----------------
def click_loop():
    global running

    delay = lambda: 1 / max(cps, 1)

    while running:
        if click_button == "left":
            mouse.click(Button.left)
        else:
            mouse.click(Button.right)

        time.sleep(delay())


def toggle():
    global running

    running = not running

    if running:
        status.configure(text="Running", text_color="#00ff88")
        threading.Thread(target=click_loop, daemon=True).start()
    else:
        status.configure(text="Stopped", text_color="#ff5555")


# ---------------- KEY SYSTEM (FIXED) ----------------
def set_toggle_key():
    global capture_mode
    capture_mode = "toggle"
    status.configure(text="Press any key for TOGGLE...")


def set_click_key():
    global capture_mode
    capture_mode = "click"
    status.configure(text="Press L or R key...")


def on_key_event(e):
    global toggle_key, click_button, capture_mode

    if capture_mode is None:
        return

    key = e.name.lower()

    # TOGGLE KEY SET
    if capture_mode == "toggle":
        toggle_key = key

        keyboard.unhook_all_hotkeys()
        keyboard.add_hotkey(toggle_key, toggle)

        toggle_btn.configure(text=f"Toggle: {toggle_key.upper()}")
        status.configure(text="Stopped", text_color="#ff5555")

    # CLICK TYPE SET
    elif capture_mode == "click":
        if key == "l":
            click_button = "left"
            click_btn.configure(text="Click: LEFT")

        elif key == "r":
            click_button = "right"
            click_btn.configure(text="Click: RIGHT")

        status.configure(text="Stopped", text_color="#ff5555")

    capture_mode = None


keyboard.on_press(on_key_event)
keyboard.add_hotkey(toggle_key, toggle)

# ---------------- RAIN SYSTEM (SMOOTH + SLANTED) ----------------
canvas = Canvas(app, width=520, height=380, bg="#0b0b0b", highlightthickness=0)
canvas.place(x=0, y=0)


def create_rain():
    for _ in range(110):
        x = random.uniform(0, 520)
        y = random.uniform(-380, 380)

        length = random.uniform(10, 22)
        speed = random.uniform(1.5, 4.5)

        drop = canvas.create_line(
            x, y,
            x + 6, y + length,
            fill="#0c83eb",
            width=1,
            stipple="gray50"
        )

        rain_drops.append({
            "id": drop,
            "x": x,
            "y": y,
            "speed": speed,
            "length": length
        })


def animate_rain():
    while True:
        for d in rain_drops:
            d["x"] += 1.0
            d["y"] += d["speed"]

            if d["y"] > 380:
                d["x"] = random.uniform(0, 520)
                d["y"] = random.uniform(-50, -10)

            canvas.coords(
                d["id"],
                d["x"],
                d["y"],
                d["x"] + 6,
                d["y"] + d["length"]
            )

        time.sleep(0.016)  # ~60 FPS


create_rain()
threading.Thread(target=animate_rain, daemon=True).start()

# ---------------- UI ----------------
title = ctk.CTkLabel(app, text="RAIN CLICKER", font=("Segoe UI", 26, "bold"))
title.place(x=150, y=20)


def set_cps(v):
    global cps
    cps = int(float(v))
    cps_label.configure(text=f"{cps} CPS")


slider = ctk.CTkSlider(app, from_=1, to=200, command=set_cps)
slider.set(10)
slider.place(x=140, y=90)

cps_label = ctk.CTkLabel(app, text="10 CPS")
cps_label.place(x=240, y=120)

toggle_btn = ctk.CTkButton(app, text="Toggle: F6", command=set_toggle_key)
toggle_btn.place(x=180, y=160)

click_btn = ctk.CTkButton(app, text="Click: LEFT", command=set_click_key)
click_btn.place(x=180, y=200)

status = ctk.CTkLabel(app, text="Stopped", text_color="#ff5555", font=("Segoe UI", 16))
status.place(x=220, y=250)

start_btn = ctk.CTkButton(app, text="START / STOP", command=toggle, width=200, height=40)
start_btn.place(x=160, y=300)

app.mainloop()