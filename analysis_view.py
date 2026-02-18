import tkinter as tk
from tkinter import ttk
from data import get_session_summary, get_comments_for_session, get_score_distribution

# --- COLOR PALETTE ---
BG_DARK = "#0f172a"
BG_CARD = "#1e293b"
ACCENT = "#22d3ee"
TEXT_MAIN = "#f8fafc"
TEXT_DIM = "#94a3b8"

def create_score_distribution(parent_frame, scores):
    """Refined bar chart for the dark theme."""
    chart_container = tk.Frame(parent_frame, bg=BG_CARD, padx=20, pady=20)
    chart_container.pack(pady=10, fill="both", expand=True)

    tk.Label(chart_container, text="Score Distribution Frequency", 
             font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg="white").pack(pady=(0, 15))

    canvas = tk.Canvas(chart_container, width=500, height=220, bg=BG_CARD, highlightthickness=0)
    canvas.pack(anchor="center")

    max_count = max(scores.values()) if scores else 1
    
    bar_color = ACCENT
    bg_bar_color = "#334155" 
    bar_width = 28
    spacing = 15
    x_start = 45
    y_base = 180
    max_height = 140

    canvas.create_line(x_start - 10, y_base, x_start + 450, y_base, fill=TEXT_DIM)

    for i in range(1, 11):
        count = scores.get(i, 0)
        height = (count / max_count) * max_height if max_count > 0 else 0
        x1 = x_start + (i - 1) * (bar_width + spacing)
        x2 = x1 + bar_width
        canvas.create_rectangle(x1, y_base - max_height, x2, y_base, fill=bg_bar_color, outline="")
        if count > 0:
            canvas.create_rectangle(x1, y_base - height, x2, y_base, fill=bar_color, outline="")
            canvas.create_text(x1 + bar_width/2, y_base - height - 12, 
                               text=str(count), font=("Segoe UI", 9, "bold"), fill=TEXT_MAIN)
        canvas.create_text(x1 + bar_width/2, y_base + 15, text=str(i), 
                           font=("Segoe UI", 10), fill=TEXT_DIM)

