import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from threading import Thread, Event
from time import gmtime, strftime, sleep
from counter import counter
from group_joiner import GroupJoiner
from output import Output
import sys
import os

class RobloxGroupJoinerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Auto-Group Joiner")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.button_color = "#313244"
        self.success_color = "#a6e3a1"
        self.error_color = "#f38ba8"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.is_running = False
        self.stop_event = Event()
        self.threads = []
        self.cookies = []
        self.proxies = []
        self.group_id = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🚀 Roblox Auto-Group Joiner",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Mass join Roblox groups with captcha solving",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Left panel - Inputs
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Group ID
        self.create_input_section(left_frame, "Group ID", "Enter Roblox Group ID", 0)
        
        # Cookies
        self.create_textarea_section(left_frame, "Cookies (.ROBLOSECURITY)", "Enter cookies (one per line)", 1, 5)
        
        # Proxies
        self.create_textarea_section(left_frame, "Proxies", "Enter proxies (one per line)\nFormat: http://user:pass@ip:port", 2, 5)
        
        # Right panel - Status and controls
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Stats frame
        stats_frame = tk.LabelFrame(
            right_frame,
            text="Statistics",
            font=("Segoe UI", 12, "bold"),
            bg=self.button_color,
            fg=self.fg_color,
            bd=2
        )
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            stats_frame,
            text="Status: Idle",
            font=("Segoe UI", 11),
            bg=self.button_color,
            fg=self.fg_color,
            anchor="w"
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Groups joined counter
        self.joined_label = tk.Label(
            stats_frame,
            text="Groups Joined: 0",
            font=("Segoe UI", 11),
            bg=self.button_color,
            fg=self.success_color,
            anchor="w"
        )
        self.joined_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Runtime
        self.runtime_label = tk.Label(
            stats_frame,
            text="Runtime: 00:00:00",
            font=("Segoe UI", 11),
            bg=self.button_color,
            fg=self.fg_color,
            anchor="w"
        )
        self.runtime_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Control buttons
        button_frame = tk.Frame(right_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ Start",
            font=("Segoe UI", 12, "bold"),
            bg=self.success_color,
            fg="#1e1e2e",
            activebackground="#94e2d5",
            command=self.start_joining,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.stop_button = tk.Button(
            button_frame,
            text="⬛ Stop",
            font=("Segoe UI", 12, "bold"),
            bg=self.error_color,
            fg="#1e1e2e",
            activebackground="#eba0ac",
            command=self.stop_joining,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Log output
        log_frame = tk.LabelFrame(
            right_frame,
            text="Activity Log",
            font=("Segoe UI", 12, "bold"),
            bg=self.button_color,
            fg=self.fg_color,
            bd=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg="#181825",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Footer
        footer = tk.Label(
            self.root,
            text="Powered by FunBypass.com | Made with ❤️",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.fg_color
        )
        footer.pack(side=tk.BOTTOM, pady=10)
        
    def create_input_section(self, parent, label_text, placeholder, row):
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        label.pack(fill=tk.X, pady=(10, 5))
        
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            bg=self.button_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=0
        )
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.on_entry_click(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.on_focus_out(entry, placeholder))
        entry.pack(fill=tk.X, ipady=8, padx=2)
        
        if row == 0:
            self.group_id_entry = entry
            
    def create_textarea_section(self, parent, label_text, placeholder, row, height):
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        label.pack(fill=tk.X, pady=(10, 5))
        
        text_widget = scrolledtext.ScrolledText(
            parent,
            font=("Consolas", 9),
            bg=self.button_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=0,
            height=height,
            wrap=tk.WORD
        )
        text_widget.insert("1.0", placeholder)
        text_widget.bind("<FocusIn>", lambda e: self.on_text_click(text_widget, placeholder))
        text_widget.bind("<FocusOut>", lambda e: self.on_text_focus_out(text_widget, placeholder))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=2)
        
        if row == 1:
            self.cookies_text = text_widget
        elif row == 2:
            self.proxies_text = text_widget
            
    def on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.fg_color)
            
    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#6c7086")
            
    def on_text_click(self, text_widget, placeholder):
        if text_widget.get("1.0", tk.END).strip() == placeholder:
            text_widget.delete("1.0", tk.END)
            text_widget.config(fg=self.fg_color)
            
    def on_text_focus_out(self, text_widget, placeholder):
        if text_widget.get("1.0", tk.END).strip() == "":
            text_widget.insert("1.0", placeholder)
            text_widget.config(fg="#6c7086")
            
    def log(self, message, level="INFO"):
        self.log_text.config(state=tk.NORMAL)
        
        colors = {
            "INFO": self.accent_color,
            "SUCCESS": self.success_color,
            "ERROR": self.error_color,
            "CAPTCHA": "#f9e2af"
        }
        
        color = colors.get(level, self.fg_color)
        
        self.log_text.insert(tk.END, f"[{level}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def start_joining(self):
        # Validate inputs
        group_id = self.group_id_entry.get()
        if not group_id or group_id == "Enter Roblox Group ID":
            messagebox.showerror("Error", "Please enter a Group ID")
            return
            
        cookies_text = self.cookies_text.get("1.0", tk.END).strip()
        if not cookies_text or cookies_text == "Enter cookies (one per line)":
            messagebox.showerror("Error", "Please enter at least one cookie")
            return
            
        self.cookies = [c.strip() for c in cookies_text.split("\n") if c.strip()]
        
        # Load proxies from text area and file
        proxies_text = self.proxies_text.get("1.0", tk.END).strip()
        if proxies_text and proxies_text != "Enter proxies (one per line)\nFormat: http://user:pass@ip:port":
            self.proxies = [p.strip() for p in proxies_text.split("\n") if p.strip()]
            
            # Save proxies to both root and input directory
            for filepath in ["proxies.txt", "input/proxies.txt"]:
                os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as f:
                    for proxy in self.proxies:
                        f.write(f"{proxy}\n")
        
        self.group_id = group_id
        self.is_running = True
        self.stop_event.clear()
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running", fg=self.success_color)
        
        # Start threads
        for cookie in self.cookies:
            t = Thread(target=GroupJoiner.join_group, args=(self.group_id, cookie, self.stop_event))
            self.threads.append(t)
            t.start()
            
        # Start stats updater
        Thread(target=self.update_stats, daemon=True).start()
        
        self.log(f"Started joining group {group_id} with {len(self.cookies)} cookies", "SUCCESS")
        
    def stop_joining(self):
        self.is_running = False
        self.stop_event.set()
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg=self.error_color)
        
        self.log("Stopped joining groups", "INFO")
        
    def update_stats(self):
        elapsed = 0
        
        while self.is_running:
            joined = counter.get_value()
            
            self.joined_label.config(text=f"Groups Joined: {joined}")
            self.runtime_label.config(text=f"Runtime: {strftime('%H:%M:%S', gmtime(elapsed))}")
            
            elapsed += 1
            sleep(1)


def main():
    # Redirect output to GUI
    original_output_init = Output.__init__
    
    def custom_init(self, level):
        original_output_init(self, level)
        self.gui_log = None
        
    def custom_log(self, *args, **kwargs):
        message = ' '.join(str(arg) for arg in args)
        if hasattr(self, 'gui_log') and self.gui_log:
            self.gui_log(message, self.level)
        # Also print to console
        original_log(self, *args, **kwargs)
        
    original_log = Output.log
    Output.__init__ = custom_init
    Output.log = custom_log
    
    # Create GUI
    root = tk.Tk()
    app = RobloxGroupJoinerUI(root)
    
    # Set GUI log function
    Output.log.__func__.__defaults__ = (app.log,)
    
    root.mainloop()


if __name__ == "__main__":
    main()
