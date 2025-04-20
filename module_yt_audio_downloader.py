from pydub import AudioSegment
from pytubefix import YouTube
from pathlib import Path
from moviepy import VideoFileClip
import os

# rename this class to be more descriptive
class YtAudioDownloader:
    _user_data = "CgsyUHkwSWZQTHRsSSjfkJG7BjIKCgJCUhIEGgAgTQ%3D%3D"
    _po_token = "MnTK9tGlwPKGdsrO5NQV4M-N48HTWklLmvpMvL5jGjA1amqO0Hep0ofXoH_Fm8Kzl8DwZyrkHWHl9OuG95_qxHGiie_6reqcVR5WI7o4Yw8K0mDnxhM_JCen6diO7u-q2ANAiv-CJD47061lwjvWn4eqWDSTbg=="

    def __init__(self, video_url, temp_dir):
        self._video_url = video_url
        self._temp_dir = temp_dir

    def execute(self):
        result = self._download()
        self._temp_audio_path = result['audio_path']
        self._temp_video_path = result['video_path']

        audio = AudioSegment.from_file(self._temp_audio_path)
        video = VideoFileClip(self._temp_video_path)

        return { 'audio': audio, 'video': video, 'audio_path': self._temp_audio_path }
        
    def _download(self):
        yt = YouTube(
            self._video_url, 
            use_po_token=True, 
            po_token_verifier=(self._user_data, self._po_token))
        
        video = yt.streams.get_lowest_resolution()
        audio = yt.streams.get_audio_only()

        video_path = video.download(output_path=self._temp_dir, filename=self._sanitaze_filename(video.title, 'm4a'))
        audio_path = audio.download(output_path=self._temp_dir, filename=self._sanitaze_filename(audio.title, 'mp3'))	

        return { 'video_path': video_path, 'audio_path': audio_path }

    def _sanitaze_filename(self, filename, extension='m4a'):
        sanitazed = ''.join(e for e in filename if e.isalnum() or e.isspace())
        return sanitazed.strip() + '.' + extension

    def get_downloaded_audio_name(self):
        if (self._temp_audio_path):
            return Path(self._temp_audio_path).stem
        return ''

    def delete_downloaded_audio(self):
        if (self._temp_audio_path):
            os.remove(self._temp_audio_path)