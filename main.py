from flask import Flask, jsonify, request
from module_audio_splitter import AudioSplitter
from module_yt_audio_downloader import YtAudioDownloader
from module_chunks_handler import ChunksHandler
import os

app = Flask(__name__)
HOST = '192.168.18.6'
PORT = 5000

@app.route('/yt', methods=['POST'])
def create_chunks_from_youtube_video():
    ## download audio from YouTube
    audio_downloader = YtAudioDownloader(request.json['url'], './/temp')
    audio = audio_downloader.execute()

    ## split audio in chunks
    splitter = AudioSplitter(audio)
    chunks = splitter.execute()
    
    ## save chunks and delete downloaded audio
    handler = ChunksHandler()
    handler.save_chunks(chunks, audio_downloader.get_downloaded_audio_name())
    audio_downloader.delete_downloaded_audio()

    return jsonify()

@app.route('/upload_recording/<audio>', methods=['POST'])
def upload_recording(audio):
    handler = ChunksHandler()
    handler.upload_recording(audio, request.json['b64'], request.args['chunk_name'])
    return jsonify()

@app.route('/audios', methods=['GET'])
def get_audio_folders():
    handler = ChunksHandler()
    return jsonify({ 'audios': handler.get_audio_folders() })

@app.route('/audio/<audio>', methods=['GET'])
def get_original_URIs(audio):
    handler = ChunksHandler()
    return jsonify(handler.get_original_URIs(audio, HOST, PORT))

@app.route('/recording/<audio>', methods=['GET'])
def get_recording_URIs(audio):
    handler = ChunksHandler()
    return jsonify(handler.get_recording_URIs(audio, HOST, PORT))

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)