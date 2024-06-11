from pytube import YouTube

def get_youtube_thumbnail(video_url):
    try:
        yt = YouTube(video_url)
        thumbnail_url = yt.thumbnail_url
        return thumbnail_url
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
video_url = "https://youtu.be/PAb0rnwofwY?si=DjDJqMHp_dvKbtS7"
thumbnail_url = get_youtube_thumbnail(video_url)
print(f"Thumbnail URL: {thumbnail_url}")
