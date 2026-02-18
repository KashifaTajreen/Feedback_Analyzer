import tkinter as tk
from tkinter import messagebox
from data import get_all_sessions, init_sessions_db, delete_session 
from host_tools import open_create_session, verify_host_password
from gui import run_gui 
from analysis_view import run_analysis_view

def run_dashboard(parent, user_email):
    init_sessions_db() 
    if parent: parent.withdraw()
    
    # --- COLORS ---
    BG_DARK = "#0f172a"      
    BG_CARD = "#1e293b"      
    ACCENT = "#22d3ee"       
    TEXT_MAIN = "#f8fafc"    
    TEXT_DIM = "#94a3b8"     
    BTN_PRIMARY = "#0ea5e9"  
    BTN_SECONDARY = "#334155"
    GIVE_FEEDBACK_GREEN = "#10b981"

    root = tk.Tk() if parent is None else tk.Toplevel(parent)
    root.title("Feedback Dashboard")
    root.state("zoomed")
    root.configure(bg=BG_DARK)

    # --- PERSISTENT HEADER ---
    header_frame = tk.Frame(root, bg=BG_DARK, pady=20)
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="FEEDBACK ANALYZER", font=("Segoe UI", 28, "bold"), bg=BG_DARK, fg=ACCENT).pack()
    tk.Label(header_frame, text=f"Logged in : {user_email.split('@')[0].upper()}", font=("Segoe UI", 11), bg=BG_DARK, fg=TEXT_DIM).pack()

    # --- SCROLLABLE AREA ---
    canvas = tk.Canvas(root, bg=BG_DARK, highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=BG_DARK)

    window_id = canvas.create_window((root.winfo_screenwidth()//2, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def load_sessions():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        try:
            sessions = get_all_sessions()
            for i, s in enumerate(sessions):
                # CARD CONTAINER
                card = tk.Frame(scrollable_frame, bg=BG_CARD, width=320, height=220, # Reduced height
                                highlightbackground=BTN_SECONDARY, highlightthickness=1)
                card.grid(row=i//3, column=i%3, padx=20, pady=20)
                card.pack_propagate(False)

                # THREE DOTS
                menu_btn = tk.Label(card, text="⋮", font=("Segoe UI", 18, "bold"), bg=BG_CARD, fg=TEXT_DIM, cursor="hand2")
                menu_btn.place(relx=0.95, rely=0.05, anchor="ne")

                def show_menu(event, session=s):
                    menu = tk.Menu(root, tearoff=0, bg=BG_CARD, fg=TEXT_MAIN, activebackground=ACCENT, activeforeground=BG_DARK)
                    menu.add_command(label="🗑 Delete Session", command=lambda: handle_delete(session))
                    menu.post(event.x_root, event.y_root)
                menu_btn.bind("<Button-1>", show_menu)

                # LABELS
                tk.Label(card, text=s['name'], font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(pady=(20, 2))
                tk.Label(card, text=f"ID: {s['id']}", font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_DIM).pack()

                # BUTTONS (Tightened padding)
                tk.Button(card, text="Give Feedback", bg=GIVE_FEEDBACK_GREEN, fg="white", relief="flat",
                          font=("Segoe UI", 10, "bold"), cursor="hand2", 
                          command=lambda sess=s: run_gui(root, sess)).pack(fill="x", padx=30, pady=(25, 10))

                tk.Button(card, text="View Analysis", bg=BTN_SECONDARY, fg=TEXT_MAIN, relief="flat",
                          font=("Segoe UI", 10, "bold"), cursor="hand2", 
                          command=lambda sess=s: verify_host_password(root, sess, lambda: run_analysis_view(root, sess))).pack(fill="x", padx=30)

                #  HOVER EFFECTS
                def on_enter(e, c=card): c.config(highlightbackground=ACCENT, highlightthickness=2)
                def on_leave(e, c=card): c.config(highlightbackground=BTN_SECONDARY, highlightthickness=1)
                card.bind("<Enter>", on_enter)
                card.bind("<Leave>", on_leave)

        except Exception as e:
            print(f"Error: {e}")

    def handle_delete(session):
        def on_success():
            if messagebox.askyesno("Confirm Delete", f"Permanently delete '{session['name']}'?"):
                if delete_session(session['id']): # Checking for successful return
                    load_sessions()
        verify_host_password(root, session, on_success)

    # FAB BUTTON
    add_btn = tk.Button(root, text="+ Create New Session", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 11, "bold"), 
                        relief="flat", cursor="hand2", padx=20, pady=10, command=lambda: open_create_session(root, load_sessions))
    add_btn.place(relx=0.97, rely=0.95, anchor="se")

    load_sessions()
    root.mainloop()


           



