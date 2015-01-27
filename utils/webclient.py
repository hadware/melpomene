# -*- coding: utf-8 -*-

__author__ = 'hadware'

import urllib2, urllib
import json
import os
from datetime import datetime
import lxml.html
import re
from voices import Voice
from string import lower
class VoiceNotFound(Exception):
    pass

class ApiClient(object):
    """Base abstract class for all the api clients"""
    def __init__(self, domain, tmp_folder):
        self.domain = domain
        self.tmp_folder = tmp_folder
        self.opener = urllib2.build_opener()

    def get_cache_path(self):
        """Returns the path to the folder where the fragments are stored"""
        return self.tmp_folder + "/audio_fragments/"

    def build_url(self, path):
        """Just builds an url based on the gven path"""
        return "http://" + self.domain + "/" + path

    def retrieve_voice_list(self):
        pass

    def get_voices(self):
        """Retrieve a simple list of all the voices"""
        #retrieving the json object that contains all the available voices
        if not hasattr(self, "voices"):
            self.retrieve_voice_list()

            #gathering all the voice names and leaving out the rest
            self.voice_objects = []
            for voice in self.voices:
                self.voice_objects.append(Voice(voice["name"], voice["language"], self))

        return self.voice_objects

class VoxygenClient(ApiClient):
    """Class whose job will be to interact with the Voxygen API"""

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
            self.voices = []
            for language_entry in self.voice_json["groups"]:
                self.voices += [{"name" : voice["name"].encode("ascii", "ignore"),
                                 "language" : language_entry["name"],
                                 "example" : voice["text"]} for voice in language_entry["voices"]]

    def get_rendered_audio(self, voice, text, filepath):
        """Retrieves a MP3 of the rendered audio, saves it in tmp_folder, returns the filename"""

        #file hasn't been rendered, we query the API for the file
        #setting get args for the request
        get_args = urllib.urlencode({"method" : "redirect",
                                     "text" : text.encode('utf8'),
                                     "voice" : voice,
                                     "ts" : datetime.now().strftime("%s%f")[:-3]})
        request = self.base_request("sites/all/modules/voxygen_voices/assets/proxy/index.php?" + get_args)
        #retrieving the response, without reading it yet
        response = self.opener.open(request)

        with open(os.path.abspath(filepath), "wb") as sound_file:
            sound_file.write(response.read())

class AcapelaClient(ApiClient):
    """Class whose job will be to interact with the Acapela API"""

    def __init__(self, domain, tmp_folder):
        super(AcapelaClient, self).__init__(domain, tmp_folder)
        self.pattern = re.compile(r"http://.*.mp3") #storing the compiled regular expression

    def base_request(self, path):
        """Builds a base request for the voxygen api, mimicking a FF browser"""
        request = urllib2.Request(self.build_url(path))
        request.add_header("Referer" , "http://www.acapela-group.com/demo-tts/DemoHTML5Form_V2_fr.php")
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36')
        return request

    def retrieve_voice_list(self):
        """simply retrieves the voice json"""
        if not hasattr(self, "form_html"):
            request = self.base_request("demo-tts/DemoHTML5Form_V2_fr.php")
            html_file = self.opener.open(request).read()
            self.form_html = lxml.html.fromstring(html_file).forms[0]
            languages_html = self.form_html.cssselect("fieldset")[0].cssselect("option")
            voices_groups_html = self.form_html.cssselect("fieldset")[1].cssselect("select")
            self.languages = dict()
            for language in languages_html:

                self.languages[language.get("value")]= {"language" : language.text.strip(),
                                                        "voices": list()}

            #voices are grouped by language
            for voice_group in voices_groups_html:
                for voice in voice_group.cssselect("option"):
                    self.languages[voice_group.get("id")]["voices"].append(voice.get("value"))

            #voices grouped in a list
            self.voices = []
            for sonid in self.languages:
                for voice in self.languages[sonid]["voices"]:
                    self.voices.append({"name" : voice,
                                        "language" : self.languages[sonid]["language"],
                                        "sonid" : sonid})

    def get_rendered_audio(self, voice, text, filepath):
        """Retrieves a MP3 of the rendered audio, saves it in tmp_folder, returns the filename"""

        #finding out the voice's "sonid" needed by acapela

        for single_voice_data in self.voices:
            if single_voice_data["name"] == voice:
                voice_sonid = single_voice_data["sonid"]

        request = self.base_request("demo-tts/DemoHTML5Form_V2_fr.php")
        #can't use the regular urlencode function, it shuffles the arguments' order and the shit acapela sever doesn't like that
        params ="MyLanguages=%s&MySelectedVoice=%s&MyTextForTTS=%s&SendToVaaS=" \
                % (voice_sonid, voice, urllib.quote(text.encode('utf8')))
        request.add_data(params)
        html = self.opener.open(request).read()
        #to retrieve the url of the rendered MP3, we have to match this line
        #var myPhpVar = \'http://194.158.21.231:8081/MESSAGES/012099097112101108097071114111117112/AcapelaGroup_WebDemo_HTML/sounds/99531273_d8e7295067062.mp3\'
        render_link = self.pattern.findall(html)[0]

        urllib.urlretrieve(render_link, filepath)#dowloading the link, aaand it's done


class WebClient():
    """Mainly a class to call when there's something to fetch on the voxygen 'API' """

    def __init__(self, voxygen_domain="voxygen.fr", acapela_domain="www.acapela-group.com", tmp_folder = "/tmp/vox_populi"):
        """Construtor"""
        self.tmp_folder = tmp_folder
        self.voxygen_client = VoxygenClient(voxygen_domain, tmp_folder)
        self.acapela_client = AcapelaClient(acapela_domain, tmp_folder)


        #the "head client"  takes care of checking if the tmp_folder exists
        try:
            os.mkdir(self.tmp_folder)
        except OSError:
            pass

        try:
            os.mkdir(self.get_cache_path())
        except OSError:
            pass

        #retrieves all the voices, stores them into a dict indexed by their names
        self.voices = self.voxygen_client.get_voices() + self.acapela_client.get_voices()
        self.voices_dict = {lower(voice.name) : voice for voice in self.voices}

    def get_cache_path(self):
        """Returns the path to the folder where the fragments are stored"""
        return self.tmp_folder + "/audio_fragments/"


    def get_voices(self):
        """Retrieve a a list of all the voice object instances"""
        return self.voices

    def get_voices_grouped_by_langage(self):
        """Groups voices by language lists"""
        pass

    def get_voice_object_from_name(self, voice):
        """Mainly used by the parser : returns a voice object corresponding to the voice's name, if found
        If it's not able to find a matching voice, returns none"""
        try:
            return self.voices_dict[lower(voice).strip()]
        except KeyError:
            raise VoiceNotFound("The voice %s isn't a valid one" % voice)



