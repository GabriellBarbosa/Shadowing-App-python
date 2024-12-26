from flask import Flask, jsonify, request
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pytubefix import YouTube
from audio_splitter_module import AudioSplitter
import os
import io
import base64

app = Flask(__name__)
HOST = '192.168.18.6'
PORT = 5000

user_data = "CgsyUHkwSWZQTHRsSSjfkJG7BjIKCgJCUhIEGgAgTQ%3D%3D"
po_token = "MnTK9tGlwPKGdsrO5NQV4M-N48HTWklLmvpMvL5jGjA1amqO0Hep0ofXoH_Fm8Kzl8DwZyrkHWHl9OuG95_qxHGiie_6reqcVR5WI7o4Yw8K0mDnxhM_JCen6diO7u-q2ANAiv-CJD47061lwjvWn4eqWDSTbg=="

@app.route('/yt', methods=['POST'])
def upload_audio_from_yt():
    yt = YouTube(
        request.json['url'], 
        use_po_token=True, 
        po_token_verifier=(user_data, po_token))
    ys = yt.streams.get_audio_only()
    path = ys.download(output_path=".//temp")
    audio = AudioSegment.from_file(path)

    ## split audio in chunks
    splitter = AudioSplitter(audio)
    chunks = splitter.execute()
    
    folder_name = ''.join(e for e in ys.title if e.isalnum() or e.isspace())
    save(chunks, folder_name.strip())
    os.remove(path)
    return jsonify()

def split_in_chunks(audio):
    splitter = AudioSplitter(audio)
    return 

def save(audio_chunks, new_folder_name):
    for i, chunk in enumerate(audio_chunks):
        out_path = f'.//static//audios//{new_folder_name}//original' 
        create_new_directory(out_path)
        out_file = out_path + f'.//{i}.wav'
        chunk.export(out_file, format='wav')

@app.route('/upload_recording/<audio>', methods=['POST'])
def upload_recording(audio):
    out_path = f'static//audios//{audio}//recording'
    create_new_directory(out_path)
    blob = base64_to_blob(request.json['b64'])
    audio = create_audio_from(blob)
    save_recording(audio, out_path, request.args['chunk_name'])
    return jsonify()

def base64_to_blob(b64_str):
    sanitized_b64 = remove_file_type_from(b64_str)
    encoded_b64 = sanitized_b64.encode()
    return base64.decodebytes(encoded_b64)

def remove_file_type_from(b64_str):
    return b64_str.split(',')[1]

def create_audio_from(blob):
    return AudioSegment.from_file(io.BytesIO(blob))

def save_recording(audio, out_path, chunk_name):
    out_file = out_path + f'//{chunk_name}'
    audio.export(out_file, format='wav')
    
def create_new_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

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