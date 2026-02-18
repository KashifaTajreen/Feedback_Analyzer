
import tkinter as tk
from tkinter import messagebox
from newaccount import open_create_account_window
from data import init_users_db, validate_login
from dashboard import run_dashboard

# Initialize DB
init_users_db()

def run_login():
    global logged_in_user
    root = tk.Tk()
    root.title("Feedback Analyzer - Login")
    root.state("zoomed")
    
    # --- 1. GRADIENT BACKGROUND ---
    canvas = tk.Canvas(root, highlightthickness=0)
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

    root.after(10, draw_gradient)

    # --- 2. THE WHITE CARD ---
    card_color = "#FFFFFF"
    primary_btn = "#4F46E5"
    secondary_text = "#64748B"
    
    card = tk.Frame(canvas, bg=card_color, padx=50, pady=50, 
                    highlightbackground="#CBD5E1", highlightthickness=1)
    canvas.create_window(root.winfo_screenwidth()//2, root.winfo_screenheight()//2, window=card)

    # --- 3. THE HEADER ---
    header_frame = tk.Frame(card, bg=card_color)
    header_frame.pack(fill="x", pady=(0, 30))

    tk.Label(header_frame, text="Welcome Back to", font=("Segoe UI", 20), 
             bg=card_color, fg="#1E293B").pack()
    tk.Label(header_frame, text="Feedback Analyzer", font=("Segoe UI", 24, "bold"), 
             bg=card_color, fg="#1E293B").pack()

    # --- 4. INPUT AREA ---
    input_container = tk.Frame(card, bg=card_color)
    input_container.pack(fill="x")

    tk.Label(input_container, text="Email Address", font=("Segoe UI", 12, "bold"), 
             bg=card_color, fg=secondary_text).pack(anchor="w")
    email_entry = tk.Entry(input_container, width=40, font=("Segoe UI", 12),
                           bg="#F8FAFC", relief="solid", borderwidth=1)
    email_entry.pack(ipady=10, pady=(5, 20), fill="x")

    tk.Label(input_container, text="Password", font=("Segoe UI", 12, "bold"), 
             bg=card_color, fg=secondary_text).pack(anchor="w")
    password_entry = tk.Entry(input_container, width=40, font=("Segoe UI", 12), show="•",
                              bg="#F8FAFC", relief="solid", borderwidth=1)
    password_entry.pack(ipady=10, pady=(5, 30), fill="x")

    # --- 5.LOGIN LOGIC ---
    def submit_login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if validate_login(email, password):
            messagebox.showinfo("Success", f"Welcome back, {email}! 🌺")
            root.after(100,lambda:
                       run_dashboard(root,email))
            # root.destroy()  # Close the login window
            # run_dashboard(None, email) # Open the dashboard
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    # --- 6. BUTTONS ---
    login_btn = tk.Button(card, text="Sign In", bg=primary_btn, fg="white", 
                          font=("Segoe UI", 12, "bold"), relief="flat", 
                          cursor="hand2", command=submit_login) # Linked to logic
    login_btn.pack(fill="x", ipady=8)

    # Hover effects
    login_btn.bind("<Enter>", lambda e: login_btn.configure(bg='#4338CA'))
    login_btn.bind("<Leave>", lambda e: login_btn.configure(bg=primary_btn))

    create_btn = tk.Button(card, text="Don't have an account? Create one", 
                           font=("Segoe UI", 9), bg=card_color, fg=primary_btn, 
                           borderwidth=0, cursor="hand2", 
                           command=open_create_account_window)
    create_btn.pack(pady=(15, 0))

    root.mainloop()

if __name__ == "__main__":
    run_login()

