from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        try:
            yt = YouTube(video_url)

            # Fetch streams
            progressive_streams = yt.streams.filter(progressive=True, file_extension="mp4")
            video_streams = yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True)
            audio_streams = yt.streams.filter(only_audio=True)

            video_details = {
                "title": yt.title,
                "uploader": yt.author,
                "thumbnail": yt.thumbnail_url,
                "views": yt.views,
                "length": yt.length,
                "progressive_streams": progressive_streams,
                "video_streams": video_streams,
                "audio_streams": audio_streams
            }

            return render_template("index.html", video_details=video_details)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
