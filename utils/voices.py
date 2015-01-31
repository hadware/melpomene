__author__ = 'hadware'


class Voice(object):
    """A voice "reference", containing metadata about the voice, and its webclient"""

    def __init__(self, name, language, webclient_ref, description = None, country = None):
        self.name = name #string : matches the api's case-sentive original voice
        self.language = language
        self.country = country
        self.webclient = webclient_ref
        if description is not None:
            self.description = description

    def get_rendered_audio(self, text, filepath):
        self.webclient.get_rendered_audio(text=text, voice=self.name, filepath=filepath)

    def __str__(self):
        return "%s (%s)" % (self.name, self.webclient.name)

