# -*- coding: utf-8 -*-

__author__ = 'hadware'

from sound_manager import SoundManager
from parser import DialogParser, VoiceNotFound
from webclient import WebClient
from sys import argv
import os
import shutil

"""This is the main module"""

if __name__ == "__main__":
    #creating the web client
    client = WebClient()

    #retrieving the available voice list and giving it to the parser constructor
    parser = DialogParser(voices = client.get_voices())

    #parsing the file into a "dialog" (list of voices and their lines)
    try:
        dialog = parser.parse_from_file(os.path.abspath(argv[1]))

    except VoiceNotFound:
        print("Les voix ne sont pas les bonnes!")
    else:
        #using the web client to retrieve the rendered sound files
        sound_files = [client.get_rendered_audio(line["voice"], line["text"]) for line in dialog]

        #making the sound manager render the final sound file
        sound_manager = SoundManager(file_list=sound_files)
        rendered_file = sound_manager.render_dialog()

        #copying the rendered file to the cwd
        if len(argv) == 3: #if there's a new name argument
            shutil.copyfile(rendered_file, os.getcwd() + "/" + argv[2])
        else:
            shutil.copyfile(rendered_file, os.getcwd())


