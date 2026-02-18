import tkinter as tk
from tkinter import messagebox

def run_gui(dashboard_root, session):
    # Hide the dashboard to focus on the form
    dashboard_root.withdraw()
    
    root = tk.Toplevel(dashboard_root)
    root.title(f"Feedback Form - {session['name']}")
    root.state("zoomed")

    # --- 1. THEME ALIGNMENT (Matches Dashboard) ---
    bg_color = "#334155"        # Professional Slate Blue
    card_color = "#FFFFFF"      # Crisp White Card
    accent_cyan = "#00D1FF"     # Electric Cyan Pop
    text_dark = "#1E293B"       
    text_muted = "#64748B"      

    root.configure(bg=bg_color)

    # --- 2. THE FLOATING CARD ---
    # Added a thicker border to match the "sharp" look of dashboard cards
    card = tk.Frame(root, bg=card_color, padx=50, pady=40,
                    highlightbackground="#000000", highlightthickness=1)
    card.place(relx=0.5, rely=0.5, anchor="center")

    # --- 3. TOP DECORATIVE ACCENT ---
    # This adds a small bar of color at the top of the card
    accent_bar = tk.Frame(card, bg=accent_cyan, height=4)
    accent_bar.pack(fill="x", pady=(0, 20))

    # --- 4. HEADER SECTION ---
    tk.Label(card, text=session['name'], font=("Segoe UI", 22, "bold"), 
             bg=card_color, fg=text_dark).pack(anchor="w")
    
    tk.Label(card, text="Please provide your honest feedback below", font=("Segoe UI", 10), 
             bg=card_color, fg=text_muted).pack(anchor="w", pady=(0, 25))

    # --- 5. INPUT FIELDS---
    def create_modern_entry(label_text, is_text=False):
        label = tk.Label(card, text=label_text.upper(), font=("Segoe UI", 8, "bold"), 
                         bg=card_color, fg=text_muted)
        label.pack(anchor="w", pady=(10, 2))
        
        if is_text:
            ent = tk.Text(card, width=45, height=5, font=("Segoe UI", 11), 
                          bg="#F8FAFC", relief="solid", borderwidth=1)
        else:
            ent = tk.Entry(card, width=45, font=("Segoe UI", 11), 
                           bg="#F8FAFC", relief="solid", borderwidth=1)
        
        ent.pack(ipady=8 if not is_text else 0, fill="x", pady=(0, 5))
        return ent

    name_entry = create_modern_entry("Reviewer Name")
    id_entry = create_modern_entry("Reviewer ID")
    score_entry = create_modern_entry("Score (1-10)")
    comment_text = create_modern_entry("Comments", is_text=True)

    # --- 6. LOGIC ---
    def submit_feedback():
        reviewer_name = name_entry.get().strip()
        reviewer_ID = id_entry.get().strip()
        score = score_entry.get().strip()
        comment = comment_text.get("1.0", tk.END).strip()
        
        if not all([reviewer_name, reviewer_ID, score, comment]):
            messagebox.showerror('Error', 'All fields are required.')
            return

        try:
            score_int = int(score)
            if not (1 <= score_int <= 10): raise ValueError
        except ValueError:
            messagebox.showerror('Error', 'Score must be a number between 1 and 10.')
            return

        from data import insert_feedback, insert_sentiment
        from analysis import analyze_sentiment
        
        insert_feedback(reviewer_name, reviewer_ID, score_int, comment, session['id'])
        sentiment_score = analyze_sentiment(comment)
        insert_sentiment(session['name'], session['id'], sentiment_score)

        messagebox.showinfo('Success', 'Feedback submitted! ✨')
        on_close()

    # --- 7. ACTION BUTTONS ---
    # The primary button uses the Electric Cyan pop from the dashboard
    submit_btn = tk.Button(card, text="SUBMIT FEEDBACK", bg=accent_cyan, fg="#000000", 
                           font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                           command=submit_feedback)
    submit_btn.pack(fill="x", ipady=10, pady=(25, 10))

    def on_close():
        root.destroy()
        dashboard_root.deiconify() # Reveal the dashboard again
        dashboard_root.state("zoomed")

    cancel_btn = tk.Button(card, text="Cancel and Return", font=("Segoe UI", 9), 
                           bg=card_color, fg=text_muted, borderwidth=0, 
                           cursor="hand2", command=on_close)
    cancel_btn.pack()

    root.protocol("WM_DELETE_WINDOW", on_close)



