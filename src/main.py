import tkinter as tk
from ui import AdeptusAstartesUI
from downloader import VideoDownloader
from logger_setup import setup_logger

def main():
    # Initialize the master logger
    logger = setup_logger()
    logger.info("Initializing Adeptus Astartes protocol...")

    # Boot up Tkinter
    root = tk.Tk()
    
    def on_closing():
        logger.info("Application closed by user.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Launch the UI, passing in the Downloader logic
    app = AdeptusAstartesUI(root, VideoDownloader)
    
    try:
        root.mainloop()
    except Exception as e:
        logger.critical("Fatal application error in main loop.", exc_info=True)

if __name__ == "__main__":
    main()