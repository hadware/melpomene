#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hadware'

from sys import argv
import os
import shutil
from voxpopuli_gui import VoxPopuliMain
from gi.repository import Gtk
from utils import *

"""This is the main module"""

def print_help():
    """Prints out the help"""
    print('''
    Utilisation : ./voxpopuli dialogue.txt rendu.ogg

    Pour utiliser l'interface graphique:
        ./voxpopuli --gui

            ou

        ./voxpopuli_gui

    Pour afficher les voix disponibles :
        ./voxpopuli --voices

    Ce message d'aide s'affiche avec
        ./voxpopuli --help

    NB: Le fichier du dialogue doit être sans retour à la ligne pour la même tirade d'une voix.
    Exemple correct:
        Zozo: Je vais te punir, petit baptou fragile.
        Loic : Vazy mon grand, explose moi le conduit.
    Exemple incorrect:
        Zozo: Je vais te punir,
        petit baptou fragile.
        Loic : Vazy mon grand, explose moi le conduit.
            ''')

if __name__ == "__main__":

    #affichage de l'aide
    if len(argv) == 1:
        print_help()

    elif argv[1] in ["help", "-h", "--help", "-help", "A L'AIDE", "HIFLE", "AYUDA"]:
        print_help()

    elif argv[1] == "--voices":
        #creating the web client
        client = WebClient()
        voices_list = client.get_full_voices()
        for langage_group in voices_list:
            print("Langue : %s" % langage_group["language"])
            for voice in langage_group["voices"]:
                print("\t - %s" % voice)

    elif argv[1] == "--gui":
        # gui requested
        main = VoxPopuliMain()
        Gtk.main()

    else:
        render_manager = RenderManager()

        with open(os.path.abspath(argv[1]), mode = "r+") as text_file:
            text = unicode(text_file.read(), "utf-8")

            try:
                render_manager.render(text)
            except VoiceNotFound:
                print("Les voix ne sont pas les bonnes! Utilise l'option --voices pour afficher les voix disponibles.")
            else:

                #copying the rendered file to the cwd
                if len(argv) == 3: #if there's a new name argument
                    render_manager.file_manager.save_render(os.getcwd() + "/" + argv[2])
                else:
                    render_manager.file_manager.save_render_in_folder(os.getcwd())


