
import yt_dlp
import threading
from logger_setup import setup_logger, YTDLPLogger

logger = setup_logger()

class VideoDownloader:
    def __init__(self, ui_callbacks):
        # ui_callbacks is a dictionary of functions passed from the UI
        self.on_start = ui_callbacks.get('on_start')
        self.on_progress = ui_callbacks.get('on_progress')
        self.on_finish = ui_callbacks.get('on_finish')
        self.on_error = ui_callbacks.get('on_error')

    def start_download(self, url):
        thread = threading.Thread(target=self._process_download, args=(url,), name="DownloadWorker")
        thread.start()

    def _process_download(self, url):
        logger.debug("Background thread started.")
        if self.on_start:
            self.on_start()

        def progress_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total and self.on_progress:
                    percent = (downloaded / total) * 100
                    self.on_progress(percent, f"Downloading... {percent:.1f}%")
            elif d['status'] == 'finished':
                if self.on_progress:
                    self.on_progress(100, "Download complete. Merging audio & video...")

        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'logger': YTDLPLogger(logger),
            'quiet': True,
            'no_warnings': False,
            'progress_hooks': [progress_hook]
        }

        try:
            logger.info(f"Starting download sequence for: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            logger.info("Download completed successfully.")
            if self.on_finish:
                self.on_finish("✅ Process completed successfully!")
                
        except Exception as e:
            logger.error(f"Download error: {str(e)}", exc_info=True)
            if self.on_error:
                self.on_error("❌ Download failed. Check logs.")