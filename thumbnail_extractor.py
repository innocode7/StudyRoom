import tkinter as tk
from tkinter import messagebox, filedialog  # filedialog를 별도로 가져옵니다.
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ThumbnailDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Thumbnail Downloader")

        self.url_label = tk.Label(root, text="Video URL:")  # URL 입력 라벨
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(root, width=50)  # URL 입력 필드
        self.url_entry.pack(pady=5)

        self.fetch_button = tk.Button(root, text="Fetch Thumbnail", command=self.fetch_thumbnail)  # 썸네일 추출 버튼
        self.fetch_button.pack(pady=5)

        self.thumbnail_label = tk.Label(root)  # 썸네일 표시 라벨
        self.thumbnail_label.pack(pady=5)

        self.download_button = tk.Button(root, text="Download Thumbnail", command=self.download_thumbnail, state=tk.DISABLED)  # 다운로드 버튼
        self.download_button.pack(pady=5)

        self.thumbnail_url = None

    def fetch_thumbnail(self):
        video_url = self.url_entry.get()  # 입력된 URL 가져오기
        if not video_url:
            messagebox.showerror("Error", "Please enter a video URL.")  # URL이 입력되지 않으면 오류 메시지 표시
            return

        try:
            yt = YouTube(video_url)  # YouTube 객체 생성
            self.thumbnail_url = yt.thumbnail_url  # 썸네일 URL 가져오기
            response = requests.get(self.thumbnail_url)
            img_data = BytesIO(response.content)  # 이미지를 메모리로 읽기
            img = Image.open(img_data)
            img.thumbnail((400, 400))  # 이미지 크기 조정
            self.img = ImageTk.PhotoImage(img)

            self.thumbnail_label.config(image=self.img)  # GUI에 이미지 표시
            self.download_button.config(state=tk.NORMAL)  # 다운로드 버튼 활성화
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")  # 오류 발생 시 메시지 표시

    def download_thumbnail(self):
        if not self.thumbnail_url:
            messagebox.showerror("Error", "No thumbnail to download.")  # 썸네일 URL이 없는 경우 오류 메시지
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",  # 파일 저장 대화상자 열기
                                                 filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            response = requests.get(self.thumbnail_url)
            with open(file_path, 'wb') as f:  # 파일 저장
                f.write(response.content)
            messagebox.showinfo("Success", f"Thumbnail downloaded to {file_path}")  # 성공 메시지

if __name__ == "__main__":
    root = tk.Tk()
    app = ThumbnailDownloader(root)
    root.mainloop()
