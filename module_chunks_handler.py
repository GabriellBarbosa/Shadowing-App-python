from pydub import AudioSegment
import os
import io
import base64

class ChunksHandler:
    def save_chunks(self, audio_chunks, new_folder_name):
        for i, chunk in enumerate(audio_chunks):
            out_path = f'.//static//audios//{new_folder_name}//original'
            self._create_new_directory(out_path)
            out_file = out_path + f'.//{i}.wav'
            chunk.export(out_file, format='wav')

    def upload_recording(self, audio, b64, chunk_name):
        out_path = f'static//audios//{audio}//recording'
        self._create_new_directory(out_path)
        blob = self._base64_to_blob(b64)
        audio = self._create_audio_from(blob)
        self._save_recording(audio, out_path, chunk_name)

    def _base64_to_blob(self, b64_str):
        sanitized_b64 = self._remove_file_type_from(b64_str)
        encoded_b64 = sanitized_b64.encode()
        return base64.decodebytes(encoded_b64)

    def _remove_file_type_from(self, b64_str):
        return b64_str.split(',')[1]

    def _create_audio_from(self, blob):
        return AudioSegment.from_file(io.BytesIO(blob))

    def _save_recording(self, audio, out_path, chunk_name):
        out_file = out_path + f'//{chunk_name}'
        audio.export(out_file, format='wav')

    def _create_new_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    