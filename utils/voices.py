__author__ = 'hadware'


class Language():
        FR, EN, ES, FI, KO, AR, CZ, DE, GR, IT, JP, DN, DU, CA = range(13)

class Voice():
    """A voice "reference", containing metadata about the voice, and its webclient"""

    def __init__(self, name, language, webclient_ref, example = None):
        self.name = name #string : matches the api's case-sentive original voice
        self.language = language
        self.webclient = webclient_ref
        if example is not None:
            self.example = example

    def get_rendered_audio(self, text, filepath):
        self.webclient.get_rendered_audio(text, self.name, filepath)