def run_analysis_view(dashboard_root, session):
    """An optimized version that prioritizes UI responsiveness."""
    
    # 1. SHOW THE WINDOW IMMEDIATELY
    dashboard_root.withdraw()
    analysis_window = tk.Toplevel(dashboard_root)
    analysis_window.title(f"Analytics: {session['name']}")
    analysis_window.state("zoomed")
    analysis_window.configure(bg=BG_DARK)

    # 2. RENDER THE SCAFFOLDING (The scrollable area)
    main_canvas = tk.Canvas(analysis_window, bg=BG_DARK, highlightthickness=0)
    v_scrollbar = ttk.Scrollbar(analysis_window, orient="vertical", command=main_canvas.yview)
    scroll_frame = tk.Frame(main_canvas, bg=BG_DARK)

    def on_frame_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.itemconfig(window_id, width=main_canvas.winfo_width())

    scroll_frame.bind("<Configure>", on_frame_configure)
    window_id = main_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    main_canvas.configure(yscrollcommand=v_scrollbar.set)
    main_canvas.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")

    content_wrapper = tk.Frame(scroll_frame, bg=BG_DARK)
    content_wrapper.pack(pady=20, padx=50)

    # Temporary Loading Label
    loading_label = tk.Label(content_wrapper, text="Gathering Data...", font=("Segoe UI", 16), bg=BG_DARK, fg=ACCENT)
    loading_label.pack(pady=100)
    
    # Force the window to show up so the user isn't waiting on a blank screen
    analysis_window.update()

    def load_data_and_build_ui():
        # Fetching data inside this function
        session_id = session['id']
        summary = get_session_summary(session_id)
        comments = get_comments_for_session(session_id)
        score_counts = get_score_distribution(session_id)

        # Clear loading label
        loading_label.destroy()

        # --- HEADER ---
        tk.Label(content_wrapper, text=f"SESSION ANALYTICS", font=("Segoe UI", 10, "bold"), bg=BG_DARK, fg=ACCENT).pack()
        tk.Label(content_wrapper, text=session['name'], font=("Segoe UI", 28, "bold"), bg=BG_DARK, fg=TEXT_MAIN).pack()
        tk.Label(content_wrapper, text=f"ID: {session_id} • Total Responses: {len(comments)}", 
                 font=("Segoe UI", 11), bg=BG_DARK, fg=TEXT_DIM).pack(pady=(5, 20))

        # --- METRICS ---
        metrics_container = tk.Frame(content_wrapper, bg=BG_DARK)
        metrics_container.pack(pady=10)

        chart_frame = tk.Frame(metrics_container, bg=BG_CARD, padx=20, pady=20)
        chart_frame.pack(side="left", padx=15, fill="both")
        create_score_distribution(chart_frame, score_counts)

        stats_card = tk.Frame(metrics_container, bg=BG_CARD, padx=40, pady=40, width=450, height=315)
        stats_card.pack(side="right", padx=15, fill="both")
        stats_card.pack_propagate(False)

        avg_score = summary.get('avg_score', 0.0)
        tk.Label(stats_card, text="Overall Rating", font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(anchor="w")
        
        tk.Label(stats_card, text=f"{avg_score:.1f} / 10", 
         font=("Segoe UI", 24, "bold"), 
         bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(5, 0))
        tk.Label(stats_card, text="Average Session Score", 
         font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Analysis.Horizontal.TProgressbar", thickness=15, troughcolor="#334155", background=ACCENT)
        
        score_bar = ttk.Progressbar(stats_card, length=350, maximum=10, value=avg_score, style="Analysis.Horizontal.TProgressbar")
        score_bar.pack(pady=15, fill="x")

        # SENTIMENT COLOR LOGIC
        if avg_score >= 7: status, s_color = "Positive", "#10b981"
        elif avg_score <= 4: status, s_color = "Negative", "#ef4444"
        else: status, s_color = "Neutral", "#f59e0b"

        tk.Label(stats_card, text=f"Sentiment Analysis: {status}", font=("Segoe UI", 16, "bold"), bg=BG_CARD, fg=s_color).pack(pady=(40, 0))

        # --- TABLE ---
        table_card = tk.Frame(content_wrapper, bg=BG_CARD, padx=20, pady=20)
        table_card.pack(pady=30, fill="x")
        
        style.configure("Treeview", background=BG_CARD, foreground=TEXT_MAIN, fieldbackground=BG_CARD, rowheight=35)
        style.configure("Treeview.Heading", background="#334155", foreground=ACCENT)

        tree_frame = tk.Frame(table_card, bg=BG_CARD)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, columns=('Score', 'Comment'), show='headings', height=10)
        tree.heading('Score', text='RATING')
        tree.heading('Comment', text='FEEDBACK MESSAGE')
        tree.column('Score', width=100, anchor='center')
        tree.column('Comment', width=750, anchor='w')

        table_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=table_scroll.set)

        for s, c in comments:
            tree.insert('', tk.END, values=(f"{s}/10", c))
        
        tree.pack(side="left", fill="both", expand=True)
        table_scroll.pack(side="right", fill="y")

        # Navigation
        tk.Button(content_wrapper, text="← Return to Dashboard", font=("Segoe UI", 11, "bold"), 
                  bg="black", fg=TEXT_MAIN, padx=25, pady=10, relief="flat", cursor="hand2", 
                  command=go_back).pack(pady=20)

    def go_back():
        analysis_window.destroy()
        dashboard_root.deiconify()
        dashboard_root.state("zoomed")

    # This runs the data loading AFTER the window has appeared
    analysis_window.after(100, load_data_and_build_ui)
    analysis_window.protocol("WM_DELETE_WINDOW", go_back)

