# -*- coding: utf-8 -*-

__author__ = 'hadware'

import urllib2, urllib
import json
import hashlib
import os
from datetime import datetime

class Voice():
    """Object storing a voice"""
    def __init__(self, webclient, name, language):
        self.webclient = webclient
        self.name = name
        self.language = language


class WebClient():
    """Mainly a class to call when there's something to fetch on the voxygen 'API' """

    def __init__(self, voxygen_domain="voxygen.fr", tmp_folder = "/tmp/vox_populi"):
        """Construtor"""
        self.voxygen_domain = voxygen_domain
        self.tmp_folder = tmp_folder
        self.opener = urllib2.build_opener()
        try:
            os.mkdir(self.tmp_folder)
        except OSError:
            pass

        try:
            os.mkdir(self.get_cache_path())
        except OSError:
            pass

    def get_cache_path(self):
        """Returns the path to the folder where the fragments are stored"""
        return self.tmp_folder + "/audio_fragments/"

    def build_url(self, path):
        """Just builds an url based on the gven path"""
        return "http://" + self.voxygen_domain + "/" + path

    def base_request(self, path):
        """Builds a base request for the voxygen api, mimicking a FF browser"""
        request = urllib2.Request(self.build_url(path))
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36')
        request.add_header('Referer', self.build_url("fr"))
        return request

    def retrieve_voice_list(self):
        """simply retrieves the voice json"""
        if not hasattr(self, "voice_json"):
            request = self.base_request("voices.json")
            self.voice_json = json.loads(self.opener.open(request).read())

    def get_voices(self):
        """Retrieve a simple list of all the voices"""
        #retrieving the json object that contains all the available voices
        self.retrieve_voice_list()

        #gathering all the voice names and leaving out the rest
        complete_voice_list = []
        for language_entry in self.voice_json["groups"]:
            complete_voice_list += [voice["name"] for voice in language_entry["voices"]]

        return complete_voice_list

    def get_full_voices(self):
        """Retrieve a list of langages grouped by langages"""
        #retrieving the json object that contains all the available voices
        self.retrieve_voice_list()

        #gathering all the voice names and leaving out the rest
        complete_voice_list = []
        for language_entry in self.voice_json["groups"]:
            complete_voice_list.append({ "voices" : [voice["name"] for voice in language_entry["voices"]],
                                         "language" : language_entry["name"]})

        return complete_voice_list


    def get_rendered_audio(self, voice, text):
        """Retrieves a MP3 of the rendered audio, saves it in tmp_folder, returns the filename"""

        filename = hashlib.md5((voice + text).encode('utf8')).hexdigest() + ".mp3"
        if os.path.isfile(self.get_cache_path() + filename):
            # file has already been rendered, we return the existing file name
            return self.get_cache_path() + filename
        else: #file hasn't been rendered, we query the API for the file
            #setting get args for the request
            get_args = urllib.urlencode({"method" : "redirect",
                                         "text" : text.encode('utf8'),
                                         "voice" : voice,
                                         "ts" : datetime.now().strftime("%s%f")[:-3]})
            request = self.base_request("sites/all/modules/voxygen_voices/assets/proxy/index.php?" + get_args)
            #retrieving the response, without reading it yet
            response = self.opener.open(request)

            filepath = self.get_cache_path() + filename
            with open(os.path.abspath(filepath), "wb") as sound_file:
                sound_file.write(response.read())

            return filepath