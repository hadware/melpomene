# -*- coding: utf-8 -*-
__author__ = 'hadware'


class Language(object):
    language_count = 21
    FR, EN, ES, FI, KO, AR, CZ, DE, GR, IT, JP, DN, DU, CA, RU, MA, PO, SW, PT, TU, NO = range(language_count)

    language_names = ["Français", "Anglais", "Espagnol", "Finnois", "Coréen", "Arabe", "Tchèque", "Allemand", "Grec",
                      "Italien", "Japonais", "Danois", "Flamand", "Catalan", "Russe", "Mandarin", "Polonais",
                      "Suédois", "Portugais", "Turc", "Norvégien"]

    @classmethod
    def get_language_name(cls, language_code):
        return cls.language_names[language_code]

    @classmethod
    def get_language_code(cls, language_name):
        """Returns the langage code for the given language name"""
        # this is dirty, very dirty.
        return cls.language_names.index(language_name)