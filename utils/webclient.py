# -*- coding: utf-8 -*-
import logging
from itertools import chain
from os.path import join

__author__ = 'hadware'

import urllib2, urllib
import json
import os
from datetime import datetime
import lxml.html
import re
from voices import Voice
from locales import Language
from string import lower

SCRIPT_FOLDER_PATH = join(os.path.dirname(__file__), "../")
CACHE_FILE_NAME = "voices_cache.json"

class VoiceNotFound(Exception):

    def __init__(self, wrong_voice_name, **kwargs):
        super(VoiceNotFound, self).__init__(**kwargs)
        self.wrong_voice_name = wrong_voice_name

class NoCacheFile(Exception):
    pass

class ApiClient(object):
    """Base abstract class for all the api clients"""
    client_name =""
    def __init__(self, domain, tmp_folder):
        self.domain = domain
        self.tmp_folder = tmp_folder
        self.opener = urllib2.build_opener()

    def _get_cache_path(self):
        """Returns the path to the folder where the fragments are stored"""
        return self.tmp_folder + "/audio_fragments/"

    def _base_request(self, path):
        pass

    def _build_url(self, path):
        """Just builds an url based on the given path"""
        return "http://" + self.domain + "/" + path

    def _retrieve_voice_list(self):
        pass

    def _get_language_code(self, language_string):
        """Returns the language code for a language. This function should be overriden in each client"""
        pass

    def get_voices(self):
        """Retrieve a simple list of all the voices"""
        #retrieving the json object that contains all the available voices
        if not hasattr(self, "voices"):
            self._retrieve_voice_list()

            #gathering all the voice names and leaving out the rest
            self.voice_objects = []
            for voice in self.voices:
                #this try clause is there in case a voice has been added, but isn't yet associated to a language
                try:
                    self.voice_objects.append(Voice(voice["name"], self._get_language_code(voice["language"]), self))
                except KeyError:
                    print("Voice of language code %s has been added to %s and is not yet supported"
                          % (voice["language"], self.client_name))

        return self.voice_objects

class VoxygenClient(ApiClient):
    """Class whose job will be to interact with the Voxygen API"""
    _language_codes = {"fr": Language.FR, "de": Language.DE, "en" : Language.EN, "ar" : Language.AR, "it" : Language.IT, "es" : Language.ES, "en-US": Language.EN, "en-UK": Language.EN}
    client_name = "Voxygen"

    def _base_request(self, path):
        """Builds a base request for the voxygen api, mimicking a FF browser"""
        request = urllib2.Request(self._build_url(path))
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36')
        request.add_header('Referer', self._build_url("fr"))
        return request

    def _get_language_code(self, language_string):
        return self._language_codes[language_string]

    def _retrieve_voice_list(self):
        """simply retrieves the voice json"""
        if not hasattr(self, "voice_json"):
            request = self._base_request("voices.json")
            self.voice_json = json.loads(self.opener.open(request).read())
            self.voices = []
            for language_entry in self.voice_json["groups"]:
                self.voices += [{"name" : voice["name"].encode("ascii", "ignore"),
                                 "language" : language_entry["code"],
                                 "example" : voice["text"]} for voice in language_entry["voices"]]

    def get_rendered_audio(self, voice, text, filepath):
        """Retrieves a MP3 of the rendered audio, saves it in tmp_folder, returns the filename"""

        #file hasn't been rendered, we query the API for the file
        #setting get args for the request
        get_args = urllib.urlencode({"method" : "redirect",
                                     "text" : text.encode('utf8'),
                                     "voice" : voice,
                                     "ts" : datetime.now().strftime("%s%f")[:-3]})
        request = self._base_request("sites/all/modules/voxygen_voices/assets/proxy/index.php?" + get_args)
        #retrieving the response, without reading it yet
        response = self.opener.open(request)

        with open(os.path.abspath(filepath), "wb") as sound_file:
            sound_file.write(response.read())

