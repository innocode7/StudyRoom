import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import subprocess  # 파일 탐색기를 열기 위해 사용

class ThumbnailDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Thumbnail Downloader")

        # URL 입력 라벨
        self.url_label = tk.Label(root, text="Video URL:")
        self.url_label.pack(pady=5)

        # URL 입력 필드
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(padx=10, pady=5)
        self.url_entry.focus_set()  # URL 입력 필드에 커서 활성화

        # 버튼 프레임 생성
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        # 입력 필드 리셋 버튼
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_input)
        self.reset_button.pack(side=tk.LEFT, padx=(10, 15))  # 리셋 버튼과 썸네일 추출 버튼 사이의 간격 3배 증가
        self.reset_button.bind("<Enter>", self.on_enter_reset)
        self.reset_button.bind("<Leave>", self.on_leave)

        # 썸네일 추출 버튼
        self.fetch_button = tk.Button(button_frame, text="Fetch Thumbnail", command=self.fetch_thumbnail)
        self.fetch_button.pack(side=tk.LEFT)
        self.fetch_button.bind("<Enter>", self.on_enter)
        self.fetch_button.bind("<Leave>", self.on_leave)

        # 썸네일 표시 라벨
        self.thumbnail_label = tk.Label(root)
        self.thumbnail_label.pack(pady=5)

        # 썸네일 다운로드 버튼
        self.download_button = tk.Button(root, text="Download Thumbnail", command=self.download_thumbnail, state=tk.DISABLED)
        self.download_button.pack(pady=(5, 20))  # 아래쪽 여백 추가
        self.download_button.bind("<Enter>", self.on_enter)
        self.download_button.bind("<Leave>", self.on_leave)

        self.thumbnail_url = None
        self.video_title = None
        self.channel_name = None

    # 입력 필드를 리셋하는 함수
    def reset_input(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.focus_set()

    # 썸네일을 추출하는 함수
    def fetch_thumbnail(self):
        video_url = self.url_entry.get()
        if not video_url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        try:
            yt = YouTube(video_url)
            self.thumbnail_url = yt.thumbnail_url
            self.video_title = yt.title
            self.channel_name = yt.author
            response = requests.get(self.thumbnail_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img.thumbnail((400, 400))
            self.img = ImageTk.PhotoImage(img)

            self.thumbnail_label.config(image=self.img)
            self.download_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # 썸네일을 다운로드하는 함수
    def download_thumbnail(self):
        if not self.thumbnail_url:
            messagebox.showerror("Error", "No thumbnail to download.")
            return

        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # 안전한 파일 이름 생성
        safe_video_title = "".join(c if c.isalnum() else "_" for c in self.video_title)
        safe_channel_name = "".join(c if c.isalnum() else "_" for c in self.channel_name)
        
        # 동일한 이름의 파일이 있을 경우 일련번호 추가
        filename = f"{safe_video_title}_{safe_channel_name}.jpg"
        file_path = os.path.join(downloads_folder, filename)
        base_filename, file_extension = os.path.splitext(file_path)
        counter = 1
        while os.path.exists(file_path):
            file_path = f"{base_filename}({counter}){file_extension}"
            counter += 1

        # 썸네일 저장
        response = requests.get(self.thumbnail_url)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # 성공 메시지와 확인 버튼
        self.show_success_message(file_path)

    # 성공 메시지와 확인 버튼을 표시하는 함수
    def show_success_message(self, file_path):
        def open_folder():
            subprocess.Popen(f'explorer /select,"{file_path}"')

        success_msg = tk.Toplevel(self.root)
        success_msg.title("Success")
        success_msg.geometry("400x120")  # 메시지 창 크기 제한
        tk.Label(success_msg, text=f"Thumbnail downloaded to:\n{file_path}", wraplength=380).pack(pady=10)
        check_button = tk.Button(success_msg, text="Check Thumbnail", command=open_folder)
        check_button.pack(pady=(5, 20))  # 'Check Thumbnail' 버튼 아래에 여백 추가
        check_button.bind("<Enter>", self.on_enter_check)
        check_button.bind("<Leave>", self.on_leave)

    # 버튼에 마우스가 호버될 때 배경색 변경
    def on_enter(self, e):
        e.widget.config(bg='lightgrey')

    # 'Reset' 버튼에 마우스가 호버될 때 배경색 변경
    def on_enter_reset(self, e):
        e.widget.config(bg='lightcoral')

    # 'Check Thumbnail' 버튼에 마우스가 호버될 때 배경색 변경
    def on_enter_check(self, e):
        e.widget.config(bg='lightblue')

    # 버튼에 마우스가 호버되지 않을 때 원래 배경색으로 변경
    def on_leave(self, e):
        e.widget.config(bg='SystemButtonFace')

if __name__ == "__main__":
    root = tk.Tk()
    app = ThumbnailDownloader(root)
    root.mainloop()