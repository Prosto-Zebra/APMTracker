import time
import tkinter as tk
import threading
from collections import deque
from pynput import keyboard, mouse


actions = deque()

def log_action():
    """Append timestamp when a key or mouse is pressed."""
    actions.append(time.time())

def on_key_press(key):
    log_action()

def on_mouse_click(x, y, button, pressed):
    if pressed:
        log_action()

def start_listeners():
    """Start keyboard and mouse listeners in separate threads."""
    kb_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_click=on_mouse_click)

    kb_listener.start()
    mouse_listener.start()

# UI code down below

root = tk.Tk()
root.title("APM Tracker")
root.geometry("450x200")
root.attributes("-topmost", True) # Code for making the window always on top, useful for software/games that is fullscreen

label = tk.Label(root, text="0.00 APM", font=("Arial", 60))
label.place(relx=0.5, rely=0.5, anchor="center")

# Main function for calculating APM and updating UI

def calculate_apm():

    now = time.time()


    while actions and now - actions[0] > 60:
        actions.popleft()


    active_time = now - actions[0] if actions else 1  
    APM = (len(actions) / active_time) * 60 if actions else 0  


    label.config(text=f"{APM:.2f} APM")
    root.after(100, calculate_apm)


listener_thread = threading.Thread(target=start_listeners, daemon=True)
listener_thread.start()


calculate_apm()
root.mainloop()