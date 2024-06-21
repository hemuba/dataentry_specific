import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
from pynput import mouse
import keyboard
import threading
import pyperclip

positions = []
stop_requested = False

def click_and_paste(x, y, text, retries=3, delay=0.7):
    for _ in range(retries):
        pyautogui.click(x, y)
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(delay)  # Aggiunto un ritardo
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(delay)  # Aggiunto un ritardo
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(delay)  # Aggiunto un ritardo
        pasted_text = pyperclip.paste()
        if pasted_text == text:
            return True
    return False

def on_esc(event=None):
    global stop_requested
    stop_requested = True
    messagebox.showwarning("Warning", "Operation interrupted by user using ESC.")
    try:
        guide_window.quit()
    except:
        pass

    try:
        data_entry_window.quit()
    except:
        pass

    listener.stop()
    exit()

def start_entry():
    global stop_requested
    if len(positions) < 3:
        messagebox.showerror("Error", "Please capture all the required coordinates first!")
        return

    COUNTRY_CODES = entry_country_codes.get("1.0", "end-1c").split("\n")
    COUNTRY_NAMES = entry_country_names.get("1.0", "end-1c").split("\n")
    COUNTRY_CODES = [code for code in COUNTRY_CODES if code.strip()]
    COUNTRY_NAMES = [name for name in COUNTRY_NAMES if name.strip()]

    if len(COUNTRY_CODES) != len(COUNTRY_NAMES):
        messagebox.showerror("Error", "The number of country codes and country names do not match!")
        return

    try:
        delay = float(entry_delay.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid delay value!")
        return

    for code, name in zip(COUNTRY_CODES, COUNTRY_NAMES):
        if stop_requested:
            break
        code = code.strip()
        name = name.strip()
        success_code = click_and_paste(*positions[0], code)
        time.sleep(delay)
        success_name = click_and_paste(*positions[1], name)
        time.sleep(delay)
        if success_code and success_name:
            pyautogui.click(*positions[2])
            time.sleep(delay)
        else:
            messagebox.showwarning("Warning", "Data entry failed for one of the fields.")
            break

    if stop_requested:
        messagebox.showwarning("Warning", "Data entry was interrupted by user.")
    else:
        messagebox.showinfo("Info", "Data Entry is Done. Thank you for using this tool.")
    data_entry_window.destroy()

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        positions.append((x, y))
        instruction_label.configure(bg="green")
        guide_window.update()
        time.sleep(0.5)
        if len(positions) < 3:
            instruction_label.configure(bg="SystemButtonFace", text=f"Click on the Screen for {instructions[len(positions)]} coordinates.")
        elif len(positions) == 3:
            instruction_label.configure(bg="SystemButtonFace", text=f"Click TWO more times to proceed to the data entry interface.")
        else:
            guide_window.quit()

instructions = ["Country Code", "Country Name", "Save and Continue"]

def welcome_window():
    welcome_win = tk.Tk()
    welcome_win.title("Country Compiler AD V1")
    
    welcome_label = tk.Label(welcome_win, text="Welcome to Country Compiler AD V1!", font=("Verdana", 10))
    welcome_label.pack(pady=10)
    
    disclaimer_label = tk.Label(
        welcome_win,
        text=("WARNING: By using this software, you agree to exempt the creator"
              " from any responsibility related to improper use, malfunctions, or any"
              " other problem arising from its use."),
        font=("Verdana", 8),
        wraplength=400,  # Set a maximum width for the text
        justify="left",  # Left text alignment
        fg="red"  # Text color
    )
    disclaimer_label.pack(pady=20)

    btn_continue = tk.Button(welcome_win, text="Accept and Continue", command=welcome_win.quit, font=("Verdana", 10))
    btn_continue.pack(pady=10)
    
    welcome_win.mainloop()
    welcome_win.destroy()

welcome_window()

guide_window = tk.Tk()
guide_window.title("Country Compiler AD V1")
guide_window.bind('<Escape>', on_esc)

instruction_label = tk.Label(guide_window, text=f"Click on the Screen for {instructions[0]} coordinates.", font=("Verdana", 10))
instruction_label.pack(pady=10)

listener = mouse.Listener(on_click=on_click)
listener_thread = threading.Thread(target=listener.start)
listener_thread.start()

keyboard.add_hotkey('esc', on_esc)

guide_window.mainloop()
listener.stop()
guide_window.destroy()

def launch_data_entry_window():
    global entry_country_codes, entry_country_names, entry_delay, data_entry_window
    data_entry_window = tk.Tk()
    data_entry_window.title("Country Compiler AD V1")
    data_entry_window.bind('<Escape>', on_esc)

    instruction_label = tk.Label(data_entry_window, text="Now insert your data.", font=("Verdana", 10))
    instruction_label.pack(pady=10)

    label_country_codes = tk.Label(data_entry_window, text="Enter country codes (one per line):", font=("Verdana", 10))
    label_country_codes.pack(pady=5)
    entry_country_codes = tk.Text(data_entry_window, height=10, width=40)
    entry_country_codes.pack(pady=5)

    label_country_names = tk.Label(data_entry_window, text="Enter country names (one per line):", font=("Verdana", 10))
    label_country_names.pack(pady=5)
    entry_country_names = tk.Text(data_entry_window, height=10, width=40)
    entry_country_names.pack(pady=5)

    label_delay = tk.Label(data_entry_window, text="Enter the delay between operations (in seconds):", font=("Verdana", 10))
    label_delay.pack(pady=5)
    entry_delay = tk.Entry(data_entry_window, width=20)
    entry_delay.insert(0, "0.5")
    entry_delay.pack(pady=5)

    btn_start = tk.Button(data_entry_window, text="Start Entry", command=start_entry, font=("Verdana", 10))
    btn_start.pack(pady=10)

    btn_exit = tk.Button(data_entry_window, text="Exit", command=data_entry_window.quit, font=("Verdana", 10))
    btn_exit.pack(pady=10)

    # Adding the ESC label
    esc_label = tk.Label(data_entry_window, text="Press ESC at any time to stop the program.", font=("Verdana", 8), fg="red")
    esc_label.pack(pady=5)

    data_entry_window.mainloop()

launch_data_entry_window()
