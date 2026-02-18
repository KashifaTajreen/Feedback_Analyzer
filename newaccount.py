
import tkinter as tk
from tkinter import messagebox
from data import create_account, email_exists

def open_create_account_window():
    # Use Toplevel so it opens as a new window over the login page
    window = tk.Toplevel()
    window.title("Create New Account")
    window.state("zoomed")
    
    # --- 1.GRADIENT BACKGROUND ---
    canvas = tk.Canvas(window, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_gradient():
        canvas.update()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        for i in range(height):
            r = int(203 + (241 - 203) * (i / height))
            g = int(213 + (245 - 213) * (i / height))
            b = int(225 + (249 - 225) * (i / height))
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)

    window.after(10, draw_gradient)

    # --- 2. THE WHITE CARD ---
    card_color = "#FFFFFF"
    primary_btn = "#4F46E5"
    secondary_text = "#64748B"
    
    card = tk.Frame(canvas, bg=card_color, padx=50, pady=50, 
                    highlightbackground="#CBD5E1", highlightthickness=1)
    # Centers the card on the screen
    canvas.create_window(window.winfo_screenwidth()//2, window.winfo_screenheight()//2, window=card)

    # --- 3. THE HEADER ---
    header_frame = tk.Frame(card, bg=card_color)
    header_frame.pack(fill="x", pady=(0, 30))

    tk.Label(header_frame, text="Register Account", font=("Segoe UI", 24, "bold"), 
             bg=card_color, fg="#1E293B").pack()
    
    tk.Label(header_frame, text="Join Feedback Analyzer", font=("Segoe UI", 10), 
             bg=card_color, fg=secondary_text).pack(pady=(5, 0))

    # --- 4. INPUT AREA---
    input_container = tk.Frame(card, bg=card_color)
    input_container.pack(fill="x")

    # Email
    tk.Label(input_container, text="Email Address", font=("Segoe UI", 12, "bold"), 
             bg=card_color, fg=secondary_text).pack(anchor="w")
    email_entry = tk.Entry(input_container, width=40, font=("Segoe UI", 12),
                           bg="#F8FAFC", relief="solid", borderwidth=1)
    email_entry.pack(ipady=10, pady=(5, 20), fill="x")

    # Password
    tk.Label(input_container, text="Password", font=("Segoe UI", 12, "bold"), 
             bg=card_color, fg=secondary_text).pack(anchor="w")
    password_entry = tk.Entry(input_container, width=40, font=("Segoe UI", 12), show="•",
                              bg="#F8FAFC", relief="solid", borderwidth=1)
    password_entry.pack(ipady=10, pady=(5, 30), fill="x")

    # --- 5.FUNCTIONALITY ---
    def submit_create_account():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if email_exists(email):
            messagebox.showerror("Error", "This email is already registered.")
            return

        try:
            create_account(email, password)
            messagebox.showinfo("Success", "Account created successfully! You can now log in. 💖")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    # --- 6. BUTTONS ---
    register_btn = tk.Button(card, text="Create Account", bg=primary_btn, fg="white", 
                             font=("Segoe UI", 12, "bold"), relief="flat", 
                             cursor="hand2", command=submit_create_account)
    register_btn.pack(fill="x", ipady=8)

    # Hover effects
    register_btn.bind("<Enter>", lambda e: register_btn.configure(bg='#4338CA'))
    register_btn.bind("<Leave>", lambda e: register_btn.configure(bg=primary_btn))

    # Back to login option
    back_btn = tk.Button(card, text="Cancel", font=("Segoe UI", 9), 
                         bg=card_color, fg=secondary_text, borderwidth=0, 
                         cursor="hand2", command=window.destroy)
    back_btn.pack(pady=(15, 0))

    window.mainloop()

