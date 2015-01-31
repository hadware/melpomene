__author__ = 'hadware'

import hashlib
import os

class Cue(object):
    """A line, along with the voice reference that said it"""
    def __init__(self, voice_ref, line):
        self.voice = voice_ref
        self.line = line

    def get_hash(self):
        """Computes the md5 hash for this cue"""
        if not hasattr(self, "hash"):
            self.hash = hashlib.md5((self.voice.name + self.line).encode('utf8')).hexdigest()
        return self.hash


    def get_rendered_audio(self, cache_path):
        """retrieve the corresponding soundfile, does not generate it if it already exists"""
        filepath = cache_path + self.get_hash() + ".mp3"
        if not os.path.isfile(filepath):
            # file hasn't been rendered, we return the existing file name
            self.voice.get_rendered_audio(self.line, filepath)
            self.render_filepath = filepath
        else:
            self.render_filepath = filepath
        return self.render_filepath

class Dialog(object):

    def __init__(self):
        self.cues = []

    def add_cue(self, cue):
        self.cues.append(cue)
