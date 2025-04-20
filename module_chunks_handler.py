from pydub import AudioSegment
import os
import io
import base64

class ChunksHandler:
    def save_chunks(self, video_clips, new_folder_name):
        for i, clip in enumerate(video_clips):
            out_path = f'.//static//audios//{new_folder_name}//original//'
            self._create_new_directory(out_path)
            filename = f"chunk_{i}.mp4"
            clip.write_videofile(out_path + filename, codec="libx264")

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
    
    def get_audio_folders(self):
        return self._list_dir_content('./static/audios')

    def get_original_URIs(self, audio, host, port):
        result = [None] * self._total_original_chunks(audio)
        chunks = self._list_dir_content(f'./static/audios/{audio}/original')
        for chunk in chunks:
            index = int(chunk.split('.')[0])
            result[index] = self._get_original_chunk_path(audio, chunk, host, port)

        return result

    def get_recording_URIs(self, audio, host, port):
        result = [None] * self._total_original_chunks(audio)
        recordings = self._list_dir_content(f'./static/audios/{audio}/recording')
        for rec in recordings:
            index = int(rec.split('.')[0])
            result[index] = self._get_recording_chunk_path(audio, rec, host, port)

        return result

    def _total_original_chunks(self, audio):
        chunk_numbers = []
        chunks = self._list_dir_content(f'./static/audios/{audio}/original')
        for c in chunks:
            c_number = int(c.split('.')[0])
            chunk_numbers.append(c_number)

        return max(chunk_numbers) + 1

    def _get_original_chunk_path(self, audio, chunk, host, port):
        return {
            'path': f'http://{host}:{port}/static/audios/{audio}/original/{chunk}',
            'name': chunk
        }

    def _get_recording_chunk_path(self, audio, rec, host, port):
        return {
            'path': f'http://{host}:{port}/static/audios/{audio}/recording/{rec}',
            'name': rec
        }

    def _list_dir_content(self, path):
        try:
            return os.listdir(path)
        except:
            return []

