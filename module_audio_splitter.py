from pydub.silence import split_on_silence

class AudioSplitter:
    _CHUNK_MAX_DURATION_SEC = 6

    def __init__(self, audio):
        self._audio = audio

    def execute(self):
        large_chunks = self._split_in_large_chunks()
        small_chunks = self._split_in_small_chunks(large_chunks)
        best_size_chunks = self._join_really_small_chunks(small_chunks)
        return best_size_chunks

    def _split_in_large_chunks(self):
        return split_on_silence(self._audio, min_silence_len=400, silence_thresh=-40)

    def _split_in_small_chunks(self, chunks):
        result = []
        for chunk in chunks:
            if (chunk.duration_seconds >= self._CHUNK_MAX_DURATION_SEC):
                new_chunks = split_on_silence(chunk, min_silence_len=200, silence_thresh=-30)
                result = result + new_chunks
            else:
                result.append(chunk)

        return result

    def _join_really_small_chunks(self, chunks):
        result = []
        limit = len(chunks) - 1
        i = 0
        while (i <= limit):
            if (i + 1 <= limit and self._should_combine(chunks[i], chunks[i + 1])):
                result.append(chunks[i] + chunks[i + 1])
                i += 2
            else:
                result.append(chunks[i])
                i += 1

        return result

    def _should_combine(self, c1, c2):
        return c1.duration_seconds + c2.duration_seconds <= self._CHUNK_MAX_DURATION_SEC