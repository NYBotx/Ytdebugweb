from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directory to save downloaded files
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Allowed file extensions for security
ALLOWED_EXTENSIONS = {'mp4', 'webm'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Download function to handle video/audio
def download_video(url, download_type, quality, filename):
    yt = YouTube(url)

    stream = None
    if download_type == 'video':
        # Check if the video has audio + video stream
        if quality == '1080p':
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution("1080p")
        elif quality == '720p':
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution("720p")
        elif quality == '480p':
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution("480p")
        elif quality == '360p':
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution("360p")
        elif quality == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
    elif download_type == 'audio':
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

    # Download the stream
    if stream:
        safe_filename = secure_filename(filename + '.' + stream.subtype)
        stream.download(output_path=DOWNLOAD_FOLDER, filename=safe_filename)
        return safe_filename
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form['url']
        download_type = request.form['download_type']
        quality = request.form['quality']
        filename = request.form['filename']

        if url and filename:
            try:
                # Download the video or audio
                downloaded_file = download_video(url, download_type, quality, filename)
                if downloaded_file:
                    return render_template("index.html", download_link=f"/download/{downloaded_file}")
                else:
                    return render_template("index.html", error="Error: Unable to download the video/audio.")
            except Exception as e:
                return render_template("index.html", error=f"Error: {str(e)}")
    return render_template("index.html", download_link=None)

@app.route("/download/<filename>")
def download_file(filename):
    # Send the file to the user for download
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
