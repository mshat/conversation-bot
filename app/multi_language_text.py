from tools.language import Language


class MultiLanguageTextException(Exception): pass


class MultiLanguageText:
    def __init__(self, multi_language_texts: dict, base_lang=Language(['ENG', 'RUS']), current_lang: Language = None):
        assert base_lang in multi_language_texts.keys()
        self._base_lang = base_lang
        self._multi_language_texts = multi_language_texts
        self._languages = list(self._multi_language_texts.keys())
        self._lang = current_lang if current_lang else self._base_lang

    @property
    def languages(self):
        return self._languages

    @property
    def current_lang(self):
        return self._lang

    @current_lang.setter
    def current_lang(self, lang: Language):
        if lang in self._languages:
            self._lang = lang

    @property
    def text(self):
        if self._lang in self._languages:
            return self._multi_language_texts[self._lang]
        else:
            return self._multi_language_texts[self._base_lang]

    def get_text(self, lang):
        if lang in self._languages:
            return self._multi_language_texts[lang]
        else:
            return self._multi_language_texts[self._base_lang]
