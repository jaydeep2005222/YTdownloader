import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
import threading
import os
import shutil

class VideoDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("JAYDEEP OMPRAKASH SHARMA'S Video Downloader")
        self.master.geometry("600x700")
        self.master.configure(bg="#555555")

        self.url_label = ttk.Label(self.master, text="YouTube URL:")
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(self.master, width=60)
        self.url_entry.pack(pady=5)

        self.resolution_label = ttk.Label(self.master, text="Resolution:")
        self.resolution_label.pack(pady=5)

        self.resolution_var = tk.StringVar()
        self.resolution_combobox = ttk.Combobox(self.master, textvariable=self.resolution_var, width=15)
        self.resolution_combobox['values'] = ['Highest', '720p', '480p', '360p']
        self.resolution_combobox.current(0)
        self.resolution_combobox.pack(pady=5)

        self.download_button = ttk.Button(self.master, text="Download", command=self.download_video,)
        self.download_button.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=500, mode="indeterminate")
        self.progress_bar.pack(pady=5)

    def download_video(self):
        url = self.url_entry.get()
        resolution = self.resolution_combobox.get()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        self.progress_bar.start()

        def download():
            try:
                yt = YouTube(url)
                if resolution == "Highest":
                    stream = yt.streams.get_highest_resolution()
                else:
                    stream = yt.streams.filter(res=resolution).first()
                
                # Specify the desktop directory for saving the downloaded videos
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                download_path = os.path.join(desktop_path, "downloaded_videos")
                os.makedirs(download_path, exist_ok=True)

                # Download the video to the specified directory
                stream.download(output_path=download_path)

                messagebox.showinfo("Success", "Video downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                self.progress_bar.stop()

        threading.Thread(target=download).start()

def main():
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
