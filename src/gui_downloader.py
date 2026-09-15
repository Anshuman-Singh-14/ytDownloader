import tkinter as tk
from tkinter import messagebox
import yt_dlp
import threading
import logging
from logging.handlers import RotatingFileHandler
import sys

# ==========================================
# 1. INDUSTRY-GRADE LOGGING SETUP
# ==========================================
# Create the root logger for the app
app_logger = logging.getLogger("YTDownloader")
app_logger.setLevel(logging.DEBUG)

# Define a strict format: Time | Level | Thread | Message
log_format = logging.Formatter(
    fmt='%(asctime)s | %(levelname)-8s | %(threadName)-15s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File Handler: Creates 'downloader.log'
# Rotates automatically at 5MB per file, keeping 3 historical backups
file_handler = RotatingFileHandler('downloader.log', maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.DEBUG)

# Console Handler: Pushes logs to the terminal as well
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.INFO)

# Attach handlers to the logger
app_logger.addHandler(file_handler)
app_logger.addHandler(console_handler)

app_logger.info("Application started. Logger initialized.")

# ==========================================
# 2. CUSTOM YT-DLP LOGGER INJECTION
# ==========================================
class YTDLPLogger:
    """Redirects yt-dlp's internal console printouts into our Python logger."""
    def debug(self, msg):
        # yt-dlp uses the 'debug' channel for most of its standard download progress output
        if msg.startswith('[debug]'):
            app_logger.debug(f"yt-dlp: {msg}")
        else:
            app_logger.info(f"yt-dlp: {msg}")

    def info(self, msg):
        app_logger.info(f"yt-dlp: {msg}")

    def warning(self, msg):
        app_logger.warning(f"yt-dlp: {msg}")

    def error(self, msg):
        app_logger.error(f"yt-dlp: {msg}")

# ==========================================
# 3. GUI & DOWNLOAD LOGIC
# ==========================================
def download_video():
    url = url_entry.get().strip()
    if not url:
        app_logger.warning("Download attempted, but the URL field was empty.")
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    
    app_logger.info(f"Download initiated by user for URL: {url}")
    
    # Run the download in a background thread to prevent UI freezing
    thread = threading.Thread(target=process_download, args=(url,), name="DownloadWorker")
    thread.start()

def process_download(url):
    app_logger.debug("Background thread started successfully.")
    
    # Safely update Tkinter from a background thread using root.after
    root.after(0, lambda: status_label.config(text="Downloading... Check downloader.log for details", fg="blue"))
    root.after(0, lambda: download_btn.config(state=tk.DISABLED))
    
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'logger': YTDLPLogger(), # Inject our custom logger
        'quiet': True,           # Suppress direct console prints
        'no_warnings': False
    }

    try:
        app_logger.info("Initializing yt-dlp YoutubeDL object.")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            app_logger.info("Starting extraction and download sequence.")
            ydl.download([url])
        
        app_logger.info("Download and merge completed successfully.")
        root.after(0, lambda: status_label.config(text="✅ Download completed successfully!", fg="green"))
        root.after(0, lambda: url_entry.delete(0, tk.END))
        
    except Exception as e:
        # exc_info=True logs the full traceback alongside the error
        app_logger.error(f"A critical error occurred during download: {str(e)}", exc_info=True)
        root.after(0, lambda: status_label.config(text="❌ Download failed. Check logs.", fg="red"))
        root.after(0, lambda: messagebox.showerror("Download Error", "An error occurred. Check downloader.log for details."))
        
    finally:
        app_logger.debug("Re-enabling download button.")
        root.after(0, lambda: download_btn.config(state=tk.NORMAL))

# ==========================================
# 4. APP WINDOW SETUP
# ==========================================
def on_closing():
    app_logger.info("Application closed by user.")
    root.destroy()

root = tk.Tk()
root.title("YouTube 1080p Downloader - Pro")
root.geometry("450x200")
root.resizable(False, False)

# Catch the close event ("X" button) to log it before quitting
root.protocol("WM_DELETE_WINDOW", on_closing)

tk.Label(root, text="Paste YouTube Link Here:", font=("Helvetica", 12)).pack(pady=(20, 5))
url_entry = tk.Entry(root, width=50, font=("Helvetica", 10))
url_entry.pack(pady=5)

download_btn = tk.Button(
    root, text="Download Video", font=("Helvetica", 11, "bold"), 
    bg="#ff0000", fg="white", command=download_video
)
download_btn.pack(pady=10)

status_label = tk.Label(root, text="Waiting for URL...", font=("Helvetica", 10), fg="gray")
status_label.pack(pady=5)

if __name__ == "__main__":
    try:
        root.mainloop()
    except Exception as e:
        app_logger.critical("Fatal application error in main loop.", exc_info=True)