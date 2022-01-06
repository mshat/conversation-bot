class LanguageException(Exception): pass


class Language:
    def __init__(self, languages, current_lang=None):
        self._languages = languages
        assert len(self._languages) > 0
        self._current_lang = current_lang if current_lang else self._languages[0]

    @property
    def languages(self):
        return self._languages

    @property
    def current(self):
        return self._current_lang

    @current.setter
    def current(self, lang: str):
        if lang in self.languages:
            self._current_lang = lang
        else:
            raise LanguageException('This language is not in the list of languages!')

    def __eq__(self, other):
        return self.current == other.current

    def __hash__(self):
        return self.current.__hash__()
        