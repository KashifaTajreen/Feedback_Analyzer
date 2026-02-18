import tkinter as tk
from tkinter import messagebox
from data import insert_new_session

# --- CONSISTENT THEME COLORS ---
BG_DARK = "#0f172a"      # Midnight Slate
BG_CARD = "#1e293b"      # Input Background
ACCENT = "#22d3ee"       # Cyan Text/Highlights
TEXT_MAIN = "#f8fafc"    # Bright Off-white
TEXT_DIM = "#94a3b8"     # Muted Placeholder Text
BTN_COLOR = "#0ea5e9"    # Sky Blue Button

def add_placeholder(entry, text, is_password=False):
    entry.insert(0, text)
    entry.config(fg=TEXT_DIM)

    def on_focus_in(e):
        if entry.get() == text:
            entry.delete(0, "end")
            entry.config(fg=TEXT_MAIN)
            if is_password:
                entry.config(show="•")

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg=TEXT_DIM)
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def open_create_session(parent, refresh_callback):
    popup = tk.Toplevel(parent)
    popup.title("Create New Session")
    popup.geometry("420x580")
    popup.configure(bg=BG_DARK)
    popup.grab_set()

    # --- HEADER ---
    tk.Label(popup, text="Session Setup", font=("Segoe UI", 20, "bold"), 
             bg=BG_DARK, fg=ACCENT).pack(pady=(35, 25))
    
    # Input container
    input_frame = tk.Frame(popup, bg=BG_DARK)
    input_frame.pack(fill="x", padx=45)

    def create_styled_entry(placeholder, is_pass=False):
        # Entry with subtle border and theme colors
        e = tk.Entry(input_frame, font=("Segoe UI", 11), bg=BG_CARD, 
                     fg=TEXT_MAIN, insertbackground=TEXT_MAIN, 
                     relief="solid", borderwidth=1, highlightthickness=0)
        e.pack(pady=10, ipady=10, fill="x")
        add_placeholder(e, placeholder, is_pass)
        return e

    name_e = create_styled_entry("Session Name")
    host_e = create_styled_entry("Host Name")
    id_e = create_styled_entry("Session ID")
    date_e = create_styled_entry("YYYY-MM-DD")
    pass_e = create_styled_entry("Session Password", True)
    
    def save():
        insert_new_session(id_e.get(), name_e.get(), date_e.get(), pass_e.get(), host_e.get())
        popup.destroy()
        refresh_callback()

    # Create Button with Hover Effect
    create_btn = tk.Button(popup, text="CREATE SESSION", bg=BTN_COLOR, fg="white",
                          activebackground=ACCENT, activeforeground=BG_DARK,
                          font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                          command=save)
    create_btn.pack(pady=40, ipady=12, fill="x", padx=45)

    create_btn.bind("<Enter>", lambda e: create_btn.config(bg=ACCENT, fg=BG_DARK))
    create_btn.bind("<Leave>", lambda e: create_btn.config(bg=BTN_COLOR, fg="white"))

def verify_host_password(parent, session, success_callback):
    pw_win = tk.Toplevel(parent)
    pw_win.title("Security Check")
    pw_win.geometry("380x260")
    pw_win.configure(bg=BG_DARK)
    
    # Center logic
    pw_win.update_idletasks()
    w, h = 380, 260
    x = (pw_win.winfo_screenwidth() // 2) - (w // 2)
    y = (pw_win.winfo_screenheight() // 2) - (h // 2)
    pw_win.geometry(f"{w}x{h}+{x}+{y}")
    
    pw_win.transient(parent)
    pw_win.grab_set()

    tk.Label(pw_win, text="Verification Required",
             font=("Segoe UI", 15, "bold"), bg=BG_DARK, fg=ACCENT).pack(pady=(30, 5))
    
    tk.Label(pw_win, text=f"Accessing: {session['name']}",
             font=("Segoe UI", 10), bg=BG_DARK, fg=TEXT_DIM).pack(pady=(0, 20))

    pw_entry = tk.Entry(pw_win, show="•", font=("Segoe UI", 14), 
                        bg=BG_CARD, fg=TEXT_MAIN, relief="flat", 
                        insertbackground=TEXT_MAIN, justify="center")
    pw_entry.pack(pady=10, ipady=8, padx=60, fill="x")
    pw_entry.focus_set()

    def check_password():
        if pw_entry.get() == session['password']:
            pw_win.destroy()
            success_callback()
        else:
            messagebox.showerror("Error", "Incorrect Password")
            pw_entry.delete(0, tk.END)

    verify_btn = tk.Button(pw_win, text="Verify Access", bg=BTN_COLOR, fg="white",
                          font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                          activebackground=ACCENT, command=check_password)
    verify_btn.pack(pady=25, ipady=8, padx=60, fill="x")
    
    verify_btn.bind("<Enter>", lambda e: verify_btn.config(bg=ACCENT, fg=BG_DARK))
    verify_btn.bind("<Leave>", lambda e: verify_btn.config(bg=BTN_COLOR, fg="white"))
    
    pw_win.bind('<Return>', lambda e: check_password())

    