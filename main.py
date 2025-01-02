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
    return jsonify({ 'audios': list_dir_content('./static/audios') });

@app.route('/audio/<audio>', methods=['GET'])
def get_original_URIs(audio):
    result = [None] * total_original_chunks(audio)
    chunks = list_dir_content(f'./static/audios/{audio}/original')
    for chunk in chunks:
        index = int(chunk.split('.')[0])
        result[index] = get_original_chunk_path(audio, chunk)

    return jsonify(result)

def get_original_chunk_path(audio, chunk):
    return {
        'path': f'http://{HOST}:{PORT}/static/audios/{audio}/original/{chunk}',
        'name': chunk
    }

@app.route('/recording/<audio>', methods=['GET'])
def get_recording_URIs(audio):
    result = [None] * total_original_chunks(audio)
    recordings = list_dir_content(f'./static/audios/{audio}/recording')
    for rec in recordings:
        index = int(rec.split('.')[0])
        result[index] = get_recording_chunk_path(audio, rec)

    return jsonify(result)

def get_recording_chunk_path(audio, rec):
    return {
        'path': f'http://{HOST}:{PORT}/static/audios/{audio}/recording/{rec}',
        'name': rec
    }
    
def total_original_chunks(audio):
    chunk_numbers = []
    chunks = list_dir_content(f'./static/audios/{audio}/original')
    for c in chunks:
        c_number = int(c.split('.')[0])
        chunk_numbers.append(c_number)

    return max(chunk_numbers) + 1

def list_dir_content(path):
    try:
        return os.listdir(path)
    except:
        return []

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)