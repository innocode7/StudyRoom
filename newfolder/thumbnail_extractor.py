import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ThumbnailDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Thumbnail Downloader")

        self.url_label = tk.Label(root, text="Video URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.fetch_button = tk.Button(root, text="Fetch Thumbnail", command=self.fetch_thumbnail)
        self.fetch_button.pack(pady=5)

        self.thumbnail_label = tk.Label(root)
        self.thumbnail_label.pack(pady=5)

        self.download_button = tk.Button(root, text="Download Thumbnail", command=self.download_thumbnail, state=tk.DISABLED)
        self.download_button.pack(pady=5)

        self.thumbnail_url = None

    def fetch_thumbnail(self):
        video_url = self.url_entry.get()
        if not video_url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        try:
            yt = YouTube(video_url)
            self.thumbnail_url = yt.thumbnail_url
            response = requests.get(self.thumbnail_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img.thumbnail((400, 400))
            self.img = ImageTk.PhotoImage(img)

            self.thumbnail_label.config(image=self.img)
            self.download_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def download_thumbnail(self):
        if not self.thumbnail_url:
            messagebox.showerror("Error", "No thumbnail to download.")
            return

        file_path = tk.filedialog.asksaveasfilename(defaultextension=".jpg",
                                                    filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            response = requests.get(self.thumbnail_url)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            messagebox.showinfo("Success", f"Thumbnail downloaded to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ThumbnailDownloader(root)
    root.mainloop()
