import tkinter as tk
from tkinter import ttk
import random as rm
import subprocess
import time
import threading
import pygame

def get_chrome_tab_count():
    script = '''
    tell application "Google Chrome"
        set tabCount to 0
        repeat with w in windows
            set tabCount to tabCount + (count of tabs in w)
        end repeat
        return tabCount
    end tell
    '''
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return int(result.stdout.strip())
    except ValueError:
        return 0

brainrot_terms = {
    "rizz": "charisma",
    "gyatt": "gluteus maximus",
    "cap": "lie",
    "no cap": "truth",
    "sus": "suspicious",
    "drip": "style",
    "bet": "ok",
    "lit": "exciting",
    "fam": "family",
    "goat": "greatest of all time",
    "yeet": "throw",
    "salty": "bitter",
    "flex": "show off",
    "Skibidi": "never",
    "slay": "succeed",
    "Goblin mode": "crazy",
    "Baby Gronk": "who?",
    "kai cenat": "fierce",
    "Delulu": "delusional",
    "Fanum tax": "no"
}

def check(entry, currentsafe, result_label, root):
    result = entry.get()
    result = result.lower()
    if result == currentsafe:
        result_label.config(text="You are safe for now...", foreground="green")
        pygame.mixer.init()
        pygame.mixer.music.load("SoundEffect/Goodboy.mp3")
        pygame.mixer.music.play()
        root.after(3000, root.destroy)
    else:
        result_label.config(text=f"I'm sorry little one... The correct answer was: {currentsafe}", foreground="red")
        pygame.mixer.init()
        pygame.mixer.music.load("SoundEffect/fail.mp3")
        pygame.mixer.music.play()
        KILL()
        root.after(3000, root.destroy)

def spawn_tkinter():
    root = tk.Tk()   
    root.withdraw()
    root.title("Brain Rot Trainer")
    half_screen_width = root.winfo_screenwidth() // 2
    half_screen_height = root.winfo_screenheight() // 2
    
    half_screen_height = half_screen_height + rm.randint(-100, 100)
    half_screen_width = half_screen_width + rm.randint(-100, 100)
    root.geometry(f"600x300+{half_screen_width}+{half_screen_height}")
    
    root.resizable(False, False)
    
    term = rm.choice(list(brainrot_terms.keys()))
    currentsafe = brainrot_terms[term]
    
    term1 = ttk.Label(root, text=f"Brain Rot Term:", font=("Helvetica", 25, "bold"))
    term1.pack(pady=(5, 5))
    
    term2 = ttk.Label(root, text=f"{term}", font=("Helvetica", 50, "bold"))
    term2.pack(pady=(0, 5))
    
    entry = ttk.Entry(root)
    entry.pack(pady=(20, 0))
    entry.insert(0, "Enter proper term here")
    
    result_label = ttk.Label(root, text="", foreground="red")
    result_label.pack(pady=(5, 5))
    
    ttk.Button(root, text="Check", command=lambda: check(entry, currentsafe, result_label, root)).pack(pady=(5, 0))
    
    timer_label = ttk.Label(root, text="00:20", anchor="center", font=("DS-Digital", 24, "bold"), foreground="red") #CHANGE THIS FOR TIMER
    timer_label.pack(pady=(10, 10))
    
    def update_timer():
        current_time = int(timer_label.cget("text").split(":")[1])
        if current_time > 0 and result_label.cget("text") == "":
            current_time -= 1
            timer_label.config(text=f"00:{current_time:02d}")
            root.after(1000, update_timer)
        else:
            if result_label.cget("text") == "":
                result_label.config(text=f"I'm sorry little one... The correct answer was: {currentsafe}", foreground="red")
                KILL()
                root.after(3000, root.destroy)
            
    update_timer()
    root.deiconify()
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.protocol("WM_CLOSE", lambda: None)
    root.deiconify()
    root.bell()       
    root.mainloop()

def KILL():
    print("bye bye")

def monitor_tabs(root):
    prevtabcount = 0
    while True:
        tab_count = get_chrome_tab_count()
        if tab_count > prevtabcount:
            print("New tab opened!")
            root.after(0, spawn_tkinter)
        prevtabcount = tab_count
        time.sleep(0.25)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    threading.Thread(target=monitor_tabs, args=(root,), daemon=True).start()
    root.mainloop()
    monitor_tabs(root)
