from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        try:
            # yt-dlp options
            ydl_opts = {
                'quiet': True,
                'extract_flat': False,  # Extract full info
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video information
                info = ydl.extract_info(video_url, download=False)

                # Video metadata
                video_details = {
                    "title": info.get('title', 'N/A'),
                    "uploader": info.get('uploader', 'N/A'),
                    "thumbnail": info.get('thumbnail', ''),
                    "views": info.get('view_count', 0),
                    "length": info.get('duration', 0),
                }

                # Progressive streams (video + audio)
                progressive_streams = [
                    stream for stream in info['formats']
                    if stream.get('vcodec') != 'none' and stream.get('acodec') != 'none'
                ]

                # Video-only streams
                video_streams = [
                    stream for stream in info['formats']
                    if stream.get('acodec') == 'none'
                ]

                # Audio-only streams
                audio_streams = [
                    stream for stream in info['formats']
                    if stream.get('vcodec') == 'none'
                ]

                video_details.update({
                    "progressive_streams": progressive_streams,
                    "video_streams": video_streams,
                    "audio_streams": audio_streams,
                })

                return render_template("index.html", video_details=video_details)

        except Exception as e:
            return render_template("index.html", error=f"⚠️ An error occurred: {str(e)}")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
