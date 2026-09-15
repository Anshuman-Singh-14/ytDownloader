import tkinter as tk
from tkinter import ttk, messagebox
from logger_setup import setup_logger
import os

logger = setup_logger()

# ==========================================
# GRIMDARK COLOR PALETTE & FONTS
# ==========================================
BG_COLOR = "#0A0A0A"        # Void Black
FG_TEXT = "#D4AF37"         # Imperial Gold
ACCENT_RED = "#5C0000"      # Mechanicus Red
BTN_ACTIVE = "#8A0303"      # Heated Plasma Red
ENTRY_BG = "#1A1A1A"        # Dark gunmetal
ENTRY_FG = "#E8E1CF"        # Parchment White

FONT_GOTHIC = ("Times New Roman", 16, "bold")
FONT_COGITATOR = ("Courier New", 11, "bold")

class MechanicusDataslateUI:
    def __init__(self, root, downloader_class):
        self.root = root
        self.downloader_class = downloader_class
        
        # --- NEW MECHANCUS TITLE ---
        self.root.title("ADEPTUS MECHANICUS - NOOSPHERE EXTRACTOR")
        self.root.configure(bg=BG_COLOR)
        
        self._center_window(600, 350)
        self.root.resizable(False, False)
        
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "aquila.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            logger.warning(f"Holy sigil not found at: {icon_path}. Machine Spirit displeased.")
            
        self._setup_styles()
        self._build_widgets()

    def _center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Mechanicus.Horizontal.TProgressbar",
            troughcolor=ENTRY_BG,
            background=ACCENT_RED,
            bordercolor=BG_COLOR,
            lightcolor=BTN_ACTIVE,
            darkcolor=ACCENT_RED,
            thickness=20
        )

    def _build_widgets(self):
        tk.Label(
            self.root, 
            text="INPUT NOOSPHERE DATAPATH (URL):", 
            font=FONT_GOTHIC, 
            bg=BG_COLOR, 
            fg=FG_TEXT
        ).pack(pady=(40, 10))

        self.url_entry = tk.Entry(
            self.root, 
            width=55, 
            font=FONT_COGITATOR, 
            bg=ENTRY_BG, 
            fg=ENTRY_FG,
            insertbackground=FG_TEXT,
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.url_entry.pack(pady=10, ipady=6)

        # --- THEMED BUTTON ---
        self.download_btn = tk.Button(
            self.root, 
            text="INITIATE RITUAL OF EXTRACTION", 
            font=FONT_COGITATOR, 
            bg=ACCENT_RED, 
            fg=FG_TEXT, 
            activebackground=BTN_ACTIVE,
            activeforeground=ENTRY_FG,
            relief=tk.RAISED,
            borderwidth=3,
            command=self._on_download_click
        )
        self.download_btn.pack(pady=20, ipadx=10, ipady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root, 
            variable=self.progress_var, 
            maximum=100, 
            length=450,
            style="Mechanicus.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=(0, 10))

        self.status_label = tk.Label(
            self.root, 
            text="Machine Spirit dormant...", 
            font=FONT_COGITATOR, 
            bg=BG_COLOR, 
            fg="#707070" 
        )
        self.status_label.pack(pady=5)

    def _on_download_click(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Inquisitorial Alert", "The holy datapath (URL) cannot be empty.")
            return

        callbacks = {
            'on_start': self._cb_start,
            'on_progress': self._cb_progress,
            'on_finish': self._cb_finish,
            'on_error': self._cb_error
        }
        
        downloader = self.downloader_class(callbacks)
        downloader.start_download(url)

    # --- CALLBACKS WITH MECHANCUS FLAVOR ---
    def _cb_start(self):
        self.root.after(0, lambda: self.download_btn.config(state=tk.DISABLED, bg="#330000", fg="#555555"))
        self.root.after(0, lambda: self.progress_var.set(0))
        self.root.after(0, lambda: self.status_label.config(text="Appeasing the Machine Spirit...", fg=FG_TEXT))

    def _cb_progress(self, percent, text):
        self.root.after(0, lambda: self.progress_var.set(percent))
        flavor_text = f"Transcribing STC fragment... {percent:.1f}%"
        self.root.after(0, lambda: self.status_label.config(text=flavor_text, fg=FG_TEXT))

    def _cb_finish(self, text):
        self.root.after(0, lambda: self.progress_var.set(100))
        self.root.after(0, lambda: self.status_label.config(text="Extraction sanctioned. The Omnissiah is pleased.", fg="#00FF00")) 
        self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, bg=ACCENT_RED, fg=FG_TEXT))
        self.root.after(0, lambda: self.url_entry.delete(0, tk.END))

    def _cb_error(self, text):
        self.root.after(0, lambda: self.status_label.config(text="WARP INTERFERENCE: Scrapcode detected.", fg="#FF0000"))
        self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, bg=ACCENT_RED, fg=FG_TEXT))
        self.root.after(0, lambda: messagebox.showerror("Scrapcode Infection", "Ritual failed. Consult the holy logs for scrapcode contamination."))