class AcapelaClient(ApiClient):
    """Class whose job will be to interact with the Acapela API"""
    _acapela_languages = {u"Arabic" : Language.AR, u"Catalan" : Language.CA, u"Czech" : Language.CZ, u"Danish": Language.DN,
                          u"Dutch" : Language.DU, u"English": Language.EN, u"Finnish" : Language.FI, u"French" : Language.FR,
                          u"German" : Language.DE, u"Greek" : Language.GR, u"Italian" : Language.IT, u"Japanese" : Language.JP,
                          u"Korean" : Language.KO, u"Mandarin": Language.MA, u"Norwegian": Language.NO, u"Polish": Language.PO,
                          u"Portuguese": Language.PT, u"Russian": Language.RU, u"Spanish": Language.ES, u"Swedish": Language.SW,
                          u"Turkish": Language.TU}

    client_name = "Acapela"
    def __init__(self, domain, tmp_folder):
        super(AcapelaClient, self).__init__(domain, tmp_folder)
        #storing the compiled regular expression used to find the mp3 file's link in the javascript code
        self.pattern = re.compile(r"http://.*.mp3")
        self.voices = []

    def _base_request(self, path):
        """Builds a base request for the voxygen api, mimicking a FF browser"""
        request = urllib2.Request(self._build_url(path))
        request.add_header("Referer" , "http://www.acapela-group.com/demo-tts/DemoHTML5Form_V2_fr.php")
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36')
        return request

    def _get_language_code(self, language_string):
        for language in self._acapela_languages:
            if language_string.find(language) != -1:
                return self._acapela_languages[language]
        raise KeyError #raised if no language is found



    def _retrieve_voice_list(self):
        """simply retrieves the json listing all available voices for the site's HTML or ajax call module"""

        def remove_emotive_string(voice_name):
            """Helper function to remove the 'emotive voice' crap from the voice names"""
            splitted = voice_name.split(" ")
            if len(splitted) > 1:
                return splitted[0]
            else:
                return voice_name

        if not hasattr(self, "form_html"):
            request = self._base_request("demo-tts/DemoHTML5Form_V2_fr.php")
            html_file = self.opener.open(request).read()
            self.form_html = lxml.html.fromstring(html_file).forms[0]
            languages_html = self.form_html.cssselect("fieldset")[0].cssselect("option")
            voices_groups_html = self.form_html.cssselect("fieldset")[1].cssselect("select")
            self.languages = dict()
            for language in languages_html:

                self.languages[language.get("value")] = {"language": language.text.strip(),
                                                         "voices": list()}

            #voices are grouped by language
            for voice_group in voices_groups_html:
                for voice in voice_group.cssselect("option"):
                    self.languages[voice_group.get("id")]["voices"].append(voice.get("value"))

            #voices grouped in a list
            self.voices = []
            for sonid in self.languages:
                for voice in self.languages[sonid]["voices"]:
                    self.voices.append({"name" : remove_emotive_string(voice),
                                        "language" : self.languages[sonid]["language"],
                                        "sonid" : sonid})

    def get_voice_sonid(self, voice_name):
        for single_voice_data in self.voices:
            if single_voice_data["name"] == voice_name:
                return single_voice_data["sonid"]

    def set_sonid_for_voice(self, voice_sonid, voice_name):
        self.voices.append({"name" : voice_name, "sonid" : voice_sonid})

    def get_rendered_audio(self, voice, text, filepath):
        """Retrieves a MP3 of the rendered audio, saves it in tmp_folder"""

        #finding out the voice's "sonid" needed by acapela
        voice_sonid=""
        for single_voice_data in self.voices:
            if single_voice_data["name"] == voice:
                voice_sonid = single_voice_data["sonid"]

        request = self._base_request("demo-tts/DemoHTML5Form_V2_fr.php")
        #can't use the regular urlencode function, it shuffles the arguments' order and the shit acapela server doesn't like that
        params ="MyLanguages=%s&MySelectedVoice=%s&MyTextForTTS=%s&SendToVaaS=" \
                % (voice_sonid, voice, urllib.quote(text.encode('utf8')))
        request.add_data(params)
        html = self.opener.open(request).read()
        #to retrieve the url of the rendered MP3, we have to match this kind of line
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
        self.api_clients = [self.acapela_client, self.voxygen_client]

        #the "head client"  takes care of checking if the tmp_folder exists
        try:
            os.mkdir(self.tmp_folder)
        except OSError:
            pass

        try:
            os.mkdir(self.get_cache_path())
        except OSError:
            pass

        try:
            self._load_voices_from_cache()
        except NoCacheFile:
            #retrieves all the voices, stores them into a dict indexed by their names
            self._update_voices_from_apis()
            self._update_voices_cache_file(self.api_clients) #updating cache

    def _update_voices_from_apis(self):
        self.voices = self.voxygen_client.get_voices() + self.acapela_client.get_voices()
        self.voices_dict = {lower(voice.name) : voice for voice in self.voices}

    def _update_voices_cache_file(self, api_clients_list):
        """Creates (or overwrites) a json file storing the voices retrieved from the API"""
        voices_dict = {client.client_name : [] for client in api_clients_list}
        for voice in self.voices:

            #todo : maybe make this cleaner as well
            voice_entry = voice.to_dict()
            if voice.webclient is self.acapela_client:
                voice_entry["sonid"] = self.acapela_client.get_voice_sonid(voice.name)
            voices_dict[voice.webclient.client_name].append(voice_entry)

        with open(join(SCRIPT_FOLDER_PATH, CACHE_FILE_NAME), "w+") as json_file:
            json_file.write(json.dumps(voices_dict, sort_keys=True,
                                       indent=4))
            logging.info("Updated json voice cache file in the script's folder")

    def _load_voices_from_cache(self):
        """Creates the voice dict using the voice cache json file"""
        webclients_lookup_table = {AcapelaClient.client_name : self.acapela_client,
                                   VoxygenClient.client_name : self.voxygen_client}
        self.voices_dict = {}
        try:
            with open(join(SCRIPT_FOLDER_PATH, CACHE_FILE_NAME), "r") as json_file:
                cache_dict = json.loads(json_file.read())

            for webclient_name, client_ref in webclients_lookup_table.items():
                for voice in cache_dict[webclient_name]:
                    self.voices_dict[lower(voice["name"])] = Voice.instantiate_from_dict(voice, client_ref)
                    # TODO : make this cleaner
                    # adding the voice and its sonid to the acapela client
                    if webclient_name == AcapelaClient.client_name:
                        self.acapela_client.set_sonid_for_voice(voice["sonid"], voice["name"])

            self.voices = self.voices_dict.values()
            logging.debug("Loaded voices from the cache file")
        except IOError:
            raise NoCacheFile()

    def reload_voices_from_api(self):
        """Updates the voices using the web apis, then updates the cache"""
        self._update_voices_from_apis()
        self._update_voices_cache_file(self.api_clients)

    def get_cache_path(self):
        """Returns the path to the folder where the fragments are stored"""
        return self.tmp_folder + "/audio_fragments/"


    def get_voices(self):
        """Retrieve a a list of all the voice object instances"""
        return self.voices


    def get_voices_grouped_by_language(self):
        """Groups voices by language lists"""
        voices_dict = {i : {"name" : Language.get_language_name(i),
                            "voices" : list()} for i in range(Language.language_count)}
        for voice in list(self.voices):
            if voice.language is not None:
                voices_dict[voice.language]["voices"].append(voice)

        return voices_dict

    def get_voice_object_from_name(self, voice):
        """Mainly used by the parser : returns a voice object corresponding to the voice's name, if found
        If it's not able to find a matching voice, returns none"""
        try:
            return self.voices_dict[lower(voice).strip()]
        except KeyError:
            raise VoiceNotFound(voice)



