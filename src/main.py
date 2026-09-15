import tkinter as tk
from ui import MechanicusDataslateUI
from downloader import VideoDownloader
from logger_setup import setup_logger

def main():
    # Initialize the master logger
    logger = setup_logger()
    logger.info("Initializing Noosphere Extractor Protocol...")
    logger.info("Praise the Omnissiah.")

    # Boot up the Cogitator Interface (Tkinter)
    root = tk.Tk()
    
    def on_closing():
        logger.info("Severing Noosphere tether. The Emperor protects.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Launch the UI, passing in the Downloader logic
    app = MechanicusDataslateUI(root, VideoDownloader)
    
    try:
        root.mainloop()
    except Exception as e:
        logger.critical("Catastrophic Cogitator Failure. Core dump initiated.", exc_info=True)

if __name__ == "__main__":
    main()