from flask import Flask, jsonify, request
from module_audio_splitter import AudioSplitter
from module_yt_audio_downloader import YtAudioDownloader
from module_chunks_handler import ChunksHandler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
HOST = "192.168.15.133"
PORT = 5000


@app.route("/yt", methods=["POST"])
def create_chunks_from_youtube_video():
    ## download audio from YouTube
    downloader = YtAudioDownloader(request.json['url'], './/temp')
    content = downloader.execute()

    ## split audio in chunks
    splitter = AudioSplitter(content["audio"])
    chunks = splitter.execute()

    ## calculate start/end times of chunks
    times = []
    start = 0
    for chunk in chunks:
        end = start + len(chunk)
        times.append((start, end))
        start = end

    ## cut video based on times
    video_clips = []
    for start_ms, end_ms in times:
        start_s = start_ms / 1000
        end_s = end_ms / 1000
        clip = content["video"].subclipped(start_s, end_s)
        video_clips.append(clip)

    print(f"Video clips created: {len(video_clips)}")

    ## save chunks and delete downloaded audio
    handler = ChunksHandler()
    handler.save_chunks(video_clips, downloader.get_downloaded_audio_name())
    downloader.delete_downloaded_audio()

    return jsonify()


@app.route("/upload_recording/<audio>", methods=["POST"])
def upload_recording(audio):
    handler = ChunksHandler()
    handler.upload_recording(audio, request.json["b64"], request.args["chunk_name"])
    return jsonify()


@app.route("/audios", methods=["GET"])
def get_audio_folders():
    handler = ChunksHandler()
    return jsonify({"audios": handler.get_audio_folders()})


@app.route("/audio/<audio>", methods=["GET"])
def get_original_URIs(audio):
    handler = ChunksHandler()
    return jsonify(handler.get_original_URIs(audio, HOST, PORT))


@app.route("/recording/<audio>", methods=["GET"])
def get_recording_URIs(audio):
    handler = ChunksHandler()
    return jsonify(handler.get_recording_URIs(audio, HOST, PORT))


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
