import tkinter as tk
from tkinter import ttk, messagebox
from logger_setup import setup_logger

logger = setup_logger()

# ==========================================
# GRIMDARK COLOR PALETTE & FONTS
# ==========================================
BG_COLOR = "#0A0A0A"        # Void Black
FG_TEXT = "#D4AF37"         # Imperial Gold
ACCENT_RED = "#5C0000"      # Inquisition/Mechadendrite Red
BTN_ACTIVE = "#8A0303"      # Brighter Red for interactions
ENTRY_BG = "#1A1A1A"        # Dark gunmetal
ENTRY_FG = "#E8E1CF"        # Parchment/Bone White

FONT_GOTHIC = ("Times New Roman", 16, "bold")
FONT_COGITATOR = ("Courier New", 11, "bold")

class AdeptusAstartesUI:
    def __init__(self, root, downloader_class):
        self.root = root
        self.downloader_class = downloader_class
        
        self.root.title("ADEPTUS ASTARTES - COGITATOR DATASLATE")
        self.root.configure(bg=BG_COLOR)
        
        # Center the dataslate window
        self._center_window(600, 350)
        self.root.resizable(False, False)
        
        self._setup_styles()
        self._build_widgets()

    def _center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_styles(self):
        # Override Tkinter's progress bar for a militaristic red/black look
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Grimdark.Horizontal.TProgressbar",
            troughcolor=ENTRY_BG,
            background=ACCENT_RED,
            bordercolor=BG_COLOR,
            lightcolor=BTN_ACTIVE,
            darkcolor=ACCENT_RED,
            thickness=20
        )

    def _build_widgets(self):
        # Main Title Label
        tk.Label(
            self.root, 
            text="ENTER NOOSPHERE PROTOCOL (URL):", 
            font=FONT_GOTHIC, 
            bg=BG_COLOR, 
            fg=FG_TEXT
        ).pack(pady=(40, 10))

        # Input Box
        self.url_entry = tk.Entry(
            self.root, 
            width=55, 
            font=FONT_COGITATOR, 
            bg=ENTRY_BG, 
            fg=ENTRY_FG,
            insertbackground=FG_TEXT, # Cursor color
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.url_entry.pack(pady=10, ipady=6)

        # Download Button
        self.download_btn = tk.Button(
            self.root, 
            text="COMMENCE EXTRACTION", 
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

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root, 
            variable=self.progress_var, 
            maximum=100, 
            length=450,
            style="Grimdark.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=(0, 10))

        # Status Label
        self.status_label = tk.Label(
            self.root, 
            text="Awaiting Machine Spirit...", 
            font=FONT_COGITATOR, 
            bg=BG_COLOR, 
            fg="#707070" # Muted grey
        )
        self.status_label.pack(pady=5)

    def _on_download_click(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Inquisitorial Alert", "The holy text (URL) cannot be empty.")
            return

        callbacks = {
            'on_start': self._cb_start,
            'on_progress': self._cb_progress,
            'on_finish': self._cb_finish,
            'on_error': self._cb_error
        }
        
        downloader = self.downloader_class(callbacks)
        downloader.start_download(url)

    # --- CALLBACKS (Triggered by background thread) ---
    def _cb_start(self):
        self.root.after(0, lambda: self.download_btn.config(state=tk.DISABLED, bg="#330000", fg="#555555"))
        self.root.after(0, lambda: self.progress_var.set(0))
        self.root.after(0, lambda: self.status_label.config(text="Awakening Machine Spirit...", fg=FG_TEXT))

    def _cb_progress(self, percent, text):
        self.root.after(0, lambda: self.progress_var.set(percent))
        # Override the default text from the downloader with 40k flavor
        flavor_text = f"Extracting from Noosphere... {percent:.1f}%"
        self.root.after(0, lambda: self.status_label.config(text=flavor_text, fg=FG_TEXT))

    def _cb_finish(self, text):
        self.root.after(0, lambda: self.progress_var.set(100))
        self.root.after(0, lambda: self.status_label.config(text="Extraction complete. The Emperor protects.", fg="#00FF00")) 
        self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, bg=ACCENT_RED, fg=FG_TEXT))
        self.root.after(0, lambda: self.url_entry.delete(0, tk.END))

    def _cb_error(self, text):
        self.root.after(0, lambda: self.status_label.config(text="ERROR: Heretical interference detected.", fg="#FF0000"))
        self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, bg=ACCENT_RED, fg=FG_TEXT))
        self.root.after(0, lambda: messagebox.showerror("Corruption Detected", "Data extraction failed. Consult the downloader.log for signs of heresy."))